// -*- C++ -*-
//
// Package:    QWCumuDiff
// Class:      QWCumuDiff
// 
/**\class QWCumuDiff QWCumuDiff.cc QWAna/QWCumuDiff/src/QWCumuDiff.cc

Description: [Cumulant differential package]

Implementation:
[Quan Wang is cool]
*/
//
// Original Author:  Quan Wang
//         Created:  05/23/2014
// $Id: QWCumuDiff.cc,v 1.0 2017/02/11 15:56:58 qwang Exp $
//
//


// system include files
#include <memory>
#include <algorithm>

// user include files
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/EDAnalyzer.h"
#include "FWCore/Common/interface/TriggerNames.h"
#include "DataFormats/Common/interface/TriggerResults.h"

#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"

#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "FWCore/Utilities/interface/InputTag.h"
#include <DataFormats/ParticleFlowCandidate/interface/PFCandidateFwd.h>
#include <DataFormats/ParticleFlowCandidate/interface/PFCandidate.h>
#include "DataFormats/HepMCCandidate/interface/GenParticle.h"
#include "FWCore/ServiceRegistry/interface/Service.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"
#include "DataFormats/HeavyIonEvent/interface/EvtPlane.h"
#include "TH1.h"
#include "TH2.h"
#include "TNtuple.h"
#include "TComplex.h"
#include <complex>


#include "QWAna/QWCumuDiff/interface/QWCumuDiff.h"


using namespace std;

//#ifdef QW_DEBUG
//
// constructors and destructor
//
QWCumuDiff::QWCumuDiff(const edm::ParameterSet& iConfig):
	vertexZ_( iConfig.getUntrackedParameter<edm::InputTag>("vertexZ") ),
	centralityTag_( iConfig.getUntrackedParameter<edm::InputTag>("centrality") )
{
	const edm::ParameterSet& track = iConfig.getUntrackedParameter<edm::ParameterSet>("trackSet");
	trackEta_ = track.getUntrackedParameter<edm::InputTag>("Eta");
	trackPhi_ = track.getUntrackedParameter<edm::InputTag>("Phi");
	trackRef_ = track.getUntrackedParameter<edm::InputTag>("Ref");
	trackPt_  = track.getUntrackedParameter<edm::InputTag>("Pt");
	trackWeight_  = track.getUntrackedParameter<edm::InputTag>("Weight");

	const edm::ParameterSet& signal = iConfig.getUntrackedParameter<edm::ParameterSet>("sigSet");
	sigEta_ = signal.getUntrackedParameter<edm::InputTag>("Eta");
	sigPhi_ = signal.getUntrackedParameter<edm::InputTag>("Phi");
	sigPt_  = signal.getUntrackedParameter<edm::InputTag>("Pt");
	sigRef_ = signal.getUntrackedParameter<edm::InputTag>("Ref");
	sigWeight_ = signal.getUntrackedParameter<edm::InputTag>("Weight");

	//now do what ever initialization is needed
	minvz_ = iConfig.getUntrackedParameter<double>("minvz", -15.);
	maxvz_ = iConfig.getUntrackedParameter<double>("maxvz", 15.);

	ptBin_ = iConfig.getUntrackedParameter< std::vector<double> >("ptBin");
	Npt_ = ptBin_.size();

	rfpmineta_ = iConfig.getUntrackedParameter<double>("rfpmineta", -2.4);
	rfpmaxeta_ = iConfig.getUntrackedParameter<double>("rfpmaxeta", 2.4);
	rfpminpt_ = iConfig.getUntrackedParameter<double>("rfpminpt", 0.3);
	rfpmaxpt_ = iConfig.getUntrackedParameter<double>("rfpmaxpt", 3.0);

	dEtaGap_ = iConfig.getUntrackedParameter<double>("EtaGap", 2.0);

	cmode_ = iConfig.getUntrackedParameter<int>("cmode", 1);

        consumes<int>(centralityTag_);
        consumes<std::vector<double> >(vertexZ_);

        consumes<std::vector<double> >(trackEta_);
        consumes<std::vector<double> >(trackPhi_);
        consumes<std::vector<double> >(trackPt_);
        consumes<std::vector<double> >(trackRef_);
        consumes<std::vector<double> >(trackWeight_);

        consumes<std::vector<double> >(sigEta_);
        consumes<std::vector<double> >(sigPhi_);
        consumes<std::vector<double> >(sigPt_);
        consumes<std::vector<double> >(sigRef_);
        consumes<std::vector<double> >(sigWeight_);

	for ( int n = 1; n < 7; n++ ) {
		q[n] = correlations::QVector(0, 0, true);
	}
	qpos = correlations::QVector(0, 0, true);
	qneg = correlations::QVector(0, 0, true);

	edm::Service<TFileService> fs;

	trV = fs->make<TTree>("trV", "trV");
	trV->Branch("Noff", &gNoff, "Noff/I");
	trV->Branch("Mult", &gMult, "Mult/I");
	trV->Branch("NV0", &gV0, "gV0/I");
	trV->Branch("Vz", &Vz, "Vz/D");


	for ( int np = 0; np < 4; np++ ) {
		for ( int n = 2; n < 7; n++ ) {
			trV->Branch(Form("rQ%i%i", n, 2+2*np), &rQ[n][np], Form("rQ%i%i/D", n, 2+2*np));

			trV->Branch(Form("rVQp%i%i", n, 2+2*np), &rVQp[n][np], Form("rVQp%i%i[24]/D", n, 2+2*np));
		}

		int n = 2;
		trV->Branch(Form("wQ%i%i", n, 2+2*np), &wQ[n][np], Form("wQ%i%i/D", n, 2+2*np));
		trV->Branch(Form("wVQp%i%i", n, 2+2*np), wVQp[n][np], Form("wVQp%i%i[24]/D", n, 2+2*np));
	}

	int n = 2;
	trV->Branch(Form("wQGap%i", n), &wQGap[n], Form("wQGap%i/D", n));
	trV->Branch(Form("wV0QGap%i", n), wV0QGap[n], Form("wV0QGap%i[24]/D", n));
	trV->Branch(Form("wQpGap%i", n), &wQpGap[n], Form("wQpGap%i[24]/D", n));

	for ( int n = 2; n < 7; n++ ) {
		trV->Branch(Form("rQGap%i", n), &rQGap[n], Form("rQGap%i/D", n));

		trV->Branch(Form("rV0QGap%i", n), rV0QGap[n], Form("rV0QGap%i[24]/D", n));
		trV->Branch(Form("rQpGap%i", n), rQpGap[n], Form("rQpGap%i[24]/D", n));
	}

	trV->Branch("rQpos2", &rQpos2, "rQpos2/D");
	trV->Branch("rQneg2", &rQneg2, "rQneg2/D");
	trV->Branch("wQpos2", &wQpos2, "wQpos2/D");
	trV->Branch("wQneg2", &wQneg2, "wQneg2/D");
	trV->Branch("rQpos4", &rQpos4, "rQpos4/D");
	trV->Branch("rQneg4", &rQneg4, "rQneg4/D");
	trV->Branch("wQpos4", &wQpos4, "wQpos4/D");
	trV->Branch("wQneg4", &wQneg4, "wQneg4/D");

    trV->Branch("rVpQpos2", rVpQpos2, "rVpQpos2[24]/D");
    trV->Branch("rVpQneg2", rVpQneg2, "rVpQneg2[24]/D");
    trV->Branch("wVpQpos2", wVpQpos2, "wVpQpos2[24]/D");
    trV->Branch("wVpQneg2", wVpQneg2, "wVpQneg2[24]/D");
    trV->Branch("rVpQpos4", rVpQpos4, "rVpQpos4[24]/D");
    trV->Branch("rVpQneg4", rVpQneg4, "rVpQneg4[24]/D");
    trV->Branch("wVpQpos4", wVpQpos4, "wVpQpos4[24]/D");
    trV->Branch("wVpQneg4", wVpQneg4, "wVpQneg4[24]/D");


	cout << " cmode_ = " << cmode_ << endl;

	initQ();
}


QWCumuDiff::~QWCumuDiff()
{

	// do anything here that needs to be done at desctruction time
	// (e.g. close files, deallocate resources etc.)

}


//
// member functions
//

void
QWCumuDiff::analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup)
{
	using namespace edm;
	Handle<std::vector<double> >	hVz;

	Handle<std::vector<double> >	hEta;
	Handle<std::vector<double> >	hPhi;
	Handle<std::vector<double> >	hPt;
	Handle<std::vector<double> >	hWeight;
	Handle<std::vector<double> >	hRef;


	Handle<std::vector<double> >	sEta;
	Handle<std::vector<double> >	sPhi;
	Handle<std::vector<double> >	sPt;
	Handle<std::vector<double> >	sWeight;
	Handle<std::vector<double> >	sRef;

	iEvent.getByLabel(trackEta_,	hEta);
	iEvent.getByLabel(trackPhi_,	hPhi);
	iEvent.getByLabel(trackPt_,	hPt);
	iEvent.getByLabel(trackRef_,	hRef);
	iEvent.getByLabel(trackWeight_, hWeight);

	iEvent.getByLabel(vertexZ_, 	hVz);

	iEvent.getByLabel(sigEta_,	sEta);
	iEvent.getByLabel(sigPhi_,	sPhi);
	iEvent.getByLabel(sigPt_,	sPt);
	iEvent.getByLabel(sigRef_,	sRef);
	iEvent.getByLabel(sigWeight_, 	sWeight);

	if ( hVz->size() < 1 ) return;
	if ( fabs((*hVz)[0]) > maxvz_ or fabs((*hVz)[0]) < minvz_ ) return;
	int sz = int(hEta->size());
	if ( sz == 0 ) return;
	int sigsz = int(sPhi->size());
	if ( sigsz == 0 ) return;

	std::vector<int>	RFP;
	RFP.reserve(sz);
	int rfp_sz = 0;
	for ( int i = 0; i < sz; i++ ) {
		if ( (*hEta)[i] < rfpmaxeta_ and (*hEta)[i] > rfpmineta_
		and (*hPt)[i] < rfpmaxpt_ and (*hPt)[i] > rfpminpt_ ) {
			RFP[i] = 1;
			rfp_sz++;
		} else {
			RFP[i] = 0;
		}
	}

	for ( int n = 0; n < 7; n++ ) {
		for ( int np = 0; np < 4; np++ ) {
			rQ[n][np] = 0;
			iQ[n][np] = 0;
			wQ[n][np] = 0;

			for ( int i = 0; i < 24; i++ ) {
				rVQp[n][np][i] = 0;
				iVQp[n][np][i] = 0;
				wVQp[n][np][i] = 0;
			}
		}

		rQGap[n] = 0;
		wQGap[n] = 0;

		for ( int i = 0; i < 24; i++ ) {
			rV0QGap[n][i] = 0;
			wV0QGap[n][i] = 0;

			rQpGap[n][i] = 0;
			wQpGap[n][i] = 0;
		}
	}

    rQpos2 = 0;
    wQpos2 = 0;
    rQneg2 = 0;
    wQneg2 = 0;
    rQpos4 = 0;
    wQpos4 = 0;
    rQneg4 = 0;
    wQneg4 = 0;
    for ( int i = 0; i < 24; i++ ) {
        rVpQpos2[i] = 0.;
        wVpQpos2[i] = 0.;
        rVpQneg2[i] = 0.;
        wVpQneg2[i] = 0.;
        rVpQpos4[i] = 0.;
        wVpQpos4[i] = 0.;
        rVpQneg4[i] = 0.;
        wVpQneg4[i] = 0.;
    }

	for ( int i = 0; i < sz; i++ ) {
		if ( RFP[i] != 1 ) continue;
		for ( int n = 1; n < 7; n++ ) {
			q[n].fill((*hPhi)[i], (*hWeight)[i]);
		}
        if ( (*hEta)[i] > 0 ) {
			qpos.fill((*hPhi)[i], (*hWeight)[i]);
        } else {
			qneg.fill((*hPhi)[i], (*hWeight)[i]);
        }
	}

	correlations::Result r[7][4];
	for ( int n = 1; n < 7; n++ ) {
		for ( int np = 0; np < 4; np++ ) {
			r[n][np] = cq[n]->calculate(2+2*np, hc[n]);
		}
	}
	correlations::Result rpos2 = cqpos->calculate(2, hcsub);
	correlations::Result rneg2 = cqneg->calculate(2, hcsub);
	correlations::Result rpos4 = cqpos->calculate(4, hcsub);
	correlations::Result rneg4 = cqneg->calculate(4, hcsub);

	// RFP
	for ( int n = 2; n < 7; n++ ) {
		for ( int np = 0; np < 4; np++ ) {
			rQ[n][np] = r[n][np].sum().real();
			iQ[n][np] = r[n][np].sum().imag();
			wQ[n][np] = r[n][np].weight();
		}
	}
    rQpos2 = rpos2.sum().real();
    rQneg2 = rneg2.sum().real();
    wQpos2 = rpos2.weight();
    wQneg2 = rneg2.weight();
    rQpos4 = rpos4.sum().real();
    rQneg4 = rneg4.sum().real();
    wQpos4 = rpos4.weight();
    wQneg4 = rneg4.weight();

	// 2part RFP
	for ( int i = 0; i < sz; i++ ) {
		if ( RFP[i] != 1 ) continue;
		for ( int j = i+1; j < sz; j++ ) {
			if ( RFP[j] != 1 ) continue;
			if ( fabs( (*hEta)[i] - (*hEta)[j] ) < dEtaGap_ ) continue;
			for ( int n = 2; n < 7; n++ ) {
				rQGap[n] += cos( n*( (*hPhi)[i] - (*hPhi)[j] ) ) * (*hWeight)[i] * (*hWeight)[j];
				wQGap[n] += (*hWeight)[i] * (*hWeight)[j];
			}
		}
	}

	for ( int i = 0; i < sz; i++ ) {
		int ipt = 0;
		while ( (*hPt)[i] > ptBin_[ipt+1] ) ipt++;
		for ( int j = i+1; j < sz; j++ ) {
			if ( RFP[j] != 1 ) continue;
			if ( fabs( (*hEta)[i] - (*hEta)[j] ) < dEtaGap_ ) continue;
			for ( int n = 2; n < 7; n++ ) {
				rQpGap[n][ipt] += cos( n*( (*hPhi)[i] - (*hPhi)[j] ) ) * (*hWeight)[i] * (*hWeight)[j];
				wQpGap[n][ipt] += (*hWeight)[i] * (*hWeight)[j];
			}
		}
	}

	for ( int i = 0; i < sigsz; i++ ) {
		int ipt = 0;
		while ( (*sPt)[i] > ptBin_[ipt+1] ) ipt++;
		for ( int j = 0; j < sz; j++ ) {
			if ( RFP[j] != 1 ) continue;
			if ( (*sRef)[2*i] == (*hRef)[j] or (*sRef)[2*i+1] == (*hRef)[j] ) continue;
			if ( fabs( (*sEta)[i] - (*hEta)[j] ) < dEtaGap_ ) continue;

			for ( int n = 2; n < 7; n++ ) {
				rV0QGap[n][ipt] += cos( n*( (*sPhi)[i] - (*hPhi)[j] ) ) * (*sWeight)[i] * (*hWeight)[j];
				wV0QGap[n][ipt] += (*sWeight)[i] * (*hWeight)[j];
			}
		}
	}

	for ( int n = 1; n < 7; n++ ) {
		for ( int np = 0; np < 4; np++ ) {
			correlations::Complex qp = 0;
			double wt = 0;
			for ( int ipt = 0; ipt < Npt_; ipt++ ) {
				qp = 0;
				wt = 0;
				for ( int i = 0; i < sigsz; i++ ) {
					if ( (*sPt)[i] < ptBin_[ipt] or (*sPt)[i] > ptBin_[ipt+1] ) continue;
					correlations::QVector tq = q[n];
					for ( int j = 0; j < sz; j++ ) {
						if ( RFP[j] and ( (*sRef)[2*i] == (*hRef)[j] or (*sRef)[2*i+1] == (*hRef)[j] ) ) {
							tq.unfill( (*hPhi)[j], (*hWeight)[j] );
						}
					}
					correlations::FromQVector *cq = 0;
					switch ( cmode_ ) {
						case 1:
							cq = new correlations::closed::FromQVector(tq);
							break;
						case 2:
							cq = new correlations::recurrence::FromQVector(tq);
							break;
						case 3:
							cq = new correlations::recursive::FromQVector(tq);
							break;
					}
					correlations::Result r = cq->calculate(np*2+1, hc[n]);
					qp += (*sWeight)[i] * correlations::Complex( TMath::Cos((*sPhi)[i] * n) , TMath::Sin((*sPhi)[i] * n) ) * r.sum();
					wt += (*sWeight)[i] * r.weight();
					delete cq;
				}
				rVQp[n][np][ipt] = qp.real();
				iVQp[n][np][ipt] = qp.imag();
				wVQp[n][np][ipt] = wt;
			}
		}
	}
    // sub event v2{4}
    {
        correlations::Complex qp_pos2 = 0;
        correlations::Complex qp_neg2 = 0;
        correlations::Complex qp_pos4 = 0;
        correlations::Complex qp_neg4 = 0;
        double wt_pos2 = 0;
        double wt_neg2 = 0;
        double wt_pos4 = 0;
        double wt_neg4 = 0;
        correlations::Result rpos2 = cqpos->calculate(1, hcsub);
        correlations::Result rneg2 = cqneg->calculate(1, hcsub);
        correlations::Result rpos4 = cqpos->calculate(3, hcsub);
        correlations::Result rneg4 = cqneg->calculate(3, hcsub);

        for ( int ipt = 0; ipt < Npt_; ipt++ ) {
            qp_pos2 = 0;
            wt_pos2 = 0;
            qp_neg2 = 0;
            wt_neg2 = 0;
            qp_pos4 = 0;
            wt_pos4 = 0;
            qp_neg4 = 0;
            wt_neg4 = 0;
            for ( int i = 0; i < sigsz; i++ ) {
                if ( (*sPt)[i] < ptBin_[ipt] or (*sPt)[i] > ptBin_[ipt+1] ) continue;

                if ( (*sEta)[i] > 0 ) {
                    qp_pos2 += (*sWeight)[i] * correlations::Complex( TMath::Cos((*sPhi)[i] * 2) , TMath::Sin((*sPhi)[i] * 2) ) * rneg2.sum();
                    wt_pos2 += (*sWeight)[i] * rneg2.weight();
                    qp_pos4 += (*sWeight)[i] * correlations::Complex( TMath::Cos((*sPhi)[i] * 2) , TMath::Sin((*sPhi)[i] * 2) ) * rneg4.sum();
                    wt_pos4 += (*sWeight)[i] * rneg4.weight();
                } else {
                    qp_neg2 += (*sWeight)[i] * correlations::Complex( TMath::Cos((*sPhi)[i] * 2) , TMath::Sin((*sPhi)[i] * 2) ) * rpos2.sum();
                    wt_neg2 += (*sWeight)[i] * rpos2.weight();
                    qp_neg4 += (*sWeight)[i] * correlations::Complex( TMath::Cos((*sPhi)[i] * 2) , TMath::Sin((*sPhi)[i] * 2) ) * rpos4.sum();
                    wt_neg4 += (*sWeight)[i] * rpos4.weight();
                }
            }
            rVpQpos2[ipt] = qp_pos2.real();
            rVpQneg2[ipt] = qp_neg2.real();
            wVpQpos2[ipt] = wt_pos2;
            wVpQneg2[ipt] = wt_neg2;
            rVpQpos4[ipt] = qp_pos4.real();
            rVpQneg4[ipt] = qp_neg4.real();
            wVpQpos4[ipt] = wt_pos4;
            wVpQneg4[ipt] = wt_neg4;
        }
    }

	edm::Handle<int> ch;
	iEvent.getByLabel(centralityTag_,ch);
	gNoff = *ch;
	gMult = rfp_sz;
	gV0 = sigsz;
	Vz  = (*hVz)[0];

//	t->RunId = iEvent.id().run();
//	t->EventId = iEvent.id().event();
	trV->Fill();
	doneQ();

}


void
QWCumuDiff::initQ()
{
	hc[1] = correlations::HarmonicVector(8);
	hc[1][0] = -1;
	hc[1][1] =  1;
	hc[1][2] = -1;
	hc[1][3] =  1;
	hc[1][4] = -1;
	hc[1][5] =  1;
	hc[1][6] = -1;
	hc[1][7] =  1;

	hc[2] = correlations::HarmonicVector(8);
	hc[2][0] = -2;
	hc[2][1] =  2;
	hc[2][2] = -2;
	hc[2][3] =  2;
	hc[2][4] = -2;
	hc[2][5] =  2;
	hc[2][6] = -2;
	hc[2][7] =  2;

	hc[3] = correlations::HarmonicVector(8);
	hc[3][0] = -3;
	hc[3][1] =  3;
	hc[3][2] = -3;
	hc[3][3] =  3;
	hc[3][4] = -3;
	hc[3][5] =  3;
	hc[3][6] = -3;
	hc[3][7] =  3;

	hc[4] = correlations::HarmonicVector(8);
	hc[4][0] = -4;
	hc[4][1] =  4;
	hc[4][2] = -4;
	hc[4][3] =  4;
	hc[4][4] = -4;
	hc[4][5] =  4;
	hc[4][6] = -4;
	hc[4][7] =  4;

	hc[5] = correlations::HarmonicVector(8);
	hc[5][0] = -5;
	hc[5][1] =  5;
	hc[5][2] = -5;
	hc[5][3] =  5;
	hc[5][4] = -5;
	hc[5][5] =  5;
	hc[5][6] = -5;
	hc[5][7] =  5;

	hc[6] = correlations::HarmonicVector(8);
	hc[6][0] = -6;
	hc[6][1] =  6;
	hc[6][2] = -6;
	hc[6][3] =  6;
	hc[6][4] = -6;
	hc[6][5] =  6;
	hc[6][6] = -6;
	hc[6][7] =  6;



	q[1].resize(hc[1]);
	q[2].resize(hc[2]);
	q[3].resize(hc[3]);
	q[4].resize(hc[4]);
	q[5].resize(hc[5]);
	q[6].resize(hc[6]);

	hcsub = correlations::HarmonicVector(4);
	hcsub[0] = -2;
	hcsub[1] =  2;
	hcsub[2] = -2;
	hcsub[3] =  2;

	qpos.resize(hcsub);
	qneg.resize(hcsub);

	switch ( cmode_ ) {
		case 1:
			cq[1] = new correlations::closed::FromQVector(q[1]);
			cq[2] = new correlations::closed::FromQVector(q[2]);
			cq[3] = new correlations::closed::FromQVector(q[3]);
			cq[4] = new correlations::closed::FromQVector(q[4]);
			cq[5] = new correlations::closed::FromQVector(q[5]);
			cq[6] = new correlations::closed::FromQVector(q[6]);
			cqpos = new correlations::closed::FromQVector(qpos);
			cqneg = new correlations::closed::FromQVector(qneg);
			break;
		case 2:
			cq[1] = new correlations::recurrence::FromQVector(q[1]);
			cq[2] = new correlations::recurrence::FromQVector(q[2]);
			cq[3] = new correlations::recurrence::FromQVector(q[3]);
			cq[4] = new correlations::recurrence::FromQVector(q[4]);
			cq[5] = new correlations::recurrence::FromQVector(q[5]);
			cq[6] = new correlations::recurrence::FromQVector(q[6]);
			cqpos = new correlations::recurrence::FromQVector(qpos);
			cqneg = new correlations::recurrence::FromQVector(qneg);
			break;
		case 3:
			cq[1] = new correlations::recursive::FromQVector(q[1]);
			cq[2] = new correlations::recursive::FromQVector(q[2]);
			cq[3] = new correlations::recursive::FromQVector(q[3]);
			cq[4] = new correlations::recursive::FromQVector(q[4]);
			cq[5] = new correlations::recursive::FromQVector(q[5]);
			cq[6] = new correlations::recursive::FromQVector(q[6]);
			cqpos = new correlations::recursive::FromQVector(qpos);
			cqneg = new correlations::recursive::FromQVector(qneg);
			break;
	}
}

void
QWCumuDiff::doneQ()
{
	q[1].reset();
	q[2].reset();
	q[3].reset();
	q[4].reset();
	q[5].reset();
	q[6].reset();
    qpos.reset();
    qneg.reset();
}

// ------------ method called once each job just before starting event loop  ------------
	void 
QWCumuDiff::beginJob()
{
}

// ------------ method called once each job just after ending the event loop  ------------
	void 
QWCumuDiff::endJob() 
{
}

// ------------ method called when starting to processes a run  ------------
	void 
QWCumuDiff::beginRun(edm::Run const&, edm::EventSetup const&)
{
}

// ------------ method called when ending the processing of a run  ------------
	void 
QWCumuDiff::endRun(edm::Run const&, edm::EventSetup const&)
{
}

// ------------ method called when starting to processes a luminosity block  ------------
	void 
QWCumuDiff::beginLuminosityBlock(edm::LuminosityBlock const&, edm::EventSetup const&)
{
}

// ------------ method called when ending the processing of a luminosity block  ------------
	void 
QWCumuDiff::endLuminosityBlock(edm::LuminosityBlock const&, edm::EventSetup const&)
{
}

// ------------ method fills 'descriptions' with the allowed parameters for the module  ------------
void
QWCumuDiff::fillDescriptions(edm::ConfigurationDescriptions& descriptions) {
	//The following says we do not know what parameters are allowed so do no validation
	// Please change this to state exactly what you do use, even if it is no parameters
	edm::ParameterSetDescription desc;
	desc.setUnknown();
	descriptions.addDefault(desc);

	//Specify that only 'tracks' is allowed
	//To use, remove the default given above and uncomment below
	//ParameterSetDescription desc;
	//desc.addUntracked<edm::InputTag>("tracks","ctfWithMaterialTracks");
	//descriptions.addDefault(desc);
}

//////////////////////////////////////////


//define this as a plug-in
DEFINE_FWK_MODULE(QWCumuDiff);
