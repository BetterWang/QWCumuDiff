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

process.load("CondCore.CondDB.CondDB_cfi")

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


process.dbCent = cms.EDProducer('QWInt2Double',
		src = cms.untracked.InputTag('centralityBin', 'HFtowers')
		)


process.options = cms.untracked.PSet(
        SkipEvent = cms.untracked.vstring('ProductNotFound')
        )

process.source = cms.Source("PoolSource",
        fileNames = cms.untracked.vstring("file:/afs/cern.ch/user/q/qwang/work/cleanroomRun2/Ana/data/PbPb2018_RERECO_WrongSignV0Skim.root"),
        secondaryFileNames = cms.untracked.vstring(
            "file:/eos/cms/store/hidata/HIRun2018A/HIMinimumBias19/AOD/04Apr2019-v1/260000/FF31F840-542E-1A49-ACF7-9043F8169E67.root",
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



process.QWV0EventLm = cms.EDProducer('QWV0VectProducer'
        , vertexSrc = cms.untracked.InputTag('offlinePrimaryVerticesRecovery')
        , trackSrc = cms.untracked.InputTag('generalTracks')
        , V0Src = cms.untracked.InputTag('generalV0CandidatesNew', 'Lambda')
        , daughter_cuts = cms.untracked.PSet(
            )
        , cuts = cms.untracked.VPSet(
            cms.untracked.PSet(
                Massmin = cms.untracked.double(1.08)
                , Massmax = cms.untracked.double(1.16)
                , DecayXYZMin = cms.untracked.double(2.5)
                , ThetaXYZMin = cms.untracked.double(0.999)
                , ptMin = cms.untracked.double(0.2)
                , ptMax = cms.untracked.double(8.5)
                )
            )
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
                , DecayXYZMin = cms.untracked.double(2.5)
                , ThetaXYZMin = cms.untracked.double(0.999)
                , ptMin = cms.untracked.double(0.2)
                , ptMax = cms.untracked.double(8.5)
                )
            )
        )

process.histCentBin = cms.EDAnalyzer('QWHistAnalyzer',
		src = cms.untracked.InputTag("centralityBin", "HFtowers"),
		Nbins = cms.untracked.int32(200),
		start = cms.untracked.double(0),
		end = cms.untracked.double(200),
		)


process.EPOrg = cms.EDProducer('QWEvtPlaneProducer',
        src = cms.untracked.InputTag('hiEvtPlaneFlat'),
        level = cms.untracked.int32(0)
        )

process.EPFlat = cms.EDProducer('QWEvtPlaneProducer',
        src = cms.untracked.InputTag('hiEvtPlaneFlat'),
        level = cms.untracked.int32(2)
        )

process.EPOrgA = cms.EDProducer('QWEvtPlaneProducer',
        src = cms.untracked.InputTag('hiEvtPlane'),
        level = cms.untracked.int32(0)
        )

process.EPFlatA = cms.EDProducer('QWEvtPlaneProducer',
        src = cms.untracked.InputTag('hiEvtPlane'),
        level = cms.untracked.int32(2)
        )

process.QWEventInfo = cms.EDProducer('QWEventInfoProducer')

process.tree = cms.EDAnalyzer('QWTreeMaker',
		Vtags = cms.untracked.VPSet(
			cms.PSet(
				tag = cms.untracked.InputTag('QWV0EventLm', 'pt'),
				name = cms.untracked.string('LMpt')
				),
			cms.PSet(
				tag = cms.untracked.InputTag('QWV0EventLm', 'phi'),
				name = cms.untracked.string('LMphi')
				),
			cms.PSet(
				tag = cms.untracked.InputTag('QWV0EventLm', 'eta'),
				name = cms.untracked.string('LMeta')
				),
			cms.PSet(
				tag = cms.untracked.InputTag('QWV0EventLm', 'rapidity'),
				name = cms.untracked.string('LMrapidity')
				),
			cms.PSet(
				tag = cms.untracked.InputTag('QWV0EventLm', 'mass'),
				name = cms.untracked.string('LMmass')
				),
			cms.PSet(
				tag = cms.untracked.InputTag('QWV0EventLm', 'vtxChi2'),
				name = cms.untracked.string('LMvtxChi2')
				),
			cms.PSet(
				tag = cms.untracked.InputTag('QWV0EventLm', 'cosThetaXYZ'),
				name = cms.untracked.string('LMcosThetaXYZ')
				),
			cms.PSet(
				tag = cms.untracked.InputTag('QWV0EventLm', 'Lxyz'),
				name = cms.untracked.string('LMLxyz')
				),
			cms.PSet(
				tag = cms.untracked.InputTag('QWV0EventLm', 'vtxDecaySigXYZ'),
				name = cms.untracked.string('LMvtxDecaySigXYZ')
				),
			cms.PSet(
				tag = cms.untracked.InputTag('QWV0EventLm', 'DCA'),
				name = cms.untracked.string('LMDCA')
				),
			cms.PSet(
				tag = cms.untracked.InputTag('QWV0EventLm', 'pdgId'),
				name = cms.untracked.string('LMpdgId')
				),
			cms.PSet(
				tag = cms.untracked.InputTag('QWV0EventLm', 'pTrkQuality'),
				name = cms.untracked.string('LMpTrkQuality')
				),
			cms.PSet(
				tag = cms.untracked.InputTag('QWV0EventLm', 'pTrkNHit'),
				name = cms.untracked.string('LMpTrkNHit')
				),
			cms.PSet(
				tag = cms.untracked.InputTag('QWV0EventLm', 'pTrkPt'),
				name = cms.untracked.string('LMpTrkPt')
				),
			cms.PSet(
				tag = cms.untracked.InputTag('QWV0EventLm', 'pTrkPtError'),
				name = cms.untracked.string('LMpTrkPtError')
				),
			cms.PSet(
				tag = cms.untracked.InputTag('QWV0EventLm', 'pTrkEta'),
				name = cms.untracked.string('LMpTrkEta')
				),
			cms.PSet(
				tag = cms.untracked.InputTag('QWV0EventLm', 'pTrkNPxLayer'),
				name = cms.untracked.string('LMpTrkNPxLayer')
				),
			cms.PSet(
				tag = cms.untracked.InputTag('QWV0EventLm', 'pTrkDCASigXY'),
				name = cms.untracked.string('LMpTrkDCASigXY')
				),
			cms.PSet(
				tag = cms.untracked.InputTag('QWV0EventLm', 'pTrkDCASigZ'),
				name = cms.untracked.string('LMpTrkDCASigZ')
				),
			cms.PSet(
				tag = cms.untracked.InputTag('QWV0EventLm', 'nTrkQuality'),
				name = cms.untracked.string('LMnTrkQuality')
				),
			cms.PSet(
				tag = cms.untracked.InputTag('QWV0EventLm', 'nTrkNHit'),
				name = cms.untracked.string('LMnTrkNHit')
				),
			cms.PSet(
				tag = cms.untracked.InputTag('QWV0EventLm', 'nTrkPt'),
				name = cms.untracked.string('LMnTrkPt')
				),
			cms.PSet(
				tag = cms.untracked.InputTag('QWV0EventLm', 'nTrkPtError'),
				name = cms.untracked.string('LMnTrkPtError')
				),
			cms.PSet(
				tag = cms.untracked.InputTag('QWV0EventLm', 'nTrkEta'),
				name = cms.untracked.string('LMnTrkEta')
				),
			cms.PSet(
				tag = cms.untracked.InputTag('QWV0EventLm', 'nTrkNPxLayer'),
				name = cms.untracked.string('LMnTrkNPxLayer')
				),
			cms.PSet(
				tag = cms.untracked.InputTag('QWV0EventLm', 'nTrkDCASigXY'),
				name = cms.untracked.string('LMnTrkDCASigXY')
				),
			cms.PSet(
				tag = cms.untracked.InputTag('QWV0EventLm', 'nTrkDCASigZ'),
				name = cms.untracked.string('LMnTrkDCASigZ')
				),
			cms.PSet(
				tag = cms.untracked.InputTag('QWV0EventKs', 'pt'),
				name = cms.untracked.string('KSpt')
				),
			cms.PSet(
				tag = cms.untracked.InputTag('QWV0EventKs', 'phi'),
				name = cms.untracked.string('KSphi')
				),
			cms.PSet(
				tag = cms.untracked.InputTag('QWV0EventKs', 'eta'),
				name = cms.untracked.string('KSeta')
				),
			cms.PSet(
				tag = cms.untracked.InputTag('QWV0EventKs', 'rapidity'),
				name = cms.untracked.string('KSrapidity')
				),
			cms.PSet(
				tag = cms.untracked.InputTag('QWV0EventKs', 'mass'),
				name = cms.untracked.string('KSmass')
				),
			cms.PSet(
				tag = cms.untracked.InputTag('QWV0EventKs', 'vtxChi2'),
				name = cms.untracked.string('KSvtxChi2')
				),
			cms.PSet(
				tag = cms.untracked.InputTag('QWV0EventKs', 'cosThetaXYZ'),
				name = cms.untracked.string('KScosThetaXYZ')
				),
			cms.PSet(
				tag = cms.untracked.InputTag('QWV0EventKs', 'Lxyz'),
				name = cms.untracked.string('KSLxyz')
				),
			cms.PSet(
				tag = cms.untracked.InputTag('QWV0EventKs', 'vtxDecaySigXYZ'),
				name = cms.untracked.string('KSvtxDecaySigXYZ')
				),
			cms.PSet(
				tag = cms.untracked.InputTag('QWV0EventKs', 'DCA'),
				name = cms.untracked.string('KSDCA')
				),
			cms.PSet(
				tag = cms.untracked.InputTag('QWV0EventKs', 'pdgId'),
				name = cms.untracked.string('KSpdgId')
				),
			cms.PSet(
				tag = cms.untracked.InputTag('QWV0EventKs', 'pTrkQuality'),
				name = cms.untracked.string('KSpTrkQuality')
				),
			cms.PSet(
				tag = cms.untracked.InputTag('QWV0EventKs', 'pTrkNHit'),
				name = cms.untracked.string('KSpTrkNHit')
				),
			cms.PSet(
				tag = cms.untracked.InputTag('QWV0EventKs', 'pTrkPt'),
				name = cms.untracked.string('KSpTrkPt')
				),
			cms.PSet(
				tag = cms.untracked.InputTag('QWV0EventKs', 'pTrkPtError'),
				name = cms.untracked.string('KSpTrkPtError')
				),
			cms.PSet(
				tag = cms.untracked.InputTag('QWV0EventKs', 'pTrkEta'),
				name = cms.untracked.string('KSpTrkEta')
				),
			cms.PSet(
				tag = cms.untracked.InputTag('QWV0EventKs', 'pTrkNPxLayer'),
				name = cms.untracked.string('KSpTrkNPxLayer')
				),
			cms.PSet(
				tag = cms.untracked.InputTag('QWV0EventKs', 'pTrkDCASigXY'),
				name = cms.untracked.string('KSpTrkDCASigXY')
				),
			cms.PSet(
				tag = cms.untracked.InputTag('QWV0EventKs', 'pTrkDCASigZ'),
				name = cms.untracked.string('KSpTrkDCASigZ')
				),
			cms.PSet(
				tag = cms.untracked.InputTag('QWV0EventKs', 'nTrkQuality'),
				name = cms.untracked.string('KSnTrkQuality')
				),
			cms.PSet(
				tag = cms.untracked.InputTag('QWV0EventKs', 'nTrkNHit'),
				name = cms.untracked.string('KSnTrkNHit')
				),
			cms.PSet(
				tag = cms.untracked.InputTag('QWV0EventKs', 'nTrkPt'),
				name = cms.untracked.string('KSnTrkPt')
				),
			cms.PSet(
				tag = cms.untracked.InputTag('QWV0EventKs', 'nTrkPtError'),
				name = cms.untracked.string('KSnTrkPtError')
				),
			cms.PSet(
				tag = cms.untracked.InputTag('QWV0EventKs', 'nTrkEta'),
				name = cms.untracked.string('KSnTrkEta')
				),
			cms.PSet(
				tag = cms.untracked.InputTag('QWV0EventKs', 'nTrkNPxLayer'),
				name = cms.untracked.string('KSnTrkNPxLayer')
				),
			cms.PSet(
				tag = cms.untracked.InputTag('QWV0EventKs', 'nTrkDCASigXY'),
				name = cms.untracked.string('KSnTrkDCASigXY')
				),
			cms.PSet(
				tag = cms.untracked.InputTag('QWV0EventKs', 'nTrkDCASigZ'),
				name = cms.untracked.string('KSnTrkDCASigZ')
				),
			),
		Dtags = cms.untracked.VPSet(
			cms.PSet(
				tag = cms.untracked.InputTag('dbCent'),
				name = cms.untracked.string('Cent')
				),
			cms.PSet(
				tag = cms.untracked.InputTag('QWPrimaryVz'),
				name = cms.untracked.string('vz')
				),
			)
		)

process.QWVertex = cms.EDProducer('QWVertexProducer',
        vertexSrc = cms.untracked.InputTag('offlinePrimaryVertices')
        )

process.QWPrimaryVz = cms.EDProducer('QWVectorSelector',
        vectSrc = cms.untracked.InputTag('QWVertex', 'vz'),
        )

process.QWVzFilter15 = cms.EDFilter('QWDoubleFilter',
        src = cms.untracked.InputTag('dbCent'),
        dmax = cms.untracked.double(80.),
    )

process.ana0 = cms.Path(
        process.eventSelection
        * process.QWVertex
        * process.QWPrimaryVz
        * process.dbCent
        * process.QWV0EventLm
        * process.QWV0EventKs
        * process.tree
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
#        process.out
        )

from HLTrigger.Configuration.CustomConfigs import MassReplaceInputTag
process = MassReplaceInputTag(process,"offlinePrimaryVertices","offlinePrimaryVerticesRecovery")

