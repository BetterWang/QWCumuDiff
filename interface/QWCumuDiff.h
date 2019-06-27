#include <correlations/Types.hh>
#include <correlations/Result.hh>
#include <correlations/QVector.hh>
#include <correlations/recursive/FromQVector.hh>
#include <correlations/recurrence/FromQVector.hh>
#include <correlations/closed/FromQVector.hh>
#include <TComplex.h>
#include <TH1.h>
#include <TH2.h>
#include <TTree.h>
#include <TNtupleD.h>
#include <TRandom3.h>
#include <TFile.h>
//#include "QWConstV3.h"
#include <RecoHI/HiEvtPlaneAlgos/interface/HiEvtPlaneList.h>
#include "DataFormats/TrackReco/interface/Track.h"
#include "DataFormats/TrackReco/interface/TrackFwd.h"
#include "DataFormats/VertexReco/interface/Vertex.h"
#include "DataFormats/VertexReco/interface/VertexFwd.h"
//
// constants, enums and typedefs
//

//#define QW_DEBUG 1
//#define QW_PEREVENT 1

#define PRD(x) cout << "!!QW!! " << __LINE__ << " DEBUG OUTPUT " << (#x) << " = " << (x) << endl;
#define PR(x) cout << "!!QW!! " << __LINE__ << " DEBUG OUTPUT " << (#x) << endl;
//
// class declaration
//

///////////////// Class ////////////////////////////

class QWCumuDiff : public edm::EDAnalyzer {
	public:
		explicit QWCumuDiff(const edm::ParameterSet&);
		~QWCumuDiff();

		static void fillDescriptions(edm::ConfigurationDescriptions& descriptions);

	private:
		virtual void beginJob() ;
		virtual void analyze(const edm::Event&, const edm::EventSetup&);
		virtual void endJob() ;

		virtual void beginRun(edm::Run const&, edm::EventSetup const&);
		virtual void endRun(edm::Run const&, edm::EventSetup const&);
		virtual void beginLuminosityBlock(edm::LuminosityBlock const&, edm::EventSetup const&);
		virtual void endLuminosityBlock(edm::LuminosityBlock const&, edm::EventSetup const&);

	/////////////////////////////////////////////
		//TRandom3 * gRandom;
		// ----------member data ---------------------------

		edm::InputTag					trackEta_;
		edm::InputTag					trackPhi_;
		edm::InputTag					trackRef_;
		edm::InputTag					trackPt_;
		edm::InputTag					trackWeight_;
		edm::InputTag					vertexZ_;

		edm::InputTag					sigEta_;
		edm::InputTag					sigPhi_;
		edm::InputTag					sigPt_;
		edm::InputTag					sigRef_;
		edm::InputTag					sigWeight_;


		edm::InputTag					centralityTag_;

		double	minvz_, maxvz_;
		std::vector<double>		ptBin_;
		int				Npt_;
	/////////////////////////////////////////////
		double	rfpmineta_, rfpmaxeta_;
//		double	poimineta_, poimaxeta_;
		double	rfpminpt_, rfpmaxpt_;
//		double	poiminpt_, poimaxpt_;
		double	dEtaGap_;

		int	cmode_;
	/////////////////////////////////////////////
		TTree * trV;

		int gNoff;
		int gMult;
		int gV0;

		double rQ[7][4];
		double iQ[7][4];
		double wQ[7][4];

		double rQGap[7];
		double iQGap[7];
		double wQGap[7];

		double rQpGap[7][24];
		double wQpGap[7][24];

		double rV0QGap[7][24];
		double wV0QGap[7][24];

		double rVQp[7][4][24];
		double iVQp[7][4][24];
		double wVQp[7][4][24];

		correlations::HarmonicVector    hc[7];
		correlations::QVector           q[7];
		correlations::FromQVector       *cq[7];

        double rQpos2;
        double wQpos2;
        double rVpQpos2[24];
        double wVpQpos2[24];
        double rQpos4;
        double wQpos4;
        double rVpQpos4[24];
        double wVpQpos4[24];

        double rQneg2;
        double wQneg2;
        double rVpQneg2[24];
        double wVpQneg2[24];
        double rQneg4;
        double wQneg4;
        double rVpQneg4[24];
        double wVpQneg4[24];

		correlations::HarmonicVector    hcsub;
		correlations::QVector           qpos;
		correlations::QVector           qneg;
		correlations::FromQVector       *cqpos;
		correlations::FromQVector       *cqneg;

		void initQ();
		void doneQ();
		void Sim();
};



