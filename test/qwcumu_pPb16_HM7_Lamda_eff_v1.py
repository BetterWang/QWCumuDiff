import FWCore.ParameterSet.Config as cms

process = cms.Process("CumuV3")

process.load('Configuration.StandardSequences.Services_cff')
process.load('FWCore.MessageService.MessageLogger_cfi')
process.load('Configuration.StandardSequences.GeometryDB_cff')
process.load("TrackingTools/TransientTrack/TransientTrackBuilder_cfi")
process.load("Configuration.Geometry.GeometryDB_cff")
process.load('Configuration.StandardSequences.MagneticField_38T_cff')
process.load('Configuration.StandardSequences.EndOfProcess_cff')
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_condDBv2_cff')

from Configuration.AlCa.GlobalTag import GlobalTag
process.GlobalTag = GlobalTag(process.GlobalTag, '80X_dataRun2_Prompt_v16', '')



process.maxEvents = cms.untracked.PSet(input = cms.untracked.int32(-1))
process.MessageLogger.cerr.FwkReport.reportEvery = 100


process.options = cms.untracked.PSet(
    SkipEvent = cms.untracked.vstring('ProductNotFound')
)

process.source = cms.Source("PoolSource",
#        fileNames = cms.untracked.vstring("file:/afs/cern.ch/user/q/qwang/work/cleanroomRun2/Ana/data/pPb_V0_v1.root"),
        fileNames = cms.untracked.vstring("/store/user/davidlw/PAHighMultiplicity0/RecoSkim2016_pPb_V0Cascade_v1/170301_201930/0000/pPb_HM_28.root"),
	secondaryFileNames = cms.untracked.vstring(
#		'file:/eos/cms/store/hidata/PARun2016C/PAHighMultiplicity0/AOD/PromptReco-v1/000/285/479/00000/3AB7179C-DCAE-E611-980E-FA163EC8DDF7.root',
#		'file:/eos/cms/store/hidata/PARun2016C/PAHighMultiplicity0/AOD/PromptReco-v1/000/285/480/00000/0E343491-06AF-E611-AF4F-FA163E0C8993.root',
#		'file:/eos/cms/store/hidata/PARun2016C/PAHighMultiplicity0/AOD/PromptReco-v1/000/285/480/00000/CAAC6AB7-06AF-E611-A23C-FA163EA53949.root',
#		'file:/eos/cms/store/hidata/PARun2016C/PAHighMultiplicity0/AOD/PromptReco-v1/000/285/480/00000/D0F23BC7-06AF-E611-8D86-FA163EA3E531.root',
#		'file:/eos/cms/store/hidata/PARun2016C/PAHighMultiplicity0/AOD/PromptReco-v1/000/285/480/00000/FE0873CE-06AF-E611-92B7-02163E0140FE.root'
		'file:/eos/cms/store/hidata/PARun2016C/PAHighMultiplicity0/AOD/PromptReco-v1/000/285/480/00000/AC8FA173-08AF-E611-94F2-02163E014561.root',
		'file:/eos/cms/store/hidata/PARun2016C/PAHighMultiplicity0/AOD/PromptReco-v1/000/285/480/00000/A417C575-08AF-E611-9BFC-FA163E05A16C.root',
		'file:/eos/cms/store/hidata/PARun2016C/PAHighMultiplicity0/AOD/PromptReco-v1/000/285/480/00000/34DF5A88-08AF-E611-BC70-FA163E5AF33F.root',
		'file:/eos/cms/store/hidata/PARun2016C/PAHighMultiplicity0/AOD/PromptReco-v1/000/285/480/00000/1E07EF6E-08AF-E611-A8B7-FA163EFF24E2.root',
		)
)

import HLTrigger.HLTfilters.hltHighLevel_cfi
process.hltHM120 = HLTrigger.HLTfilters.hltHighLevel_cfi.hltHighLevel.clone()
process.hltHM120.HLTPaths = [
	"HLT_PAFullTracks_Multiplicity120_v*",
#	"HLT_PAFullTracks_Multiplicity150_v*",
#	"HLT_PAFullTracks_Multiplicity185_*",
#	"HLT_PAFullTracks_Multiplicity220_v*",
#	"HLT_PAFullTracks_Multiplicity250_v*",
#	"HLT_PAFullTracks_Multiplicity280_v*",
]
process.hltHM120.andOr = cms.bool(True)
process.hltHM120.throw = cms.bool(False)

process.hltHM150 = HLTrigger.HLTfilters.hltHighLevel_cfi.hltHighLevel.clone()
process.hltHM150.HLTPaths = [
	"HLT_PAFullTracks_Multiplicity120_v*",
	"HLT_PAFullTracks_Multiplicity150_v*",
#	"HLT_PAFullTracks_Multiplicity185_*",
#	"HLT_PAFullTracks_Multiplicity220_v*",
#	"HLT_PAFullTracks_Multiplicity250_v*",
#	"HLT_PAFullTracks_Multiplicity280_v*",
]
process.hltHM150.andOr = cms.bool(True)
process.hltHM150.throw = cms.bool(False)

process.hltHM185 = HLTrigger.HLTfilters.hltHighLevel_cfi.hltHighLevel.clone()
process.hltHM185.HLTPaths = [
#	"HLT_PAFullTracks_Multiplicity120_v*",
#	"HLT_PAFullTracks_Multiplicity150_v*",
	"HLT_PAFullTracks_Multiplicity185_*",
#	"HLT_PAFullTracks_Multiplicity220_v*",
#	"HLT_PAFullTracks_Multiplicity250_v*",
#	"HLT_PAFullTracks_Multiplicity280_v*",
]
process.hltHM185.andOr = cms.bool(True)
process.hltHM185.throw = cms.bool(False)

process.hltHM250 = HLTrigger.HLTfilters.hltHighLevel_cfi.hltHighLevel.clone()
process.hltHM250.HLTPaths = [
#	"HLT_PAFullTracks_Multiplicity120_v*",
#	"HLT_PAFullTracks_Multiplicity150_v*",
#	"HLT_PAFullTracks_Multiplicity185_*",
#	"HLT_PAFullTracks_Multiplicity220_v*",
	"HLT_PAFullTracks_Multiplicity250_v*",
#	"HLT_PAFullTracks_Multiplicity280_v*",
]
process.hltHM250.andOr = cms.bool(True)
process.hltHM250.throw = cms.bool(False)


process.TFileService = cms.Service("TFileService",
    fileName = cms.string('cumu.root')
)



process.load("HeavyIonsAnalysis.VertexAnalysis.PAPileUpVertexFilter_cff")

process.PAprimaryVertexFilter = cms.EDFilter("VertexSelector",
    src = cms.InputTag("offlinePrimaryVertices"),
    cut = cms.string("!isFake && abs(z) <= 25 && position.Rho <= 2 && tracksSize >= 2"),
    filter = cms.bool(True), # otherwise it won't filter the events
)

process.NoScraping = cms.EDFilter("FilterOutScraping",
 applyfilter = cms.untracked.bool(True),
 debugOn = cms.untracked.bool(False),
 numtrack = cms.untracked.uint32(10),
 thresh = cms.untracked.double(0.25)
)

process.load("HeavyIonsAnalysis.Configuration.hfCoincFilter_cff")
process.load("HeavyIonsAnalysis.EventAnalysis.pileUpFilter_cff")

process.eventSelection = cms.Sequence(process.hfCoincFilter * process.PAprimaryVertexFilter * process.NoScraping * process.olvFilter_pPb8TeV_dz1p0)

process.load('RecoHI.HiCentralityAlgos.CentralityFilter_cfi')
process.ppNoffFilter120 = process.centralityFilter.clone(
		selectedBins = cms.vint32(
			*range(120, 150)
			),
		BinLabel = cms.InputTag("Noff")
		)

process.ppNoffFilter150 = process.centralityFilter.clone(
		selectedBins = cms.vint32(
			*range(150, 185)
			),
		BinLabel = cms.InputTag("Noff")
		)

process.ppNoffFilter185 = process.centralityFilter.clone(
		selectedBins = cms.vint32(
			*range(185, 250)
			),
		BinLabel = cms.InputTag("Noff")
		)

process.ppNoffFilter250 = process.centralityFilter.clone(
		selectedBins = cms.vint32(
			*range(250, 600)
			),
		BinLabel = cms.InputTag("Noff")
		)

process.QWV0EventKs = cms.EDProducer('QWV0VectProducer'
		, vertexSrc = cms.untracked.InputTag('offlinePrimaryVertices', "")
		, trackSrc = cms.untracked.InputTag('generalTracks')
		, V0Src = cms.untracked.InputTag('generalV0CandidatesNew', 'Kshort')
		, cuts = cms.untracked.VPSet(
			cms.untracked.PSet(
				Massmin = cms.untracked.double(0.467)
				, Massmax = cms.untracked.double(0.523)
				, DecayXYZMin = cms.untracked.double(5.0)
				, DecayXYZMax = cms.untracked.double(999999999999.)
				, ThetaXYZMin = cms.untracked.double(0.999)
				, ThetaXYZMax = cms.untracked.double(999999999999.)
				),
			)
		)

process.QWV0EventLambda = cms.EDProducer('QWV0VectProducer'
		, vertexSrc = cms.untracked.InputTag('offlinePrimaryVertices', "")
		, trackSrc = cms.untracked.InputTag('generalTracks')
		, V0Src = cms.untracked.InputTag('generalV0CandidatesNew', 'Lambda')
		, cuts = cms.untracked.VPSet(
			cms.untracked.PSet(
				Massmin = cms.untracked.double(1.11)
				, Massmax = cms.untracked.double(1.123)
				, DecayXYZMin = cms.untracked.double(5.0)
				, DecayXYZMax = cms.untracked.double(999999999999.)
				, ThetaXYZMin = cms.untracked.double(0.999)
				, ThetaXYZMax = cms.untracked.double(999999999999.)
				),
			)
		)

process.QWV0EventLambdaAll = cms.EDProducer('QWV0VectProducer'
		, vertexSrc = cms.untracked.InputTag('offlinePrimaryVertices', "")
		, trackSrc = cms.untracked.InputTag('generalTracks')
		, V0Src = cms.untracked.InputTag('generalV0CandidatesNew', 'Lambda')
		, cuts = cms.untracked.VPSet(
			cms.untracked.PSet(
				Massmin = cms.untracked.double(0)
				, Massmax = cms.untracked.double(10.)
				, DecayXYZMin = cms.untracked.double(5.0)
				, DecayXYZMax = cms.untracked.double(999999999999.)
				, ThetaXYZMin = cms.untracked.double(0.999)
				, ThetaXYZMax = cms.untracked.double(999999999999.)
				),
			)
		)


process.QWV0EventV0 = process.QWV0EventLambda.clone()

process.load('pPb_HM_eff')
process.QWEvent.fweight = cms.untracked.InputTag('Hijing_8TeV_dataBS.root')
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

process.vectV0Mass120 = cms.EDAnalyzer('QWVectorAnalyzer',
		src = cms.untracked.InputTag("QWV0EventV0", "mass"),
		hNbins = cms.untracked.int32(100),
		hstart = cms.untracked.double(0),
		hend = cms.untracked.double(100),
		cNbins = cms.untracked.int32(100),
		cstart = cms.untracked.double(1.1),
		cend = cms.untracked.double(1.14),
		)

process.vectV0Mass150 = process.vectV0Mass120.clone()
process.vectV0Mass185 = process.vectV0Mass120.clone()
process.vectV0Mass250 = process.vectV0Mass120.clone()

process.vectPhi120Ks = process.vectPhi.clone(src = cms.untracked.InputTag('QWV0EventV0', 'phi'))
process.vectPhi150Ks = process.vectPhi.clone(src = cms.untracked.InputTag('QWV0EventV0', 'phi'))
process.vectPhi185Ks = process.vectPhi.clone(src = cms.untracked.InputTag('QWV0EventV0', 'phi'))
process.vectPhi250Ks = process.vectPhi.clone(src = cms.untracked.InputTag('QWV0EventV0', 'phi'))

process.vectEta120Ks = process.vectEta.clone(src = cms.untracked.InputTag('QWV0EventV0', 'eta'))
process.vectEta150Ks = process.vectEta.clone(src = cms.untracked.InputTag('QWV0EventV0', 'eta'))
process.vectEta185Ks = process.vectEta.clone(src = cms.untracked.InputTag('QWV0EventV0', 'eta'))
process.vectEta250Ks = process.vectEta.clone(src = cms.untracked.InputTag('QWV0EventV0', 'eta'))

process.vectPt120Ks = process.vectPt.clone(src = cms.untracked.InputTag('QWV0EventV0', 'pt'), cNbins = cms.untracked.int32(4000), cend = cms.untracked.double(40))
process.vectPt150Ks = process.vectPt.clone(src = cms.untracked.InputTag('QWV0EventV0', 'pt'), cNbins = cms.untracked.int32(4000), cend = cms.untracked.double(40))
process.vectPt185Ks = process.vectPt.clone(src = cms.untracked.InputTag('QWV0EventV0', 'pt'), cNbins = cms.untracked.int32(4000), cend = cms.untracked.double(40))
process.vectPt250Ks = process.vectPt.clone(src = cms.untracked.InputTag('QWV0EventV0', 'pt'), cNbins = cms.untracked.int32(4000), cend = cms.untracked.double(40))

process.vectPhi120 = process.vectPhi.clone()
process.vectPhi150 = process.vectPhi.clone()
process.vectPhi185 = process.vectPhi.clone()
process.vectPhi250 = process.vectPhi.clone()

process.vectPhiW120 = process.vectPhiW.clone()
process.vectPhiW150 = process.vectPhiW.clone()
process.vectPhiW185 = process.vectPhiW.clone()
process.vectPhiW250 = process.vectPhiW.clone()

process.vectEta120 = process.vectEta.clone()
process.vectEta150 = process.vectEta.clone()
process.vectEta185 = process.vectEta.clone()
process.vectEta250 = process.vectEta.clone()

process.vectEtaW120 = process.vectEtaW.clone()
process.vectEtaW150 = process.vectEtaW.clone()
process.vectEtaW185 = process.vectEtaW.clone()
process.vectEtaW250 = process.vectEtaW.clone()

process.vectPt120 = process.vectPt.clone()
process.vectPt150 = process.vectPt.clone()
process.vectPt185 = process.vectPt.clone()
process.vectPt250 = process.vectPt.clone()

process.vectPtW120 = process.vectPtW.clone()
process.vectPtW150 = process.vectPtW.clone()
process.vectPtW185 = process.vectPtW.clone()
process.vectPtW250 = process.vectPtW.clone()


process.vectMass120 = cms.EDAnalyzer('QWMassAnalyzer',
		srcMass = cms.untracked.InputTag('QWV0EventLambdaAll', 'mass'),
		srcEta = cms.untracked.InputTag('QWV0EventLambdaAll', 'eta'),
		srcPt = cms.untracked.InputTag('QWV0EventLambdaAll', 'pt'),
		Nbins = cms.untracked.int32(100),
		start = cms.untracked.double(1.1),
		end   = cms.untracked.double(1.14),
		cuts  = cms.untracked.VPSet(

			cms.untracked.PSet(
				ptMin = cms.untracked.double(0.1),
				ptMax = cms.untracked.double(0.5),
				etaMin = cms.untracked.double(-2.4),
				etaMax = cms.untracked.double(2.4),
				),

			cms.untracked.PSet(
				ptMin = cms.untracked.double(0.5),
				ptMax = cms.untracked.double(1.0),
				etaMin = cms.untracked.double(-2.4),
				etaMax = cms.untracked.double(2.4),
				),

			cms.untracked.PSet(
				ptMin = cms.untracked.double(1.0),
				ptMax = cms.untracked.double(1.5),
				etaMin = cms.untracked.double(-2.4),
				etaMax = cms.untracked.double(2.4),
				),

			cms.untracked.PSet(
				ptMin = cms.untracked.double(1.5),
				ptMax = cms.untracked.double(2.0),
				etaMin = cms.untracked.double(-2.4),
				etaMax = cms.untracked.double(2.4),
				),

			cms.untracked.PSet(
				ptMin = cms.untracked.double(2.0),
				ptMax = cms.untracked.double(2.5),
				etaMin = cms.untracked.double(-2.4),
				etaMax = cms.untracked.double(2.4),
				),

			cms.untracked.PSet(
				ptMin = cms.untracked.double(2.5),
				ptMax = cms.untracked.double(3.0),
				etaMin = cms.untracked.double(-2.4),
				etaMax = cms.untracked.double(2.4),
				),

			cms.untracked.PSet(
				ptMin = cms.untracked.double(3.0),
				ptMax = cms.untracked.double(4.0),
				etaMin = cms.untracked.double(-2.4),
				etaMax = cms.untracked.double(2.4),
				),

			cms.untracked.PSet(
				ptMin = cms.untracked.double(4.0),
				ptMax = cms.untracked.double(5.0),
				etaMin = cms.untracked.double(-2.4),
				etaMax = cms.untracked.double(2.4),
				),

			cms.untracked.PSet(
				ptMin = cms.untracked.double(5.0),
				ptMax = cms.untracked.double(6.0),
				etaMin = cms.untracked.double(-2.4),
				etaMax = cms.untracked.double(2.4),
				),

			cms.untracked.PSet(
				ptMin = cms.untracked.double(6.0),
				ptMax = cms.untracked.double(8.0),
				etaMin = cms.untracked.double(-2.4),
				etaMax = cms.untracked.double(2.4),
				),

			cms.untracked.PSet(
				ptMin = cms.untracked.double(8.0),
				ptMax = cms.untracked.double(10.0),
				etaMin = cms.untracked.double(-2.4),
				etaMax = cms.untracked.double(2.4),
				),

			cms.untracked.PSet(
				ptMin = cms.untracked.double(10.0),
				ptMax = cms.untracked.double(12.0),
				etaMin = cms.untracked.double(-2.4),
				etaMax = cms.untracked.double(2.4),
				),

			cms.untracked.PSet(
				ptMin = cms.untracked.double(12.0),
				ptMax = cms.untracked.double(16.0),
				etaMin = cms.untracked.double(-2.4),
				etaMax = cms.untracked.double(2.4),
				),

			cms.untracked.PSet(
				ptMin = cms.untracked.double(16.0),
				ptMax = cms.untracked.double(20.0),
				etaMin = cms.untracked.double(-2.4),
				etaMax = cms.untracked.double(2.4),
				),

			cms.untracked.PSet(
				ptMin = cms.untracked.double(20.0),
				ptMax = cms.untracked.double(30.0),
				etaMin = cms.untracked.double(-2.4),
				etaMax = cms.untracked.double(2.4),
				),

			cms.untracked.PSet(
				ptMin = cms.untracked.double(30.0),
				ptMax = cms.untracked.double(40.0),
				etaMin = cms.untracked.double(-2.4),
				etaMax = cms.untracked.double(2.4),
				),
			)
	)


process.vectMass150 = process.vectMass120.clone()
process.vectMass185 = process.vectMass120.clone()
process.vectMass250 = process.vectMass120.clone()


process.mon120 = cms.Sequence(process.histNoff + process.vectPhi120 + process.vectPhi120Ks + process.vectPt120 + process.vectPt120Ks + process.vectEta120 + process.vectEta120Ks + process.vectPhiW120 + process.vectPtW120 + process.vectEtaW120 + process.vectMass120)
process.mon150 = cms.Sequence(process.histNoff + process.vectPhi150 + process.vectPhi150Ks + process.vectPt150 + process.vectPt150Ks + process.vectEta150 + process.vectEta150Ks + process.vectPhiW150 + process.vectPtW150 + process.vectEtaW150 + process.vectMass150)
process.mon185 = cms.Sequence(process.histNoff + process.vectPhi185 + process.vectPhi185Ks + process.vectPt185 + process.vectPt185Ks + process.vectEta185 + process.vectEta185Ks + process.vectPhiW185 + process.vectPtW185 + process.vectEtaW185 + process.vectMass185)
process.mon250 = cms.Sequence(process.histNoff + process.vectPhi250 + process.vectPhi250Ks + process.vectPt250 + process.vectPt250Ks + process.vectEta250 + process.vectEta250Ks + process.vectPhiW250 + process.vectPtW250 + process.vectEtaW250 + process.vectMass250)

process.ana120 = cms.Path(process.hltHM120*process.eventSelection*process.Noff*process.ppNoffFilter120*process.QWEvent * process.QWV0EventV0 * process.QWV0EventLambdaAll * process.QWCumuDiff * process.mon120)
process.ana150 = cms.Path(process.hltHM150*process.eventSelection*process.Noff*process.ppNoffFilter150*process.QWEvent * process.QWV0EventV0 * process.QWV0EventLambdaAll * process.QWCumuDiff * process.mon150)
process.ana185 = cms.Path(process.hltHM185*process.eventSelection*process.Noff*process.ppNoffFilter185*process.QWEvent * process.QWV0EventV0 * process.QWV0EventLambdaAll * process.QWCumuDiff * process.mon185)
process.ana250 = cms.Path(process.hltHM250*process.eventSelection*process.Noff*process.ppNoffFilter250*process.QWEvent * process.QWV0EventV0 * process.QWV0EventLambdaAll * process.QWCumuDiff * process.mon250)

process.RECO = cms.OutputModule("PoolOutputModule",
		outputCommands = cms.untracked.vstring('keep *'),
		SelectEvents = cms.untracked.PSet(
			SelectEvents = cms.vstring('ana120', 'ana150')
			),
		fileName = cms.untracked.string('recoV0.root')
		)

process.out = cms.EndPath(process.RECO)
process.schedule = cms.Schedule(
#	process.ana120,
#	process.ana150,
#	process.ana185,
	process.ana250,
#	process.out
)
