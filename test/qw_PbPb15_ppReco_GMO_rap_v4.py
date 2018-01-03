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
process.GlobalTag = GlobalTag(process.GlobalTag, '75X_dataRun2_v13', '')

process.options = cms.untracked.PSet(
        SkipEvent = cms.untracked.vstring('ProductNotFound')
        )

process.source = cms.Source("PoolSource",
        fileNames = cms.untracked.vstring("file:/afs/cern.ch/user/q/qwang/work/cleanroomRun2/Ana/data/ppReco_GMOV0.root"),
        secondaryFileNames = cms.untracked.vstring(
            'file:/afs/cern.ch/user/q/qwang/work/cleanroomRun2/Ana/data/ppReco.root'
            ),
        )


process.TFileService = cms.Service("TFileService",
        fileName = cms.string('cumu.root')
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

process.load('HeavyIonsAnalysis.Configuration.collisionEventSelection_cff')
process.load('RecoHI.HiCentralityAlgos.CentralityFilter_cfi')

process.NoffFilter0 = process.centralityFilter.clone(
        selectedBins = cms.vint32(
            *range(0, 10)
            ),
        BinLabel = cms.InputTag("Noff")
        )
process.NoffFilter10 = process.centralityFilter.clone(
        selectedBins = cms.vint32(
            *range(10, 30)
            ),
        BinLabel = cms.InputTag("Noff")
        )
process.NoffFilter30 = process.centralityFilter.clone(
        selectedBins = cms.vint32(
            *range(30, 90)
            ),
        BinLabel = cms.InputTag("Noff")
        )
process.NoffFilter90 = process.centralityFilter.clone(
        selectedBins = cms.vint32(
            *range(90, 120)
            ),
        BinLabel = cms.InputTag("Noff")
        )
process.NoffFilter120 = process.centralityFilter.clone(
        selectedBins = cms.vint32(
            *range(120, 150)
            ),
        BinLabel = cms.InputTag("Noff")
        )
process.NoffFilter150 = process.centralityFilter.clone(
        selectedBins = cms.vint32(
            *range(150, 185)
            ),
        BinLabel = cms.InputTag("Noff")
        )
process.NoffFilter185 = process.centralityFilter.clone(
        selectedBins = cms.vint32(
            *range(185, 250)
            ),
        BinLabel = cms.InputTag("Noff")
        )
process.NoffFilter250 = process.centralityFilter.clone(
        selectedBins = cms.vint32(
            *range(250, 320)
            ),
        BinLabel = cms.InputTag("Noff")
        )

process.eventSelection = cms.Sequence(
        process.hfCoincFilter3
	+ process.QWPrimaryVertexSelection
        #        + process.primaryVertexFilter
        #        + process.clusterCompatibilityFilter
        )


process.QWV0EventKs = cms.EDProducer('QWV0VectProducer'
        , vertexSrc = cms.untracked.InputTag('GMOVertex')
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
        , vertexSrc = cms.untracked.InputTag('GMOVertex')
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


process.load('PbPb_HIMB5_ppReco_eff')
process.Noff.vertexSrc = cms.untracked.InputTag('GMOVertex')
process.QWEvent.vertexSrc = cms.untracked.InputTag('GMOVertex')
process.QWEvent.ptMax = cms.untracked.double(100)


process.vectKsMassN0 = cms.EDAnalyzer('QWMassAnalyzer',
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


process.vectKsMassN10      = process.vectKsMassN0.clone()
process.vectKsMassN30      = process.vectKsMassN0.clone()
process.vectKsMassN90      = process.vectKsMassN0.clone()
process.vectKsMassN120      = process.vectKsMassN0.clone()
process.vectKsMassN150      = process.vectKsMassN0.clone()
process.vectKsMassN185      = process.vectKsMassN0.clone()
process.vectKsMassN250      = process.vectKsMassN0.clone()


process.vectLmMassN0 = process.vectKsMassN0.clone(
        srcMass = cms.untracked.InputTag("QWV0EventLambda", "mass"),
        srcPt = cms.untracked.InputTag("QWV0EventLambda", "pt"),
        srcEta = cms.untracked.InputTag("QWV0EventLambda", "rapidity"),
        srcPhi = cms.untracked.InputTag("QWV0EventLambda", "phi"),
        Nbins = cms.untracked.int32(160),
        start = cms.untracked.double(1.08),
        end = cms.untracked.double(1.16),
        )


process.vectLmMassN10      = process.vectLmMassN0.clone()
process.vectLmMassN30      = process.vectLmMassN0.clone()
process.vectLmMassN90      = process.vectLmMassN0.clone()
process.vectLmMassN120     = process.vectLmMassN0.clone()
process.vectLmMassN150     = process.vectLmMassN0.clone()
process.vectLmMassN185     = process.vectLmMassN0.clone()
process.vectLmMassN250     = process.vectLmMassN0.clone()

process.ana0 = cms.Path(
        process.eventSelection
        * process.Noff
        * process.NoffFilter0
        * process.QWV0EventKs
        * process.QWV0EventLambda
        * process.vectKsMassN0
        * process.vectLmMassN0
        )

process.ana10 = cms.Path(
        process.eventSelection
        * process.Noff
        * process.NoffFilter10
        * process.QWV0EventKs
        * process.QWV0EventLambda
        * process.vectKsMassN10
        * process.vectLmMassN10
        )

process.ana30 = cms.Path(
        process.eventSelection
        * process.Noff
        * process.NoffFilter30
        * process.QWV0EventKs
        * process.QWV0EventLambda
        * process.vectKsMassN30
        * process.vectLmMassN30
        )

process.ana90 = cms.Path(
        process.eventSelection
        * process.Noff
        * process.NoffFilter0
        * process.QWV0EventKs
        * process.QWV0EventLambda
        * process.vectKsMassN0
        * process.vectLmMassN0
        )

process.ana120 = cms.Path(
        process.eventSelection
        * process.Noff
        * process.NoffFilter120
        * process.QWV0EventKs
        * process.QWV0EventLambda
        * process.vectKsMassN120
        * process.vectLmMassN120
        )

process.ana150 = cms.Path(
        process.eventSelection
        * process.Noff
        * process.NoffFilter150
        * process.QWV0EventKs
        * process.QWV0EventLambda
        * process.vectKsMassN150
        * process.vectLmMassN150
        )
process.ana185 = cms.Path(
        process.eventSelection
        * process.Noff
        * process.NoffFilter185
        * process.QWV0EventKs
        * process.QWV0EventLambda
        * process.vectKsMassN185
        * process.vectLmMassN185
        )


process.ana250 = cms.Path(
        process.eventSelection
        * process.Noff
        * process.NoffFilter250
        * process.QWV0EventKs
        * process.QWV0EventLambda
        * process.vectKsMassN250
        * process.vectLmMassN250
        )


process.RECO = cms.OutputModule("PoolOutputModule",
        outputCommands = cms.untracked.vstring('drop *',
            'keep *_*_*_CumuDiff'),
        SelectEvents = cms.untracked.PSet(
            SelectEvents = cms.vstring('ana250')
            ),
        fileName = cms.untracked.string('recoV0.root')
        )


process.out = cms.EndPath(process.RECO)


process.schedule = cms.Schedule(
        process.ana120,
        process.ana150,
        process.ana185,
        process.ana250,
#        process.out
        )
