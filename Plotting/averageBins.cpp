#include <iostream>
#include <string.h>
#include "TH2D.h"
#include "TFile.h"
#include "TH1D.h"


using namespace std;

void averageBin(string inFileName="clusterPlots_e0ppw_7.root", double scaling=4.0){
    string inputDir = "HistFiles/";
    TFile *inFile   = new TFile((inputDir+inFileName).c_str(), "READ");
    TH2D *cls2D     = (TH2D*)inFile->Get("cluster_y_vs_x_clsProperty");
    cls2D->Scale(1./scaling);

    int highestBin  = cls2D->FindBin(12, 0.15);
    double binContent = 0;
    /// loop over a 10x10 matrix around the highest bin
    /// x axis bins
    for(int i=-5; i < 5; i++){
        for(int j=-5; j < 5; j++){
            int bin = cls2D->FindBin(12+i*cls2D->GetXaxis()->GetBinWidth(1), 0.15+j*cls2D->GetYaxis()->GetBinWidth(1));
            binContent += cls2D->GetBinContent(bin);
        }
    }
    cout << "The average value in 10x10 bins around the maximum: " << binContent/100.0 << endl;
}