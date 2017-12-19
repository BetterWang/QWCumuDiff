#include "FWCore/Framework/interface/EDAnalyzer.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "FWCore/Utilities/interface/InputTag.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "FWCore/ServiceRegistry/interface/Service.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"
#include "TH3D.h"
#include "vector"
#include "iostream"

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
	std::vector<double> pTbins_;

	TH1D *	hN;
	TH3D *	h3D;
	std::vector<TH3D *> h3DPhi;

};

QWMassAnalyzer::QWMassAnalyzer(const edm::ParameterSet& pset) :
	srcMass_(pset.getUntrackedParameter<edm::InputTag>("srcMass")),
	srcPt_(pset.getUntrackedParameter<edm::InputTag>("srcPt")),
	srcEta_(pset.getUntrackedParameter<edm::InputTag>("srcEta")),
	srcPhi_(pset.getUntrackedParameter<edm::InputTag>("srcPhi")),
	pTbins_(pset.getUntrackedParameter<std::vector<double>>("pTbins", std::vector<double>{0.2, 0.4, 0.6, 0.8, 1.0, 1.4, 1.8, 2.2, 2.8, 3.6, 4.6, 6.0, 7.0, 8.5}))
{
	consumes< std::vector<double> >(srcMass_);
	consumes< std::vector<double> >(srcPt_);
	consumes< std::vector<double> >(srcEta_);
	consumes< std::vector<double> >(srcPhi_);

	int Nbins = pset.getUntrackedParameter<int>("Nbins");
	double start = pset.getUntrackedParameter<double>("start");
	double end = pset.getUntrackedParameter<double>("end");

	edm::Service<TFileService> fs;

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

	for ( unsigned int i = 0; i < pTbins_.size() - 1; i++ ) {
		TH3D * h3 = fs->make<TH3D>(Form("h3DPhi_%i", i), Form("pT %f - %f;Mass;phi;eta",pTbins_[i], pTbins_[i+1]), Nbins, start, end, 72, -3.14159265358979323846, 3.14159265358979323846, 50, -2.5, 2.5);
		h3DPhi.push_back(h3);
	}
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

		for ( unsigned int j = 0; j < pTbins_.size() - 1; j++ ) {
			if ( pt > pTbins_[j] and pt < pTbins_[j+1] ) {
				h3DPhi[j]->Fill(mass, phi, eta);
			}
		}
	}

	return;
}

DEFINE_FWK_MODULE(QWMassAnalyzer);
