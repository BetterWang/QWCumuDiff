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


process.histCentBin = cms.EDAnalyzer('QWHistAnalyzer',
		src = cms.untracked.InputTag("centralityBin", "HFtowers"),
		Nbins = cms.untracked.int32(200),
		start = cms.untracked.double(0),
		end = cms.untracked.double(200),
		)

process.treeKs = cms.EDAnalyzer('QWTreeMaker',
		Vtags = cms.untracked.VPSet(
			cms.PSet(
				tag = cms.untracked.InputTag('QWV0EventKs', 'pt'),
				name = cms.untracked.string('pt')
				),
			cms.PSet(
				tag = cms.untracked.InputTag('QWV0EventKs', 'phi'),
				name = cms.untracked.string('phi')
				),
			cms.PSet(
				tag = cms.untracked.InputTag('QWV0EventKs', 'eta'),
				name = cms.untracked.string('eta')
				),
			cms.PSet(
				tag = cms.untracked.InputTag('QWV0EventKs', 'rapidity'),
				name = cms.untracked.string('rapidity')
				),
			cms.PSet(
				tag = cms.untracked.InputTag('QWV0EventKs', 'mass'),
				name = cms.untracked.string('mass')
				),
			cms.PSet(
				tag = cms.untracked.InputTag('QWV0EventKs', 'vtxChi2'),
				name = cms.untracked.string('vtxChi2')
				),
			cms.PSet(
				tag = cms.untracked.InputTag('QWV0EventKs', 'cosThetaXYZ'),
				name = cms.untracked.string('cosThetaXYZ')
				),
			cms.PSet(
				tag = cms.untracked.InputTag('QWV0EventKs', 'Lxyz'),
				name = cms.untracked.string('Lxyz')
				),
			cms.PSet(
				tag = cms.untracked.InputTag('QWV0EventKs', 'vtxDecaySigXYZ'),
				name = cms.untracked.string('vtxDecaySigXYZ')
				),
			cms.PSet(
				tag = cms.untracked.InputTag('QWV0EventKs', 'DCA'),
				name = cms.untracked.string('DCA')
				),
#			cms.PSet(
#				tag = cms.untracked.InputTag('QWV0EventKs', 'pdgId'),
#				name = cms.untracked.string('pdgId')
#				),
#			cms.PSet(
#				tag = cms.untracked.InputTag('QWV0EventKs', 'pPhiCM'),
#				name = cms.untracked.string('pPhiCM')
#				),
#			cms.PSet(
#				tag = cms.untracked.InputTag('QWV0EventKs', 'nPhiCM'),
#				name = cms.untracked.string('nPhiCM')
#				)
			),
		Dtags = cms.untracked.VPSet(
			cms.PSet(
				tag = cms.untracked.InputTag('dbCent'),
				name = cms.untracked.string('Cent')
				),
			)
		)

process.treeLm = cms.EDAnalyzer('QWTreeMaker',
		Vtags = cms.untracked.VPSet(
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
#			cms.PSet(
#				tag = cms.untracked.InputTag('QWV0EventLm', 'pdgId'),
#				name = cms.untracked.string('pdgId')
#				),
#			cms.PSet(
#				tag = cms.untracked.InputTag('QWV0EventLm', 'pPhiCM'),
#				name = cms.untracked.string('pPhiCM')
#				),
#			cms.PSet(
#				tag = cms.untracked.InputTag('QWV0EventLm', 'nPhiCM'),
#				name = cms.untracked.string('nPhiCM')
#				)
			),
		Dtags = cms.untracked.VPSet(
			cms.PSet(
				tag = cms.untracked.InputTag('dbCent'),
				name = cms.untracked.string('Cent')
				),
			)
		)


process.ana0 = cms.Path(
        process.eventSelection
	* process.centralityBin
        * process.dbCent
        * process.QWV0EventKs
        * process.QWV0EventLm
        * process.treeKs
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

