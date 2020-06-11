import FWCore.ParameterSet.Config as cms
import FWCore.ParameterSet.VarParsing as VarParsing

process = cms.Process("CumuDiff")

process.load('Configuration.StandardSequences.Services_cff')
process.load('FWCore.MessageService.MessageLogger_cfi')
process.load('Configuration.StandardSequences.GeometryDB_cff')
process.load("TrackingTools/TransientTrack/TransientTrackBuilder_cfi")
process.load('Configuration.StandardSequences.MagneticField_38T_cff')
process.load('Configuration.StandardSequences.EndOfProcess_cff')
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_condDBv2_cff')

process.load("RecoVertex.PrimaryVertexProducer.OfflinePrimaryVerticesRecovery_cfi")


process.maxEvents = cms.untracked.PSet(input = cms.untracked.int32(-1))
process.MessageLogger.cerr.FwkReport.reportEvery = 100

from Configuration.AlCa.GlobalTag_condDBv2 import GlobalTag
process.GlobalTag = GlobalTag(process.GlobalTag, '103X_dataRun2_Prompt_v2', '')

process.GlobalTag.snapshotTime = cms.string("9999-12-31 23:59:59.000")
process.GlobalTag.toGet.extend([
	cms.PSet(record = cms.string("HeavyIonRcd"),
		tag = cms.string("CentralityTable_HFtowers200_DataPbPb_periHYDJETshape_run2v1033p1x01_offline"),
		connect = cms.string("frontier://FrontierProd/CMS_CONDITIONS"),
		label = cms.untracked.string("HFtowers")
		),
	])

process.load("RecoHI.HiCentralityAlgos.CentralityBin_cfi")
process.centralityBin.Centrality = cms.InputTag("hiCentrality")
process.centralityBin.centralityVariable = cms.string("HFtowers")

import HLTrigger.HLTfilters.hltHighLevel_cfi
process.hltMB = HLTrigger.HLTfilters.hltHighLevel_cfi.hltHighLevel.clone()
process.hltMB.HLTPaths = [
        "HLT_HIMinimumBias_*"
        ]
process.hltMB.andOr = cms.bool(True)
process.hltMB.throw = cms.bool(False)


process.options = cms.untracked.PSet(
        SkipEvent = cms.untracked.vstring('ProductNotFound')
        )

process.source = cms.Source("PoolSource",
        fileNames = cms.untracked.vstring(
            "file:/eos/cms/store/group/phys_heavyions/qwang/data/FF31F840-542E-1A49-ACF7-9043F8169E67.root"
            ),
        )

process.TFileService = cms.Service("TFileService",
        fileName = cms.string('cumu.root')
        )


process.load('HeavyIonsAnalysis.Configuration.hfCoincFilter_cff')
process.load('HeavyIonsAnalysis.Configuration.collisionEventSelection_cff')
process.load('RecoHI.HiCentralityAlgos.CentralityFilter_cfi')
process.load('PbPb18_HIMB_rereco')

process.eventSelection = cms.Sequence(
	process.primaryVertexFilter
	* process.hfCoincFilter2Th4
	* process.clusterCompatibilityFilter
    )

process.QWVertex = cms.EDProducer('QWVertexProducer',
        vertexSrc = cms.untracked.InputTag('offlinePrimaryVerticesRecovery')
        )

process.QWPrimaryVz = cms.EDProducer('QWVectorSelector',
        vectSrc = cms.untracked.InputTag('QWVertex', 'vz'),
        )

process.QWVzFilter15 = cms.EDFilter('QWDoubleFilter',
        src = cms.untracked.InputTag('QWPrimaryVz'),
        dmin = cms.untracked.double(-15.),
        dmax = cms.untracked.double(15.),
        )

process.QWPrimaryVertexSelection = cms.Sequence (process.QWVertex * process.QWPrimaryVz * process.QWVzFilter15)

process.Cent0 = process.centralityFilter.clone(
        selectedBins = cms.vint32(
            *range(0, 20)
            ),
        BinLabel = cms.InputTag("centralityBin", "HFtowers")
        )

process.Cent10 = process.centralityFilter.clone(
        selectedBins = cms.vint32(
            *range(20, 60)
            ),
        BinLabel = cms.InputTag("centralityBin", "HFtowers")
        )

process.Cent30 = process.centralityFilter.clone(
        selectedBins = cms.vint32(
            *range(60, 100)
            ),
        BinLabel = cms.InputTag("centralityBin", "HFtowers")
        )

process.Cent50 = process.centralityFilter.clone(
        selectedBins = cms.vint32(
            *range(100, 160)
            ),
        BinLabel = cms.InputTag("centralityBin", "HFtowers")
        )

process.Cent80 = process.centralityFilter.clone(
        selectedBins = cms.vint32(
            *range(160, 200)
            ),
        BinLabel = cms.InputTag("centralityBin", "HFtowers")
        )

process.vectPhi0  = process.vectPhi.clone()
process.vectPhi10 = process.vectPhi.clone()
process.vectPhi30 = process.vectPhi.clone()
process.vectPhi50 = process.vectPhi.clone()
process.vectPhi80 = process.vectPhi.clone()

process.vectPt0  = process.vectPt.clone()
process.vectPt10 = process.vectPt.clone()
process.vectPt30 = process.vectPt.clone()
process.vectPt50 = process.vectPt.clone()
process.vectPt80 = process.vectPt.clone()

process.vectEta0  = process.vectEta.clone()
process.vectEta10 = process.vectEta.clone()
process.vectEta30 = process.vectEta.clone()
process.vectEta50 = process.vectEta.clone()
process.vectEta80 = process.vectEta.clone()

process.corr2D0  = process.corr2D.clone();
process.corr2D10 = process.corr2D.clone();
process.corr2D30 = process.corr2D.clone();
process.corr2D50 = process.corr2D.clone();
process.corr2D80 = process.corr2D.clone();

process.vectMon0  = cms.Sequence( process.vectPhi0 * process.vectPt0 * process.vectEta0 * process.corr2D0 );

process.QWEvent.Year = cms.untracked.int32(2018)
process.QWEvent.chi2  = cms.untracked.double(0.18)

# sysLoose
process.QWEvent.dzdzerror = cms.untracked.double(5.0)
process.QWEvent.d0d0error = cms.untracked.double(5.0)
process.QWEvent.pterrorpt = cms.untracked.double(0.15)
process.QWEvent.chi2  = cms.untracked.double(0.18)

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
            Eta = cms.untracked.InputTag   ('QWEventS', 'eta'),
            Phi = cms.untracked.InputTag   ('QWEventS', 'phi'),
            Ref = cms.untracked.InputTag   ('QWEventRef2'),
            Pt = cms.untracked.InputTag    ('QWEventS', 'pt'),
            Weight = cms.untracked.InputTag('QWEventS', 'weight'),
            ),
        vertexZ = cms.untracked.InputTag('QWEvent', "vz"),
        ptBin = cms.untracked.vdouble(0.2, 0.4, 0.6, 0.8, 1.0, 1.4, 1.8, 2.2, 2.8, 3.6, 4.6,6.0, 7.0, 8.5),
        centrality = cms.untracked.InputTag('centralityBin', 'HFtowers')
        )

process.ana0 = cms.Path(
        process.hltMB
        * process.centralityBin
        * process.offlinePrimaryVerticesRecovery
        * process.eventSelection
        * process.QWPrimaryVertexSelection
        * process.QWEvent
        * process.QWEventS
        * process.QWEventRef2
        * process.QWCumuDiff
        * process.histCentBin
        * process.vectMon0
        )

process.schedule = cms.Schedule(
        process.ana0,
        )

from HLTrigger.Configuration.CustomConfigs import MassReplaceInputTag
process = MassReplaceInputTag(process,"offlinePrimaryVertices","offlinePrimaryVerticesRecovery")
process.offlinePrimaryVerticesRecovery.oldVertexLabel = "offlinePrimaryVertices"

