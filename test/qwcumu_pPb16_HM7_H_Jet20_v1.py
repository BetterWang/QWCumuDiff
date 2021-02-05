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
process.GlobalTag = GlobalTag(process.GlobalTag, '80X_dataRun2_v19', '')

# Customization
from HeavyIonsAnalysis.Configuration.CommonFunctions_cff import overrideJEC_pPb8TeV
process = overrideJEC_pPb8TeV(process)

process.GlobalTag.toGet.extend([
        cms.PSet(record = cms.string("HeavyIonRcd"),
                          #tag = cms.string("CentralityTable_HFtowersPlusTrunc200_EPOS8TeV_v80x01_mc"),
                                  tag = cms.string("CentralityTable_HFtowersPlusTrunc200_EPOS5TeV_v80x01_mc"),
                                  connect = cms.string("frontier://FrontierProd/CMS_CONDITIONS"),
                                  label = cms.untracked.string("HFtowersPlusTruncEpos")
                              ),
        cms.PSet(record = cms.string("L1TGlobalPrescalesVetosRcd"),
                                 tag = cms.string("L1TGlobalPrescalesVetos_Stage2v0_hlt"),
                                 connect = cms.string("frontier://FrontierProd/CMS_CONDITIONS")
                                 )
])


process.maxEvents = cms.untracked.PSet(input = cms.untracked.int32(1000))
process.MessageLogger.cerr.FwkReport.reportEvery = 100


process.options = cms.untracked.PSet(
    SkipEvent = cms.untracked.vstring('ProductNotFound')
)

process.source = cms.Source("PoolSource",
        fileNames = cms.untracked.vstring(
            'file:/eos/cms/store/hidata/PARun2016C/PAHighMultiplicity0/AOD/PromptReco-v1/000/285/480/00000/AC8FA173-08AF-E611-94F2-02163E014561.root',
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



#process.load("HeavyIonsAnalysis.VertexAnalysis.PAPileUpVertexFilter_cff")
process.load("HeavyIonsAnalysis.VertexAnalysis.pileUpFilter_cff")

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
process.load("HeavyIonsAnalysis.JetAnalysis.FullJetSequence_puLimitedDatapPb")

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


process.load('pPb_HM_eff')
process.QWEvent.fweight = cms.untracked.InputTag('NA')
process.QWEvent.ptMin = cms.untracked.double(0.5)
process.QWEvent.ptMax = cms.untracked.double(5.0)

process.QWEventS = process.QWEvent.clone(
		ptMin = cms.untracked.double(0.2),
		ptMax= cms.untracked.double(8.5),
        Etamin = cms.untracked.double(-1.0),
        Etamax = cms.untracked.double(1.0)
        )

process.QWEventRef2 = cms.EDProducer('QWVector2',
        src = cms.untracked.InputTag('QWEventS', 'ref')
        )

process.QWCumuDiff = cms.EDAnalyzer('QWCumuDiff',
		trackSet = cms.untracked.PSet(
			Eta = cms.untracked.InputTag('QWEvent', 'eta'),
			Phi = cms.untracked.InputTag('QWEvent', 'phi'),
			Ref = cms.untracked.InputTag('QWEvent', 'ref'),
			Pt  = cms.untracked.InputTag('QWEvent', 'pt'),
			Weight = cms.untracked.InputTag('QWEvent', 'weight'),
			),
		sigSet = cms.untracked.PSet(
			Eta = cms.untracked.InputTag('QWEventS', 'eta'),
			Phi = cms.untracked.InputTag('QWEventS', 'phi'),
			Ref = cms.untracked.InputTag('QWEventRef2'),
			Pt = cms.untracked.InputTag('QWEventS', 'pt'),
			Weight = cms.untracked.InputTag('QWEventS', 'weight'),
			),
		vertexZ = cms.untracked.InputTag('QWEvent', "vz"),
		ptBin = cms.untracked.vdouble(0.2, 0.4, 0.6, 0.8, 1.0, 1.4, 1.8, 2.2, 2.8, 3.6, 4.6,6.0, 7.0, 8.5),
		centrality = cms.untracked.InputTag('Noff')
		)

process.vectPhi120Ks = process.vectPhi.clone(src = cms.untracked.InputTag('QWEvent', 'phi'))
process.vectPhi150Ks = process.vectPhi.clone(src = cms.untracked.InputTag('QWEvent', 'phi'))
process.vectPhi185Ks = process.vectPhi.clone(src = cms.untracked.InputTag('QWEvent', 'phi'))
process.vectPhi250Ks = process.vectPhi.clone(src = cms.untracked.InputTag('QWEvent', 'phi'))

process.vectEta120Ks = process.vectEta.clone(src = cms.untracked.InputTag('QWEventS', 'eta'))
process.vectEta150Ks = process.vectEta.clone(src = cms.untracked.InputTag('QWEventS', 'eta'))
process.vectEta185Ks = process.vectEta.clone(src = cms.untracked.InputTag('QWEventS', 'eta'))
process.vectEta250Ks = process.vectEta.clone(src = cms.untracked.InputTag('QWEventS', 'eta'))

process.vectPt120Ks = process.vectPt.clone(src = cms.untracked.InputTag('QWEventS', 'pt'), cNbins = cms.untracked.int32(1000), cend = cms.untracked.double(10))
process.vectPt150Ks = process.vectPt.clone(src = cms.untracked.InputTag('QWEventS', 'pt'), cNbins = cms.untracked.int32(1000), cend = cms.untracked.double(10))
process.vectPt185Ks = process.vectPt.clone(src = cms.untracked.InputTag('QWEventS', 'pt'), cNbins = cms.untracked.int32(1000), cend = cms.untracked.double(10))
process.vectPt250Ks = process.vectPt.clone(src = cms.untracked.InputTag('QWEventS', 'pt'), cNbins = cms.untracked.int32(1000), cend = cms.untracked.double(10))

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


process.mon120 = cms.Sequence(process.histNoff + process.vectPhi120Ks + process.vectPt120Ks + process.vectEta120Ks )
process.mon150 = cms.Sequence(process.histNoff + process.vectPhi150Ks + process.vectPt150Ks + process.vectEta150Ks )
process.mon185 = cms.Sequence(process.histNoff + process.vectPhi185Ks + process.vectPt185Ks + process.vectEta185Ks )
process.mon250 = cms.Sequence(process.histNoff + process.vectPhi250Ks + process.vectPt250Ks + process.vectEta250Ks )

process.QWVetoJet20 = cms.EDFilter('QWJetPtFilter',
        src = cms.untracked.InputTag('akPu4PFJets'),
        dmin = cms.untracked.double(0.),
        dmax = cms.untracked.double(20.),
        )

#process.ana120 = cms.Path(process.hltHM120*process.eventSelection*process.Noff*process.ppNoffFilter120*process.QWEvent * process.QWEventS * process.QWEventRef2 * process.mon120 )
#process.ana150 = cms.Path(process.hltHM150*process.eventSelection*process.Noff*process.ppNoffFilter150*process.QWEvent * process.QWEventS * process.QWEventRef2 * process.mon150 )
#process.ana185 = cms.Path(process.hltHM185*process.eventSelection*process.Noff*process.ppNoffFilter185*process.QWEvent * process.QWEventS * process.QWEventRef2 * process.mon185 )
#process.ana250 = cms.Path(process.hltHM250*process.eventSelection*process.Noff*process.ppNoffFilter250*process.QWEvent * process.QWEventS * process.QWEventRef2 * process.mon250 )
#
process.ana120 = cms.Path(process.hltHM120*process.eventSelection*process.Noff*process.ppNoffFilter120*process.PFTowers*process.akPu4PFJets*~process.QWVetoJet20*process.QWEvent * process.QWEventS * process.QWEventRef2 * process.QWCumuDiff * process.mon120 )
process.ana150 = cms.Path(process.hltHM150*process.eventSelection*process.Noff*process.ppNoffFilter150*process.PFTowers*process.akPu4PFJets*~process.QWVetoJet20*process.QWEvent * process.QWEventS * process.QWEventRef2 * process.QWCumuDiff * process.mon150 )
process.ana185 = cms.Path(process.hltHM185*process.eventSelection*process.Noff*process.ppNoffFilter185*process.PFTowers*process.akPu4PFJets*~process.QWVetoJet20*process.QWEvent * process.QWEventS * process.QWEventRef2 * process.QWCumuDiff * process.mon185 )
process.ana250 = cms.Path(process.hltHM250*process.eventSelection*process.Noff*process.ppNoffFilter250*process.PFTowers*process.akPu4PFJets*~process.QWVetoJet20*process.QWEvent * process.QWEventS * process.QWEventRef2 * process.QWCumuDiff * process.mon250 )
process.RECO = cms.OutputModule("PoolOutputModule",
		outputCommands = cms.untracked.vstring('drop *',
                                         'keep *_*_*_CumuV3'
                                         ),
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
