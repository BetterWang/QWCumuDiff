import FWCore.ParameterSet.Config as cms

process = cms.Process("CumuDiff")

process.load('Configuration.StandardSequences.Services_cff')
process.load('FWCore.MessageService.MessageLogger_cfi')
process.load('Configuration.StandardSequences.GeometryDB_cff')
process.load("TrackingTools/TransientTrack/TransientTrackBuilder_cfi")
process.load('Configuration.StandardSequences.MagneticField_38T_cff')
process.load('Configuration.StandardSequences.EndOfProcess_cff')
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_condDBv2_cff')


process.maxEvents = cms.untracked.PSet(input = cms.untracked.int32(-1))
process.MessageLogger.cerr.FwkReport.reportEvery = 100

from Configuration.AlCa.GlobalTag_condDBv2 import GlobalTag
process.GlobalTag = GlobalTag(process.GlobalTag, '75X_dataRun2_v13', '')

process.options = cms.untracked.PSet(
    SkipEvent = cms.untracked.vstring('ProductNotFound')
)

process.source = cms.Source("PoolSource",
        fileNames = cms.untracked.vstring("/store/user/davidlw/HIMinimumBias5/RecoSkim2015_pprereco_V0Cascade_Golden_v2/170302_083114/0000/PbPb_MB_102.root"),
	secondaryFileNames = cms.untracked.vstring(
		'/store/hidata/HIRun2015/HIMinimumBias5/AOD/02May2016-v1/10000/B2468076-DB24-E611-B42F-D4AE5264D511.root'
		),
)


import HLTrigger.HLTfilters.hltHighLevel_cfi

process.hltMB = HLTrigger.HLTfilters.hltHighLevel_cfi.hltHighLevel.clone()
process.hltMB.HLTPaths = [
	"HLT_HIL1MinimumBiasHF2AND*",
	"HLT_HIL1MinimumBiasHF1AND*",
]
process.hltMB.andOr = cms.bool(True)
process.hltMB.throw = cms.bool(False)

process.TFileService = cms.Service("TFileService",
    fileName = cms.string('cumu.root')
)


process.load('HeavyIonsAnalysis.Configuration.collisionEventSelection_cff')

process.primaryVertexFilter.src = cms.InputTag("offlinePrimaryVertices")

process.load('RecoHI.HiCentralityAlgos.CentralityFilter_cfi')
process.ppRecoCentFilter = process.centralityFilter.clone(
	selectedBins = cms.vint32(
		*range(60, 180)
		),
	BinLabel = cms.InputTag("centralityBins")
	)

process.eventSelection = cms.Sequence(
        process.hfCoincFilter3
        + process.primaryVertexFilter
#        + process.clusterCompatibilityFilter
)


process.QWV0EventKs = cms.EDProducer('QWV0VectProducer'
		, vertexSrc = cms.untracked.InputTag('offlinePrimaryVertices', "")
		, trackSrc = cms.untracked.InputTag('generalTracks')
		, V0Src = cms.untracked.InputTag('generalV0CandidatesNew', 'Kshort')
		, Massmin = cms.untracked.double(0.467)
		, Massmax = cms.untracked.double(0.523)
		, DecayXYZMin = cms.untracked.double(5.0)
		, DecayXYZMax = cms.untracked.double(999999999999.)
		, ThetaXYZMin = cms.untracked.double(0.999)
		, ThetaXYZMax = cms.untracked.double(999999999999.)
		)

process.QWV0EventLambda = cms.EDProducer('QWV0VectProducer'
		, vertexSrc = cms.untracked.InputTag('offlinePrimaryVertices', "")
		, trackSrc = cms.untracked.InputTag('generalTracks')
		, V0Src = cms.untracked.InputTag('generalV0CandidatesNew', 'Lambda')
		, Massmin = cms.untracked.double(1.11)
		, Massmax = cms.untracked.double(1.123)
		, DecayXYZMin = cms.untracked.double(5.0)
		, DecayXYZMax = cms.untracked.double(999999999999.)
		, ThetaXYZMin = cms.untracked.double(0.999)
		, ThetaXYZMax = cms.untracked.double(999999999999.)
		)

process.QWV0EventV0 = process.QWV0EventLambda.clone()
#process.QWV0EventV0 = process.QWV0EventKs.clone()

process.load('PbPb_HIMB5_ppReco_eff')
#process.QWEvent.fweight = cms.untracked.InputTag('Hydjet_ppReco_tight4_v2.root')
process.QWEvent.ptMax = cms.untracked.double(100)


process.QWCumuDiff = cms.EDAnalyzer('QWCumuDiff',
		trackSet = cms.untracked.PSet(
			Eta = cms.untracked.InputTag('QWEvent', 'eta'),
			Phi = cms.untracked.InputTag('QWEvent', 'phi'),
			Ref = cms.untracked.InputTag('QWEvent', 'ref'),
			Pt  = cms.untracked.InputTag('QWEvent', 'pt'),
			Weight = cms.untracked.InputTag('QWEvent', 'weight'),
			),
		sigSet = cms.untracked.PSet(
			Eta = cms.untracked.InputTag('QWV0EventV0', 'eta'),
			Phi = cms.untracked.InputTag('QWV0EventV0', 'phi'),
			Ref = cms.untracked.InputTag('QWV0EventV0', 'Refs'),
			Pt = cms.untracked.InputTag('QWV0EventV0', 'pt'),
			Weight = cms.untracked.InputTag('QWV0EventV0', 'weight'),
			),
		vertexZ = cms.untracked.InputTag('QWEvent', "vz"),
		ptBin = cms.untracked.vdouble(0.1, 0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 4.0, 5.0, 6.0, 8.0, 10.0, 12.0, 16.0, 20.0, 30.0, 40.0, 100.0),
		centrality = cms.untracked.InputTag('Noff')
		)


process.vectV0Mass = cms.EDAnalyzer('QWVectorAnalyzer',
		src = cms.untracked.InputTag("QWV0EventV0", "mass"),
		hNbins = cms.untracked.int32(100),
		hstart = cms.untracked.double(0),
		hend = cms.untracked.double(100),
		cNbins = cms.untracked.int32(100),
		cstart = cms.untracked.double(.40),
		cend = cms.untracked.double(0.60),
		)

# Lambda
process.vectV0Mass.cstart = cms.untracked.double(1.0)
process.vectV0Mass.cend = cms.untracked.double(1.2)

process.vectPt.cNbins = cms.untracked.int32(4000)
process.vectPt.cend = cms.untracked.double(40)

process.vectPtW.cNbins = cms.untracked.int32(4000)
process.vectPtW.cend = cms.untracked.double(40)

process.vectPhiV0 = process.vectPhi.clone(src = cms.untracked.InputTag('QWV0EventV0', 'phi'))
process.vectEtaV0 = process.vectEta.clone(src = cms.untracked.InputTag('QWV0EventV0', 'eta'))
process.vectPtV0  = process.vectPt.clone(src = cms.untracked.InputTag('QWV0EventV0', 'pt'))

process.ana = cms.Path(process.eventSelection * process.makeEvent * process.ppRecoCentFilter * process.QWV0EventV0 * process.QWCumuDiff * process.vectMonW * process.vectV0Mass * process.vectPhiV0 * process.vectEtaV0 * process.vectPtV0)

process.RECO = cms.OutputModule("PoolOutputModule",
		outputCommands = cms.untracked.vstring('keep *'),
		SelectEvents = cms.untracked.PSet(
			SelectEvents = cms.vstring('ana')
			),
		fileName = cms.untracked.string('recoV0.root')
		)

process.out = cms.EndPath(process.RECO)


process.schedule = cms.Schedule(
	process.ana,
)
