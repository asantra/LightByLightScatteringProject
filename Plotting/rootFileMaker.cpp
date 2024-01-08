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
        auto hist = dtmp.Histo1D(it->second, it->first);
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
        auto hist = dtmp.Histo2D(it->second.outTH2DModel(it->first), it->second.outFirst(it->first), it->second.outSecond(it->first));
        stringstream ss2;
        ss2 << it->first;
        TH2D *histos = (TH2D*)hist->Clone((ss2.str()+"_"+suffixname).c_str());
        out2DHistoDict.insert(make_pair(ss2.str()+"_"+suffixname, histos));
    }
    cout << "prepared " << counter2 << " 2D histograms for " << suffixname << " working point." << endl;
}


void rootFileMaker(string inputFolder, string outputFile, string version="1", string sampleTag = "Data", bool inGrid=false)
{
    // ### boolean to know which process should be done
    //  Record start time
    gROOT->SetBatch();
    auto start = std::chrono::steady_clock::now();
    bool isData = false;
    bool isMC = false;
    ROOT::EnableImplicitMT();

    /// work here if you also want MC
    if (sampleTag == "Data"){
        isData = true;
    }
    else if (sampleTag == "MC"){
        isMC = true;
    }
    else{
        std::cout << "Unknown option for Data/MC" << std::endl;
        return;
    }
    std::cout << "Making Some Distribution for  " << sampleTag << std::endl;

    TFile *myFile=nullptr;
    string eosDirS = "";
    // work only with one file
    if (inGrid){
        // WIS cluster files
        eosDirS = "/storage/agrp/arkas/PtarmiganWorkAreaHorizontal/";
        myFile = new TFile((eosDirS+inputFolder+outputFile).c_str(), "RECREATE");
        std::cout << "The output file for histograms: " << outputFile.c_str() << std::endl;
    }
    // work on all files in a folder
    else{
        // ### Get all relevant settings from settings.py ###
        /// eos files on lxplus
        // eosDirS = "/eos/user/a/asantra/MuonWorkingPointFiles";
        // local files
        eosDirS = "/storage/agrp/arkas/";
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
    map<string, ROOT::RDF::TH1DModel> allHisto1Dict_Electron;
    map<string, ROOT::RDF::TH1DModel> allHisto1Dict_Photon;
    map<string, ROOT::RDF::TH1DModel> allHisto1Dict_Positron;

    allHisto1Dict_Electron.insert(make_pair("E_0", ROOT::RDF::TH1DModel("hEnergy_Electron", "hEnergy_Electron; E [GeV]; Particles/bin", 105, 0, 10.5)));
    allHisto1Dict_Electron.insert(make_pair("vx_0", ROOT::RDF::TH1DModel("hvx0_Electron", "hvx0_Electron; vx [cm]; Particles/bin", 500, -0.025, 0.025)));
    allHisto1Dict_Electron.insert(make_pair("vy_0", ROOT::RDF::TH1DModel("hvy0_Electron", "hvy0_Electron; vy [cm]; Particles/bin", 300, -0.015, 0.015)));
    allHisto1Dict_Electron.insert(make_pair("vz_0", ROOT::RDF::TH1DModel("hvz0_Electron", "hvz0_Electron; vz [cm]; Particles/bin", 6000, -0.03, 0.03)));
    allHisto1Dict_Electron.insert(make_pair("px_0", ROOT::RDF::TH1DModel("hpx0_Electron", "hpx0_Electron; px [GeV]; Particles/bin", 200, -0.004, 0.004)));
    allHisto1Dict_Electron.insert(make_pair("py_0", ROOT::RDF::TH1DModel("hpy0_Electron", "hpy0_Electron; py [GeV]; Particles/bin", 200, -0.004, 0.004)));
    allHisto1Dict_Electron.insert(make_pair("pz_0", ROOT::RDF::TH1DModel("hpz0_Electron", "hpz0_Electron; pz [GeV]; Particles/bin", 105, 0, 10.5)));

    
    allHisto1Dict_Photon.insert(make_pair("E_0", ROOT::RDF::TH1DModel("hEnergy_Photon", "hEnergy_Photon; E [GeV]; Particles/bin", 105, 0, 10.5)));
    allHisto1Dict_Photon.insert(make_pair("a0out_0", ROOT::RDF::TH1DModel("ha0_Photon", "ha0_Photon; a_{0}; Particles/bin", 200, 0, 10.0)));
    allHisto1Dict_Photon.insert(make_pair("vx_0", ROOT::RDF::TH1DModel("hvx0_Photon", "hvx0_Photon; vx [cm]; Particles/bin", 500, -0.025, 0.025)));
    allHisto1Dict_Photon.insert(make_pair("vy_0", ROOT::RDF::TH1DModel("hvy0_Photon", "hvy0_Photon; vy [cm]; Particles/bin", 300, -0.015, 0.015)));
    allHisto1Dict_Photon.insert(make_pair("vz_0", ROOT::RDF::TH1DModel("hvz0_Photon", "hvz0_Photon; vz [cm]; Particles/bin", 6000, -0.03, 0.03)));
    allHisto1Dict_Photon.insert(make_pair("px_0", ROOT::RDF::TH1DModel("hpx0_Photon", "hpx0_Photon; px [GeV]; Particles/bin", 200, -0.004, 0.004)));
    allHisto1Dict_Photon.insert(make_pair("py_0", ROOT::RDF::TH1DModel("hpy0_Photon", "hpy0_Photon; py [GeV]; Particles/bin", 200, -0.004, 0.004)));
    allHisto1Dict_Photon.insert(make_pair("pz_0", ROOT::RDF::TH1DModel("hpz0_Photon", "hpz0_Photon; pz [GeV]; Particles/bin", 105, 0, 10.5)));

    
    allHisto1Dict_Positron.insert(make_pair("E_0", ROOT::RDF::TH1DModel("hEnergy_Positron", "hEnergy_Positron; E [GeV]; Particles/bin", 105, 0, 10.5)));
    allHisto1Dict_Positron.insert(make_pair("a0out_0", ROOT::RDF::TH1DModel("ha0_Positron", "ha0_Positron; a_{0}; Particles/bin", 200, 0, 10.0)));
    allHisto1Dict_Positron.insert(make_pair("vx_0", ROOT::RDF::TH1DModel("hvx0_Positron", "hvx0_Positron; vx [cm]; Particles/bin", 500, -0.025, 0.025)));
    allHisto1Dict_Positron.insert(make_pair("vy_0", ROOT::RDF::TH1DModel("hvy0_Positron", "hvy0_Positron; vy [cm]; Particles/bin", 300, -0.015, 0.015)));
    allHisto1Dict_Positron.insert(make_pair("vz_0", ROOT::RDF::TH1DModel("hvz0_Positron", "hvz0_Positron; vz [cm]; Particles/bin", 600, -0.003, 0.003)));
    allHisto1Dict_Positron.insert(make_pair("px_0", ROOT::RDF::TH1DModel("hpx0_Positron", "hpx0_Positron; px [GeV]; Particles/bin", 200, -0.004, 0.004)));
    allHisto1Dict_Positron.insert(make_pair("py_0", ROOT::RDF::TH1DModel("hpy0_Positron", "hpy0_Positron; py [GeV]; Particles/bin", 200, -0.004, 0.004)));
    allHisto1Dict_Positron.insert(make_pair("pz_0", ROOT::RDF::TH1DModel("hpz0_Positron", "hpz0_Positron; pz [GeV]; Particles/bin", 105, 0, 10.5)));

    
    
    // /// create 2D maps, with manyMaps class
    map<string, manyMaps> allHisto2Dict_Electron;
    map<string, manyMaps> allHisto2Dict_Photon;
    map<string, manyMaps> allHisto2Dict_Positron;
    // /// barrel histograms
    allHisto2Dict_Electron.insert(make_pair("electron_vy_vs_vx", manyMaps("electron_vy_vs_vx", "vx_0", "vy_0", ROOT::RDF::TH2DModel("electron_vy_vs_vx", "electron_vy_vs_vx; vx (cm); vy (cm)", 500, -0.025, 0.025, 300, -0.015, 0.015))));
    allHisto2Dict_Photon.insert(make_pair("photon_vy_vs_vx", manyMaps("photon_vy_vs_vx", "vx_0", "vy_0", ROOT::RDF::TH2DModel("photon_vy_vs_vx", "photon_vy_vs_vx; vx (cm); vy (cm)", 500, -0.025, 0.025, 300, -0.015, 0.015))));
    allHisto2Dict_Positron.insert(make_pair("positron_vy_vs_vx", manyMaps("positron_vy_vs_vx", "vx_0", "vy_0", ROOT::RDF::TH2DModel("positron_vy_vs_vx", "positron_vy_vs_vx; vx (cm); vy (cm)", 500, -0.025, 0.025, 300, -0.015, 0.015))));
    
    string treeInS = "tt";
    string treeInFileS = ""; 

    stringstream ss;
    ss << treeInS;
    TChain chain(ss.str().c_str());

    // work only with one file
    if (inGrid){
        treeInFileS = eosDirS+inputFolder+"raw_e320_xi10_gamma10_v"+version+".root";
        cout << "file added: " << treeInFileS << endl;
        chain.Add(treeInFileS.c_str());
    }
    // add all files in a iven folder
    else{
        for(int j=1; j <=250; j++){
            chain.Add((eosDirS+inputFolder+"/run_"+std::to_string(j)+"/raw_e320_xi10_gamma10_v"+version+".root").c_str());
        }
    }
        

    ROOT::RDataFrame d(chain);
    auto count = d.Count();
    // # Determine the number of events to loop over
    unsigned long long rangeNumber = -1;
    rangeNumber = *count;
    // # Start loop over all events
    std::cout << "Looping over " << rangeNumber << " Events" << std::endl;

    auto dNewVar = d.Define("E_0", "E[0]")
                    .Define("vx_0", "vx[0]")
                    .Define("vy_0", "vy[0]")
                    .Define("vz_0", "vz[0]")
                    .Define("px_0", "px[0]")
                    .Define("py_0", "py[0]")
                    .Define("pz_0", "pz[0]")
                    .Define("a0out_0", "a0out[0]")
                    .Define("pdgId_0", "pdgId[0]");

    auto dEl = dNewVar.Filter("pdgId_0==11");
    auto dPh = dNewVar.Filter("pdgId_0==22");
    auto dPo = dNewVar.Filter("pdgId_0==-11");

    /// map to store histograms
    map<string, TH1D*> prepared1DHistogram;
    map<string, TH2D*> prepared2DHistogram;

    ///////////////////////////////////////////
    /// differenrt particle working point /////
    ///////////////////////////////////////////
    prepare1DHistogram(dEl, "electron", allHisto1Dict_Electron, prepared1DHistogram);
    prepare2DHistogram(dEl, "electron", allHisto2Dict_Electron, prepared2DHistogram);

    prepare1DHistogram(dPh, "photon", allHisto1Dict_Photon, prepared1DHistogram);
    prepare2DHistogram(dPh, "photon", allHisto2Dict_Photon, prepared2DHistogram);

    prepare1DHistogram(dPo, "positron", allHisto1Dict_Positron, prepared1DHistogram);
    prepare2DHistogram(dPo, "positron", allHisto2Dict_Positron, prepared2DHistogram);
    
    
    
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
