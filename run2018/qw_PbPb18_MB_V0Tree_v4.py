import FWCore.ParameterSet.Config as cms

process = cms.Process("CumuDiff")

process.load('Configuration.StandardSequences.Services_cff')
process.load('FWCore.MessageService.MessageLogger_cfi')
process.load('Configuration.StandardSequences.GeometryDB_cff')
process.load("TrackingTools/TransientTrack/TransientTrackBuilder_cfi")
process.load('Configuration.StandardSequences.MagneticField_38T_cff')
process.load('Configuration.StandardSequences.EndOfProcess_cff')
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_condDBv2_cff')

#process.load("RecoVertex.PrimaryVertexProducer.OfflinePrimaryVerticesRecovery_cfi")


process.maxEvents = cms.untracked.PSet(input = cms.untracked.int32(-1))
process.MessageLogger.cerr.FwkReport.reportEvery = 100

from Configuration.AlCa.GlobalTag_condDBv2 import GlobalTag
process.GlobalTag = GlobalTag(process.GlobalTag, '103X_dataRun2_Prompt_v2', '')

process.GlobalTag.snapshotTime = cms.string("9999-12-31 23:59:59.000")
process.GlobalTag.toGet.extend([
	cms.PSet(record = cms.string("HeavyIonRcd"),
		tag = cms.string("CentralityTable_HFtowers200_DataPbPb_periHYDJETshape_run2v1031x02_offline"),
		connect = cms.string("frontier://FrontierProd/CMS_CONDITIONS"),
		label = cms.untracked.string("HFtowers")
		),
	])

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
        fileNames = cms.untracked.vstring("file:/afs/cern.ch/user/q/qwang/work/cleanroomRun2/Ana/data/PbPb2018_MB_V0Skim.root"),
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


process.histCentBin = cms.EDAnalyzer('QWHistAnalyzer',
		src = cms.untracked.InputTag("centralityBin", "HFtowers"),
		Nbins = cms.untracked.int32(200),
		start = cms.untracked.double(0),
		end = cms.untracked.double(200),
		)

process.HFQ2 = cms.EDProducer('QWCaloQProducer',
        caloSrc = cms.untracked.InputTag('towerMaker'),
        etaMin = cms.untracked.double(3.),
        etaMax = cms.untracked.double(5.),
        N = cms.untracked.int32(2)
    )

process.HFQ3 = process.HFQ2.clone(N = cms.untracked.int32(3))


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


process.treeLm = cms.EDAnalyzer('QWTreeMaker',
		Vtags = cms.untracked.VPSet(
			cms.PSet(
				tag = cms.untracked.InputTag('EPOrg', 'angle'),
				name = cms.untracked.string('EPOrg')
				),
			cms.PSet(
				tag = cms.untracked.InputTag('EPOrg', 'sumSin'),
				name = cms.untracked.string('EPOrgSin')
				),
			cms.PSet(
				tag = cms.untracked.InputTag('EPOrg', 'sumCos'),
				name = cms.untracked.string('EPOrgCos')
				),
			cms.PSet(
				tag = cms.untracked.InputTag('EPFlat', 'angle'),
				name = cms.untracked.string('EPFlat')
				),
			cms.PSet(
				tag = cms.untracked.InputTag('EPFlat', 'sumSin'),
				name = cms.untracked.string('EPFlatSin')
				),
			cms.PSet(
				tag = cms.untracked.InputTag('EPFlat', 'sumCos'),
				name = cms.untracked.string('EPFlatCos')
				),
			cms.PSet(
				tag = cms.untracked.InputTag('QWV0EventLm', 'pt'),
				name = cms.untracked.string('pt')
				),
			cms.PSet(
				tag = cms.untracked.InputTag('QWV0EventLm', 'phi'),
				name = cms.untracked.string('phi')
				),
			cms.PSet(
				tag = cms.untracked.InputTag('QWV0EventLm', 'eta'),
				name = cms.untracked.string('eta')
				),
			cms.PSet(
				tag = cms.untracked.InputTag('QWV0EventLm', 'rapidity'),
				name = cms.untracked.string('rapidity')
				),
			cms.PSet(
				tag = cms.untracked.InputTag('QWV0EventLm', 'mass'),
				name = cms.untracked.string('mass')
				),
			cms.PSet(
				tag = cms.untracked.InputTag('QWV0EventLm', 'vtxChi2'),
				name = cms.untracked.string('vtxChi2')
				),
			cms.PSet(
				tag = cms.untracked.InputTag('QWV0EventLm', 'cosThetaXYZ'),
				name = cms.untracked.string('cosThetaXYZ')
				),
			cms.PSet(
				tag = cms.untracked.InputTag('QWV0EventLm', 'Lxyz'),
				name = cms.untracked.string('Lxyz')
				),
			cms.PSet(
				tag = cms.untracked.InputTag('QWV0EventLm', 'vtxDecaySigXYZ'),
				name = cms.untracked.string('vtxDecaySigXYZ')
				),
			cms.PSet(
				tag = cms.untracked.InputTag('QWV0EventLm', 'DCA'),
				name = cms.untracked.string('DCA')
				),
			cms.PSet(
				tag = cms.untracked.InputTag('QWV0EventLm', 'pdgId'),
				name = cms.untracked.string('pdgId')
				),
			cms.PSet(
				tag = cms.untracked.InputTag('QWV0EventLm', 'pTrkQuality'),
				name = cms.untracked.string('pTrkQuality')
				),
			cms.PSet(
				tag = cms.untracked.InputTag('QWV0EventLm', 'pTrkNHit'),
				name = cms.untracked.string('pTrkNHit')
				),
			cms.PSet(
				tag = cms.untracked.InputTag('QWV0EventLm', 'pTrkPt'),
				name = cms.untracked.string('pTrkPt')
				),
			cms.PSet(
				tag = cms.untracked.InputTag('QWV0EventLm', 'pTrkPtError'),
				name = cms.untracked.string('pTrkPtError')
				),
			cms.PSet(
				tag = cms.untracked.InputTag('QWV0EventLm', 'pTrkEta'),
				name = cms.untracked.string('pTrkEta')
				),
			cms.PSet(
				tag = cms.untracked.InputTag('QWV0EventLm', 'pTrkNPxLayer'),
				name = cms.untracked.string('pTrkNPxLayer')
				),
			cms.PSet(
				tag = cms.untracked.InputTag('QWV0EventLm', 'nTrkQuality'),
				name = cms.untracked.string('nTrkQuality')
				),
			cms.PSet(
				tag = cms.untracked.InputTag('QWV0EventLm', 'nTrkNHit'),
				name = cms.untracked.string('nTrkNHit')
				),
			cms.PSet(
				tag = cms.untracked.InputTag('QWV0EventLm', 'nTrkPt'),
				name = cms.untracked.string('nTrkPt')
				),
			cms.PSet(
				tag = cms.untracked.InputTag('QWV0EventLm', 'nTrkPtError'),
				name = cms.untracked.string('nTrkPtError')
				),
			cms.PSet(
				tag = cms.untracked.InputTag('QWV0EventLm', 'nTrkEta'),
				name = cms.untracked.string('nTrkEta')
				),
			cms.PSet(
				tag = cms.untracked.InputTag('QWV0EventLm', 'nTrkNPxLayer'),
				name = cms.untracked.string('nTrkNPxLayer')
				),
			cms.PSet(
				tag = cms.untracked.InputTag('QWV0EventLm', 'pPxCM'),
				name = cms.untracked.string('pPxCM')
				),
			cms.PSet(
				tag = cms.untracked.InputTag('QWV0EventLm', 'pPyCM'),
				name = cms.untracked.string('pPyCM')
				),
			cms.PSet(
				tag = cms.untracked.InputTag('QWV0EventLm', 'pPzCM'),
				name = cms.untracked.string('pPzCM')
				),
			cms.PSet(
				tag = cms.untracked.InputTag('QWV0EventLm', 'nPxCM'),
				name = cms.untracked.string('nPxCM')
				),
			cms.PSet(
				tag = cms.untracked.InputTag('QWV0EventLm', 'nPyCM'),
				name = cms.untracked.string('nPyCM')
				),
			cms.PSet(
				tag = cms.untracked.InputTag('QWV0EventLm', 'nPzCM'),
				name = cms.untracked.string('nPzCM')
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



process.ana0 = cms.Path(
        process.eventSelection
        * process.dbCent
        * process.QWV0EventLm
        * process.EPOrg
        * process.EPFlat
        * process.QWVertex
        * process.QWPrimaryVz
        * process.treeLm
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

