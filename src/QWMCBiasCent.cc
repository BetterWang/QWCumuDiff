#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/EDProducer.h"

#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"

#include "FWCore/Utilities/interface/InputTag.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"

#include "SimDataFormats/HiGenData/interface/GenHIEvent.h"

#include "TFile.h"
#include "TH2.h"
#include "TMath.h"

// Data vs Hydjet Drum5F difference

using namespace std;
class QWMCBiasCent : public edm::EDProducer {
public:
	explicit QWMCBiasCent(const edm::ParameterSet&);
	~QWMCBiasCent();

private:
	virtual void produce(edm::Event&, const edm::EventSetup&) override;
	///
	edm::InputTag	srcCent_;

};

QWMCBiasCent::QWMCBiasCent(const edm::ParameterSet& pset) :
	srcCent_(pset.getUntrackedParameter<edm::InputTag>("srcCentrality"))
{
	consumes<double>(srcCent_);
	produces<double>("Centrality");
}

QWMCBiasCent::~QWMCBiasCent()
{
	return;
}

void QWMCBiasCent::produce(edm::Event& iEvent, const edm::EventSetup& iSetup)
{
	using namespace edm;
	Handle<double> pC;
	iEvent.getByLabel(srcCent_, pC);

    double ret = *pC;
    if ( ret < 60. ) {
        ret += 10.;
    } else if ( ret < 100. ) {
        ret += 9.;
    } else if ( ret < 160. ) {
        ret += 8.;
    }

	iEvent.put(make_unique<double>(ret), "Centrality");
}


DEFINE_FWK_MODULE(QWMCBiasCent);
