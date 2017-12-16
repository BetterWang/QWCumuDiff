#include "FWCore/Framework/interface/EDAnalyzer.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "FWCore/Utilities/interface/InputTag.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "FWCore/ServiceRegistry/interface/Service.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"
#include "TH3D.h"
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
	edm::InputTag   srcPhi_;
	std::vector<TH1D *> vhmass_;
	std::vector<TH1D *> vhphi_;
	std::vector<TH1D *> vheta_;
	TH1D *	hN;
	TH3D *	h3D;

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
	srcEta_(pset.getUntrackedParameter<edm::InputTag>("srcEta")),
	srcPhi_(pset.getUntrackedParameter<edm::InputTag>("srcPhi"))
{
	consumes< std::vector<double> >(srcMass_);
	consumes< std::vector<double> >(srcPt_);
	consumes< std::vector<double> >(srcEta_);
	consumes< std::vector<double> >(srcPhi_);

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
		c.Etamin_ = pcut.getUntrackedParameter<double>("etaMin", -2.4);
		c.Etamax_ = pcut.getUntrackedParameter<double>("etaMax", 2.4);
		cuts_.push_back(c);

		TH1D * h = fs->make<TH1D>( Form("hMass_%i", idx), Form("pT (%f,%f), eta (%f,%f);mass;count", c.pTmin_, c.pTmax_, c.Etamin_, c.Etamax_), Nbins, start, end );
		vhmass_.push_back( h );
		h = fs->make<TH1D>( Form("hPhi_%i", idx), Form("pT (%f,%f), eta (%f,%f);mass;count", c.pTmin_, c.pTmax_, c.Etamin_, c.Etamax_), 100, -3.14159265358979323846, 3.14159265358979323846);
		vhphi_.push_back( h );
		h = fs->make<TH1D>( Form("hEta_%i", idx), Form("pT (%f,%f), eta (%f,%f);mass;count", c.pTmin_, c.pTmax_, c.Etamin_, c.Etamax_), 100, -2.5, 2.5);
		vheta_.push_back( h );
		idx++;
	}

	hN = fs->make<TH1D>("hN", "hN", 20, 0, 20);

	std::vector<double> veta = pset.getUntrackedParameter<std::vector<double>>("EtaBins", std::vector<double>{-2.5, -2.4, -2.3, -2.2, -2.1, -2.0,
			-1.9, -1.8, -1.7, -1.6, -1.5, -1.4, -1.3, -1.2, -1.1, -1.0,
			-0.9, -0.8, -0.7, -0.6, -0.5, -0.4, -0.3, -0.2, -0.1, 0.0,
			0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0,
			1.1, 1.2, 1.3, 1.4, 1.5, 1.6, 1.7, 1.8, 1.9, 2.0,
			2.1, 2.2, 2.3, 2.4, 2.5});
	std::vector<double> vpT  = pset.getUntrackedParameter<std::vector<double>>("PtBins", std::vector<double>{0.2, 0.4, 0.6, 0.8, 1.0, 1.4, 1.8, 2.2, 2.8, 3.6, 4.6,6.0, 7.0, 8.5});

	std::vector<double> vMass;
	{
		double dmass = (end - start)/Nbins;
		for ( int i = 0; i < Nbins; i++ ) {
			vMass.push_back(start + dmass*i);
		}
	}
	vMass.push_back(end);
	h3D = fs->make<TH3D>("h3D", "h3D;Mass;pT;eta", Nbins, vMass.data(), vpT.size()-1, vpT.data(), veta.size()-1, veta.data());
}

void
QWMassAnalyzer::analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup)
{
	using namespace edm;
	Handle< std::vector<double> > vmass;
	Handle< std::vector<double> > veta;
	Handle< std::vector<double> > vphi;
	Handle< std::vector<double> > vpt;

	iEvent.getByLabel(srcMass_, vmass);
	iEvent.getByLabel(srcPt_, vpt);
	iEvent.getByLabel(srcEta_, veta);
	iEvent.getByLabel(srcPhi_, vphi);

	int sz = (*vmass).size();

	hN->Fill(sz);
	for ( int i = 0; i < sz; i++ ) {
		double mass = (*vmass)[i];
		double pt = (*vpt)[i];
		double eta = (*veta)[i];
		double phi = (*vphi)[i];

		h3D->Fill(mass, pt, eta);

		int idx = 0;
		for ( auto const cut : cuts_ ) {
			if ( pt > cut.pTmin_ and pt < cut.pTmax_
				and eta > cut.Etamin_ and eta < cut.Etamax_ ) {
				vhmass_[idx]->Fill(mass);
				vheta_[idx]->Fill(eta);
				vhphi_[idx]->Fill(phi);
			}
			idx++;
		}
	}

	return;
}

DEFINE_FWK_MODULE(QWMassAnalyzer);
