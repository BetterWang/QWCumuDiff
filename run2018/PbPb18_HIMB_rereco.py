import FWCore.ParameterSet.Config as cms

QWV0EventLm = cms.EDProducer('QWV0VectProducer'
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
                , AbsRapmax = cms.untracked.double(1.0)
                , AbsRapmin = cms.untracked.double(-1.0)
                )
            )
        )

QWV0EventKs = cms.EDProducer('QWV0VectProducer'
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
                , AbsRapmax = cms.untracked.double(1.0)
                , AbsRapmin = cms.untracked.double(-1.0)
                )
            )
        )


# tracks 1.0 < pT < 5.0, |eta|<2.4
# ppReco tracking 
QWEvent = cms.EDProducer("QWEventProducer"
        , vertexSrc = cms.untracked.InputTag('offlinePrimaryVerticesRecovery')
        , trackSrc = cms.untracked.InputTag('generalTracks')
        , fweight = cms.untracked.InputTag('NA')
        , centralitySrc = cms.untracked.InputTag("centralityBin", "HFtowers")
        , dzdzerror = cms.untracked.double(3.0)
        , d0d0error = cms.untracked.double(3.0)
        , pterrorpt = cms.untracked.double(0.1)
        , ptMin = cms.untracked.double(0.5)
        , ptMax= cms.untracked.double(5.0)
        , Etamin = cms.untracked.double(-2.4)
        , Etamax = cms.untracked.double(2.4)
        )


dbCent = cms.EDProducer('QWInt2Double',
		src = cms.untracked.InputTag('centralityBin', 'HFtowers')
		)

QWEventInfo = cms.EDProducer('QWEventInfoProducer')


EPOrg = cms.EDProducer('QWEvtPlaneProducer',
        src = cms.untracked.InputTag('hiEvtPlaneFlat'),
        level = cms.untracked.int32(0)
        )

EPFlat = cms.EDProducer('QWEvtPlaneProducer',
        src = cms.untracked.InputTag('hiEvtPlaneFlat'),
        level = cms.untracked.int32(2)
        )

EPOrgA = cms.EDProducer('QWEvtPlaneProducer',
        src = cms.untracked.InputTag('hiEvtPlane'),
        level = cms.untracked.int32(0)
        )

EPFlatA = cms.EDProducer('QWEvtPlaneProducer',
        src = cms.untracked.InputTag('hiEvtPlane'),
        level = cms.untracked.int32(2)
        )




# monitoring

histCentBin = cms.EDAnalyzer('QWHistAnalyzer',
		src = cms.untracked.InputTag("centralityBin", "HFtowers"),
		Nbins = cms.untracked.int32(200),
		start = cms.untracked.double(0),
		end = cms.untracked.double(200),
		)

vectPhi = cms.EDAnalyzer('QWVectorAnalyzer',
        src = cms.untracked.InputTag("QWEvent", "phi"),
        hNbins = cms.untracked.int32(1000),
        hstart = cms.untracked.double(0),
        hend = cms.untracked.double(1000),
        cNbins = cms.untracked.int32(1000),
        cstart = cms.untracked.double(-3.14159265358979323846),
        cend = cms.untracked.double(3.14159265358979323846),
        )

vectPt = cms.EDAnalyzer('QWVectorAnalyzer',
        src = cms.untracked.InputTag("QWEvent", "pt"),
        hNbins = cms.untracked.int32(1000),
        hstart = cms.untracked.double(0),
        hend = cms.untracked.double(1000),
        cNbins = cms.untracked.int32(1000),
        cstart = cms.untracked.double(0),
        cend = cms.untracked.double(5),
        )

vectEta = cms.EDAnalyzer('QWVectorAnalyzer',
        src = cms.untracked.InputTag("QWEvent", "eta"),
        hNbins = cms.untracked.int32(1000),
        hstart = cms.untracked.double(0),
        hend = cms.untracked.double(1000),
        cNbins = cms.untracked.int32(1000),
        cstart = cms.untracked.double(-2.5),
        cend = cms.untracked.double(2.5),
        )

corr2D = cms.EDAnalyzer('QWVCorrAnalyzer',
        srcX = cms.untracked.InputTag("QWEvent", "phi"),
        srcY = cms.untracked.InputTag("QWEvent", "eta"),
        NbinsX = cms.untracked.int32( 160 ),
        NbinsY = cms.untracked.int32( 50 ),
        hstartX = cms.untracked.double(-3.14159265358979323846),
        hendX = cms.untracked.double(3.14159265358979323846),
        hstartY = cms.untracked.double(-2.5),
        hendY = cms.untracked.double(2.5)
        )

vectMon = cms.Sequence(histCentBin * vectPhi * vectPt * vectEta * corr2D)


#vectPhiV0 = cms.EDAnalyzer('QWVectorAnalyzer',
#        src = cms.untracked.InputTag("QWV0EventLm", "phi"),
#        hNbins = cms.untracked.int32(10),
#        hstart = cms.untracked.double(0),
#        hend = cms.untracked.double(10),
#        cNbins = cms.untracked.int32(1000),
#        cstart = cms.untracked.double(-3.14159265358979323846),
#        cend = cms.untracked.double(3.14159265358979323846),
#        )
#
#vectPtV0 = cms.EDAnalyzer('QWVectorAnalyzer',
#        src = cms.untracked.InputTag("QWV0EventLm", "pt"),
#        hNbins = cms.untracked.int32(10),
#        hstart = cms.untracked.double(0),
#        hend = cms.untracked.double(10),
#        cNbins = cms.untracked.int32(1000),
#        cstart = cms.untracked.double(0),
#        cend = cms.untracked.double(10),
#        )
#
#vectEtaV0 = cms.EDAnalyzer('QWVectorAnalyzer',
#        src = cms.untracked.InputTag("QWV0EventLm", "eta"),
#        hNbins = cms.untracked.int32(10),
#        hstart = cms.untracked.double(0),
#        hend = cms.untracked.double(10),
#        cNbins = cms.untracked.int32(1000),
#        cstart = cms.untracked.double(-2.5),
#        cend = cms.untracked.double(2.5),
#        )
#
#vectRapV0 = cms.EDAnalyzer('QWVectorAnalyzer',
#        src = cms.untracked.InputTag("QWV0EventLm", "rapidity"),
#        hNbins = cms.untracked.int32(10),
#        hstart = cms.untracked.double(0),
#        hend = cms.untracked.double(10),
#        cNbins = cms.untracked.int32(1000),
#        cstart = cms.untracked.double(-2.5),
#        cend = cms.untracked.double(2.5),
#        )
#
#vectMonV0 = cms.Sequence( vectPhiV0 * vectPtV0 * vectEtaV0 * vectRapV0 )

vectMassKs = cms.EDAnalyzer('QWMassAnalyzer',
        srcMass = cms.untracked.InputTag("QWV0MVAVector", "mass"),
        srcPt   = cms.untracked.InputTag("QWV0MVAVector", "pt"),
        srcEta  = cms.untracked.InputTag("QWV0MVAVector", "rapidity"),
        srcPhi  = cms.untracked.InputTag("QWV0MVAVector", "phi"),
        Nbins   = cms.untracked.int32(270),
        start   = cms.untracked.double(.43),
        end     = cms.untracked.double(0.565),
        )


vectMassLm = cms.EDAnalyzer('QWMassAnalyzer',
        srcMass = cms.untracked.InputTag("QWV0MVAVector", "mass"),
        srcPt   = cms.untracked.InputTag("QWV0MVAVector", "pt"),
        srcEta  = cms.untracked.InputTag("QWV0MVAVector", "rapidity"),
        srcPhi  = cms.untracked.InputTag("QWV0MVAVector", "phi"),
        Nbins   = cms.untracked.int32(160),
        start   = cms.untracked.double(1.08),
        end     = cms.untracked.double(1.16),
        )


