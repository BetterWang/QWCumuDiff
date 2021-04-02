#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/EDFilter.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "DataFormats/PatCandidates/interface/Jet.h"
#include "iostream"
#include "TRandom3.h"

class QWJetPtFilter : public edm::EDFilter {
public:
	explicit QWJetPtFilter(const edm::ParameterSet&);
	~QWJetPtFilter() {return;}
private:
	virtual bool filter(edm::Event&, const edm::EventSetup&);

	edm::InputTag	src_;
    edm::EDGetTokenT<reco::JetView>     jetTag_;
	double      min_;
	double      max_;
	double      Etamin_;
	double      Etamax_;
	double      JER_;
    bool        bJER_;
    TRandom3*   rnd_;
};

QWJetPtFilter::QWJetPtFilter(const edm::ParameterSet& pset) :
	src_(pset.getUntrackedParameter<edm::InputTag>("src")),
	min_(pset.getUntrackedParameter<double>("dmin", std::numeric_limits<double>::min())),
	max_(pset.getUntrackedParameter<double>("dmax", std::numeric_limits<double>::max())),
	Etamin_(pset.getUntrackedParameter<double>("Etamin", -std::numeric_limits<double>::max())),
	Etamax_(pset.getUntrackedParameter<double>("Etamax", std::numeric_limits<double>::max())),
	JER_(pset.getUntrackedParameter<double>("JER", 0.)),
    rnd_(nullptr)
{
    jetTag_ = consumes<reco::JetView> (src_);
    if ( JER_ > 0. ) {
        bJER_ = true;
        rnd_ = new TRandom3();
    } else {
        bJER_ = false;
    }

	return;
}

bool QWJetPtFilter::filter(edm::Event& iEvent, const edm::EventSetup& iSetup)
{
    edm::Handle<reco::JetView> jets;
    iEvent.getByToken(jetTag_, jets);

    for(unsigned int j = 0; j < jets->size(); ++j){
        const reco::Jet& jet = (*jets)[j];
        double jtpt = jet.pt();
        if ( bJER_ ) {
            double sigma = jtpt * JER_;
            jtpt = rnd_->Gaus(jtpt, sigma);
        }
        double jteta = jet.eta();
        if ( (jteta>Etamin_) and (jteta<Etamax_) ) {
            if ( (jtpt < min_) or (jtpt > max_) ) {
                //std::cout << " --> jet " << j << " eta = " << jteta << " pt = " << jtpt << std::endl;
                return false;
            }
        }
    }
    return true;
}

DEFINE_FWK_MODULE(QWJetPtFilter);
