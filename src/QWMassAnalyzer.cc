#include "FWCore/Framework/interface/EDAnalyzer.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "FWCore/Utilities/interface/InputTag.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "FWCore/ServiceRegistry/interface/Service.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"
#include "TH1D.h"
#include <iostream>

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
	std::vector<double>	ptBin_;
	std::vector<TH1D*> h;
	std::vector<TH1D*> hc;
};

QWMassAnalyzer::QWMassAnalyzer(const edm::ParameterSet& pset) :
	srcMass_(pset.getUntrackedParameter<edm::InputTag>("srcMass")),
	srcPt_(pset.getUntrackedParameter<edm::InputTag>("srcPt"))
{
	consumes<std::vector<double> >(srcMass_);
	consumes<std::vector<double> >(srcPt_);

	ptBin_ = pset.getUntrackedParameter<std::vector<double> >("ptBin");

	int hNbins = pset.getUntrackedParameter<int>("hNbins");
	double hstart = pset.getUntrackedParameter<double>("hstart");
	double hend = pset.getUntrackedParameter<double>("hend");

	int cNbins = pset.getUntrackedParameter<int>("cNbins");
	double cstart = pset.getUntrackedParameter<double>("cstart");
	double cend = pset.getUntrackedParameter<double>("cend");

	edm::Service<TFileService> fs;
	for ( int i = 0; i < ptBin_.size() - 1; i++ ) {
		h.push_back(fs->make<TH1D>(Form("h%i", i), Form("%f-%f", ptBin_[i], ptBin_[i+1], hNbins, hstart, hend));
		h[i]->Sumw2();
		hc.push_back(fs->make<TH1D>(Form("hc%i", i), Form("%f-%f", ptBin_[i], ptBin_[i+1], cNbins, cstart, cend));
		hc[i]->Sumw2();
	}
	h = fs->make<TH1D>("h", "h", hNbins, hstart, hend);
	h->Sumw2();
	hc = fs->make<TH1D>("hc", "hc", cNbins, cstart, cend);
	hc->Sumw2();
}

void
QWMassAnalyzer::analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup)
{
	using namespace edm;
	Handle<std::vector<double> > mass;
	Handle<std::vector<double> > pt;

	iEvent.getByLabel(srcMass_, mass);
	iEvent.getByLabel(srcPt_, pt);

	int cnt = 0;
	int sz = mass->size();
	for ( int i = 0; i < sz; i++ ) {
		if ( (*pt)[i] > ptMin_ and (*pt)[i] < ptMax_ ) {
			cnt++;
			hc->Fill((*mass)[i]);
		}
	}
	h->Fill(cnt);
	return;
}

DEFINE_FWK_MODULE(QWMassAnalyzer);
