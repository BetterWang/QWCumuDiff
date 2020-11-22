import FWCore.ParameterSet.Config as cms

process = cms.Process("CumuDiff")

process.load('Configuration.StandardSequences.Services_cff')
process.load('FWCore.MessageService.MessageLogger_cfi')
process.load('Configuration.StandardSequences.GeometryDB_cff')
process.load("TrackingTools/TransientTrack/TransientTrackBuilder_cfi")
process.load('Configuration.StandardSequences.MagneticField_38T_cff')
process.load('Configuration.StandardSequences.EndOfProcess_cff')
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_condDBv2_cff')

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

#process.CondDB.connect = "sqlite_file:HeavyIonRPRcd_PbPb2018_offline.db"
#process.PoolDBESSource = cms.ESSource("PoolDBESSource",
#        process.CondDB,
#        toGet = cms.VPSet(
#            cms.PSet(
#                record = cms.string('HeavyIonRPRcd'),
#                tag = cms.string('HeavyIonRPRcd')
#                )
#            )
#        )
#process.es_prefer_flatparms = cms.ESPrefer('PoolDBESSource','')
#
#process.hiEvtPlane.trackTag = cms.InputTag("generalTracks")
#process.hiEvtPlane.vertexTag = cms.InputTag("offlinePrimaryVerticesRecovery")
#process.hiEvtPlane.loadDB = cms.bool(True)
#process.hiEvtPlane.useNtrk = cms.untracked.bool(False)
#process.hiEvtPlane.caloCentRef = cms.double(-1)
#process.hiEvtPlane.caloCentRefWidth = cms.double(-1)
#process.hiEvtPlaneFlat.caloCentRef = cms.double(-1)
#process.hiEvtPlaneFlat.caloCentRefWidth = cms.double(-1)
#process.hiEvtPlaneFlat.vertexTag = cms.InputTag("offlinePrimaryVerticesRecovery")
#process.hiEvtPlaneFlat.useNtrk = cms.untracked.bool(False)
#
#
process.load("RecoHI.HiCentralityAlgos.CentralityBin_cfi")
process.centralityBin.Centrality = cms.InputTag("hiCentrality")
process.centralityBin.centralityVariable = cms.string("HFtowers")

process.dbCent = cms.EDProducer('QWInt2Double',
		src = cms.untracked.InputTag('centralityBin', 'HFtowers')
		)


process.options = cms.untracked.PSet(
        SkipEvent = cms.untracked.vstring('ProductNotFound')
        )

process.source = cms.Source("PoolSource",
        fileNames = cms.untracked.vstring("/store/user/qwang/V0Production2018/HIMinimumBias4/V0Skim_v3/190827_145751/0007/reco_7870.root"),
        secondaryFileNames = cms.untracked.vstring(
            "/store/hidata/HIRun2018A/HIMinimumBias4/AOD/04Apr2019-v1/610008/E2650C5C-3A74-4B49-8D70-3A6619FBB0D8.root",
            "/store/hidata/HIRun2018A/HIMinimumBias4/AOD/04Apr2019-v1/610012/77650EC7-A974-0B40-B58C-A4F012C37664.root",
            "/store/hidata/HIRun2018A/HIMinimumBias4/AOD/04Apr2019-v1/610014/E5376FDC-944F-F242-AC8B-411754A27A8E.root",
            "/store/hidata/HIRun2018A/HIMinimumBias4/AOD/04Apr2019-v1/610011/A4274F69-8C06-764D-A765-43EABAC4BA7F.root",
            "/store/hidata/HIRun2018A/HIMinimumBias4/AOD/04Apr2019-v1/610011/2F32692A-0306-2145-AD62-A0E103AF78BF.root",
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
        , APCut = cms.untracked.bool(False)
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
        , APCut = cms.untracked.bool(False)
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
#			cms.PSet(
#				tag = cms.untracked.InputTag('EPOrg', 'angle'),
#				name = cms.untracked.string('EPOrg')
#				),
#			cms.PSet(
#				tag = cms.untracked.InputTag('EPOrg', 'sumSin'),
#				name = cms.untracked.string('EPOrgSin')
#				),
#			cms.PSet(
#				tag = cms.untracked.InputTag('EPOrg', 'sumCos'),
#				name = cms.untracked.string('EPOrgCos')
#				),
#			cms.PSet(
#				tag = cms.untracked.InputTag('EPFlat', 'angle'),
#				name = cms.untracked.string('EPFlat')
#				),
#			cms.PSet(
#				tag = cms.untracked.InputTag('EPFlat', 'sumSin'),
#				name = cms.untracked.string('EPFlatSin')
#				),
#			cms.PSet(
#				tag = cms.untracked.InputTag('EPFlat', 'sumCos'),
#				name = cms.untracked.string('EPFlatCos')
#				),
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
				tag = cms.untracked.InputTag('QWV0EventLm', 'pTrkPx'),
				name = cms.untracked.string('LMpTrkPx')
				),
			cms.PSet(
				tag = cms.untracked.InputTag('QWV0EventLm', 'pTrkPy'),
				name = cms.untracked.string('LMpTrkPy')
				),
			cms.PSet(
				tag = cms.untracked.InputTag('QWV0EventLm', 'pTrkPz'),
				name = cms.untracked.string('LMpTrkPz')
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
				tag = cms.untracked.InputTag('QWV0EventLm', 'nTrkPx'),
				name = cms.untracked.string('LMnTrkPx')
				),
			cms.PSet(
				tag = cms.untracked.InputTag('QWV0EventLm', 'nTrkPy'),
				name = cms.untracked.string('LMnTrkPy')
				),
			cms.PSet(
				tag = cms.untracked.InputTag('QWV0EventLm', 'nTrkPz'),
				name = cms.untracked.string('LMnTrkPz')
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
				tag = cms.untracked.InputTag('QWV0EventLm', 'pPxCM'),
				name = cms.untracked.string('LMpPxCM')
				),
			cms.PSet(
				tag = cms.untracked.InputTag('QWV0EventLm', 'pPyCM'),
				name = cms.untracked.string('LMpPyCM')
				),
			cms.PSet(
				tag = cms.untracked.InputTag('QWV0EventLm', 'pPzCM'),
				name = cms.untracked.string('LMpPzCM')
				),
			cms.PSet(
				tag = cms.untracked.InputTag('QWV0EventLm', 'nPxCM'),
				name = cms.untracked.string('LMnPxCM')
				),
			cms.PSet(
				tag = cms.untracked.InputTag('QWV0EventLm', 'nPyCM'),
				name = cms.untracked.string('LMnPyCM')
				),
			cms.PSet(
				tag = cms.untracked.InputTag('QWV0EventLm', 'nPzCM'),
				name = cms.untracked.string('LMnPzCM')
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
				tag = cms.untracked.InputTag('QWV0EventKs', 'pTrkPx'),
				name = cms.untracked.string('KSpTrkPx')
				),
			cms.PSet(
				tag = cms.untracked.InputTag('QWV0EventKs', 'pTrkPy'),
				name = cms.untracked.string('KSpTrkPy')
				),
			cms.PSet(
				tag = cms.untracked.InputTag('QWV0EventKs', 'pTrkPz'),
				name = cms.untracked.string('KSpTrkPz')
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
				tag = cms.untracked.InputTag('QWV0EventKs', 'nTrkPx'),
				name = cms.untracked.string('KSnTrkPx')
				),
			cms.PSet(
				tag = cms.untracked.InputTag('QWV0EventKs', 'nTrkPy'),
				name = cms.untracked.string('KSnTrkPy')
				),
			cms.PSet(
				tag = cms.untracked.InputTag('QWV0EventKs', 'nTrkPz'),
				name = cms.untracked.string('KSnTrkPz')
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
			cms.PSet(
				tag = cms.untracked.InputTag('QWV0EventKs', 'pPxCM'),
				name = cms.untracked.string('KSpPxCM')
				),
			cms.PSet(
				tag = cms.untracked.InputTag('QWV0EventKs', 'pPyCM'),
				name = cms.untracked.string('KSpPyCM')
				),
			cms.PSet(
				tag = cms.untracked.InputTag('QWV0EventKs', 'pPzCM'),
				name = cms.untracked.string('KSpPzCM')
				),
			cms.PSet(
				tag = cms.untracked.InputTag('QWV0EventKs', 'nPxCM'),
				name = cms.untracked.string('KSnPxCM')
				),
			cms.PSet(
				tag = cms.untracked.InputTag('QWV0EventKs', 'nPyCM'),
				name = cms.untracked.string('KSnPyCM')
				),
			cms.PSet(
				tag = cms.untracked.InputTag('QWV0EventKs', 'nPzCM'),
				name = cms.untracked.string('KSnPzCM')
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
			cms.PSet(
				tag = cms.untracked.InputTag('QWEventInfo', 'RunId'),
				name = cms.untracked.string('RunId')
				),
			cms.PSet(
				tag = cms.untracked.InputTag('QWEventInfo', 'EventId'),
				name = cms.untracked.string('EventId')
				),
			cms.PSet(
				tag = cms.untracked.InputTag('QWEventInfo', 'Lumi'),
				name = cms.untracked.string('Lumi')
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
        src = cms.untracked.InputTag('QWPrimaryVz'),
        dmin = cms.untracked.double(-15.),
        dmax = cms.untracked.double(15.),
        )

process.QWCentFilter = cms.EDFilter('QWDoubleFilter',
        src = cms.untracked.InputTag('dbCent'),
        dmax = cms.untracked.double(160.),
        )

process.ana0 = cms.Path(
        process.eventSelection
        * process.QWVertex
        * process.QWPrimaryVz
        * process.QWVzFilter15
        * process.dbCent
#        * process.QWCentFilter
        * process.QWV0EventLm
        * process.QWV0EventKs
#        * process.hiEvtPlane
#        * process.hiEvtPlaneFlat
#        * process.EPOrg
#        * process.EPFlat
        * process.QWEventInfo
        * process.tree
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
#        process.out
        )

from HLTrigger.Configuration.CustomConfigs import MassReplaceInputTag
process = MassReplaceInputTag(process,"offlinePrimaryVertices","offlinePrimaryVerticesRecovery")

