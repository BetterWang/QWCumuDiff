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
process.GlobalTag = GlobalTag(process.GlobalTag, 'auto:phase1_2018_realistic', '')

process.GlobalTag.snapshotTime = cms.string("9999-12-31 23:59:59.000")
process.GlobalTag.toGet.extend([
	cms.PSet(record = cms.string("HeavyIonRcd"),
		tag = cms.string("CentralityTable_HFtowers200_HydjetDrum5F_v1020x01_mc"),
		connect = cms.string("frontier://FrontierProd/CMS_CONDITIONS"),
		label = cms.untracked.string("HFtowers")
		),
	])

process.load("RecoHI.HiCentralityAlgos.CentralityBin_cfi")
process.centralityBin.Centrality = cms.InputTag("hiCentrality")
process.centralityBin.centralityVariable = cms.string("HFtowers")

process.load('RecoHI.HiCentralityAlgos.CentralityFilter_cfi')
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
			*range(100, 140)
			),
		BinLabel = cms.InputTag("centralityBin", "HFtowers")
		)

process.options = cms.untracked.PSet(
        SkipEvent = cms.untracked.vstring('ProductNotFound')
        )

process.source = cms.Source("PoolSource",
	fileNames = cms.untracked.vstring("file:/afs/cern.ch/user/q/qwang/work/cleanroomRun2/Ana/CMSSW_10_3_1_patch3/src/QWAna/QWV0Skim/reco.root"),
        secondaryFileNames = cms.untracked.vstring(
		'file:/afs/cern.ch/user/q/qwang/work/cleanroomRun2/Ana/data/PbPb2018_MB.root'
            ),
        )

process.TFileService = cms.Service("TFileService",
        fileName = cms.string('cumu.root')
        )


process.load('HeavyIonsAnalysis.Configuration.hfCoincFilter_cff')
process.load('HeavyIonsAnalysis.Configuration.collisionEventSelection_cff')

process.eventSelection = cms.Sequence(
	process.primaryVertexFilter
	* process.hfCoincFilter2Th4
	* process.clusterCompatibilityFilter
        )


process.QWV0EventKs = cms.EDProducer('QWV0VectProducer'
        , vertexSrc = cms.untracked.InputTag('offlinePrimaryVerticesRecovery')
        , trackSrc = cms.untracked.InputTag('generalTracks')
        , V0Src = cms.untracked.InputTag('generalV0CandidatesNew', 'Kshort')
        , daughter_cuts = cms.untracked.PSet(
            )
        , cuts = cms.untracked.VPSet(
            cms.untracked.PSet(
                Massmin = cms.untracked.double(0.43)
                , Massmax = cms.untracked.double(0.565)
                , DecayXYZMin = cms.untracked.double(5.0)
                , ThetaXYZMin = cms.untracked.double(0.999)
                , ptMin = cms.untracked.double(0.2)
                , ptMax = cms.untracked.double(8.5)
                )
            )
        )

process.QWV0EventLambda = cms.EDProducer('QWV0VectProducer'
        , vertexSrc = cms.untracked.InputTag('offlinePrimaryVerticesRecovery')
        , trackSrc = cms.untracked.InputTag('generalTracks')
        , V0Src = cms.untracked.InputTag('generalV0CandidatesNew', 'Lambda')
        , daughter_cuts = cms.untracked.PSet(
            )
        , cuts = cms.untracked.VPSet(
            cms.untracked.PSet(
                Massmin = cms.untracked.double(1.08)
                , Massmax = cms.untracked.double(1.16)
                , DecayXYZMin = cms.untracked.double(5.0)
                , ThetaXYZMin = cms.untracked.double(0.9998)
                , ptMin = cms.untracked.double(0.2)
                , ptMax = cms.untracked.double(1.0)
                ),
            cms.untracked.PSet(
                Massmin = cms.untracked.double(1.08)
                , Massmax = cms.untracked.double(1.16)
                , DecayXYZMin = cms.untracked.double(5.0)
                , ThetaXYZMin = cms.untracked.double(0.9999)
                , ptMin = cms.untracked.double(1.0)
                , ptMax = cms.untracked.double(8.5)
                )
            )
        )


process.vectKsMassN30 = cms.EDAnalyzer('QWMassAnalyzer',
        srcMass = cms.untracked.InputTag("QWV0EventKs", "mass"),
        srcPt = cms.untracked.InputTag("QWV0EventKs", "pt"),
        srcEta = cms.untracked.InputTag("QWV0EventKs", "rapidity"),
        srcPhi = cms.untracked.InputTag("QWV0EventKs", "phi"),
        hNbins = cms.untracked.int32(10),
        hstart = cms.untracked.double(0),
        hend = cms.untracked.double(10),
        Nbins = cms.untracked.int32(270),
        start = cms.untracked.double(.43),
        end = cms.untracked.double(0.565),
        )


process.vectKsMassN0       = process.vectKsMassN30.clone()
process.vectKsMassN10      = process.vectKsMassN30.clone()
process.vectKsMassN20      = process.vectKsMassN30.clone()
process.vectKsMassN40      = process.vectKsMassN30.clone()
process.vectKsMassN50      = process.vectKsMassN30.clone()
process.vectKsMassN60      = process.vectKsMassN30.clone()
process.vectKsMassN70      = process.vectKsMassN30.clone()


process.vectLmMassN30 = process.vectKsMassN30.clone(
        srcMass = cms.untracked.InputTag("QWV0EventLambda", "mass"),
        srcPt = cms.untracked.InputTag("QWV0EventLambda", "pt"),
        srcEta = cms.untracked.InputTag("QWV0EventLambda", "rapidity"),
        srcPhi = cms.untracked.InputTag("QWV0EventLambda", "phi"),
        Nbins = cms.untracked.int32(160),
        start = cms.untracked.double(1.08),
        end = cms.untracked.double(1.16),
        )


process.vectLmMassN0       = process.vectLmMassN30.clone()
process.vectLmMassN10      = process.vectLmMassN30.clone()
process.vectLmMassN20      = process.vectLmMassN30.clone()
process.vectLmMassN40      = process.vectLmMassN30.clone()
process.vectLmMassN50      = process.vectLmMassN30.clone()
process.vectLmMassN60      = process.vectLmMassN30.clone()
process.vectLmMassN70      = process.vectLmMassN30.clone()

process.histCentBin = cms.EDAnalyzer('QWHistAnalyzer',
		src = cms.untracked.InputTag("centralityBin", "HFtowers"),
		Nbins = cms.untracked.int32(200),
		start = cms.untracked.double(0),
		end = cms.untracked.double(200),
		)

process.ana0 = cms.Path(
        process.eventSelection
	* process.centralityBin
        * process.Cent0
        * process.QWV0EventKs
        * process.QWV0EventLambda
        * process.vectKsMassN0
        * process.vectLmMassN0
	* process.histCentBin
        )

process.ana10 = cms.Path(
        process.eventSelection
	* process.centralityBin
        * process.Cent10
        * process.QWV0EventKs
        * process.QWV0EventLambda
        * process.vectKsMassN10
        * process.vectLmMassN10
	* process.histCentBin
        )

process.ana20 = cms.Path(
        process.eventSelection
	* process.centralityBin
        * process.Cent20
        * process.QWV0EventKs
        * process.QWV0EventLambda
        * process.vectKsMassN20
        * process.vectLmMassN20
	* process.histCentBin
        )

process.ana30 = cms.Path(
        process.eventSelection
	* process.centralityBin
        * process.Cent30
        * process.QWV0EventKs
        * process.QWV0EventLambda
        * process.vectKsMassN30
        * process.vectLmMassN30
	* process.histCentBin
        )

process.ana40 = cms.Path(
        process.eventSelection
	* process.centralityBin
        * process.Cent40
        * process.QWV0EventKs
        * process.QWV0EventLambda
        * process.vectKsMassN40
        * process.vectLmMassN40
	* process.histCentBin
        )

process.ana50 = cms.Path(
        process.eventSelection
	* process.centralityBin
        * process.Cent50
        * process.QWV0EventKs
        * process.QWV0EventLambda
        * process.vectKsMassN50
        * process.vectLmMassN50
	* process.histCentBin
        )

process.ana60 = cms.Path(
        process.eventSelection
	* process.centralityBin
        * process.Cent60
        * process.QWV0EventKs
        * process.QWV0EventLambda
        * process.vectKsMassN60
        * process.vectLmMassN60
	* process.histCentBin
        )

process.ana70 = cms.Path(
        process.eventSelection
	* process.centralityBin
        * process.Cent70
        * process.QWV0EventKs
        * process.QWV0EventLambda
        * process.vectKsMassN70
        * process.vectLmMassN70
	* process.histCentBin
        )


process.RECO = cms.OutputModule("PoolOutputModule",
        outputCommands = cms.untracked.vstring('drop *',
            'keep *_*_*_CumuDiff'),
        SelectEvents = cms.untracked.PSet(
            SelectEvents = cms.vstring('ana30')
            ),
        fileName = cms.untracked.string('recoV0.root')
        )


process.out = cms.EndPath(process.RECO)


process.schedule = cms.Schedule(
        process.ana0,
        process.ana10,
        process.ana30,
        process.ana50,
#        process.out
        )

from HLTrigger.Configuration.CustomConfigs import MassReplaceInputTag
process = MassReplaceInputTag(process,"offlinePrimaryVertices","offlinePrimaryVerticesRecovery")

