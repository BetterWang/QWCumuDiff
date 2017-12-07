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
	fileNames = cms.untracked.vstring("file:/afs/cern.ch/user/q/qwang/work/cleanroomRun2/Ana/data/ppReco_GMOV0.root"),
	secondaryFileNames = cms.untracked.vstring(
		'file:/afs/cern.ch/user/q/qwang/work/cleanroomRun2/Ana/data/ppReco.root'
		),
)


process.TFileService = cms.Service("TFileService",
    fileName = cms.string('cumu.root')
)


process.load('HeavyIonsAnalysis.Configuration.collisionEventSelection_cff')
process.load('RecoHI.HiCentralityAlgos.CentralityFilter_cfi')

process.NoffFilter0 = process.centralityFilter.clone(
	selectedBins = cms.vint32(
		*range(0, 10)
		),
	BinLabel = cms.InputTag("Noff")
	)
process.NoffFilter10 = process.centralityFilter.clone(
	selectedBins = cms.vint32(
		*range(10, 30)
		),
	BinLabel = cms.InputTag("Noff")
	)
process.NoffFilter30 = process.centralityFilter.clone(
	selectedBins = cms.vint32(
		*range(30, 90)
		),
	BinLabel = cms.InputTag("Noff")
	)
process.NoffFilter90 = process.centralityFilter.clone(
	selectedBins = cms.vint32(
		*range(90, 120)
		),
	BinLabel = cms.InputTag("Noff")
	)
process.NoffFilter120 = process.centralityFilter.clone(
	selectedBins = cms.vint32(
		*range(120, 185)
		),
	BinLabel = cms.InputTag("Noff")
	)
process.NoffFilter185 = process.centralityFilter.clone(
	selectedBins = cms.vint32(
		*range(185, 250)
		),
	BinLabel = cms.InputTag("Noff")
	)
process.NoffFilter250 = process.centralityFilter.clone(
	selectedBins = cms.vint32(
		*range(250, 320)
		),
	BinLabel = cms.InputTag("Noff")
	)

process.eventSelection = cms.Sequence(
        process.hfCoincFilter3
#        + process.primaryVertexFilter
#        + process.clusterCompatibilityFilter
)


process.QWV0EventKs = cms.EDProducer('QWV0VectProducer'
		, vertexSrc = cms.untracked.InputTag('GMOVertex')
		, trackSrc = cms.untracked.InputTag('generalTracks')
		, V0Src = cms.untracked.InputTag('generalV0CandidatesNew', 'Kshort')
		, daughter_cuts = cms.untracked.PSet(
			)
		, cuts = cms.untracked.VPSet(
			cms.untracked.PSet(
				Massmin = cms.untracked.double(0.43)
				, Massmax = cms.untracked.double(0.57)
				, DecayXYZMin = cms.untracked.double(5.0)
				, ThetaXYZMin = cms.untracked.double(0.999)
				, ptMin = cms.untracked.double(0.2)
				, ptMax = cms.untracked.double(8.5)
				)
			)
		)

process.QWV0EventLambda = cms.EDProducer('QWV0VectProducer'
		, vertexSrc = cms.untracked.InputTag('GMOVertex')
		, trackSrc = cms.untracked.InputTag('generalTracks')
		, V0Src = cms.untracked.InputTag('generalV0CandidatesNew', 'Kshort')
		, daughter_cuts = cms.untracked.PSet(
			)
		, cuts = cms.untracked.VPSet(
			cms.untracked.PSet(
				Massmin = cms.untracked.double(1.08)
				, Massmax = cms.untracked.double(1.16)
				, DecayXYZMin = cms.untracked.double(5.0)
				, ThetaXYZMin = cms.untracked.double(0.9999)
				, ptMin = cms.untracked.double(0.2)
				, ptMax = cms.untracked.double(1.0)
				),
			cms.untracked.PSet(
				Massmin = cms.untracked.double(1.08)
				, Massmax = cms.untracked.double(1.16)
				, DecayXYZMin = cms.untracked.double(5.0)
				, ThetaXYZMin = cms.untracked.double(0.9998)
				, ptMin = cms.untracked.double(1.0)
				, ptMax = cms.untracked.double(8.5)
				)
			)
		)


process.load('PbPb_HIMB5_ppReco_eff')
process.Noff.vertexSrc = cms.untracked.InputTag('GMOVertex')
process.QWEvent.vertexSrc = cms.untracked.InputTag('GMOVertex')
process.QWEvent.ptMax = cms.untracked.double(100)


process.vectKsMassN0_pT02 = cms.EDAnalyzer('QWVectorAnalyzer',
		srcMass = cms.untracked.InputTag("QWV0EventKs", "mass"),
		srcPt = cms.untracked.InputTag("QWV0EventKs", "pt"),
		hNbins = cms.untracked.int32(10),
		hstart = cms.untracked.double(0),
		hend = cms.untracked.double(10),
		cNbins = cms.untracked.int32(100),
		cstart = cms.untracked.double(.40),
		cend = cms.untracked.double(0.60),
		ptMin = cms.untracked.double(0.2),
		ptMax = cms.untracked.double(0.4),
		)

process.vectKsMassN0_pT04 = process.vectKsMassN0_pT02.clone(
		ptMin = cms.untracked.double(0.4),
		ptMax = cms.untracked.double(0.6),
		)

## Lambda
#process.vectV0Mass.cstart = cms.untracked.double(1.0)
#process.vectV0Mass.cend = cms.untracked.double(1.2)

process.vectPt.cNbins = cms.untracked.int32(4000)
process.vectPt.cend = cms.untracked.double(40)
process.vectPtW.cNbins = cms.untracked.int32(4000)
process.vectPtW.cend = cms.untracked.double(40)

process.vectPhiV0 = process.vectPhi.clone(src = cms.untracked.InputTag('QWV0EventV0', 'phi'))
process.vectEtaV0 = process.vectEta.clone(src = cms.untracked.InputTag('QWV0EventV0', 'eta'))
process.vectPtV0  = process.vectPt.clone(src = cms.untracked.InputTag('QWV0EventV0', 'pt'))


process.ana = cms.Path(process.eventSelection * process.makeEvent * process.NoffFilter * process.QWV0EventV0 * process.QWCumuDiff * process.vectMonW * process.vectV0Mass * process.vectPhiV0 * process.vectEtaV0 * process.vectPtV0)

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
#	process.out
)
