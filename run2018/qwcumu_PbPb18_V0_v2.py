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

options = VarParsing.VarParsing('analysis')

options.register('part',
                'LM',
                VarParsing.VarParsing.multiplicity.singleton,
                VarParsing.VarParsing.varType.string,
                "LM or KS")

options.register('massRange',
                'Peak',
                VarParsing.VarParsing.multiplicity.singleton,
                VarParsing.VarParsing.varType.string,
                "Peak/SBPos/SBNeg")

options.register('rap',
                'Mid',
                VarParsing.VarParsing.multiplicity.singleton,
                VarParsing.VarParsing.varType.string,
                "Mid/Fwd")

options.register('BDT',
                0.15,
                VarParsing.VarParsing.multiplicity.singleton,
                VarParsing.VarParsing.varType.float,
                "BDT cut")

options.parseArguments()

massLow = 0.;
massHigh = 0.;

if options.part == 'LM':
    if options.massRange == 'Peak':
        massLow = 1.1115
        massHigh = 1.1200
    if options.massRange == 'SBPos':
        massLow = 1.122
        massHigh = 1.16
    if options.massRange == 'SBNeg':
        massLow = 1.08
        massHigh = 1.1095

if options.part == 'KS':
    if options.massRange == 'Peak':
        massLow = 0.492
        massHigh = 0.503
    if options.massRange == 'SBPos':
        massLow = 0.506
        massHigh = 0.565
    if options.massRange == 'SBNeg':
        massLow = 0.43
        massHigh = 0.489

print options.part
print options.massRange
print options.rap
print options.BDT


#process.load("RecoHI.HiEvtPlaneAlgos.HiEvtPlane_cfi")
#process.load("RecoHI.HiEvtPlaneAlgos.hiEvtPlaneFlat_cfi")
#
#process.load("CondCore.CondDB.CondDB_cfi")

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


process.options = cms.untracked.PSet(
        SkipEvent = cms.untracked.vstring('ProductNotFound')
        )

process.source = cms.Source("PoolSource",
        fileNames = cms.untracked.vstring("file:/afs/cern.ch/user/q/qwang/work/cleanroomRun2/Ana/data/PbPb2018_RERECO_V0Skim.root"),
        secondaryFileNames = cms.untracked.vstring(
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

if options.part == 'LM':
    process.vectMass0  = process.vectMassLm.clone();
    process.vectMass10 = process.vectMassLm.clone();
    process.vectMass30 = process.vectMassLm.clone();
    process.vectMass50 = process.vectMassLm.clone();
    process.vectMass80 = process.vectMassLm.clone();

if options.part == 'KS':
    process.vectMass0  = process.vectMassKs.clone();
    process.vectMass10 = process.vectMassKs.clone();
    process.vectMass30 = process.vectMassKs.clone();
    process.vectMass50 = process.vectMassKs.clone();
    process.vectMass80 = process.vectMassKs.clone();

process.vectMon0  = cms.Sequence( process.vectPhi0 * process.vectPt0 * process.vectEta0 * process.corr2D0  * process.vectMass0 );
process.vectMon10 = cms.Sequence( process.vectPhi10* process.vectPt10* process.vectEta10* process.corr2D10 * process.vectMass10);
process.vectMon30 = cms.Sequence( process.vectPhi30* process.vectPt30* process.vectEta30* process.corr2D30 * process.vectMass30);
process.vectMon50 = cms.Sequence( process.vectPhi50* process.vectPt50* process.vectEta50* process.corr2D50 * process.vectMass50);
process.vectMon80 = cms.Sequence( process.vectPhi80* process.vectPt80* process.vectEta80* process.corr2D80 * process.vectMass80);


if options.part == 'LM':
    process.QWV0Event = process.QWV0EventLm.clone()
if options.part == 'KS':
    process.QWV0Event = process.QWV0EventKs.clone()

if options.rap == 'Fwd':
    process.QWV0Event.cuts[0].AbsRapmax = cms.untracked.double(2.0)
    process.QWV0Event.cuts[0].AbsRapmin = cms.untracked.double(1.0)

process.QWV0MVA = cms.EDProducer('QWV0MVAVectProducer'
        , vertexSrc = cms.untracked.InputTag('offlinePrimaryVerticesRecovery')
        , V0Src = cms.untracked.InputTag('QWV0Event', 'Lambda')
        , dbCent = cms.untracked.InputTag('dbCent')
        , mvaXML = cms.untracked.string('MC_Full_BDT250_D4.LM.weights.xml')
        , mvaCut = cms.untracked.double(options.BDT)
        )


if options.part == 'KS':
    process.QWV0MVA.V0Src = cms.untracked.InputTag('QWV0Event', 'Kshort')
    process.QWV0MVA.mvaXML = cms.untracked.string('MC_Full_BDT250_D4.KS.weights.xml')

process.QWV0MVAVector = cms.EDProducer('QWV0VectProducer'
        , vertexSrc = cms.untracked.InputTag('offlinePrimaryVerticesRecovery')
        , trackSrc = cms.untracked.InputTag('generalTracks')
        , V0Src = cms.untracked.InputTag('QWV0MVA', 'Lambda')
        , daughter_cuts = cms.untracked.PSet(
            )
        , cuts = cms.untracked.VPSet(
            cms.untracked.PSet(
                )
            )
        )

if options.part == 'KS':
    process.QWV0MVAVector.V0Src = cms.untracked.InputTag('QWV0MVA', 'Kshort')

process.QWV0MVAMon = process.QWV0MVAVector.clone()

process.QWCumuDiff = cms.EDAnalyzer('QWCumuDiff',
        trackSet = cms.untracked.PSet(
            Eta = cms.untracked.InputTag('QWEvent', 'eta'),
            Phi = cms.untracked.InputTag('QWEvent', 'phi'),
            Ref = cms.untracked.InputTag('QWEvent', 'ref'),
            Pt  = cms.untracked.InputTag('QWEvent', 'pt'),
            Weight = cms.untracked.InputTag('QWEvent', 'weight'),
            ),
        sigSet = cms.untracked.PSet(
            Eta = cms.untracked.InputTag   ('QWV0MVAVector', 'rapidity'),
            Phi = cms.untracked.InputTag   ('QWV0MVAVector', 'phi'),
            Ref = cms.untracked.InputTag   ('QWV0MVAVector', 'Refs'),
            Pt = cms.untracked.InputTag    ('QWV0MVAVector', 'pt'),
            Weight = cms.untracked.InputTag('QWV0MVAVector', 'weight'),
            ),
        vertexZ = cms.untracked.InputTag('QWEvent', "vz"),
        ptBin = cms.untracked.vdouble(0.2, 0.4, 0.6, 0.8, 1.0, 1.4, 1.8, 2.2, 2.8, 3.6, 4.6,6.0, 7.0, 8.5),
        centrality = cms.untracked.InputTag('centralityBin', 'HFtowers')
        )

process.QWEvent.Year = cms.untracked.int32(2018)
process.QWEvent.chi2  = cms.untracked.double(0.18)

process.ana0 = cms.Path(
        process.eventSelection
        * process.QWPrimaryVertexSelection
        * process.Cent0
        * process.dbCent
        * process.QWEvent
        * process.QWV0Event
        * process.QWV0MVA
        * process.QWV0MVAVector
        * process.QWCumuDiff
        * process.histCentBin
        * process.vectMon0
        )

process.ana10 = cms.Path(
        process.eventSelection
        * process.QWPrimaryVertexSelection
        * process.Cent10
        * process.dbCent
        * process.QWEvent
        * process.QWV0Event
        * process.QWV0MVA
        * process.QWV0MVAVector
        * process.QWCumuDiff
        * process.histCentBin
        * process.vectMon10
        )

process.ana30 = cms.Path(
        process.eventSelection
        * process.QWPrimaryVertexSelection
        * process.Cent30
        * process.dbCent
        * process.QWEvent
        * process.QWV0Event
        * process.QWV0MVA
        * process.QWV0MVAVector
        * process.QWCumuDiff
        * process.histCentBin
        * process.vectMon30
        )


process.ana50 = cms.Path(
        process.eventSelection
        * process.QWPrimaryVertexSelection
        * process.Cent50
        * process.dbCent
        * process.QWEvent
        * process.QWV0Event
        * process.QWV0MVA
        * process.QWV0MVAVector
        * process.QWCumuDiff
        * process.histCentBin
        * process.vectMon50
        )

process.ana80 = cms.Path(
        process.eventSelection
        * process.QWPrimaryVertexSelection
        * process.Cent80
        * process.dbCent
        * process.QWEvent
        * process.QWV0Event
        * process.QWV0MVA
        * process.QWV0MVAVector
        * process.QWCumuDiff
        * process.histCentBin
        * process.vectMon80
        )

process.RECO = cms.OutputModule("PoolOutputModule",
        outputCommands = cms.untracked.vstring('drop *',
            'keep *_*_*_CumuDiff'),
        SelectEvents = cms.untracked.PSet(
            SelectEvents = cms.vstring('ana0', 'ana10', 'ana30', 'ana50', 'ana80')
            ),
        fileName = cms.untracked.string('recoV0.root')
        )


process.out = cms.EndPath(process.RECO)

if options.massRange == 'Peak':
    process.QWV0MVAVector.cuts[0].Massmin = cms.untracked.double(massLow)
    process.QWV0MVAVector.cuts[0].Massmax = cms.untracked.double(massHigh)
    process.ana0.insert(10, process.QWV0MVAMon)
    process.ana10.insert(10, process.QWV0MVAMon)
    process.ana30.insert(10, process.QWV0MVAMon)
    process.ana50.insert(10, process.QWV0MVAMon)
    process.ana80.insert(10, process.QWV0MVAMon)
    process.vectMass0.srcMass  = cms.untracked.InputTag("QWV0MVAMon", "mass")
    process.vectMass10.srcMass = cms.untracked.InputTag("QWV0MVAMon", "mass")
    process.vectMass30.srcMass = cms.untracked.InputTag("QWV0MVAMon", "mass")
    process.vectMass50.srcMass = cms.untracked.InputTag("QWV0MVAMon", "mass")
    process.vectMass80.srcMass = cms.untracked.InputTag("QWV0MVAMon", "mass")
    process.vectMass0.srcPt    = cms.untracked.InputTag("QWV0MVAMon", "pt")
    process.vectMass10.srcPt   = cms.untracked.InputTag("QWV0MVAMon", "pt")
    process.vectMass30.srcPt   = cms.untracked.InputTag("QWV0MVAMon", "pt")
    process.vectMass50.srcPt   = cms.untracked.InputTag("QWV0MVAMon", "pt")
    process.vectMass80.srcPt   = cms.untracked.InputTag("QWV0MVAMon", "pt")
    process.vectMass0.srcEta   = cms.untracked.InputTag("QWV0MVAMon", "rapidity")
    process.vectMass10.srcEta  = cms.untracked.InputTag("QWV0MVAMon", "rapidity")
    process.vectMass30.srcEta  = cms.untracked.InputTag("QWV0MVAMon", "rapidity")
    process.vectMass50.srcEta  = cms.untracked.InputTag("QWV0MVAMon", "rapidity")
    process.vectMass80.srcEta  = cms.untracked.InputTag("QWV0MVAMon", "rapidity")
    process.vectMass0.srcPhi   = cms.untracked.InputTag("QWV0MVAMon", "phi")
    process.vectMass10.srcPhi  = cms.untracked.InputTag("QWV0MVAMon", "phi")
    process.vectMass30.srcPhi  = cms.untracked.InputTag("QWV0MVAMon", "phi")
    process.vectMass50.srcPhi  = cms.untracked.InputTag("QWV0MVAMon", "phi")
    process.vectMass80.srcPhi  = cms.untracked.InputTag("QWV0MVAMon", "phi")
else:
    process.QWV0Event.cuts[0].Massmin = cms.untracked.double(massLow)
    process.QWV0Event.cuts[0].Massmax = cms.untracked.double(massHigh)


process.schedule = cms.Schedule(
        process.ana0,
        process.ana10,
        process.ana30,
        process.ana50,
        process.ana80,
#        process.out
        )

from HLTrigger.Configuration.CustomConfigs import MassReplaceInputTag
process = MassReplaceInputTag(process,"offlinePrimaryVertices","offlinePrimaryVerticesRecovery")

