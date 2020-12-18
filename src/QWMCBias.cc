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
class QWMCBias : public edm::EDProducer {
public:
	explicit QWMCBias(const edm::ParameterSet&);
	~QWMCBias();

private:
	virtual void produce(edm::Event&, const edm::EventSetup&) override;
	///
	edm::InputTag	srcCent_;
	edm::InputTag	srcPTrkPt_;
	edm::InputTag	srcNTrkPt_;

    const double weight_[6][19] = {
        // 0,    1,      2,      3,      4,      5,      6,      7,      8,      9,      10,     11,     12,     13,     14,     15,     16,     17,     18,
        // 0.5,  1.0,    1.5,    2,0,    2.5,    3.0,    3.5,    4.0,    4.5,    5.0,    5.5,    6.0,    6.5,    7.0,    7.5,    8.0,    8.5,    9.0,    9.5
        {1.0000, 1.0000, 1.0000, 1.0000, 1.0000, 1.0000, 1.0000, 1.0000, 1.0000, 1.0000, 1.0000, 1.0000, 1.0000, 1.0000, 1.0000, 1.0000, 1.0000, 1.0000, 1.0000},
        {0.9658, 1.0057, 1.0428, 1.0777, 1.0802, 1.0514, 0.9931, 0.9314, 0.8697, 0.8159, 0.8065, 0.7988, 0.8142, 0.8290, 0.8483, 0.8814, 0.8929, 0.8816, 0.8648},
        {0.9695, 1.0149, 1.0584, 1.0988, 1.1246, 1.1206, 1.0949, 1.0476, 1.0100, 0.9710, 0.9534, 0.9449, 0.9482, 0.9465, 0.9138, 0.9348, 0.9517, 0.9474, 0.9699},
        {0.9787, 1.0022, 1.0433, 1.1108, 1.1745, 1.2290, 1.2653, 1.2750, 1.2787, 1.2280, 1.2169, 1.2077, 1.1627, 1.1828, 1.1864, 1.1489, 1.1901, 1.1716, 1.1537},
        {0.9413, 0.9138, 0.9430, 1.0363, 1.1660, 1.3263, 1.4736, 1.5947, 1.6706, 1.7054, 1.6785, 1.6370, 1.5694, 1.6527, 1.6110, 1.4441, 1.5905, 1.3949, 1.5082},
        {1.0000, 1.0000, 1.0000, 1.0000, 1.0000, 1.0000, 1.0000, 1.0000, 1.0000, 1.0000, 1.0000, 1.0000, 1.0000, 1.0000, 1.0000, 1.0000, 1.0000, 1.0000, 1.0000}
    };

    double getWeight( int c, double pt ) {
        if ( (pt <= 0.5) or (pt >= 10.) ) {
            return 1.;
        }
        int ipt = int(2*(pt - 0.5));
        return weight_[c][ipt];
    };
};

QWMCBias::QWMCBias(const edm::ParameterSet& pset) :
	srcCent_(pset.getUntrackedParameter<edm::InputTag>("srcCentrality")),
	srcPTrkPt_(pset.getUntrackedParameter<edm::InputTag>("pTrkPt")),
	srcNTrkPt_(pset.getUntrackedParameter<edm::InputTag>("nTrkPt"))
{
	consumes<double>(srcCent_);
	consumes<vector<double>>(srcPTrkPt_);
	consumes<vector<double>>(srcNTrkPt_);

	produces<vector<double>>("weight");
}

QWMCBias::~QWMCBias()
{
	return;
}

void QWMCBias::produce(edm::Event& iEvent, const edm::EventSetup& iSetup)
{
	using namespace edm;
	Handle<double> pC;
	iEvent.getByLabel(srcCent_, pC);

    int c = 0;
    if ( (*pC>=10) and (*pC<20) ) {
        c = 1;
    } else if ( (*pC>=20) and (*pC<60) ) {
        c = 2;
    } else if ( (*pC>=60) and (*pC<100) ) {
        c = 3;
    } else if ( (*pC>=100) and (*pC<160) ) {
        c = 4;
    } else if ( (*pC>=160) and (*pC<200) ) {
        c = 5;
    }

	Handle<vector<double>> ppPt;
	Handle<vector<double>> pnPt;
	iEvent.getByLabel(srcPTrkPt_, ppPt);
	iEvent.getByLabel(srcNTrkPt_, pnPt);

    unique_ptr<vector<double>> pWeight(new vector<double>());

    int N = ppPt->size();
    for ( int i = 0; i < N; i++ ) {
        double weight = getWeight( c, (*ppPt)[i] );
        weight *= getWeight( c, (*pnPt)[i] );
        pWeight->push_back(weight);
    }

	iEvent.put(move(pWeight), "weight");
}


DEFINE_FWK_MODULE(QWMCBias);
