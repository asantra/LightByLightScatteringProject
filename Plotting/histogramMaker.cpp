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

/// @brief
/// @param wgt --> getting from ntuple
/// @param sample --> weight=1.0 for data, otherwise value from ntuple
/// @return weight
double returnWeight(float wgt, string sample)
{
    if (sample == "Data")
        return 1.0;
    else
        return wgt;
}

/// prepare 1D histograms from RDataFrame
void prepare1DHistogram(ROOT::RDF::RInterface<ROOT::Detail::RDF::RJittedFilter, void> dtmp, string suffixname, map<string, ROOT::RDF::TH1DModel> allHisto1Dict, map<string, TH1D *> &out1DHistoDict)
{
    int counter = 0;
    // turn on Sumw2()
    TH1::SetDefaultSumw2(true);
    /// get 1D histogram and save inside a map
    for (map<string, ROOT::RDF::TH1DModel>::iterator it = allHisto1Dict.begin(); it != allHisto1Dict.end(); ++it)
    {
        counter++;
        auto hist = dtmp.Histo1D(it->second, it->first);
        stringstream ss2;
        ss2 << it->first;
        TH1D *histos = (TH1D *)hist->Clone((ss2.str() + "_" + suffixname).c_str());
        histos = getOverflow(histos);
        histos = getUnderflow(histos);
        out1DHistoDict.insert(make_pair(ss2.str() + "_" + suffixname, histos));
    }
    cout << "prepared " << counter << " 1D histograms for " << suffixname << " particle." << endl;
}

/// prepare 2D histograms from RDataFrame
void prepare2DHistogram(ROOT::RDF::RInterface<ROOT::Detail::RDF::RJittedFilter, void> dtmp, string suffixname, map<string, manyMaps> allHisto2Dict, map<string, TH2D *> &out2DHistoDict)
{
    int counter2 = 0;
    /// get 2D histogram and save inside a map
    for (map<string, manyMaps>::iterator it = allHisto2Dict.begin(); it != allHisto2Dict.end(); ++it)
    {
        counter2++;
        auto hist = dtmp.Histo2D(it->second.outTH2DModel(it->first), it->second.outFirst(it->first), it->second.outSecond(it->first));
        stringstream ss2;
        ss2 << it->first;
        TH2D *histos = (TH2D *)hist->Clone((ss2.str() + "_" + suffixname).c_str());
        out2DHistoDict.insert(make_pair(ss2.str() + "_" + suffixname, histos));
    }
    cout << "prepared " << counter2 << " 2D histograms for " << suffixname << " particle." << endl;
}

void histogramMaker(string inputFolder = "", string outputFile = "ELI-NP_Signal_LCFA_Histogram.root", string version = "1", string sampleTag = "Data", bool workOneFile = false)
{
    //  Record start time
    gROOT->SetBatch();
    auto start = std::chrono::steady_clock::now();
    bool isData = false;
    bool isMC = false;
    ROOT::EnableImplicitMT();

    // turn on Sumw2()
    TH1::SetDefaultSumw2(true);

    /// work here if you also want MC
    if (sampleTag == "Data")
    {
        isData = true;
    }
    else if (sampleTag == "MC")
    {
        isMC = true;
    }
    else
    {
        std::cout << "Unknown option for Data/MC" << std::endl;
        return;
    }
    std::cout << "Making Some Distribution for  " << sampleTag << std::endl;

    TFile *myFile = nullptr;
    string eosDirS = "";
    // work only with one file
    if (workOneFile)
    {
        // WIS cluster files
        eosDirS = "/storage/agrp/arkas/E320Files/PtarmiganWorkAreaHorizontal_a0_10.0_xFOne";
        string outputDirS = "HistFiles"; // the output directory
        int status = mkdir(outputDirS.c_str(), 0777);
        /// saving the alpha weights to the root file
        myFile = new TFile((outputDirS + "/" + outputFile).c_str(), "RECREATE");
        std::cout << "The output file for histograms: " << outputFile.c_str() << std::endl;
    }
    // work on all files in a folder
    else
    {
        // ### Get all relevant settings from settings.py ###
        /// eos files on lxplus
        // eosDirS = "/eos/user/a/asantra/MuonWorkingPointFiles";
        // on WIS
        // eosDirS = "/storage/agrp/arkas/E320Files/PtarmiganWorkAreaHorizontal_a0_10.0_xFOne";
        // string outputDirS = "HistFiles"; // the output directory

        eosDirS = "/storage/agrp/arkas/ELINP_a0_20.0_LCFAFiles";
        string outputDirS = "HistFiles_LCFA"; // the output directory

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
    map<string, ROOT::RDF::TH1DModel> allHisto1Dict_Gamma;
    map<string, ROOT::RDF::TH1DModel> allHisto1Dict_Positron;

    /// Electron
    allHisto1Dict_Electron.insert(make_pair("E_0", ROOT::RDF::TH1DModel("h_E_ele", "; E [GeV]; Particles/bin", 1000, 0, 10.0)));
    allHisto1Dict_Electron.insert(make_pair("vx_0", ROOT::RDF::TH1DModel("h_vx_ele", "; vx [cm]; Particles/bin", 1000, -0.01, 0.01)));
    allHisto1Dict_Electron.insert(make_pair("vy_0", ROOT::RDF::TH1DModel("h_vy_ele", "; vy [cm]; Particles/bin", 1000, -0.01, 0.01)));
    allHisto1Dict_Electron.insert(make_pair("vz_0", ROOT::RDF::TH1DModel("h_vz_ele", "; vz [cm]; Particles/bin", 1000, -0.005, 0.005)));
    allHisto1Dict_Electron.insert(make_pair("px_0", ROOT::RDF::TH1DModel("h_px_ele", "; px [GeV]; Particles/bin", 1000, -0.005, 0.005)));
    allHisto1Dict_Electron.insert(make_pair("py_0", ROOT::RDF::TH1DModel("h_py_ele", "; py [GeV]; Particles/bin", 1000, -0.005, 0.005)));
    allHisto1Dict_Electron.insert(make_pair("pz_0", ROOT::RDF::TH1DModel("h_pz_ele", "; pz [GeV]; Particles/bin", 1000, 0, 10.0)));
    allHisto1Dict_Electron.insert(make_pair("eta_0", ROOT::RDF::TH1DModel("h_eta_ele", "; #eta ; Particles/bin", 1000, 1, 20.0)));
    allHisto1Dict_Electron.insert(make_pair("theta_0", ROOT::RDF::TH1DModel("h_theta_ele", "; #theta [rad]; Particles/bin", 1000, 0.0, 0.1)));
    allHisto1Dict_Electron.insert(make_pair("phi_0", ROOT::RDF::TH1DModel("h_phi_ele", "; #phi [rad]; Particles/bin", 1000, -3.14, 3.14)));
    allHisto1Dict_Electron.insert(make_pair("a0out_0", ROOT::RDF::TH1DModel("h_a0Out_ele", "; a_{0}; Particles/bin", 1000, 0, 20.0)));
    allHisto1Dict_Electron.insert(make_pair("time_0", ROOT::RDF::TH1DModel("h_time_ele", "; time [s]; Particles/bin", 1000, -0.1, 0.1)));

    /// Positron
    allHisto1Dict_Positron.insert(make_pair("E_0", ROOT::RDF::TH1DModel("h_E_pos", "; E [GeV]; Particles/bin", 100, 0, 10.0)));
    allHisto1Dict_Positron.insert(make_pair("vx_0", ROOT::RDF::TH1DModel("h_vx_pos", "; vx [cm]; Particles/bin", 100, -0.03, 0.03)));
    allHisto1Dict_Positron.insert(make_pair("vy_0", ROOT::RDF::TH1DModel("h_vy_pos", "; vy [cm]; Particles/bin", 60, -0.01, 0.01)));
    allHisto1Dict_Positron.insert(make_pair("vz_0", ROOT::RDF::TH1DModel("h_vz_pos", "; vz [cm]; Particles/bin", 50, -0.005, 0.005)));
    allHisto1Dict_Positron.insert(make_pair("px_0", ROOT::RDF::TH1DModel("h_px_pos", "; px [GeV]; Particles/bin", 100, -0.02, 0.02)));
    allHisto1Dict_Positron.insert(make_pair("py_0", ROOT::RDF::TH1DModel("h_py_pos", "; py [GeV]; Particles/bin", 50, -0.005, 0.005)));
    allHisto1Dict_Positron.insert(make_pair("pz_0", ROOT::RDF::TH1DModel("h_pz_pos", "; pz [GeV]; Particles/bin", 50, 0, 10.0)));
    allHisto1Dict_Positron.insert(make_pair("eta_0", ROOT::RDF::TH1DModel("h_eta_pos", "; #eta ; Particles/bin", 50, 1, 20.0)));
    allHisto1Dict_Positron.insert(make_pair("theta_0", ROOT::RDF::TH1DModel("h_theta_pos", "; #theta [rad]; Particles/bin", 50, 0.0, 0.1)));
    allHisto1Dict_Positron.insert(make_pair("phi_0", ROOT::RDF::TH1DModel("h_phi_pos", "; #phi [rad]; Particles/bin", 50, -3.14, 3.14)));
    allHisto1Dict_Positron.insert(make_pair("a0out_0", ROOT::RDF::TH1DModel("h_a0Out_pos", "; a_{0}; Particles/bin", 200, 5, 30.0)));
    allHisto1Dict_Positron.insert(make_pair("time_0", ROOT::RDF::TH1DModel("h_time_pos", "; time [s]; Particles/bin", 50, -0.1, 0.1)));

    /// Photon
    allHisto1Dict_Gamma.insert(make_pair("E_0", ROOT::RDF::TH1DModel("h_E_gam", "; E [GeV]; Particles/bin", 1000, 0, 10.0)));
    allHisto1Dict_Gamma.insert(make_pair("vx_0", ROOT::RDF::TH1DModel("h_vx_gam", "; vx [cm]; Particles/bin", 1000, -0.01, 0.01)));
    allHisto1Dict_Gamma.insert(make_pair("vy_0", ROOT::RDF::TH1DModel("h_vy_gam", "; vy [cm]; Particles/bin", 1000, -0.01, 0.01)));
    allHisto1Dict_Gamma.insert(make_pair("vz_0", ROOT::RDF::TH1DModel("h_vz_gam", "; vz [cm]; Particles/bin", 1000, -0.005, 0.005)));
    allHisto1Dict_Gamma.insert(make_pair("px_0", ROOT::RDF::TH1DModel("h_px_gam", "; px [GeV]; Particles/bin", 1000, -0.005, 0.005)));
    allHisto1Dict_Gamma.insert(make_pair("py_0", ROOT::RDF::TH1DModel("h_py_gam", "; py [GeV]; Particles/bin", 1000, -0.005, 0.005)));
    allHisto1Dict_Gamma.insert(make_pair("pz_0", ROOT::RDF::TH1DModel("h_pz_gam", "; pz [GeV]; Particles/bin", 1000, 0, 10.0)));
    allHisto1Dict_Gamma.insert(make_pair("eta_0", ROOT::RDF::TH1DModel("h_eta_gam", "; #eta ; Particles/bin", 1000, 1, 20.0)));
    allHisto1Dict_Gamma.insert(make_pair("theta_0", ROOT::RDF::TH1DModel("h_theta_gam", "; #theta [rad]; Particles/bin", 1000, 0.0, 0.1)));
    allHisto1Dict_Gamma.insert(make_pair("phi_0", ROOT::RDF::TH1DModel("h_phi_gam", "; #phi [rad]; Particles/bin", 1000, -3.14, 3.14)));
    allHisto1Dict_Gamma.insert(make_pair("a0out_0", ROOT::RDF::TH1DModel("h_a0Out_gam", "; a_{0}; Particles/bin", 1000, 0, 20.0)));
    allHisto1Dict_Gamma.insert(make_pair("time_0", ROOT::RDF::TH1DModel("h_time_gam", "; time [s]; Particles/bin", 1000, -0.1, 0.1)));

    // /// create 2D maps, with manyMaps class
    map<string, manyMaps> allHisto2Dict_Electron;
    map<string, manyMaps> allHisto2Dict_Gamma;
    map<string, manyMaps> allHisto2Dict_Positron;
    allHisto2Dict_Electron.insert(make_pair("electron_vy_vs_vx", manyMaps("electron_vy_vs_vx", "vx_0", "vy_0", ROOT::RDF::TH2DModel("electron_vy_vs_vx", "electron_vy_vs_vx; vx (cm); vy (cm)", 1000, -0.01, 0.01, 1000, -0.01, 0.01))));
    allHisto2Dict_Gamma.insert(make_pair("photon_vy_vs_vx", manyMaps("photon_vy_vs_vx", "vx_0", "vy_0", ROOT::RDF::TH2DModel("photon_vy_vs_vx", "photon_vy_vs_vx; vx (cm); vy (cm)", 1000, -0.01, 0.01, 1000, -0.01, 0.01))));
    allHisto2Dict_Positron.insert(make_pair("positron_vy_vs_vx", manyMaps("positron_vy_vs_vx", "vx_0", "vy_0", ROOT::RDF::TH2DModel("positron_vy_vs_vx", "positron_vy_vs_vx; vx (cm); vy (cm)", 1000, -0.01, 0.01, 1000, -0.01, 0.01))));

    string treeInS = "tt";
    string treeInFileS = "";

    stringstream ss;
    ss << treeInS;
    TChain chain(ss.str().c_str());

    // work only with one file
    if (workOneFile)
    {
        treeInFileS = eosDirS + "/" + inputFolder + "/raw_e320_a0_10.0_gamma10.0_Iteration1_v" + version + ".root";
        cout << "file added: " << treeInFileS << endl;
        chain.Add(treeInFileS.c_str());
    }
    // add all files in a given folder
    else
    {
        /// here add as many files as you want
        /// Since I have 6000 files, I am looping until 6000
        int j = 0;

        // for (j = 1; j <= 6000; j++)
        // {
        //     chain.Add((eosDirS + "/" + inputFolder + "/run_" + std::to_string(j) + "/raw_e320_a0_10.0_gamma10.0_Iteration" + std::to_string(j) + "_v" + version + ".root").c_str());
        // }

        /// for LCFA or LMA files
        for (j = 1; j <= 10; j++)
        {
            chain.Add((eosDirS + "/" + inputFolder + "/raw_elinp_a0_20.0_Iteration" + std::to_string(j) + "_v" + version + "_positrons_only.root").c_str());
        }
        cout << "Added " << (j - 1) << " files." << endl;
    }

    // create a RDataFrame based on the old tree
    ROOT::RDataFrame d(chain);
    auto count = d.Count();
    // Determine the number of events to loop over
    unsigned long long rangeNumber = -1;
    rangeNumber = *count;
    // Start loop over all events
    std::cout << "Looping over " << rangeNumber << " Events" << std::endl;

    // define a new RDataFrame with new variables relevant for plotting
    // this is needed because the ntuples are stored as vectors
    auto dNewVar = d.Define("E_0", "E[0]")
                       .Define("vx_0", "vx[0]")
                       .Define("vy_0", "vy[0]")
                       .Define("vz_0", "vz[0]")
                       .Define("px_0", "px[0]")
                       .Define("py_0", "py[0]")
                       .Define("pz_0", "pz[0]")
                       .Define("eta_0", "eta[0]")
                       .Define("theta_0", "theta[0]")
                       .Define("phi_0", "phi[0]")
                       .Define("time_0", "time[0]")
                       .Define("a0out_0", "a0out[0]")
                       .Define("pdgId_0", "pdgId[0]");

    /// filter according to particles
    auto dEl = dNewVar.Filter("pdgId_0==11");  // electron
    auto dPh = dNewVar.Filter("pdgId_0==22");  // photon
    auto dPo = dNewVar.Filter("pdgId_0==-11"); // positron

    /// map to store histograms
    map<string, TH1D *> prepared1DHistogram;
    map<string, TH2D *> prepared2DHistogram;

    ///////////////////////////////////////////
    /// differenrt particle working point /////
    ///////////////////////////////////////////
    prepare1DHistogram(dEl, "electron", allHisto1Dict_Electron, prepared1DHistogram);
    prepare2DHistogram(dEl, "electron", allHisto2Dict_Electron, prepared2DHistogram);

    prepare1DHistogram(dPh, "gamma", allHisto1Dict_Gamma, prepared1DHistogram);
    prepare2DHistogram(dPh, "gamma", allHisto2Dict_Gamma, prepared2DHistogram);

    prepare1DHistogram(dPo, "positron", allHisto1Dict_Positron, prepared1DHistogram);
    prepare2DHistogram(dPo, "positron", allHisto2Dict_Positron, prepared2DHistogram);

    /////////////////////////////////////////////////
    // Save histograms                            ///
    /////////////////////////////////////////////////
    /// write the histograms to the root file

    /// write 1D histograms
    for (map<string, TH1D *>::iterator it = prepared1DHistogram.begin(); it != prepared1DHistogram.end(); ++it)
    {
        it->second->Write(it->first.c_str());
    }

    /// write 2D histograms
    for (map<string, TH2D *>::iterator it = prepared2DHistogram.begin(); it != prepared2DHistogram.end(); ++it)
    {
        it->second->Write(it->first.c_str());
    }
    myFile->Close();

    // Record end time
    auto finish = std::chrono::steady_clock::now();
    auto diff = finish - start;
    std::cout << "Total elapsed time : " << chrono::duration<double, milli>(diff).count() / 1000.0 << " s" << endl;
    delete myFile;
}
