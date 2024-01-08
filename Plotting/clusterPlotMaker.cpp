/*
"""
2023/07/27
Arka Santra

Script that makes the hisotgrams for data or MC .


To run the script:

string:: root file to process
string:: the output root file name

"""
*/

#include <iostream>
#include "TFile.h"
#include "TH1.h"
#include "TH2.h"
#include "TString.h"
#include "TCollection.h"
#include "TLorentzVector.h"
#include "TKey.h"
#include "TClass.h"
#include "TMath.h"
#include <string>
#include <sys/stat.h>
#include "TChain.h"
#include "TTree.h"
#include <ROOT/RDataFrame.hxx>
#include <algorithm>
#include <time.h>
#include <chrono> // for high_resolution_clock
#include <sstream>
#include <cmath>
#include <ROOT/RDF/HistoModels.hxx>
#include "inputFunctions.h"

using namespace std;
using namespace ROOT;
bool debug = false;

double returnWeight(float wgt, string sample){
    if (sample=="Data")
        return 1.0;
    else
        return wgt;
}

/// prepare 1D histograms from RDataFrame
void prepare1DHistogram(ROOT::RDF::RInterface<ROOT::Detail::RDF::RJittedFilter, void> dtmp, string suffixname, map<string, ROOT::RDF::TH1DModel> allHisto1Dict, map<string, TH1D*> &out1DHistoDict){
    int counter = 0;
    for (map<string, ROOT::RDF::TH1DModel>::iterator it = allHisto1Dict.begin(); it != allHisto1Dict.end(); ++it)
    {
        counter++;
        auto hist = dtmp.Histo1D(it->second, it->first, "particleWgt");
        stringstream ss2;
        ss2 << it->first;
        TH1D *histos = (TH1D*)hist->Clone((ss2.str()+"_"+suffixname).c_str());
        histos        = getOverflow(histos);
        histos        = getUnderflow(histos);
        out1DHistoDict.insert(make_pair(ss2.str()+"_"+suffixname, histos));
    }
    cout << "prepared " << counter << " 1D histograms for " << suffixname << " working point." << endl;
}
    
/// prepare 2D histograms from RDataFrame
void prepare2DHistogram(ROOT::RDF::RInterface<ROOT::Detail::RDF::RJittedFilter, void> dtmp, string suffixname, map<string, manyMaps> allHisto2Dict, map<string, TH2D*> &out2DHistoDict){
    int counter2 = 0;
    for (map<string, manyMaps>::iterator it = allHisto2Dict.begin(); it != allHisto2Dict.end(); ++it)
    {
        counter2++;
        auto hist = dtmp.Histo2D(it->second.outTH2DModel(it->first), it->second.outFirst(it->first), it->second.outSecond(it->first), "particleWgt");
        stringstream ss2;
        ss2 << it->first;
        TH2D *histos = (TH2D*)hist->Clone((ss2.str()+"_"+suffixname).c_str());
        out2DHistoDict.insert(make_pair(ss2.str()+"_"+suffixname, histos));
    }
    cout << "prepared " << counter2 << " 2D histograms for " << suffixname << " working point." << endl;
}


void clusterPlotMaker(string inputFolder="", string outputFile="clusterPlots", string sampleTag = "Data", bool inGrid=false)
{
    // ### boolean to know which process should be done
    //  Record start time
    gROOT->SetBatch();
    auto start = std::chrono::steady_clock::now();
    ROOT::EnableImplicitMT();

    std::cout << "Making Some Distribution for  " << sampleTag << std::endl;

    TFile *myFile=nullptr;
    string eosDirS = "";
    // work only with one file
    if (inGrid){
        // WIS cluster files
        eosDirS = "/storage/agrp/arkas/AllPixGrid/ProcessedData/SignalNextTrial_e1gpc_10.0_BX1to100/";
        myFile = new TFile((inputFolder+outputFile).c_str(), "RECREATE");
        std::cout << "The output file for histograms: " << outputFile.c_str() << std::endl;
    }
    // work on all files in a folder
    else{
        // ### Get all relevant settings from settings.py ###
        /// eos files on lxplus
        // eosDirS = "/eos/user/a/asantra/MuonWorkingPointFiles";
        // local files
        eosDirS = "/storage/agrp/arkas/AllPixGrid/ProcessedData/SignalNextTrial_e1gpc_10.0_BX1to100/";
        /// local files
        // string eosDirS = "/Users/arkasantra/arka/MCPWork/MCPFiles";
        string outputDirS = "HistFiles"; // the output directory
        int status = mkdir(outputDirS.c_str(), 0777);

        /// saving the alpha weights to the root file
        myFile = new TFile((outputDirS + "/" + outputFile).c_str(), "RECREATE");
        std::cout << "The output file for histograms: " << (outputDirS + "/" + outputFile).c_str() << std::endl;
        std::cout << "-----------------" << std::endl;
        std::cout << "Processing " << sampleTag << std::endl;
    }
    myFile->cd();


    /// open the histograms
    map<string, ROOT::RDF::TH1DModel> allHisto1Dict_Cls;
    allHisto1Dict_Cls.insert(make_pair("nParticles", ROOT::RDF::TH1DModel("h_nParticles", "h_nParticles; number of particles; Entries/bin", 10, 0, 10)));
    
    // /// create 2D maps, with manyMaps class
    map<string, manyMaps> allHisto2Dict_Cls;
    // /// histograms
    /// the number of bins such that bin width is approximately one pixel
    allHisto2Dict_Cls.insert(make_pair("cluster_y_vs_x", manyMaps("cluster_y_vs_x", "cls_geo_x_global", "cls_geo_y_global", ROOT::RDF::TH2DModel("cluster_y_vs_x", "cluster_y_vs_x; x [cm]; y [cm]", 11286, 0, 33, 521, -0.7, 0.7))));
    
    string treeInS = "clusters";
    string treeInFileS = ""; 

    stringstream ss;
    ss << treeInS;
    TChain chain(ss.str().c_str());

    // work only with one file
    if (inGrid){
        treeInFileS = eosDirS+"dataFile_Signal_e1gpc_10.0_EFieldV10p7p1pyN17Vpercm_Processed_Stave00_Event1.root";
        cout << "file added: " << treeInFileS << endl;
        chain.Add(treeInFileS.c_str());
    }
    // add all files in a given folder
    else{
        for(int j=1; j <=10; j++){
            try{
                chain.Add((eosDirS+"dataFile_Signal_e1gpc_10.0_EFieldV10p7p1pyN17Vpercm_Processed_Stave00_Event"+to_string(j)+".root").c_str());
                chain.Add((eosDirS+"dataFile_Signal_e1gpc_10.0_EFieldV10p7p1pyN17Vpercm_Processed_Stave01_Event"+to_string(j)+".root").c_str());
                chain.Add((eosDirS+"dataFile_Signal_e1gpc_10.0_EFieldV10p7p1pyN17Vpercm_Processed_Stave02_Event"+to_string(j)+".root").c_str());
                chain.Add((eosDirS+"dataFile_Signal_e1gpc_10.0_EFieldV10p7p1pyN17Vpercm_Processed_Stave03_Event"+to_string(j)+".root").c_str());
                chain.Add((eosDirS+"dataFile_Signal_e1gpc_10.0_EFieldV10p7p1pyN17Vpercm_Processed_Stave04_Event"+to_string(j)+".root").c_str());
                chain.Add((eosDirS+"dataFile_Signal_e1gpc_10.0_EFieldV10p7p1pyN17Vpercm_Processed_Stave05_Event"+to_string(j)+".root").c_str());
                chain.Add((eosDirS+"dataFile_Signal_e1gpc_10.0_EFieldV10p7p1pyN17Vpercm_Processed_Stave06_Event"+to_string(j)+".root").c_str());
                chain.Add((eosDirS+"dataFile_Signal_e1gpc_10.0_EFieldV10p7p1pyN17Vpercm_Processed_Stave07_Event"+to_string(j)+".root").c_str());
                chain.Add((eosDirS+"dataFile_Signal_e1gpc_10.0_EFieldV10p7p1pyN17Vpercm_Processed_Stave08_Event"+to_string(j)+".root").c_str());
            }
            catch(...){
                std::cout << " something wrong here: " << (eosDirS+"dataFile_Signal_e1gpc_10.0_EFieldV10p7p1pyN17Vpercm_Processed_Stave08_Event"+to_string(j)+".root").c_str() << std::endl;
            }
        }
    }
        

    ROOT::RDataFrame d(chain);
    auto count = d.Count();
    // # Determine the number of events to loop over
    unsigned long long rangeNumber = -1;
    rangeNumber = *count;
    // # Start loop over all events
    std::cout << "Looping over " << rangeNumber << " Events" << std::endl;

    auto dSel    = d.Filter("isSignal==1")
                    .Define("nParticles", "getParticleNumbers(tru_trackId)")
                    .Define("particleWgt", "nParticles")
                    .Define("cls_geo_x_global", "getClsX(rglobal_geo)")
                    .Define("cls_geo_x_global", "getClsY(rglobal_geo)");

    /// map to store histograms
    map<string, TH1D*> prepared1DHistogram;
    map<string, TH2D*> prepared2DHistogram;

    ///////////////////////////////////////////
    /// differenrt particle working point /////
    ///////////////////////////////////////////
    prepare1DHistogram(dSel, "clsProperty", allHisto1Dict_Cls, prepared1DHistogram);
    prepare2DHistogram(dSel, "clsProperty", allHisto2Dict_Cls, prepared2DHistogram);

    
    /////////////////////////////////////////////////
    // Save histograms                            ///
    /////////////////////////////////////////////////
    /// write the histograms to the root file, barrel
    for (map<string, TH1D*>::iterator it = prepared1DHistogram.begin(); it != prepared1DHistogram.end(); ++it){
        it->second->Write(it->first.c_str());
    }
    for (map<string, TH2D*>::iterator it = prepared2DHistogram.begin(); it != prepared2DHistogram.end(); ++it){
        it->second->Write(it->first.c_str());
    }
    myFile->Close();
    
    // Record end time
    auto finish = std::chrono::steady_clock::now();
    auto diff = finish - start;
    std::cout << "Elapsed time : " << chrono::duration<double, milli>(diff).count() / 1000.0 << " s" << endl;
    delete myFile;
}
