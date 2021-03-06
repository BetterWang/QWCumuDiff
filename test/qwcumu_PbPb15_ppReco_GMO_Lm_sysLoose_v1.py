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
                Massmin = cms.untracked.double(0.492)
                , Massmax = cms.untracked.double(0.503)
                , DecayXYZMin = cms.untracked.double(5.0)
                , ThetaXYZMin = cms.untracked.double(0.999)
                , ptMin = cms.untracked.double(0.2)
                , ptMax = cms.untracked.double(8.5)
                , Rapmin = cms.untracked.double(-1.0)
                , Rapmax = cms.untracked.double(1.0)
                )
            )
        )

process.QWV0EventLambda = cms.EDProducer('QWV0VectProducer'
        , vertexSrc = cms.untracked.InputTag('GMOVertex')
        , trackSrc = cms.untracked.InputTag('generalTracks')
        , V0Src = cms.untracked.InputTag('generalV0CandidatesNew', 'Lambda')
        , daughter_cuts = cms.untracked.PSet(
            dauDCASig = cms.untracked.double(1.)
            )
        , cuts = cms.untracked.VPSet(
            cms.untracked.PSet(
                Massmin = cms.untracked.double(1.1115)
                , Massmax = cms.untracked.double(1.1200)
                , DecayXYZMin = cms.untracked.double(2.5)
                , ThetaXYZMin = cms.untracked.double(0.999)
                , ptMin = cms.untracked.double(0.2)
                , ptMax = cms.untracked.double(1.0)
                ),
            cms.untracked.PSet(
                Massmin = cms.untracked.double(1.1115)
                , Massmax = cms.untracked.double(1.1200)
                , DecayXYZMin = cms.untracked.double(2.5)
                , ThetaXYZMin = cms.untracked.double(0.999)
                , ptMin = cms.untracked.double(1.0)
                , ptMax = cms.untracked.double(8.5)
                )
            )
        )

#process.QWCumuDiff = cms.EDAnalyzer('QWCumuDiff',
#		trackSet = cms.untracked.PSet(
#			Eta = cms.untracked.InputTag('QWEvent', 'eta'),
#			Phi = cms.untracked.InputTag('QWEvent', 'phi'),
#			Ref = cms.untracked.InputTag('QWEvent', 'ref'),
#			Pt  = cms.untracked.InputTag('QWEvent', 'pt'),
#			Weight = cms.untracked.InputTag('QWEvent', 'weight'),
#			),
#		sigSet = cms.untracked.PSet(
#			Eta = cms.untracked.InputTag('QWV0EventKs', 'rapidity'),
#			Phi = cms.untracked.InputTag('QWV0EventKs', 'phi'),
#			Ref = cms.untracked.InputTag('QWV0EventKs', 'Refs'),
#			Pt = cms.untracked.InputTag('QWV0EventKs', 'pt'),
#			Weight = cms.untracked.InputTag('QWV0EventKs', 'weight'),
#			),
#		vertexZ = cms.untracked.InputTag('QWEvent', "vz"),
#		ptBin = cms.untracked.vdouble(0.2, 0.4, 0.6, 0.8, 1.0, 1.4, 1.8, 2.2, 2.8, 3.6, 4.6,6.0, 7.0, 8.5),
#		centrality = cms.untracked.InputTag('Noff')
#		)

process.QWCumuDiff = cms.EDAnalyzer('QWCumuDiff',
		trackSet = cms.untracked.PSet(
			Eta = cms.untracked.InputTag('QWEvent', 'eta'),
			Phi = cms.untracked.InputTag('QWEvent', 'phi'),
			Ref = cms.untracked.InputTag('QWEvent', 'ref'),
			Pt  = cms.untracked.InputTag('QWEvent', 'pt'),
			Weight = cms.untracked.InputTag('QWEvent', 'weight'),
			),
		sigSet = cms.untracked.PSet(
			Eta = cms.untracked.InputTag('QWV0EventLambda', 'rapidity'),
			Phi = cms.untracked.InputTag('QWV0EventLambda', 'phi'),
			Ref = cms.untracked.InputTag('QWV0EventLambda', 'Refs'),
			Pt = cms.untracked.InputTag('QWV0EventLambda', 'pt'),
			Weight = cms.untracked.InputTag('QWV0EventLambda', 'weight'),
			),
		vertexZ = cms.untracked.InputTag('QWEvent', "vz"),
		ptBin = cms.untracked.vdouble(0.2, 0.4, 0.6, 0.8, 1.0, 1.4, 1.8, 2.2, 2.8, 3.6, 4.6,6.0, 7.0, 8.5),
		centrality = cms.untracked.InputTag('Noff')
		)


process.load('PbPb_HIMB5_ppReco_eff')
process.Noff.vertexSrc = cms.untracked.InputTag('GMOVertex')
process.QWEvent.vertexSrc = cms.untracked.InputTag('GMOVertex')
process.QWEvent.fweight = cms.untracked.InputTag('NA')
process.QWEvent.ptMin = cms.untracked.double(0.2)
process.QWEvent.ptMax = cms.untracked.double(8.5)


process.vectV0MassLm120 = cms.EDAnalyzer('QWVectorAnalyzer',
		src = cms.untracked.InputTag("QWV0EventLambda", "mass"),
		hNbins = cms.untracked.int32(100),
		hstart = cms.untracked.double(0),
		hend = cms.untracked.double(100),
		cNbins = cms.untracked.int32(160),
		cstart = cms.untracked.double(1.08),
		cend = cms.untracked.double(1.16),
		)

process.vectV0MassLm150 = process.vectV0MassLm120.clone()
process.vectV0MassLm185 = process.vectV0MassLm120.clone()
process.vectV0MassLm250 = process.vectV0MassLm120.clone()

process.vectPhi120Lm = process.vectPhi.clone(src = cms.untracked.InputTag('QWV0EventLambda', 'phi'))
process.vectPhi150Lm = process.vectPhi.clone(src = cms.untracked.InputTag('QWV0EventLambda', 'phi'))
process.vectPhi185Lm = process.vectPhi.clone(src = cms.untracked.InputTag('QWV0EventLambda', 'phi'))
process.vectPhi250Lm = process.vectPhi.clone(src = cms.untracked.InputTag('QWV0EventLambda', 'phi'))

process.vectEta120Lm = process.vectEta.clone(src = cms.untracked.InputTag('QWV0EventLambda', 'rapidity'))
process.vectEta150Lm = process.vectEta.clone(src = cms.untracked.InputTag('QWV0EventLambda', 'rapidity'))
process.vectEta185Lm = process.vectEta.clone(src = cms.untracked.InputTag('QWV0EventLambda', 'rapidity'))
process.vectEta250Lm = process.vectEta.clone(src = cms.untracked.InputTag('QWV0EventLambda', 'rapidity'))

process.vectPt120Lm = process.vectPt.clone(src = cms.untracked.InputTag('QWV0EventLambda', 'pt'), cNbins = cms.untracked.int32(1000), cend = cms.untracked.double(10))
process.vectPt150Lm = process.vectPt.clone(src = cms.untracked.InputTag('QWV0EventLambda', 'pt'), cNbins = cms.untracked.int32(1000), cend = cms.untracked.double(10))
process.vectPt185Lm = process.vectPt.clone(src = cms.untracked.InputTag('QWV0EventLambda', 'pt'), cNbins = cms.untracked.int32(1000), cend = cms.untracked.double(10))
process.vectPt250Lm = process.vectPt.clone(src = cms.untracked.InputTag('QWV0EventLambda', 'pt'), cNbins = cms.untracked.int32(1000), cend = cms.untracked.double(10))

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

process.vectPt120 = process.vectPt.clone(cNbins = cms.untracked.int32(1000), cend = cms.untracked.double(10.))
process.vectPt150 = process.vectPt.clone(cNbins = cms.untracked.int32(1000), cend = cms.untracked.double(10.))
process.vectPt185 = process.vectPt.clone(cNbins = cms.untracked.int32(1000), cend = cms.untracked.double(10.))
process.vectPt250 = process.vectPt.clone(cNbins = cms.untracked.int32(1000), cend = cms.untracked.double(10.))

process.vectPtW120 = process.vectPtW.clone()
process.vectPtW150 = process.vectPtW.clone()
process.vectPtW185 = process.vectPtW.clone()
process.vectPtW250 = process.vectPtW.clone()


process.mon120 = cms.Sequence(process.histNoff + process.vectPhi120 + process.vectPhi120Lm + process.vectPt120 + process.vectPt120Lm + process.vectEta120 + process.vectEta120Lm + process.vectV0MassLm120)
process.mon150 = cms.Sequence(process.histNoff + process.vectPhi150 + process.vectPhi150Lm + process.vectPt150 + process.vectPt150Lm + process.vectEta150 + process.vectEta150Lm + process.vectV0MassLm150)
process.mon185 = cms.Sequence(process.histNoff + process.vectPhi185 + process.vectPhi185Lm + process.vectPt185 + process.vectPt185Lm + process.vectEta185 + process.vectEta185Lm + process.vectV0MassLm185)
process.mon250 = cms.Sequence(process.histNoff + process.vectPhi250 + process.vectPhi250Lm + process.vectPt250 + process.vectPt250Lm + process.vectEta250 + process.vectEta250Lm + process.vectV0MassLm250)


process.ana120 = cms.Path(
        process.eventSelection
        * process.Noff
        * process.NoffFilter120
        * process.QWEvent
#        * process.QWV0EventKs
        * process.QWV0EventLambda
        * process.mon120
	* process.QWCumuDiff
        )

process.ana150 = cms.Path(
        process.eventSelection
        * process.Noff
        * process.NoffFilter150
        * process.QWEvent
#        * process.QWV0EventKs
        * process.QWV0EventLambda
        * process.mon150
	* process.QWCumuDiff
        )

process.ana185 = cms.Path(
        process.eventSelection
        * process.Noff
        * process.NoffFilter185
        * process.QWEvent
#        * process.QWV0EventKs
        * process.QWV0EventLambda
        * process.mon185
	* process.QWCumuDiff
        )


process.ana250 = cms.Path(
        process.eventSelection
        * process.Noff
        * process.NoffFilter250
        * process.QWEvent
#        * process.QWV0EventKs
        * process.QWV0EventLambda
        * process.mon250
	* process.QWCumuDiff
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
