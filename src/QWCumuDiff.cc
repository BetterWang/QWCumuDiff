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
	trackEta_( iConfig.getUntrackedParameter<edm::InputTag>("trackEta") ),
	trackPhi_( iConfig.getUntrackedParameter<edm::InputTag>("trackPhi") ),
	trackPt_( iConfig.getUntrackedParameter<edm::InputTag>("trackPt") ),
	trackWeight_( iConfig.getUntrackedParameter<edm::InputTag>("trackWeight") ),
	trackCharge_( iConfig.getUntrackedParameter<edm::InputTag>("trackCharge") ),
	trackRef_( iConfig.getUntrackedParameter<edm::InputTag>("trackRef") ),
	vertexZ_( iConfig.getUntrackedParameter<edm::InputTag>("vertexZ") ),
	sigEta_( iConfig.getUntrackedParameter<edm::InputTag>("sigEta") ),
	sigPhi_( iConfig.getUntrackedParameter<edm::InputTag>("sigPhi") ),
	sigPt_( iConfig.getUntrackedParameter<edm::InputTag>("sigPt") ),
	sigWeight_( iConfig.getUntrackedParameter<edm::InputTag>("sigWeight") ),
	sigTrackRef1_( iConfig.getUntrackedParameter<edm::InputTag>("sigTrackRef1") ),
	sigTrackRef2_( iConfig.getUntrackedParameter<edm::InputTag>("sigTrackRef2") ),
	centralityTag_( iConfig.getUntrackedParameter<edm::InputTag>("centrality") )
{
	//now do what ever initialization is needed
	minvz_ = iConfig.getUntrackedParameter<double>("minvz", -15.);
	maxvz_ = iConfig.getUntrackedParameter<double>("maxvz", 15.);

	rfpmineta_ = iConfig.getUntrackedParameter<double>("rfpmineta", -2.4);
	rfpmaxeta_ = iConfig.getUntrackedParameter<double>("rfpmaxeta", 2.4);
	rfpminpt_ = iConfig.getUntrackedParameter<double>("rfpminpt", 0.3);
	rfpmaxpt_ = iConfig.getUntrackedParameter<double>("rfpmaxpt", 100);

	poimineta_ = iConfig.getUntrackedParameter<double>("poimineta", -2.4);
	poimaxeta_ = iConfig.getUntrackedParameter<double>("poimaxeta", 2.4);
	poiminpt_ = iConfig.getUntrackedParameter<double>("poiminpt", 0.3);
	poimaxpt_ = iConfig.getUntrackedParameter<double>("poimaxpt", 3.0);

	b2PartGap_ = iConfig.getUntrackedParameter<bool>("b2PartGap", true);
	dEtaGap_ = iConfig.getUntrackedParameter<double>("etaGap", 2.);

	cmode_ = iConfig.getUntrackedParameter<int>("cmode", 1);
	nvtx_ = iConfig.getUntrackedParameter<int>("nvtx", 100);

	ptBin_ = iConfig.getUntrackedParameter< std::vector<double> >("ptBin");
	etaBin_ = iConfig.getUntrackedParameter< std::vector<double> >("etaBin");
	Npt_ = ptBin_.size();
	Neta_ = etaBin_.size();

        consumes<int>(centralityTag_);
        consumes<std::vector<double> >(trackEta_);
        consumes<std::vector<double> >(trackPhi_);
        consumes<std::vector<double> >(trackPt_);
        consumes<std::vector<double> >(trackWeight_);
        consumes<std::vector<double> >(trackCharge_);
        consumes<std::vector<double> >(trackRef_);
        consumes<std::vector<double> >(vertexZ_);

        consumes<std::vector<double> >(sigEta_);
        consumes<std::vector<double> >(sigPhi_);
        consumes<std::vector<double> >(sigPt_);
        consumes<std::vector<double> >(sigWeight_);
        consumes<std::vector<double> >(sigTrackRef1_);
        consumes<std::vector<double> >(sigTrackRef2_);

	for ( int n = 1; n < 7; n++ ) {
		q[n] = correlations::QVector(0, 0, true);
	}

	edm::Service<TFileService> fs;

	trV = fs->make<TTree>("trV", "trV");
	trV->Branch("Noff", &gNoff, "Noff/I");
	trV->Branch("Mult", &gMult, "Mult/I");

	trV->Branch("wQGap22", &wQGap[2], "wQGap22/D");
	trV->Branch("wQpGap22", wQpGap[2], "wQpGap22[24]/D");
	trV->Branch("wQetaGap22", wQetaGap[2], "wQetaGap22[24]/D");


	for ( int n = 2; n < 7; n++ ) {
		trV->Branch(Form("rQGap%i%i", n, 2), &rQGap[n], Form("rQGap%i%i/D", n, 2));
		trV->Branch(Form("rQpGap%i%i", n, 2), rQpGap[n], Form("rQpGap%i%i[24]/D", n, 2));
		trV->Branch(Form("rQetaGap%i%i", n, 2), rQetaGap[n], Form("rQetaGap%i%i[24]/D", n, 2));
	}

	for ( int np = 0; np < 4; np++ ) {
		for ( int n = 2; n < 7; n++ ) {
			trV->Branch(Form("rQ%i%i", n, 2+2*np), &rQ[n][np], Form("rQ%i%i/D", n, 2+2*np));
			trV->Branch(Form("rQ%i%ip", n, 2+2*np), rQp[n][np], Form("rQ%i%ip[24]/D", n, 2+2*np));
			trV->Branch(Form("rQ%i%ieta", n, 2+2*np), rQeta[n][np], Form("rQ%i%ieta[24]/D", n, 2+2*np));
		}

		int n = 2;
		trV->Branch(Form("wQ%i%i", n, 2+2*np), &wQ[n][np], Form("wQ%i%i/D", n, 2+2*np));
		trV->Branch(Form("wQ%i%ip", n, 2+2*np), wQp[n][np], Form("wQ%i%ip[24]/D", n, 2+2*np));
		trV->Branch(Form("wQ%i%ieta", n, 2+2*np), wQeta[n][np], Form("wQ%i%ieta[24]/D", n, 2+2*np));
	}

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
//	analyzeData(iEvent, iSetup);

	Handle<std::vector<double> >	hEta;
	Handle<std::vector<double> >	hPhi;
	Handle<std::vector<double> >	hPt;
	Handle<std::vector<double> >	hWeight;
	Handle<std::vector<double> >	hCharge;
	Handle<std::vector<double> >	hRef;
	Handle<std::vector<double> >	hVz;

	Handle<std::vector<double> >	sEta;
	Handle<std::vector<double> >	sPhi;
	Handle<std::vector<double> >	sPt;
	Handle<std::vector<double> >	sWeight;
	Handle<std::vector<double> >	sRef1;
	Handle<std::vector<double> >	sRef2;

	iEvent.getByLabel(trackEta_,	hEta);
	iEvent.getByLabel(trackPhi_,	hPhi);
	iEvent.getByLabel(trackPt_,	hPt);
	iEvent.getByLabel(trackWeight_, hWeight);
	iEvent.getByLabel(trackRef_,	hRef);

	iEvent.getByLabel(trackCharge_, hCharge);
	iEvent.getByLabel(vertexZ_, 	hVz);

	iEvent.getByLabel(sigEta_,	sEta);
	iEvent.getByLabel(sigPhi_,	sPhi);
	iEvent.getByLabel(sigPt_,	sPt);
	iEvent.getByLabel(sigWeight_, 	sWeight);

	if ( hVz->size() < 1 ) return;
	if ( (*hVz)[0] > maxvz_ or (*hVz)[0] < minvz_ ) return;
	int sz = int(hEta->size());
	if ( sz == 0 ) return;
	int sigsz = int(sEta->size());
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
		rQGap[n] = 0;
		wQGap[n] = 0;

		for ( int np = 0; np < 4; np++ ) {
			rQ[n][np] = 0;
			iQ[n][np] = 0;
			wQ[n][np] = 0;

			for ( int j = 0; j < 24; j++ ) {
				rQp[n][np][j] = 0;
				iQp[n][np][j] = 0;
				wQp[n][np][j] = 0;

				rQeta[n][np][j] = 0;
				iQeta[n][np][j] = 0;
				wQeta[n][np][j] = 0;
			}
		}
		for ( int j = 0; j < 24; j++ ) {
			rQpGap[n][j] = 0;
			wQpGap[n][j] = 0;
			rQetaGap[n][j] = 0;
			wQetaGap[n][j] = 0;
		}
	}

	for ( int i = 0; i < sz; i++ ) {
		if ( RFP[i] != 1 ) continue;
		for ( int n = 1; n < 7; n++ ) {
			q[n].fill((*hPhi)[i], (*hWeight)[i]);
		}
	}
	if ( b2PartGap_ ) {
		for ( int i = 0; i < sz; i++ ) {
			if ( RFP[i] != 1 ) continue;
			for ( int n = 1; n < 7; n++ ) {
				// ref 2part gap
				for ( int j = i+1; j < sz; j++ ) {
					if ( RFP[j] != 1 ) continue;
					if ( fabs((*hEta)[i] - (*hEta)[j]) < dEtaGap_ ) continue;
					rQGap[n] += cos( n*( (*hPhi)[j] - (*hPhi)[i] ) ) * (*hWeight)[i] * (*hWeight)[j];
					wQGap[n] += (*hWeight)[i] * (*hWeight)[j];
				}
			}
		}
		for ( int i = 0; i < sz; i++ ) {
			if ( RFP[i] != 1 ) continue;
			for ( int n = 1; n < 7; n++ ) {
				for ( int j = 0; j < sigsz; j++ ) {
					// pT differential
					if ( (*hRef)[i] == (*sRef1)[j] or (*hRef)[i] == (*sRef2)[j] ) continue;
					if ( (*sEta)[j] > poimaxeta_ or (*sEta)[j] < poimineta_ ) continue;
					int ipt = -1;
					while ( (*sPt)[j] > ptBin_[ipt+1] ) ipt++;
					if ( ipt >= 24 or ipt < 0 ) continue;
					rQpGap[n][ipt] += cos( n*( (*hPhi)[i] - (*sPhi)[j] ) ) * (*hWeight)[i] * (*sWeight)[j];
					wQpGap[n][ipt] += (*hWeight)[i] * (*sWeight)[j];
				}
				for ( int j = 0; j < sigsz; j++ ) {
					// eta diff
					if ( (*hRef)[i] == (*sRef1)[j] or (*hRef)[i] == (*sRef2)[j] ) continue;
					if ( (*sPt)[j] > poimaxpt_ or (*sPt)[j] < poiminpt_ ) continue;
					int ieta = -1;
					while ( (*sEta)[j] > etaBin_[ieta+1] ) ieta++;
					if ( ieta >= 24 or ieta < 0 ) continue;
					rQetaGap[n][ieta] += cos( n*( (*hPhi)[i] - (*sPhi)[j] ) ) * (*hWeight)[i] * (*sWeight)[j];
					wQetaGap[n][ieta] += (*hWeight)[i] * (*sWeight)[j];
				}
			}
		}
	}

	correlations::Result r[7][4];
	for ( int n = 1; n < 7; n++ ) {
		for ( int np = 0; np < 4; np++ ) {
			r[n][np] = cq[n]->calculate(2+2*np, hc[n]);
		}
	}

	// RFP
	for ( int n = 1; n < 7; n++ ) {
		for ( int np = 0; np < 4; np++ ) {
			rQ[n][np] = r[n][np].sum().real();
			iQ[n][np] = r[n][np].sum().imag();
			wQ[n][np] = r[n][np].weight();
		}
	}

	for ( int n = 1; n < 7; n++ ) {
		for ( int np = 0; np < 4; np++ ) {
			correlations::Complex qp = 0;
			double wt = 0;
			// pt differential
			for ( int ipt = 0; ipt < Npt_; ipt++ ) {
				qp = 0;
				wt = 0;
				for ( int i = 0; i < sigsz; i++ ) {
					if ( (*sEta)[i] < poimineta_ or (*sEta)[i] > poimaxeta_ ) continue;
					//if ( (*sPt)[i] < poiminpt_ or (*sPt)[i] > poimaxpt_ ) continue;
					if ( (*sPt)[i] < ptBin_[ipt] or (*sPt)[i] > ptBin_[ipt+1] ) continue;
					correlations::QVector tq = q[n];
					for ( int j = 0; j < sz; j++ ) {
						if ( RFP[j] and ( (*sRef1)[i] == (*hRef)[j] or (*sRef2)[i] == (*hRef)[j] ) ) {
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
				rQp[n][np][ipt] = qp.real();
				iQp[n][np][ipt] = qp.imag();
				wQp[n][np][ipt] = wt;
			}
			// eta differential
			for ( int ieta = 0; ieta < Neta_; ieta++ ) {
				qp = 0;
				wt = 0;
				for ( int i = 0; i < sigsz; i++ ) {
					if ( (*sPt)[i] < poiminpt_ or (*sPt)[i] > poimaxpt_ ) continue;
					if ( (*sEta)[i] < etaBin_[ieta] || (*sEta)[i] > etaBin_[ieta+1] ) continue;
					correlations::QVector tq = q[n];
					for ( int j = 0; j < sz; j++ ) {
						if ( RFP[j] and ( (*sRef1)[i] == (*hRef)[j] or (*sRef2)[i] == (*hRef)[j] ) ) {
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
				rQeta[n][np][ieta] = qp.real();
				iQeta[n][np][ieta] = qp.imag();
				wQeta[n][np][ieta] = wt;
			}
		}
	}

	edm::Handle<int> ch;
	iEvent.getByLabel(centralityTag_,ch);
	gNoff = *ch;
	gMult = rfp_sz;

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
	switch ( cmode_ ) {
		case 1:
			cq[1] = new correlations::closed::FromQVector(q[1]);
			cq[2] = new correlations::closed::FromQVector(q[2]);
			cq[3] = new correlations::closed::FromQVector(q[3]);
			cq[4] = new correlations::closed::FromQVector(q[4]);
			cq[5] = new correlations::closed::FromQVector(q[5]);
			cq[6] = new correlations::closed::FromQVector(q[6]);
			break;
		case 2:
			cq[1] = new correlations::recurrence::FromQVector(q[1]);
			cq[2] = new correlations::recurrence::FromQVector(q[2]);
			cq[3] = new correlations::recurrence::FromQVector(q[3]);
			cq[4] = new correlations::recurrence::FromQVector(q[4]);
			cq[5] = new correlations::recurrence::FromQVector(q[5]);
			cq[6] = new correlations::recurrence::FromQVector(q[6]);
			break;
		case 3:
			cq[1] = new correlations::recursive::FromQVector(q[1]);
			cq[2] = new correlations::recursive::FromQVector(q[2]);
			cq[3] = new correlations::recursive::FromQVector(q[3]);
			cq[4] = new correlations::recursive::FromQVector(q[4]);
			cq[5] = new correlations::recursive::FromQVector(q[5]);
			cq[6] = new correlations::recursive::FromQVector(q[6]);
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
