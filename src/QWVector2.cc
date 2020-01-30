#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/EDProducer.h"

#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"

#include "FWCore/Utilities/interface/InputTag.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"

class QWVector2 : public edm::EDProducer {
public:
	explicit QWVector2(const edm::ParameterSet&);
	~QWVector2();

private:
	virtual void produce(edm::Event&, const edm::EventSetup&) override;
	edm::InputTag	src_;
};

QWVector2::QWVector2(const edm::ParameterSet& pset) :
	src_(pset.getUntrackedParameter<edm::InputTag>("src"))
{
	consumes<std::vector<double>>(src_);
	produces<std::vector<double>>();
}

QWVector2::~QWVector2() {
	return;
}

void QWVector2::produce(edm::Event& iEvent, const edm::EventSetup& iSetup)
{
    edm::Handle<std::vector<double> > vect;
	iEvent.getByLabel(src_, vect);
    std::unique_ptr<std::vector<double> > pvect( new std::vector<double> );

    for ( unsigned int i = 0; i < vect->size(); i++ ) {
        pvect->push_back( (*vect)[i] );
        pvect->push_back( (*vect)[i] );
    }
	iEvent.put(std::move(pvect));
}

DEFINE_FWK_MODULE(QWVector2);
