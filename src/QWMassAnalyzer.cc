#include "FWCore/Framework/interface/EDAnalyzer.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "FWCore/Utilities/interface/InputTag.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "FWCore/ServiceRegistry/interface/Service.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"
#include "TH1D.h"
#include "vector"

class QWMassAnalyzer : public edm::EDAnalyzer {
public:
	explicit QWMassAnalyzer(const edm::ParameterSet&);
	~QWMassAnalyzer() {};
private:
	virtual void beginJob() {};
	virtual void analyze(const edm::Event&, const edm::EventSetup&);
	virtual void endJob() {};

	edm::InputTag   srcMass_;
	edm::InputTag   srcPt_;
	edm::InputTag   srcEta_;
	std::vector<TH1D *> vh_;

	typedef struct {
		double pTmin_;
		double pTmax_;
		double Etamin_;
		double Etamax_;
	} cut;

	std::vector< QWMassAnalyzer::cut > cuts_;
};

QWMassAnalyzer::QWMassAnalyzer(const edm::ParameterSet& pset) :
	srcMass_(pset.getUntrackedParameter<edm::InputTag>("srcMass")),
	srcPt_(pset.getUntrackedParameter<edm::InputTag>("srcPt")),
	srcEta_(pset.getUntrackedParameter<edm::InputTag>("srcEta"))
{
	consumes< std::vector<double> >(srcMass_);
	consumes< std::vector<double> >(srcPt_);
	consumes< std::vector<double> >(srcEta_);

	int Nbins = pset.getUntrackedParameter<int>("Nbins");
	double start = pset.getUntrackedParameter<double>("start");
	double end = pset.getUntrackedParameter<double>("end");

	edm::Service<TFileService> fs;

	auto pcuts = pset.getUntrackedParameter< std::vector< edm::ParameterSet > >("cuts");
	int idx = 0;
	for ( auto pcut : pcuts ) {
		QWMassAnalyzer::cut c;
		c.pTmin_ = pcut.getUntrackedParameter<double>("ptMin", 0.);
		c.pTmax_ = pcut.getUntrackedParameter<double>("ptMax", 100.);
		c.Etamin_ = pcut.getUntrackedParameter<double>("etaMin", -1.0);
		c.Etamax_ = pcut.getUntrackedParameter<double>("etaMax", 1.0);
		cuts_.push_back(c);

		TH1D * h = fs->make<TH1D>( Form("hMass_%i", idx), Form("pT (%f,%f), eta (%f,%f);mass;count", c.pTmin_, c.pTmax_, c.Etamin_, c.Etamax_), Nbins, start, end );
		h->Sumw2();
		vh_.push_back( h );
		idx++;
	}
}

void
QWMassAnalyzer::analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup)
{
	using namespace edm;
	Handle< std::vector<double> > vmass;
	Handle< std::vector<double> > veta;
	Handle< std::vector<double> > vpt;

	iEvent.getByLabel(srcMass_, vmass);
	iEvent.getByLabel(srcPt_, vpt);
	iEvent.getByLabel(srcEta_, veta);

	int sz = (*vmass).size();

	for ( int i = 0; i < sz; i++ ) {
		double mass = (*vmass)[i];
		double pt = (*vpt)[i];
		double eta = (*veta)[i];

		int idx = 0;
		for ( auto const cut : cuts_ ) {
			if ( pt > cut.pTmin_ and pt < cut.pTmax_
				and eta > cut.Etamin_ and eta < cut.Etamax_ ) {
				vh_[idx]->Fill(mass);
			}
			idx++;
		}
	}

	return;
}

DEFINE_FWK_MODULE(QWMassAnalyzer);
