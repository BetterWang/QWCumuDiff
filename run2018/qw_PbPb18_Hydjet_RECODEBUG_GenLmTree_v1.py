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



process.dbCent = cms.EDProducer('QWInt2Double',
		src = cms.untracked.InputTag('centralityBin', 'HFtowers')
		)


process.options = cms.untracked.PSet(
        SkipEvent = cms.untracked.vstring('ProductNotFound')
        )

process.source = cms.Source("PoolSource",
	fileNames = cms.untracked.vstring("file:/afs/cern.ch/user/q/qwang/work/cleanroomRun2/Ana/CMSSW_10_3_1_patch3/src/QWAna/QWV0Skim/reco_Hydjet.root"),
    secondaryFileNames = cms.untracked.vstring('file:/afs/cern.ch/user/q/qwang/work/cleanroomRun2/Ana/data/HydjetDrum5F_RECODEBUG.root')
    )

process.TFileService = cms.Service("TFileService",
        fileName = cms.string('cumu.root')
        )


process.QWGenV0Lm = cms.EDProducer('QWGenV0VectProducer',
        trackingVertexCollection = cms.untracked.InputTag('mix', 'MergedTrackTruth'),
        parent_pdgId = cms.untracked.int32(3122),
        daughter_pdgId1 = cms.untracked.int32(211),
        daughter_pdgId2 = cms.untracked.int32(2212)
        )


process.histCentBin = cms.EDAnalyzer('QWHistAnalyzer',
		src = cms.untracked.InputTag("centralityBin", "HFtowers"),
		Nbins = cms.untracked.int32(200),
		start = cms.untracked.double(0),
		end = cms.untracked.double(200),
		)


process.treeLm = cms.EDAnalyzer('QWTreeMaker',
		Vtags = cms.untracked.VPSet(
			cms.PSet(
				tag = cms.untracked.InputTag('QWGenV0Lm', 'pt'),
				name = cms.untracked.string('pt')
				),
			cms.PSet(
				tag = cms.untracked.InputTag('QWGenV0Lm', 'phi'),
				name = cms.untracked.string('phi')
				),
			cms.PSet(
				tag = cms.untracked.InputTag('QWGenV0Lm', 'eta'),
				name = cms.untracked.string('eta')
				),
			cms.PSet(
				tag = cms.untracked.InputTag('QWGenV0Lm', 'rapidity'),
				name = cms.untracked.string('rapidity')
				),
			cms.PSet(
				tag = cms.untracked.InputTag('QWGenV0Lm', 'mass'),
				name = cms.untracked.string('mass')
				),
			cms.PSet(
				tag = cms.untracked.InputTag('QWGenV0Lm', 'pdgId'),
				name = cms.untracked.string('pdgId')
				),
			cms.PSet(
				tag = cms.untracked.InputTag('QWGenV0Lm', 'pPx'),
				name = cms.untracked.string('pPx')
				),
			cms.PSet(
				tag = cms.untracked.InputTag('QWGenV0Lm', 'pPy'),
				name = cms.untracked.string('pPy')
				),
			cms.PSet(
				tag = cms.untracked.InputTag('QWGenV0Lm', 'pPz'),
				name = cms.untracked.string('pPz')
				),
			cms.PSet(
				tag = cms.untracked.InputTag('QWGenV0Lm', 'nPx'),
				name = cms.untracked.string('nPx')
				),
			cms.PSet(
				tag = cms.untracked.InputTag('QWGenV0Lm', 'nPy'),
				name = cms.untracked.string('nPy')
				),
			cms.PSet(
				tag = cms.untracked.InputTag('QWGenV0Lm', 'nPz'),
				name = cms.untracked.string('nPz')
				),
			cms.PSet(
				tag = cms.untracked.InputTag('QWGenV0Lm', 'pPxCM'),
				name = cms.untracked.string('pPxCM')
				),
			cms.PSet(
				tag = cms.untracked.InputTag('QWGenV0Lm', 'pPyCM'),
				name = cms.untracked.string('pPyCM')
				),
			cms.PSet(
				tag = cms.untracked.InputTag('QWGenV0Lm', 'pPzCM'),
				name = cms.untracked.string('pPzCM')
				),
			cms.PSet(
				tag = cms.untracked.InputTag('QWGenV0Lm', 'nPxCM'),
				name = cms.untracked.string('nPxCM')
				),
			cms.PSet(
				tag = cms.untracked.InputTag('QWGenV0Lm', 'nPyCM'),
				name = cms.untracked.string('nPyCM')
				),
			cms.PSet(
				tag = cms.untracked.InputTag('QWGenV0Lm', 'nPzCM'),
				name = cms.untracked.string('nPzCM')
				),
			),
		Dtags = cms.untracked.VPSet(
			cms.PSet(
				tag = cms.untracked.InputTag('dbCent'),
				name = cms.untracked.string('Cent')
				),
			)
		)


process.ana0 = cms.Path(
        process.dbCent
        * process.QWGenV0Lm
        * process.treeLm
        * process.histCentBin
        )


process.schedule = cms.Schedule(
        process.ana0,
        )
