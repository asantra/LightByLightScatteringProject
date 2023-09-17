import os, sys
import argparse
from ROOT import *
from copy import copy, deepcopy
sys.path.insert(0, '/Users/arkasantra/arka/include')
from Functions import *
import pprint






def DrawHists(FirstTH1, LegendName, PlotColor,xAxisName, yAxisName, xrange1down, xrange1up, yrange1down, yrange1up, CanvasName, yline1low, yline1up, drawline=False, logy=False, latexName='', latexName2 = '', latexName3='', leftLegend=False, doAtlas=False, doLumi=False, noRatio=False, do80=False, do59=False, drawPattern="", logz=False, logx=False, latexName4='', zAxisName='Entries per primary electron',zrange1down=0,zrange1up=0.07):
   debug = False
   if(debug): print("just entering plot code")
   ### without mean
   Tex  = MakeLatex(0.80,0.60,latexName)
   Tex2 = MakeLatex(0.80,0.54,latexName2)
   Tex3 = MakeLatex(0.80,0.48,latexName3)
   Tex4 = MakeLatex(0.34,0.42,latexName4)
   
   
   if(debug): print ("defining Tex ")
   c = TCanvas("c","c",500, 500)
   gStyle.SetOptStat(0)
   ### for others
   gPad.SetLeftMargin(0.15)
   gPad.SetRightMargin(0.14)
   gPad.SetBottomMargin(0.14)
   c.cd()
   c.SetGrid()
   
   if(logx):
     c.SetLogx()
   if(logy):
     c.SetLogy()
   if(logz):
     c.SetLogz()
     
   if(debug): print ("Set Logy ")
   line = MakeLine(xrange1down,yline1low,xrange1up,yline1up)
   if(leftLegend):
       legend1 = LeftLegendMaker()
   else:
       legend1 = LegendMaker()
   if(debug): print ("Set Legend ")
   tex1 = TLatex(); tex2 = TLatex(); tex3 = TLatex()
   L = [tex1, tex2, tex3]
   TexMaker(L, doAtlas, doLumi, noRatio, do80, do59)
   stList = []
   #
   if(debug): print ("Set Ranges ")
   integralList = []; integralListError = []
   strType = str(type(FirstTH1[0]))
   
   for i in range(0, len(FirstTH1)):
     
     FirstTH1[i] = AxisLabelEtc(FirstTH1[i], yAxisName, xAxisName)
     if("TH2" not in strType):
        FirstTH1[i] = SetHistColorEtc(FirstTH1[i], PlotColor[i])
     else:
        FirstTH1[i] = SetHistColorEtc(FirstTH1[i], PlotColor[i])
        FirstTH1[i].SetLineColor(kWhite)
       
     FirstTH1[i].SetFillColor(0)
     if("TH2D" in strType):
        xBinMax = FirstTH1[i].GetNbinsX()
        yBinMax = FirstTH1[i].GetNbinsY()
        integralList.append(FirstTH1[i].Integral(0, xBinMax+1, 0, yBinMax+1))
     elif("TH1" in strType):
         w = FirstTH1[i].Integral(0, FirstTH1[i].GetNbinsX()+1)
         integralList.append(w)
         # comment in if you want only shape distribution
         #if(w!=0):
            #FirstTH1[i].Scale(1.0/w)
     else:
        
        
        pass
     FirstTH1[i].GetYaxis().SetRangeUser(yrange1down,yrange1up)
     FirstTH1[i].GetXaxis().SetRangeUser(xrange1down,xrange1up)
     if zAxisName:
        FirstTH1[i].GetZaxis().SetTitle("Events")
     else:
        FirstTH1[i].GetZaxis().SetTitle(zAxisName)
     
       
     FirstTH1[i].SetMaximum(yrange1up)
     FirstTH1[i].SetMinimum(yrange1down)
     if("TH1D" in strType):legend1.AddEntry(FirstTH1[i],LegendName[i]+" ("+str(round(integralList[i],1))+")", "l")
     else: legend1.AddEntry(FirstTH1[i],LegendName[i]+" ("+str(round(integralList[i],1))+")", "l")
     
   
   
   if(debug): print ("After for loop ")
   FirstTH1[0].GetXaxis().SetRangeUser(xrange1down,xrange1up)
   FirstTH1[0].GetXaxis().SetNdivisions(5)
   #FirstTH1[0].GetYaxis().SetRangeUser(yrange1down,yrange1up)
   if "electrons" in FirstTH1[0].GetName():
       FirstTH1[0].GetZaxis().SetRangeUser(0,10)
   elif "positrons" in FirstTH1[0].GetName():
       FirstTH1[0].GetZaxis().SetRangeUser(0,5)
   elif "gamma" in FirstTH1[0].GetName():
       FirstTH1[0].GetZaxis().SetRangeUser(0,100)
   else:
       FirstTH1[0].GetZaxis().SetRangeUser(zrange1down,zrange1up)
       
   FirstTH1[0].GetXaxis().SetNdivisions(9)
   gPad.SetTickx()
   gPad.SetTicky()

   if "TH2" in strType:
       drawStyle = "COLZ"
   elif "TH1" in strType:
       drawStyle = "hist"
   else:
       drawStyle = "AL"
   
   #gPad.SetRightMargin(0.08)
   #gPad.SetBottomMargin(1.0)
   FirstTH1[0].Draw(drawStyle) # ce, hist
    
   
   gPad.Update();
   gPad.RedrawAxis();
   if "TH2" in strType:
        FirstTH1[0].GetZaxis().SetLabelSize(0.02)
        FirstTH1[0].GetZaxis().SetTitleOffset(1.4)
        FirstTH1[0].GetYaxis().SetTitleOffset(1.1)
        FirstTH1[0].GetYaxis().SetLabelSize(0.03)
        #FirstTH1[0].GetZaxis().SetRangeUser(0, 1e3)
        try:
            pl = FirstTH1[0].GetListOfFunctions().FindObject("palette")
            pl.SetX1NDC(0.86);
            pl.SetX2NDC(0.88);
            pl.SetY1NDC(0.14);
            pl.SetY2NDC(0.90);
            # pl.SetLabelSize(0.005);
            gPad.Modified();
            gPad.Update();
        except:
            print("This histogram is empty: ", FirstTH1[0].GetName())
   
   if(debug): 
       print ("After first Draw ")
       print("len(FirstTH1): ", len(FirstTH1), " FirstTH1: ", FirstTH1)

   if(len(FirstTH1)>1):
    #### special file for Allpix-squared plot, otherwise remove -1 in the range
    for i in range(1, len(FirstTH1)):
        if(debug): print("drawing i=", i, " FirstTH1: ", FirstTH1[i])
        FirstTH1[i].Draw(drawStyle+" sames") 
        FirstTH1[i].SetFillColor(0)
        
   #FirstTH1[0].Draw("hist sames")
   if(debug): print ("After Draw loop ")
   
   Tex.Draw("sames")
   Tex2.Draw("sames")
   Tex3.Draw("sames")
   Tex4.Draw("sames")
   #if(drawline):
     #line.Draw()
   L[0].Draw()
   L[1].Draw()
   L[2].Draw()
   if "TH1" in strType: legend1.Draw()
   else: pass #legend1.Draw()
   
   SaveFile(c, CanvasName)
   return deepcopy(c)



def main():
    gROOT.SetBatch()
    parser = argparse.ArgumentParser(description='Code to get plots from the root files coming from h5')
    parser.add_argument('-in1', action="store", dest="infile1", type=str, default="raw_lightbylight_xi3_gamma0p7_histograms.root")
    parser.add_argument('-in2', action="store", dest="infile2", type=str, default="raw_lightbylight_xi10_gamma0p7_histograms.root")
    parser.add_argument('-in3', action="store", dest="infile3", type=str, default="raw_lightbylight_xi20_gamma0p7_histograms.root")
    parser.add_argument('-in4', action="store", dest="infile4", type=str, default="raw_lightbylight_xi30_gamma0p7_histograms.root")
    parser.add_argument('-out', action="store", dest="outDir", type=str, default="gamma0p7")
    

    args = parser.parse_args()


    plotFolder = "plotFolder/"+args.outDir
    if not os.path.exists(plotFolder):
        os.makedirs(plotFolder)

    inRootFile1      = TFile("outputDirectory/"+args.infile1, "READ")
    inRootFile2      = TFile("outputDirectory/"+args.infile2, "READ")
    inRootFile3      = TFile("outputDirectory/"+args.infile3, "READ")
    inRootFile4      = TFile("outputDirectory/"+args.infile4, "READ")
    

    hEnergy_Electron1        = inRootFile1.Get("hEnergy_Electron")
    hEnergy_ElectronIn1      = inRootFile1.Get("hEnergy_Electron_In")
    hPhi_Electron1           = inRootFile1.Get("hPhi_Electron")
    hTheta_Electron1         = inRootFile1.Get("hTheta_Electron")
    hEnergyVsTheta_Electron1 = inRootFile1.Get("hEnergyVsTheta_Electron")
    hEnergy_Photon1          = inRootFile1.Get("hEnergy_Photon")
    hPhi_Photon1             = inRootFile1.Get("hPhi_Photon")
    hTheta_Photon1           = inRootFile1.Get("hTheta_Photon")
    hEnergyVsTheta_Photon1   = inRootFile1.Get("hEnergyVsTheta_Photon")

    hEnergy_Electron2        = inRootFile2.Get("hEnergy_Electron")
    hEnergy_ElectronIn2      = inRootFile2.Get("hEnergy_Electron_In")
    hPhi_Electron2           = inRootFile2.Get("hPhi_Electron")
    hTheta_Electron2         = inRootFile2.Get("hTheta_Electron")
    hEnergyVsTheta_Electron2 = inRootFile2.Get("hEnergyVsTheta_Electron")
    hEnergy_Photon2          = inRootFile2.Get("hEnergy_Photon")
    hPhi_Photon2             = inRootFile2.Get("hPhi_Photon")
    hTheta_Photon2           = inRootFile2.Get("hTheta_Photon")
    hEnergyVsTheta_Photon2   = inRootFile2.Get("hEnergyVsTheta_Photon")

    hEnergy_Electron3        = inRootFile3.Get("hEnergy_Electron")
    hEnergy_ElectronIn3      = inRootFile3.Get("hEnergy_Electron_In")
    hPhi_Electron3           = inRootFile3.Get("hPhi_Electron")
    hTheta_Electron3         = inRootFile3.Get("hTheta_Electron")
    hEnergyVsTheta_Electron3 = inRootFile3.Get("hEnergyVsTheta_Electron")
    hEnergy_Photon3          = inRootFile3.Get("hEnergy_Photon")
    hPhi_Photon3             = inRootFile3.Get("hPhi_Photon")
    hTheta_Photon3           = inRootFile3.Get("hTheta_Photon")
    hEnergyVsTheta_Photon3   = inRootFile3.Get("hEnergyVsTheta_Photon")

    hEnergy_Electron4        = inRootFile4.Get("hEnergy_Electron")
    hEnergy_ElectronIn4      = inRootFile4.Get("hEnergy_Electron_In")
    hPhi_Electron4           = inRootFile4.Get("hPhi_Electron")
    hTheta_Electron4         = inRootFile4.Get("hTheta_Electron")
    hEnergyVsTheta_Electron4 = inRootFile4.Get("hEnergyVsTheta_Electron")
    hEnergy_Photon4          = inRootFile4.Get("hEnergy_Photon")
    hPhi_Photon4             = inRootFile4.Get("hPhi_Photon")
    hTheta_Photon4           = inRootFile4.Get("hTheta_Photon")
    hEnergyVsTheta_Photon4   = inRootFile4.Get("hEnergyVsTheta_Photon")

    print("After reading histogram")

    drawline=False
    logy=True
    latexName='Electrons'
    if args.outDir == "gamma0p7":
       latexName2 = '#gamma=0.7'
    elif args.outDir == "gamma0p35":
       latexName2 = '#gamma=0.35'
    else:
       latexName2 = ''
     
    leftLegend=False
    doAtlas=False
    doLumi=False
    noRatio=False
    do80=False
    do59=False
    drawPattern="hist"
    logz=False
    logx=False
    latexName4=''

    print("Plotting 1D histogram")

    latexName3 = 'before interaction'
    ColorList  = [2, 4, kGreen+3, kOrange+2]
    LegendName = ["a_{0}=3.0", "a_{0}=10.0", "a_{0}=20.0", "a_{0}=30.0"]
    logy=False
    FirstTH1 = [hEnergy_ElectronIn1, hEnergy_ElectronIn2, hEnergy_ElectronIn3, hEnergy_ElectronIn4]
    DrawHists(FirstTH1, LegendName, ColorList,"E [MeV]", "Entries per primary electron", 0, 800, 0.001, 2.0, plotFolder+"/EnergyInDist_Electron", 1, 1, drawline, logy, latexName, latexName2, latexName3, leftLegend, doAtlas, doLumi, noRatio, do80, do59, drawPattern, logz, logx, latexName4)


    logy=True
    FirstTH1 = [hEnergy_ElectronIn1, hEnergy_ElectronIn2, hEnergy_ElectronIn3, hEnergy_ElectronIn4]
    DrawHists(FirstTH1, LegendName, ColorList,"E [MeV]", "Entries per primary electron", 0, 800, 1e-5, 6e2, plotFolder+"/EnergyInDist_Electron_Log", 1, 1, drawline, logy, latexName, latexName2, latexName3, leftLegend, doAtlas, doLumi, noRatio, do80, do59, drawPattern, logz, logx, latexName4)



    logy=False
    latexName3 = 'after interaction'
    FirstTH1 = [hEnergy_Electron1, hEnergy_Electron2, hEnergy_Electron3, hEnergy_Electron4]
    DrawHists(FirstTH1, LegendName, ColorList,"E [MeV]", "Entries per primary electron", 0, 800, 0.001, 1.4, plotFolder+"/EnergyOutDist_Electron", 1, 1, drawline, logy, latexName, latexName2, latexName3, leftLegend, doAtlas, doLumi, noRatio, do80, do59, drawPattern, logz, logx, latexName4)


    logy=True
    FirstTH1 = [hEnergy_Electron1, hEnergy_Electron2, hEnergy_Electron3, hEnergy_Electron4]
    DrawHists(FirstTH1, LegendName, ColorList,"E [MeV]", "Entries per primary electron", 0, 800, 1e-5, 5e1, plotFolder+"/EnergyOutDist_Electron_Log", 1, 1, drawline, logy, latexName, latexName2, latexName3, leftLegend, doAtlas, doLumi, noRatio, do80, do59, drawPattern, logz, logx, latexName4)


    latexName3=''
    logy=False

    FirstTH1 = [hPhi_Electron1, hPhi_Electron2, hPhi_Electron3, hPhi_Electron4]
    DrawHists(FirstTH1, LegendName, ColorList,"#phi [Rad]", "Entries per primary electron", -3.2, 3.2, 0, 0.05, plotFolder+"/PhiDist_Electron", 1, 1, drawline, logy, latexName, latexName2, latexName3, leftLegend, doAtlas, doLumi, noRatio, do80, do59, drawPattern, logz, logx, latexName4)

    
    FirstTH1 = [hTheta_Electron1, hTheta_Electron2, hTheta_Electron3, hTheta_Electron4]
    logy=True
    DrawHists(FirstTH1, LegendName, ColorList,"#theta [Rad]", "Entries per primary electron", 0,0.55, 5e-6, 5, plotFolder+"/ThetaDist_Electron_Log", 1, 1, drawline, logy, latexName, latexName2, latexName3, leftLegend, doAtlas, doLumi, noRatio, do80, do59, drawPattern, logz, logx, latexName4)

    FirstTH1 = [hTheta_Electron1, hTheta_Electron2, hTheta_Electron3, hTheta_Electron4]
    logy=False
    DrawHists(FirstTH1, LegendName, ColorList,"#theta [Rad]", "Entries per primary electron", 0, 0.55, 0, 1.2, plotFolder+"/ThetaDist_Electron", 1, 1, drawline, logy, latexName, latexName2, latexName3, leftLegend, doAtlas, doLumi, noRatio, do80, do59, drawPattern, logz, logx, latexName4)

    latexName='Photons'
    logy = False
    FirstTH1 = [hEnergy_Photon1, hEnergy_Photon2, hEnergy_Photon3, hEnergy_Photon4]
    DrawHists(FirstTH1, LegendName, ColorList,"E [MeV]", "Entries per primary electron", 0, 600, 0.001, 20, plotFolder+"/EnergyDist_Photon", 1, 1, drawline, logy, latexName, latexName2, latexName3, leftLegend, doAtlas, doLumi, noRatio, do80, do59, drawPattern, logz, logx, latexName4)

    logy = True
    FirstTH1 = [hEnergy_Photon1, hEnergy_Photon2, hEnergy_Photon3, hEnergy_Photon4]
    DrawHists(FirstTH1, LegendName, ColorList,"E [MeV]", "Entries per primary electron", 0, 600, 1e-5, 5e1, plotFolder+"/EnergyDist_Photon_Log", 1, 1, drawline, logy, latexName, latexName2, latexName3, leftLegend, doAtlas, doLumi, noRatio, do80, do59, drawPattern, logz, logx, latexName4)

    logy=False
    FirstTH1 = [hPhi_Photon1, hPhi_Photon2, hPhi_Photon3, hPhi_Photon4]
    DrawHists(FirstTH1, LegendName, ColorList,"#phi [Rad]", "Entries per primary electron", -3.2, 3.2, 0, 1.0, plotFolder+"/PhiDist_Photon", 1, 1, drawline, logy, latexName, latexName2, latexName3, leftLegend, doAtlas, doLumi, noRatio, do80, do59, drawPattern, logz, logx, latexName4)

    logy=True
    FirstTH1 = [hTheta_Photon1, hTheta_Photon2, hTheta_Photon3, hTheta_Photon4]
    DrawHists(FirstTH1, LegendName, ColorList,"#theta [Rad]", "Entries per primary electron", 0, 0.55, 5e-6, 5, plotFolder+"/ThetaDist_Photon_Log", 1, 1, drawline, logy, latexName, latexName2, latexName3, leftLegend, doAtlas, doLumi, noRatio, do80, do59, drawPattern, logz, logx, latexName4)

    logy=False
    FirstTH1 = [hTheta_Photon1, hTheta_Photon2, hTheta_Photon3, hTheta_Photon4]
    DrawHists(FirstTH1, LegendName, ColorList,"#theta [Rad]", "Entries per primary electron", 0, 0.55, 0.0, 5.0, plotFolder+"/ThetaDist_Photon", 1, 1, drawline, logy, latexName, latexName2, latexName3, leftLegend, doAtlas, doLumi, noRatio, do80, do59, drawPattern, logz, logx, latexName4)

    logy=False
    drawPattern = "COLZ"
    FirstTH1 = [hEnergyVsTheta_Photon1]
    latexName3 = "a_{0}=3.0"
    DrawHists(FirstTH1, LegendName, ColorList,"#theta [Rad]", "E [MeV]", 0, 0.55, 0, 500.0, plotFolder+"/ThetaVsE_Photon1", 1, 1, drawline, logy, latexName, latexName2, latexName3, leftLegend, doAtlas, doLumi, noRatio, do80, do59, drawPattern, logz, logx, latexName4)


    FirstTH1 = [hEnergyVsTheta_Photon2]
    latexName3 = "a_{0}=10.0"
    DrawHists(FirstTH1, LegendName, ColorList,"#theta [Rad]", "E [MeV]", 0, 0.55, 0, 500.0, plotFolder+"/ThetaVsE_Photon2", 1, 1, drawline, logy, latexName, latexName2, latexName3, leftLegend, doAtlas, doLumi, noRatio, do80, do59, drawPattern, logz, logx, latexName4)

    FirstTH1 = [hEnergyVsTheta_Photon3]
    latexName3 = "a_{0}=20.0"
    DrawHists(FirstTH1, LegendName, ColorList,"#theta [Rad]", "E [MeV]", 0, 0.55, 0, 500.0, plotFolder+"/ThetaVsE_Photon3", 1, 1, drawline, logy, latexName, latexName2, latexName3, leftLegend, doAtlas, doLumi, noRatio, do80, do59, drawPattern, logz, logx, latexName4)

    FirstTH1 = [hEnergyVsTheta_Photon4]
    latexName3 = "a_{0}=30.0"
    DrawHists(FirstTH1, LegendName, ColorList,"#theta [Rad]", "E [MeV]", 0, 0.55, 0, 500.0, plotFolder+"/ThetaVsE_Photon4", 1, 1, drawline, logy, latexName, latexName2, latexName3, leftLegend, doAtlas, doLumi, noRatio, do80, do59, drawPattern, logz, logx, latexName4)


    

if __name__=="__main__":
    main()