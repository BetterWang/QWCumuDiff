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

process.QWVertex = cms.EDProducer('QWVertexProducer',
		vertexSrc = cms.untracked.InputTag('offlinePrimaryVertices')
	)
process.QWPrimaryVz = cms.EDProducer('QWVectorSelector',
		vectSrc = cms.untracked.InputTag('QWVertex', 'vz'),
	)
process.QWVzFilter15 = cms.EDFilter('QWDoubleFilter',
		src = cms.untracked.InputTag('QWPrimaryVz'),
		dmin = cms.untracked.double(-15.),
		dmax = cms.untracked.double(15.),
	)
process.QWPrimaryVertexSelection = cms.Sequence( process.QWVertex * process.QWPrimaryVz * process.QWVzFilter15 )

process.load("HeavyIonsAnalysis.Configuration.hfCoincFilter_cff")
process.load("HeavyIonsAnalysis.EventAnalysis.pileUpFilter_cff")

process.eventSelection = cms.Sequence(process.hfCoincFilter * process.PAprimaryVertexFilter * process.NoScraping * process.olvFilter_pPb8TeV_dz1p0 * process.QWPrimaryVertexSelection)

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
			*range(250, 320)
			),
		BinLabel = cms.InputTag("Noff")
		)


process.QWV0EventLambda = cms.EDProducer('QWV0VectProducer'
        , vertexSrc = cms.untracked.InputTag('offlinePrimaryVertices')
        , trackSrc = cms.untracked.InputTag('generalTracks')
        , V0Src = cms.untracked.InputTag('generalV0CandidatesNew', 'Lambda')
        , daughter_cuts = cms.untracked.PSet(
                dauDCASig = cms.untracked.double(1.)
            )
        , cuts = cms.untracked.VPSet(
            cms.untracked.PSet(
                Massmin = cms.untracked.double(1.1115)
                , Massmax = cms.untracked.double(1.1200)
                , DecayXYZMin = cms.untracked.double(2.5)
                , ThetaXYZMin = cms.untracked.double(0.99)
                , ptMin = cms.untracked.double(0.2)
                , ptMax = cms.untracked.double(8.5)
                , Rapmin = cms.untracked.double(-1.0)
                , Rapmax = cms.untracked.double(1.0)
                )
            )
        )


process.load('pPb_HM_eff')
process.QWEvent.fweight = cms.untracked.InputTag('NA')
process.QWEvent.ptMin = cms.untracked.double(0.2)
process.QWEvent.ptMax = cms.untracked.double(8.5)

process.QWCumuDiff = cms.EDAnalyzer('QWCumuDiff',
		trackSet = cms.untracked.PSet(
			Eta = cms.untracked.InputTag('QWEvent', 'eta'),
			Phi = cms.untracked.InputTag('QWEvent', 'phi'),
			Ref = cms.untracked.InputTag('QWEvent', 'ref'),
			Pt  = cms.untracked.InputTag('QWEvent', 'pt'),
			Weight = cms.untracked.InputTag('QWEvent', 'weight'),
			),
		sigSet = cms.untracked.PSet(
			Eta = cms.untracked.InputTag('QWV0EventLambda', 'rapidity'),
			Phi = cms.untracked.InputTag('QWV0EventLambda', 'phi'),
			Ref = cms.untracked.InputTag('QWV0EventLambda', 'Refs'),
			Pt = cms.untracked.InputTag('QWV0EventLambda', 'pt'),
			Weight = cms.untracked.InputTag('QWV0EventLambda', 'weight'),
			),
		vertexZ = cms.untracked.InputTag('QWEvent', "vz"),
		ptBin = cms.untracked.vdouble(0.2, 0.4, 0.6, 0.8, 1.0, 1.4, 1.8, 2.2, 2.8, 3.6, 4.6,6.0, 7.0, 8.5),
		centrality = cms.untracked.InputTag('Noff')
		)

process.vectV0MassLm120 = cms.EDAnalyzer('QWVectorAnalyzer',
		src = cms.untracked.InputTag("QWV0EventLambda", "mass"),
		hNbins = cms.untracked.int32(100),
		hstart = cms.untracked.double(0),
		hend = cms.untracked.double(100),
		cNbins = cms.untracked.int32(160),
		cstart = cms.untracked.double(1.08),
		cend = cms.untracked.double(1.16),
		)

process.vectV0MassLm150 = process.vectV0MassLm120.clone()
process.vectV0MassLm185 = process.vectV0MassLm120.clone()
process.vectV0MassLm250 = process.vectV0MassLm120.clone()

process.vectPhi120Lm = process.vectPhi.clone(src = cms.untracked.InputTag('QWV0EventLambda', 'phi'))
process.vectPhi150Lm = process.vectPhi.clone(src = cms.untracked.InputTag('QWV0EventLambda', 'phi'))
process.vectPhi185Lm = process.vectPhi.clone(src = cms.untracked.InputTag('QWV0EventLambda', 'phi'))
process.vectPhi250Lm = process.vectPhi.clone(src = cms.untracked.InputTag('QWV0EventLambda', 'phi'))

process.vectEta120Lm = process.vectEta.clone(src = cms.untracked.InputTag('QWV0EventLambda', 'rapidity'))
process.vectEta150Lm = process.vectEta.clone(src = cms.untracked.InputTag('QWV0EventLambda', 'rapidity'))
process.vectEta185Lm = process.vectEta.clone(src = cms.untracked.InputTag('QWV0EventLambda', 'rapidity'))
process.vectEta250Lm = process.vectEta.clone(src = cms.untracked.InputTag('QWV0EventLambda', 'rapidity'))

process.vectPt120Lm = process.vectPt.clone(src = cms.untracked.InputTag('QWV0EventLambda', 'pt'), cNbins = cms.untracked.int32(1000), cend = cms.untracked.double(10))
process.vectPt150Lm = process.vectPt.clone(src = cms.untracked.InputTag('QWV0EventLambda', 'pt'), cNbins = cms.untracked.int32(1000), cend = cms.untracked.double(10))
process.vectPt185Lm = process.vectPt.clone(src = cms.untracked.InputTag('QWV0EventLambda', 'pt'), cNbins = cms.untracked.int32(1000), cend = cms.untracked.double(10))
process.vectPt250Lm = process.vectPt.clone(src = cms.untracked.InputTag('QWV0EventLambda', 'pt'), cNbins = cms.untracked.int32(1000), cend = cms.untracked.double(10))

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

process.vectPt120 = process.vectPt.clone(cNbins = cms.untracked.int32(1000), cend = cms.untracked.double(10.))
process.vectPt150 = process.vectPt.clone(cNbins = cms.untracked.int32(1000), cend = cms.untracked.double(10.))
process.vectPt185 = process.vectPt.clone(cNbins = cms.untracked.int32(1000), cend = cms.untracked.double(10.))
process.vectPt250 = process.vectPt.clone(cNbins = cms.untracked.int32(1000), cend = cms.untracked.double(10.))

process.vectPtW120 = process.vectPtW.clone()
process.vectPtW150 = process.vectPtW.clone()
process.vectPtW185 = process.vectPtW.clone()
process.vectPtW250 = process.vectPtW.clone()


process.mon120 = cms.Sequence(process.histNoff + process.vectPhi120 + process.vectPhi120Lm + process.vectPt120 + process.vectPt120Lm + process.vectEta120 + process.vectEta120Lm + process.vectV0MassLm120)
process.mon150 = cms.Sequence(process.histNoff + process.vectPhi150 + process.vectPhi150Lm + process.vectPt150 + process.vectPt150Lm + process.vectEta150 + process.vectEta150Lm + process.vectV0MassLm150)
process.mon185 = cms.Sequence(process.histNoff + process.vectPhi185 + process.vectPhi185Lm + process.vectPt185 + process.vectPt185Lm + process.vectEta185 + process.vectEta185Lm + process.vectV0MassLm185)
process.mon250 = cms.Sequence(process.histNoff + process.vectPhi250 + process.vectPhi250Lm + process.vectPt250 + process.vectPt250Lm + process.vectEta250 + process.vectEta250Lm + process.vectV0MassLm250)


process.ana120 = cms.Path(process.hltHM120*process.eventSelection*process.Noff*process.ppNoffFilter120*process.QWEvent * process.QWV0EventLambda * process.QWCumuDiff * process.mon120 )
process.ana150 = cms.Path(process.hltHM150*process.eventSelection*process.Noff*process.ppNoffFilter150*process.QWEvent * process.QWV0EventLambda * process.QWCumuDiff * process.mon150 )
process.ana185 = cms.Path(process.hltHM185*process.eventSelection*process.Noff*process.ppNoffFilter185*process.QWEvent * process.QWV0EventLambda * process.QWCumuDiff * process.mon185 )
process.ana250 = cms.Path(process.hltHM250*process.eventSelection*process.Noff*process.ppNoffFilter250*process.QWEvent * process.QWV0EventLambda * process.QWCumuDiff * process.mon250 )

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
	process.ana185,
#	process.ana250,
#	process.out
)
