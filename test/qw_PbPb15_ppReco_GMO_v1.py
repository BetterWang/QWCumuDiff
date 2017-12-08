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
		*range(120, 185)
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
				, Massmax = cms.untracked.double(0.57)
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
		, V0Src = cms.untracked.InputTag('generalV0CandidatesNew', 'Kshort')
		, daughter_cuts = cms.untracked.PSet(
			)
		, cuts = cms.untracked.VPSet(
			cms.untracked.PSet(
				Massmin = cms.untracked.double(1.08)
				, Massmax = cms.untracked.double(1.16)
				, DecayXYZMin = cms.untracked.double(5.0)
				, ThetaXYZMin = cms.untracked.double(0.9999)
				, ptMin = cms.untracked.double(0.2)
				, ptMax = cms.untracked.double(1.0)
				),
			cms.untracked.PSet(
				Massmin = cms.untracked.double(1.08)
				, Massmax = cms.untracked.double(1.16)
				, DecayXYZMin = cms.untracked.double(5.0)
				, ThetaXYZMin = cms.untracked.double(0.9998)
				, ptMin = cms.untracked.double(1.0)
				, ptMax = cms.untracked.double(8.5)
				)
			)
		)


process.load('PbPb_HIMB5_ppReco_eff')
process.Noff.vertexSrc = cms.untracked.InputTag('GMOVertex')
process.QWEvent.vertexSrc = cms.untracked.InputTag('GMOVertex')
process.QWEvent.ptMax = cms.untracked.double(100)


process.vectKsMassN0_pT02 = cms.EDAnalyzer('QWMassAnalyzer',
		srcMass = cms.untracked.InputTag("QWV0EventKs", "mass"),
		srcPt = cms.untracked.InputTag("QWV0EventKs", "pt"),
		hNbins = cms.untracked.int32(10),
		hstart = cms.untracked.double(0),
		hend = cms.untracked.double(10),
		cNbins = cms.untracked.int32(100),
		cstart = cms.untracked.double(.40),
		cend = cms.untracked.double(0.60),
		ptMin = cms.untracked.double(0.2),
		ptMax = cms.untracked.double(0.4),
		)

process.vectKsMassN0_pT04 = process.vectKsMassN0_pT02.clone(
		ptMin = cms.untracked.double(0.4),
		ptMax = cms.untracked.double(0.6),
		)

process.vectKsMassN0_pT06 = process.vectKsMassN0_pT02.clone(
		ptMin = cms.untracked.double(0.6),
		ptMax = cms.untracked.double(0.8),
		)

process.vectKsMassN0_pT08 = process.vectKsMassN0_pT02.clone(
		ptMin = cms.untracked.double(0.8),
		ptMax = cms.untracked.double(1.0),
		)

process.vectKsMassN0_pT10 = process.vectKsMassN0_pT02.clone(
		ptMin = cms.untracked.double(1.0),
		ptMax = cms.untracked.double(1.4),
		)

process.vectKsMassN0_pT14 = process.vectKsMassN0_pT02.clone(
		ptMin = cms.untracked.double(1.4),
		ptMax = cms.untracked.double(1.8),
		)

process.vectKsMassN0_pT18 = process.vectKsMassN0_pT02.clone(
		ptMin = cms.untracked.double(1.8),
		ptMax = cms.untracked.double(2.2),
		)

process.vectKsMassN0_pT22 = process.vectKsMassN0_pT02.clone(
		ptMin = cms.untracked.double(2.2),
		ptMax = cms.untracked.double(2.8),
		)

process.vectKsMassN0_pT28 = process.vectKsMassN0_pT02.clone(
		ptMin = cms.untracked.double(2.8),
		ptMax = cms.untracked.double(3.6),
		)

process.vectKsMassN0_pT36 = process.vectKsMassN0_pT02.clone(
		ptMin = cms.untracked.double(3.6),
		ptMax = cms.untracked.double(4.6),
		)

process.vectKsMassN0_pT46 = process.vectKsMassN0_pT02.clone(
		ptMin = cms.untracked.double(4.6),
		ptMax = cms.untracked.double(6.0),
		)

process.vectKsMassN0_pT60 = process.vectKsMassN0_pT02.clone(
		ptMin = cms.untracked.double(6.0),
		ptMax = cms.untracked.double(7.0),
		)

process.vectKsMassN0_pT70 = process.vectKsMassN0_pT02.clone(
		ptMin = cms.untracked.double(7.0),
		ptMax = cms.untracked.double(8.5),
		)

process.vectKsMassN0 = process.vectKsMassN0_pT02.clone(
		ptMin = cms.untracked.double(0.2),
		ptMax = cms.untracked.double(8.5),
		)

process.vectKsMassN10      = process.vectKsMassN0.clone()
process.vectKsMassN10_pT02 = process.vectKsMassN0_pT02.clone()
process.vectKsMassN10_pT04 = process.vectKsMassN0_pT04.clone()
process.vectKsMassN10_pT06 = process.vectKsMassN0_pT06.clone()
process.vectKsMassN10_pT08 = process.vectKsMassN0_pT08.clone()
process.vectKsMassN10_pT10 = process.vectKsMassN0_pT10.clone()
process.vectKsMassN10_pT14 = process.vectKsMassN0_pT14.clone()
process.vectKsMassN10_pT18 = process.vectKsMassN0_pT18.clone()
process.vectKsMassN10_pT22 = process.vectKsMassN0_pT22.clone()
process.vectKsMassN10_pT28 = process.vectKsMassN0_pT28.clone()
process.vectKsMassN10_pT36 = process.vectKsMassN0_pT36.clone()
process.vectKsMassN10_pT46 = process.vectKsMassN0_pT46.clone()
process.vectKsMassN10_pT60 = process.vectKsMassN0_pT60.clone()
process.vectKsMassN10_pT70 = process.vectKsMassN0_pT70.clone()

process.vectKsMassN30      = process.vectKsMassN0.clone()
process.vectKsMassN30_pT02 = process.vectKsMassN0_pT02.clone()
process.vectKsMassN30_pT04 = process.vectKsMassN0_pT04.clone()
process.vectKsMassN30_pT06 = process.vectKsMassN0_pT06.clone()
process.vectKsMassN30_pT08 = process.vectKsMassN0_pT08.clone()
process.vectKsMassN30_pT10 = process.vectKsMassN0_pT10.clone()
process.vectKsMassN30_pT14 = process.vectKsMassN0_pT14.clone()
process.vectKsMassN30_pT18 = process.vectKsMassN0_pT18.clone()
process.vectKsMassN30_pT22 = process.vectKsMassN0_pT22.clone()
process.vectKsMassN30_pT28 = process.vectKsMassN0_pT28.clone()
process.vectKsMassN30_pT36 = process.vectKsMassN0_pT36.clone()
process.vectKsMassN30_pT46 = process.vectKsMassN0_pT46.clone()
process.vectKsMassN30_pT60 = process.vectKsMassN0_pT60.clone()
process.vectKsMassN30_pT70 = process.vectKsMassN0_pT70.clone()

process.vectKsMassN90      = process.vectKsMassN0.clone()
process.vectKsMassN90_pT02 = process.vectKsMassN0_pT02.clone()
process.vectKsMassN90_pT04 = process.vectKsMassN0_pT04.clone()
process.vectKsMassN90_pT06 = process.vectKsMassN0_pT06.clone()
process.vectKsMassN90_pT08 = process.vectKsMassN0_pT08.clone()
process.vectKsMassN90_pT10 = process.vectKsMassN0_pT10.clone()
process.vectKsMassN90_pT14 = process.vectKsMassN0_pT14.clone()
process.vectKsMassN90_pT18 = process.vectKsMassN0_pT18.clone()
process.vectKsMassN90_pT22 = process.vectKsMassN0_pT22.clone()
process.vectKsMassN90_pT28 = process.vectKsMassN0_pT28.clone()
process.vectKsMassN90_pT36 = process.vectKsMassN0_pT36.clone()
process.vectKsMassN90_pT46 = process.vectKsMassN0_pT46.clone()
process.vectKsMassN90_pT60 = process.vectKsMassN0_pT60.clone()
process.vectKsMassN90_pT70 = process.vectKsMassN0_pT70.clone()

process.vectKsMassN120      = process.vectKsMassN0.clone()
process.vectKsMassN120_pT02 = process.vectKsMassN0_pT02.clone()
process.vectKsMassN120_pT04 = process.vectKsMassN0_pT04.clone()
process.vectKsMassN120_pT06 = process.vectKsMassN0_pT06.clone()
process.vectKsMassN120_pT08 = process.vectKsMassN0_pT08.clone()
process.vectKsMassN120_pT10 = process.vectKsMassN0_pT10.clone()
process.vectKsMassN120_pT14 = process.vectKsMassN0_pT14.clone()
process.vectKsMassN120_pT18 = process.vectKsMassN0_pT18.clone()
process.vectKsMassN120_pT22 = process.vectKsMassN0_pT22.clone()
process.vectKsMassN120_pT28 = process.vectKsMassN0_pT28.clone()
process.vectKsMassN120_pT36 = process.vectKsMassN0_pT36.clone()
process.vectKsMassN120_pT46 = process.vectKsMassN0_pT46.clone()
process.vectKsMassN120_pT60 = process.vectKsMassN0_pT60.clone()
process.vectKsMassN120_pT70 = process.vectKsMassN0_pT70.clone()

process.vectKsMassN185      = process.vectKsMassN0.clone()
process.vectKsMassN185_pT02 = process.vectKsMassN0_pT02.clone()
process.vectKsMassN185_pT04 = process.vectKsMassN0_pT04.clone()
process.vectKsMassN185_pT06 = process.vectKsMassN0_pT06.clone()
process.vectKsMassN185_pT08 = process.vectKsMassN0_pT08.clone()
process.vectKsMassN185_pT10 = process.vectKsMassN0_pT10.clone()
process.vectKsMassN185_pT14 = process.vectKsMassN0_pT14.clone()
process.vectKsMassN185_pT18 = process.vectKsMassN0_pT18.clone()
process.vectKsMassN185_pT22 = process.vectKsMassN0_pT22.clone()
process.vectKsMassN185_pT28 = process.vectKsMassN0_pT28.clone()
process.vectKsMassN185_pT36 = process.vectKsMassN0_pT36.clone()
process.vectKsMassN185_pT46 = process.vectKsMassN0_pT46.clone()
process.vectKsMassN185_pT60 = process.vectKsMassN0_pT60.clone()
process.vectKsMassN185_pT70 = process.vectKsMassN0_pT70.clone()

process.vectKsMassN250      = process.vectKsMassN0.clone()
process.vectKsMassN250_pT02 = process.vectKsMassN0_pT02.clone()
process.vectKsMassN250_pT04 = process.vectKsMassN0_pT04.clone()
process.vectKsMassN250_pT06 = process.vectKsMassN0_pT06.clone()
process.vectKsMassN250_pT08 = process.vectKsMassN0_pT08.clone()
process.vectKsMassN250_pT10 = process.vectKsMassN0_pT10.clone()
process.vectKsMassN250_pT14 = process.vectKsMassN0_pT14.clone()
process.vectKsMassN250_pT18 = process.vectKsMassN0_pT18.clone()
process.vectKsMassN250_pT22 = process.vectKsMassN0_pT22.clone()
process.vectKsMassN250_pT28 = process.vectKsMassN0_pT28.clone()
process.vectKsMassN250_pT36 = process.vectKsMassN0_pT36.clone()
process.vectKsMassN250_pT46 = process.vectKsMassN0_pT46.clone()
process.vectKsMassN250_pT60 = process.vectKsMassN0_pT60.clone()
process.vectKsMassN250_pT70 = process.vectKsMassN0_pT70.clone()



process.monKsMassN0 = cms.Sequence(
		  process.vectKsMassN0
		+ process.vectKsMassN0_pT02
		+ process.vectKsMassN0_pT04
		+ process.vectKsMassN0_pT06
		+ process.vectKsMassN0_pT08
		+ process.vectKsMassN0_pT10
		+ process.vectKsMassN0_pT14
		+ process.vectKsMassN0_pT18
		+ process.vectKsMassN0_pT22
		+ process.vectKsMassN0_pT28
		+ process.vectKsMassN0_pT36
		+ process.vectKsMassN0_pT46
		+ process.vectKsMassN0_pT60
		+ process.vectKsMassN0_pT70
		)

process.monKsMassN10 = cms.Sequence(
		  process.vectKsMassN10
		+ process.vectKsMassN10_pT02
		+ process.vectKsMassN10_pT04
		+ process.vectKsMassN10_pT06
		+ process.vectKsMassN10_pT08
		+ process.vectKsMassN10_pT10
		+ process.vectKsMassN10_pT14
		+ process.vectKsMassN10_pT18
		+ process.vectKsMassN10_pT22
		+ process.vectKsMassN10_pT28
		+ process.vectKsMassN10_pT36
		+ process.vectKsMassN10_pT46
		+ process.vectKsMassN10_pT60
		+ process.vectKsMassN10_pT70
		)

process.monKsMassN30 = cms.Sequence(
		  process.vectKsMassN30
		+ process.vectKsMassN30_pT02
		+ process.vectKsMassN30_pT04
		+ process.vectKsMassN30_pT06
		+ process.vectKsMassN30_pT08
		+ process.vectKsMassN30_pT10
		+ process.vectKsMassN30_pT14
		+ process.vectKsMassN30_pT18
		+ process.vectKsMassN30_pT22
		+ process.vectKsMassN30_pT28
		+ process.vectKsMassN30_pT36
		+ process.vectKsMassN30_pT46
		+ process.vectKsMassN30_pT60
		+ process.vectKsMassN30_pT70
		)

process.monKsMassN90 = cms.Sequence(
		  process.vectKsMassN90
		+ process.vectKsMassN90_pT02
		+ process.vectKsMassN90_pT04
		+ process.vectKsMassN90_pT06
		+ process.vectKsMassN90_pT08
		+ process.vectKsMassN90_pT10
		+ process.vectKsMassN90_pT14
		+ process.vectKsMassN90_pT18
		+ process.vectKsMassN90_pT22
		+ process.vectKsMassN90_pT28
		+ process.vectKsMassN90_pT36
		+ process.vectKsMassN90_pT46
		+ process.vectKsMassN90_pT60
		+ process.vectKsMassN90_pT70
		)

process.monKsMassN120 = cms.Sequence(
		  process.vectKsMassN120
		+ process.vectKsMassN120_pT02
		+ process.vectKsMassN120_pT04
		+ process.vectKsMassN120_pT06
		+ process.vectKsMassN120_pT08
		+ process.vectKsMassN120_pT10
		+ process.vectKsMassN120_pT14
		+ process.vectKsMassN120_pT18
		+ process.vectKsMassN120_pT22
		+ process.vectKsMassN120_pT28
		+ process.vectKsMassN120_pT36
		+ process.vectKsMassN120_pT46
		+ process.vectKsMassN120_pT60
		+ process.vectKsMassN120_pT70
		)

process.monKsMassN185 = cms.Sequence(
		  process.vectKsMassN185
		+ process.vectKsMassN185_pT02
		+ process.vectKsMassN185_pT04
		+ process.vectKsMassN185_pT06
		+ process.vectKsMassN185_pT08
		+ process.vectKsMassN185_pT10
		+ process.vectKsMassN185_pT14
		+ process.vectKsMassN185_pT18
		+ process.vectKsMassN185_pT22
		+ process.vectKsMassN185_pT28
		+ process.vectKsMassN185_pT36
		+ process.vectKsMassN185_pT46
		+ process.vectKsMassN185_pT60
		+ process.vectKsMassN185_pT70
		)

process.monKsMassN250 = cms.Sequence(
		  process.vectKsMassN250
		+ process.vectKsMassN250_pT02
		+ process.vectKsMassN250_pT04
		+ process.vectKsMassN250_pT06
		+ process.vectKsMassN250_pT08
		+ process.vectKsMassN250_pT10
		+ process.vectKsMassN250_pT14
		+ process.vectKsMassN250_pT18
		+ process.vectKsMassN250_pT22
		+ process.vectKsMassN250_pT28
		+ process.vectKsMassN250_pT36
		+ process.vectKsMassN250_pT46
		+ process.vectKsMassN250_pT60
		+ process.vectKsMassN250_pT70
		)

process.vectLmMassN0_pT02 = cms.EDAnalyzer('QWMassAnalyzer',
		srcMass = cms.untracked.InputTag("QWV0EventLambda", "mass"),
		srcPt = cms.untracked.InputTag("QWV0EventLambda", "pt"),
		hNbins = cms.untracked.int32(10),
		hstart = cms.untracked.double(0),
		hend = cms.untracked.double(10),
		cNbins = cms.untracked.int32(100),
		cstart = cms.untracked.double(1.08),
		cend = cms.untracked.double(1.18),
		ptMin = cms.untracked.double(0.2),
		ptMax = cms.untracked.double(0.4),
		)

process.vectLmMassN0_pT04 = process.vectLmMassN0_pT02.clone(
		ptMin = cms.untracked.double(0.4),
		ptMax = cms.untracked.double(0.6),
		)

process.vectLmMassN0_pT06 = process.vectLmMassN0_pT02.clone(
		ptMin = cms.untracked.double(0.6),
		ptMax = cms.untracked.double(0.8),
		)

process.vectLmMassN0_pT08 = process.vectLmMassN0_pT02.clone(
		ptMin = cms.untracked.double(0.8),
		ptMax = cms.untracked.double(1.0),
		)

process.vectLmMassN0_pT10 = process.vectLmMassN0_pT02.clone(
		ptMin = cms.untracked.double(1.0),
		ptMax = cms.untracked.double(1.4),
		)

process.vectLmMassN0_pT14 = process.vectLmMassN0_pT02.clone(
		ptMin = cms.untracked.double(1.4),
		ptMax = cms.untracked.double(1.8),
		)

process.vectLmMassN0_pT18 = process.vectLmMassN0_pT02.clone(
		ptMin = cms.untracked.double(1.8),
		ptMax = cms.untracked.double(2.2),
		)

process.vectLmMassN0_pT22 = process.vectLmMassN0_pT02.clone(
		ptMin = cms.untracked.double(2.2),
		ptMax = cms.untracked.double(2.8),
		)

process.vectLmMassN0_pT28 = process.vectLmMassN0_pT02.clone(
		ptMin = cms.untracked.double(2.8),
		ptMax = cms.untracked.double(3.6),
		)

process.vectLmMassN0_pT36 = process.vectLmMassN0_pT02.clone(
		ptMin = cms.untracked.double(3.6),
		ptMax = cms.untracked.double(4.6),
		)

process.vectLmMassN0_pT46 = process.vectLmMassN0_pT02.clone(
		ptMin = cms.untracked.double(4.6),
		ptMax = cms.untracked.double(6.0),
		)

process.vectLmMassN0_pT60 = process.vectLmMassN0_pT02.clone(
		ptMin = cms.untracked.double(6.0),
		ptMax = cms.untracked.double(7.0),
		)

process.vectLmMassN0_pT70 = process.vectLmMassN0_pT02.clone(
		ptMin = cms.untracked.double(7.0),
		ptMax = cms.untracked.double(8.5),
		)

process.vectLmMassN0 = process.vectLmMassN0_pT02.clone(
		ptMin = cms.untracked.double(0.2),
		ptMax = cms.untracked.double(8.5),
		)

process.vectLmMassN10      = process.vectLmMassN0.clone()
process.vectLmMassN10_pT02 = process.vectLmMassN0_pT02.clone()
process.vectLmMassN10_pT04 = process.vectLmMassN0_pT04.clone()
process.vectLmMassN10_pT06 = process.vectLmMassN0_pT06.clone()
process.vectLmMassN10_pT08 = process.vectLmMassN0_pT08.clone()
process.vectLmMassN10_pT10 = process.vectLmMassN0_pT10.clone()
process.vectLmMassN10_pT14 = process.vectLmMassN0_pT14.clone()
process.vectLmMassN10_pT18 = process.vectLmMassN0_pT18.clone()
process.vectLmMassN10_pT22 = process.vectLmMassN0_pT22.clone()
process.vectLmMassN10_pT28 = process.vectLmMassN0_pT28.clone()
process.vectLmMassN10_pT36 = process.vectLmMassN0_pT36.clone()
process.vectLmMassN10_pT46 = process.vectLmMassN0_pT46.clone()
process.vectLmMassN10_pT60 = process.vectLmMassN0_pT60.clone()
process.vectLmMassN10_pT70 = process.vectLmMassN0_pT70.clone()

process.vectLmMassN30      = process.vectLmMassN0.clone()
process.vectLmMassN30_pT02 = process.vectLmMassN0_pT02.clone()
process.vectLmMassN30_pT04 = process.vectLmMassN0_pT04.clone()
process.vectLmMassN30_pT06 = process.vectLmMassN0_pT06.clone()
process.vectLmMassN30_pT08 = process.vectLmMassN0_pT08.clone()
process.vectLmMassN30_pT10 = process.vectLmMassN0_pT10.clone()
process.vectLmMassN30_pT14 = process.vectLmMassN0_pT14.clone()
process.vectLmMassN30_pT18 = process.vectLmMassN0_pT18.clone()
process.vectLmMassN30_pT22 = process.vectLmMassN0_pT22.clone()
process.vectLmMassN30_pT28 = process.vectLmMassN0_pT28.clone()
process.vectLmMassN30_pT36 = process.vectLmMassN0_pT36.clone()
process.vectLmMassN30_pT46 = process.vectLmMassN0_pT46.clone()
process.vectLmMassN30_pT60 = process.vectLmMassN0_pT60.clone()
process.vectLmMassN30_pT70 = process.vectLmMassN0_pT70.clone()


process.vectLmMassN90      = process.vectLmMassN0.clone()
process.vectLmMassN90_pT02 = process.vectLmMassN0_pT02.clone()
process.vectLmMassN90_pT04 = process.vectLmMassN0_pT04.clone()
process.vectLmMassN90_pT06 = process.vectLmMassN0_pT06.clone()
process.vectLmMassN90_pT08 = process.vectLmMassN0_pT08.clone()
process.vectLmMassN90_pT10 = process.vectLmMassN0_pT10.clone()
process.vectLmMassN90_pT14 = process.vectLmMassN0_pT14.clone()
process.vectLmMassN90_pT18 = process.vectLmMassN0_pT18.clone()
process.vectLmMassN90_pT22 = process.vectLmMassN0_pT22.clone()
process.vectLmMassN90_pT28 = process.vectLmMassN0_pT28.clone()
process.vectLmMassN90_pT36 = process.vectLmMassN0_pT36.clone()
process.vectLmMassN90_pT46 = process.vectLmMassN0_pT46.clone()
process.vectLmMassN90_pT60 = process.vectLmMassN0_pT60.clone()
process.vectLmMassN90_pT70 = process.vectLmMassN0_pT70.clone()


process.vectLmMassN120      = process.vectLmMassN0.clone()
process.vectLmMassN120_pT02 = process.vectLmMassN0_pT02.clone()
process.vectLmMassN120_pT04 = process.vectLmMassN0_pT04.clone()
process.vectLmMassN120_pT06 = process.vectLmMassN0_pT06.clone()
process.vectLmMassN120_pT08 = process.vectLmMassN0_pT08.clone()
process.vectLmMassN120_pT10 = process.vectLmMassN0_pT10.clone()
process.vectLmMassN120_pT14 = process.vectLmMassN0_pT14.clone()
process.vectLmMassN120_pT18 = process.vectLmMassN0_pT18.clone()
process.vectLmMassN120_pT22 = process.vectLmMassN0_pT22.clone()
process.vectLmMassN120_pT28 = process.vectLmMassN0_pT28.clone()
process.vectLmMassN120_pT36 = process.vectLmMassN0_pT36.clone()
process.vectLmMassN120_pT46 = process.vectLmMassN0_pT46.clone()
process.vectLmMassN120_pT60 = process.vectLmMassN0_pT60.clone()
process.vectLmMassN120_pT70 = process.vectLmMassN0_pT70.clone()

process.vectLmMassN185      = process.vectLmMassN0.clone()
process.vectLmMassN185_pT02 = process.vectLmMassN0_pT02.clone()
process.vectLmMassN185_pT04 = process.vectLmMassN0_pT04.clone()
process.vectLmMassN185_pT06 = process.vectLmMassN0_pT06.clone()
process.vectLmMassN185_pT08 = process.vectLmMassN0_pT08.clone()
process.vectLmMassN185_pT10 = process.vectLmMassN0_pT10.clone()
process.vectLmMassN185_pT14 = process.vectLmMassN0_pT14.clone()
process.vectLmMassN185_pT18 = process.vectLmMassN0_pT18.clone()
process.vectLmMassN185_pT22 = process.vectLmMassN0_pT22.clone()
process.vectLmMassN185_pT28 = process.vectLmMassN0_pT28.clone()
process.vectLmMassN185_pT36 = process.vectLmMassN0_pT36.clone()
process.vectLmMassN185_pT46 = process.vectLmMassN0_pT46.clone()
process.vectLmMassN185_pT60 = process.vectLmMassN0_pT60.clone()
process.vectLmMassN185_pT70 = process.vectLmMassN0_pT70.clone()

process.vectLmMassN250      = process.vectLmMassN0.clone()
process.vectLmMassN250_pT02 = process.vectLmMassN0_pT02.clone()
process.vectLmMassN250_pT04 = process.vectLmMassN0_pT04.clone()
process.vectLmMassN250_pT06 = process.vectLmMassN0_pT06.clone()
process.vectLmMassN250_pT08 = process.vectLmMassN0_pT08.clone()
process.vectLmMassN250_pT10 = process.vectLmMassN0_pT10.clone()
process.vectLmMassN250_pT14 = process.vectLmMassN0_pT14.clone()
process.vectLmMassN250_pT18 = process.vectLmMassN0_pT18.clone()
process.vectLmMassN250_pT22 = process.vectLmMassN0_pT22.clone()
process.vectLmMassN250_pT28 = process.vectLmMassN0_pT28.clone()
process.vectLmMassN250_pT36 = process.vectLmMassN0_pT36.clone()
process.vectLmMassN250_pT46 = process.vectLmMassN0_pT46.clone()
process.vectLmMassN250_pT60 = process.vectLmMassN0_pT60.clone()
process.vectLmMassN250_pT70 = process.vectLmMassN0_pT70.clone()

process.monLmMassN0 = cms.Sequence(
		  process.vectLmMassN0
		+ process.vectLmMassN0_pT02
		+ process.vectLmMassN0_pT04
		+ process.vectLmMassN0_pT06
		+ process.vectLmMassN0_pT08
		+ process.vectLmMassN0_pT10
		+ process.vectLmMassN0_pT14
		+ process.vectLmMassN0_pT18
		+ process.vectLmMassN0_pT22
		+ process.vectLmMassN0_pT28
		+ process.vectLmMassN0_pT36
		+ process.vectLmMassN0_pT46
		+ process.vectLmMassN0_pT60
		+ process.vectLmMassN0_pT70
		)

process.monLmMassN10 = cms.Sequence(
		  process.vectLmMassN10
		+ process.vectLmMassN10_pT02
		+ process.vectLmMassN10_pT04
		+ process.vectLmMassN10_pT06
		+ process.vectLmMassN10_pT08
		+ process.vectLmMassN10_pT10
		+ process.vectLmMassN10_pT14
		+ process.vectLmMassN10_pT18
		+ process.vectLmMassN10_pT22
		+ process.vectLmMassN10_pT28
		+ process.vectLmMassN10_pT36
		+ process.vectLmMassN10_pT46
		+ process.vectLmMassN10_pT60
		+ process.vectLmMassN10_pT70
		)

process.monLmMassN30 = cms.Sequence(
		  process.vectLmMassN30
		+ process.vectLmMassN30_pT02
		+ process.vectLmMassN30_pT04
		+ process.vectLmMassN30_pT06
		+ process.vectLmMassN30_pT08
		+ process.vectLmMassN30_pT10
		+ process.vectLmMassN30_pT14
		+ process.vectLmMassN30_pT18
		+ process.vectLmMassN30_pT22
		+ process.vectLmMassN30_pT28
		+ process.vectLmMassN30_pT36
		+ process.vectLmMassN30_pT46
		+ process.vectLmMassN30_pT60
		+ process.vectLmMassN30_pT70
		)

process.monLmMassN90 = cms.Sequence(
		  process.vectLmMassN90
		+ process.vectLmMassN90_pT02
		+ process.vectLmMassN90_pT04
		+ process.vectLmMassN90_pT06
		+ process.vectLmMassN90_pT08
		+ process.vectLmMassN90_pT10
		+ process.vectLmMassN90_pT14
		+ process.vectLmMassN90_pT18
		+ process.vectLmMassN90_pT22
		+ process.vectLmMassN90_pT28
		+ process.vectLmMassN90_pT36
		+ process.vectLmMassN90_pT46
		+ process.vectLmMassN90_pT60
		+ process.vectLmMassN90_pT70
		)

process.monLmMassN120 = cms.Sequence(
		  process.vectLmMassN120
		+ process.vectLmMassN120_pT02
		+ process.vectLmMassN120_pT04
		+ process.vectLmMassN120_pT06
		+ process.vectLmMassN120_pT08
		+ process.vectLmMassN120_pT10
		+ process.vectLmMassN120_pT14
		+ process.vectLmMassN120_pT18
		+ process.vectLmMassN120_pT22
		+ process.vectLmMassN120_pT28
		+ process.vectLmMassN120_pT36
		+ process.vectLmMassN120_pT46
		+ process.vectLmMassN120_pT60
		+ process.vectLmMassN120_pT70
		)


process.monLmMassN185 = cms.Sequence(
		  process.vectLmMassN185
		+ process.vectLmMassN185_pT02
		+ process.vectLmMassN185_pT04
		+ process.vectLmMassN185_pT06
		+ process.vectLmMassN185_pT08
		+ process.vectLmMassN185_pT10
		+ process.vectLmMassN185_pT14
		+ process.vectLmMassN185_pT18
		+ process.vectLmMassN185_pT22
		+ process.vectLmMassN185_pT28
		+ process.vectLmMassN185_pT36
		+ process.vectLmMassN185_pT46
		+ process.vectLmMassN185_pT60
		+ process.vectLmMassN185_pT70
		)

process.monLmMassN250 = cms.Sequence(
		  process.vectLmMassN250
		+ process.vectLmMassN250_pT02
		+ process.vectLmMassN250_pT04
		+ process.vectLmMassN250_pT06
		+ process.vectLmMassN250_pT08
		+ process.vectLmMassN250_pT10
		+ process.vectLmMassN250_pT14
		+ process.vectLmMassN250_pT18
		+ process.vectLmMassN250_pT22
		+ process.vectLmMassN250_pT28
		+ process.vectLmMassN250_pT36
		+ process.vectLmMassN250_pT46
		+ process.vectLmMassN250_pT60
		+ process.vectLmMassN250_pT70
		)

process.vectPt.cNbins = cms.untracked.int32(4000)
process.vectPt.cend = cms.untracked.double(40)
process.vectPtW.cNbins = cms.untracked.int32(4000)
process.vectPtW.cend = cms.untracked.double(40)

process.vectPhiV0 = process.vectPhi.clone(src = cms.untracked.InputTag('QWV0EventV0', 'phi'))
process.vectEtaV0 = process.vectEta.clone(src = cms.untracked.InputTag('QWV0EventV0', 'eta'))
process.vectPtV0  = process.vectPt.clone(src = cms.untracked.InputTag('QWV0EventV0', 'pt'))

process.ana = cms.Path(
		process.eventSelection
		* process.makeEvent
		* process.QWV0EventKs
		* process.QWV0EventLambda
		)

process.ana0 = cms.Path(
		process.eventSelection
		* process.makeEvent
		* process.NoffFilter0
		* process.QWV0EventKs
		* process.QWV0EventLambda
		* process.monKsMassN0
		* process.monLmMassN0
		)

process.ana10 = cms.Path(
		process.eventSelection
		* process.makeEvent
		* process.NoffFilter10
		* process.QWV0EventKs
		* process.QWV0EventLambda
		* process.monKsMassN10
		* process.monLmMassN10
		)

process.ana30 = cms.Path(
		process.eventSelection
		* process.makeEvent
		* process.NoffFilter30
		* process.QWV0EventKs
		* process.QWV0EventLambda
		* process.monKsMassN30
		* process.monLmMassN30
		)

process.ana90 = cms.Path(
		process.eventSelection
		* process.makeEvent
		* process.NoffFilter90
		* process.QWV0EventKs
		* process.QWV0EventLambda
		* process.monKsMassN90
		* process.monLmMassN90
		)

process.ana120 = cms.Path(
		process.eventSelection
		* process.makeEvent
		* process.NoffFilter120
		* process.QWV0EventKs
		* process.QWV0EventLambda
		* process.monKsMassN120
		* process.monLmMassN120
		)

process.ana185 = cms.Path(
		process.eventSelection
		* process.makeEvent
		* process.NoffFilter185
		* process.QWV0EventKs
		* process.QWV0EventLambda
		* process.monKsMassN185
		* process.monLmMassN185
		)

process.ana250 = cms.Path(
		process.eventSelection
		* process.makeEvent
		* process.NoffFilter250
		* process.QWV0EventKs
		* process.QWV0EventLambda
		* process.monKsMassN250
		* process.monLmMassN250
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
	process.ana,
	process.ana0,
	process.ana10,
	process.ana30,
	process.ana90,
	process.ana120,
	process.ana185,
	process.ana250,
	process.out
)
