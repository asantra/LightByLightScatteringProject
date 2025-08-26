import os, sys
import argparse
from ROOT import TFile, TCanvas, gStyle, gPad, TLatex, TLegend, TLine, gROOT
from copy import copy, deepcopy
# sys.path.insert(0, '/Users/arkasantra/arka/include')
from Functions import *
import pprint






def DrawHists(FirstTH1, LegendName, PlotColor,xAxisName, yAxisName, xrange1down, xrange1up, yrange1down, yrange1up, CanvasName, yline1low, yline1up, drawline=False, logy=False, latexName='', latexName2 = '', latexName3='', leftLegend=False, doAtlas=False, doLumi=False, noRatio=False, do80=False, do59=False, drawPattern="", logz=False, logx=False, latexName4='', zAxisName='Entries per primary electron',zrange1down=0,zrange1up=0.07):
   debug = False
   if(debug): print("just entering plot code")
   ### without mean
   Tex  = MakeLatex(0.80,0.85,latexName)
   Tex2 = MakeLatex(0.80,0.79,latexName2)
   Tex3 = MakeLatex(0.80,0.73,latexName3)
   Tex4 = MakeLatex(0.80,0.67,latexName4)
   
   
   if(debug): print ("defining Tex ")
   c = TCanvas("c","c",500, 500)
   gStyle.SetOptStat(0)
   ### for others
   gPad.SetLeftMargin(0.15)
   gPad.SetRightMargin(0.14)
   gPad.SetBottomMargin(0.14)
   c.cd()
#    c.SetGrid()
   
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
     if("TH1D" in strType):
        # legend1.AddEntry(FirstTH1[i],LegendName[i]+" ("+str(round(integralList[i],1))+")", "l")
        legend1.AddEntry(FirstTH1[i],LegendName[i], "l")
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
       drawStyle = drawPattern
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
   
#    Tex.Draw("sames")
#    Tex2.Draw("sames")
#    Tex3.Draw("sames")
#    Tex4.Draw("sames")
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
    parser.add_argument('-in1', action="store", dest="infile1", type=str, default="ELI-NP_Signal_LCFA_Histogram.root")
    parser.add_argument('-in12', action="store", dest="infile2", type=str, default="ELI-NP_Signal_LMA_Histogram.root")
    parser.add_argument('-out', action="store", dest="outDir", type=str, default="ComparisonPlots_ELI-NP")
    

    args = parser.parse_args()


    plotFolder = "plotFolder_ELI-NP/"+args.outDir
    if not os.path.exists(plotFolder):
        os.makedirs(plotFolder)
    plotFolderNonLog = "plotFolder_ELI-NP/"+args.outDir+"_NonLog"
    if not os.path.exists(plotFolderNonLog):
        os.makedirs(plotFolderNonLog)

    inputFolder1 = "/storage/agrp/arkas/E320Files/Analyzer/HistFiles_LCFA"
    inRootFile1  = TFile(inputFolder1+"/"+args.infile1, "READ")

    inputFolder2 = "/storage/agrp/arkas/E320Files/Analyzer/HistFiles_LMA"
    inRootFile2  = TFile(inputFolder2+"/"+args.infile2, "READ")
    

    for particle in ['positron']:
        hEnergy1        = inRootFile1.Get("E_0_"+particle)
        hPx1            = inRootFile1.Get("px_0_"+particle)
        hPy1            = inRootFile1.Get("py_0_"+particle)
        hPz1            = inRootFile1.Get("pz_0_"+particle)
        hvx1            = inRootFile1.Get("vx_0_"+particle)
        hvy1            = inRootFile1.Get("vy_0_"+particle)
        hvz1            = inRootFile1.Get("vz_0_"+particle)
        ### a0 only for positron and photon
        if particle!="electron":
           ha01         = inRootFile1.Get("a0out_0_"+particle)

        hEnergy2        = inRootFile2.Get("E_0_"+particle)
        hPx2            = inRootFile2.Get("px_0_"+particle)
        hPy2            = inRootFile2.Get("py_0_"+particle)
        hPz2            = inRootFile2.Get("pz_0_"+particle)
        hvx2            = inRootFile2.Get("vx_0_"+particle)
        hvy2            = inRootFile2.Get("vy_0_"+particle)
        hvz2            = inRootFile2.Get("vz_0_"+particle)
        ### a0 only for positron and photon
        if particle!="electron":
           ha02         = inRootFile2.Get("a0out_0_"+particle)
    
        print("After reading histogram")

        drawline=False
        logy=False
        latexName=particle
        latexName2 = 'a_{0}=20.0'
        
        leftLegend=False
        doAtlas=False
        doLumi=False
        noRatio=False
        do80=False
        do59=False
        drawPattern="hist"
        logz=False
        logx=False
        
        print("Plotting 1D histogram")

        ColorList  = [4, 2]
        LegendName = ["LCFA", "LMA"]
        logy=True
        ymin = 0.1


        FirstTH1 = [hEnergy1, hEnergy2]
        ymax = FirstTH1[0].GetMaximum()*2
        mean = FirstTH1[0].GetMean()
        stddev = FirstTH1[0].GetStdDev()
        latexName3 = "mean: "+'{:.2e}'.format(mean)
        latexName4= 'std dev: '+'{:.2e}'.format(stddev)
        DrawHists(FirstTH1, LegendName, ColorList,"E [GeV]", "Particles/bin", 0, 10.5, ymin, ymax, plotFolder+"/Energy_"+particle, 1, 1, drawline, logy, latexName, latexName2, latexName3, leftLegend, doAtlas, doLumi, noRatio, do80, do59, drawPattern, logz, logx, latexName4)
        


        FirstTH1 = [hPx1, hPx2]
        ymax = FirstTH1[0].GetMaximum()*2
        mean = FirstTH1[0].GetMean()
        stddev = FirstTH1[0].GetStdDev()
        latexName3 = "mean: "+'{:.2e}'.format(mean)
        latexName4= 'std dev: '+'{:.2e}'.format(stddev)
        DrawHists(FirstTH1, LegendName, ColorList,"p_{x} [GeV]", "Particles/bin", -0.02, 0.02, ymin, ymax, plotFolder+"/px_"+particle, 1, 1, drawline, logy, latexName, latexName2, latexName3, leftLegend, doAtlas, doLumi, noRatio, do80, do59, drawPattern, logz, logx, latexName4)
        


        FirstTH1 = [hPy1, hPy2]
        ymax = FirstTH1[0].GetMaximum()*2
        mean = FirstTH1[0].GetMean()
        stddev = FirstTH1[0].GetStdDev()
        latexName3 = "mean: "+'{:.2e}'.format(mean)
        latexName4= 'std dev: '+'{:.2e}'.format(stddev)
        DrawHists(FirstTH1, LegendName, ColorList,"p_{y} [GeV]", "Particles/bin", -0.005, 0.005, ymin, ymax, plotFolder+"/py_"+particle, 1, 1, drawline, logy, latexName, latexName2, latexName3, leftLegend, doAtlas, doLumi, noRatio, do80, do59, drawPattern, logz, logx, latexName4)
        


        FirstTH1 = [hPz1, hPz2]
        ymax = FirstTH1[0].GetMaximum()*2
        mean = FirstTH1[0].GetMean()
        stddev = FirstTH1[0].GetStdDev()
        latexName3 = "mean: "+'{:.2e}'.format(mean)
        latexName4= 'std dev: '+'{:.2e}'.format(stddev)
        DrawHists(FirstTH1, LegendName, ColorList,"p_{z} [GeV]", "Particles/bin", 0, 10, ymin, ymax, plotFolder+"/pz_"+particle, 1, 1, drawline, logy, latexName, latexName2, latexName3, leftLegend, doAtlas, doLumi, noRatio, do80, do59, drawPattern, logz, logx, latexName4)
        


        FirstTH1 = [hvx1, hvx2]
        ymax = FirstTH1[0].GetMaximum()*2
        mean = FirstTH1[0].GetMean()
        stddev = FirstTH1[0].GetStdDev()
        latexName3 = "mean: "+'{:.2e}'.format(mean)
        latexName4= 'std dev: '+'{:.2e}'.format(stddev)
        DrawHists(FirstTH1, LegendName, ColorList,"v_{x} [cm]", "Particles/bin", 0, 0.025, ymin, ymax, plotFolder+"/vx_"+particle, 1, 1, drawline, logy, latexName, latexName2, latexName3, leftLegend, doAtlas, doLumi, noRatio, do80, do59, drawPattern, logz, logx, latexName4)
        


        FirstTH1 = [hvy1, hvy2]
        ymax = FirstTH1[0].GetMaximum()*2
        mean = FirstTH1[0].GetMean()
        stddev = FirstTH1[0].GetStdDev()
        latexName3 = "mean: "+'{:.2e}'.format(mean)
        latexName4= 'std dev: '+'{:.2e}'.format(stddev)
        DrawHists(FirstTH1, LegendName, ColorList,"v_{y} [cm]", "Particles/bin", -0.01, 0.01, ymin, ymax, plotFolder+"/vy_"+particle, 1, 1, drawline, logy, latexName, latexName2, latexName3, leftLegend, doAtlas, doLumi, noRatio, do80, do59, drawPattern, logz, logx, latexName4)
        


        FirstTH1 = [hvz1, hvz2]
        ymax = FirstTH1[0].GetMaximum()*2
        mean = FirstTH1[0].GetMean()
        stddev = FirstTH1[0].GetStdDev()
        latexName3 = "mean: "+'{:.2e}'.format(mean)
        latexName4= 'std dev: '+'{:.2e}'.format(stddev)
        DrawHists(FirstTH1, LegendName, ColorList,"v_{z} [cm]", "Particles/bin", -0.005, 0.005, ymin, ymax, plotFolder+"/vz_"+particle, 1, 1, drawline, logy, latexName, latexName2, latexName3, leftLegend, doAtlas, doLumi, noRatio, do80, do59, drawPattern, logz, logx, latexName4)




        if particle!="electron":
            FirstTH1 = [ha01, ha02]
            ymax = FirstTH1[1].GetMaximum()*2
            mean = FirstTH1[0].GetMean()
            stddev = FirstTH1[0].GetStdDev()
            latexName3 = "mean: "+'{:.2e}'.format(mean)
            latexName4= 'std dev: '+'{:.2e}'.format(stddev)
            DrawHists(FirstTH1, LegendName, ColorList,"a_{0}", "Particles/bin", 5.0, 30.0, ymin, ymax, plotFolder+"/a0_"+particle, 1, 1, drawline, logy, latexName, latexName2, latexName3, leftLegend, doAtlas, doLumi, noRatio, do80, do59, drawPattern, logz, logx, latexName4)



        logy=False
        FirstTH1 = [hEnergy1, hEnergy2]
        ymax = FirstTH1[0].GetMaximum()*2
        mean = FirstTH1[0].GetMean()
        stddev = FirstTH1[0].GetStdDev()
        latexName3 = "mean: "+'{:.2e}'.format(mean)
        latexName4= 'std dev: '+'{:.2e}'.format(stddev)
        DrawHists(FirstTH1, LegendName, ColorList,"E [GeV]", "Particles/bin", 0, 10, ymin, ymax, plotFolderNonLog+"/Energy_"+particle, 1, 1, drawline, logy, latexName, latexName2, latexName3, leftLegend, doAtlas, doLumi, noRatio, do80, do59, drawPattern, logz, logx, latexName4)
        


        FirstTH1 = [hPx1, hPx2]
        ymax = FirstTH1[0].GetMaximum()*2
        mean = FirstTH1[0].GetMean()
        stddev = FirstTH1[0].GetStdDev()
        latexName3 = "mean: "+'{:.2e}'.format(mean)
        latexName4= 'std dev: '+'{:.2e}'.format(stddev)
        DrawHists(FirstTH1, LegendName, ColorList,"p_{x} [GeV]", "Particles/bin", -0.02, 0.02, ymin, ymax, plotFolderNonLog+"/px_"+particle, 1, 1, drawline, logy, latexName, latexName2, latexName3, leftLegend, doAtlas, doLumi, noRatio, do80, do59, drawPattern, logz, logx, latexName4)
        


        FirstTH1 = [hPy1, hPy2]
        ymax = FirstTH1[0].GetMaximum()*2
        mean = FirstTH1[0].GetMean()
        stddev = FirstTH1[0].GetStdDev()
        latexName3 = "mean: "+'{:.2e}'.format(mean)
        latexName4= 'std dev: '+'{:.2e}'.format(stddev)
        DrawHists(FirstTH1, LegendName, ColorList,"p_{y} [GeV]", "Particles/bin", -0.005, 0.005, ymin, ymax, plotFolderNonLog+"/py_"+particle, 1, 1, drawline, logy, latexName, latexName2, latexName3, leftLegend, doAtlas, doLumi, noRatio, do80, do59, drawPattern, logz, logx, latexName4)
        


        FirstTH1 = [hPz1, hPz2]
        ymax = FirstTH1[0].GetMaximum()*2
        mean = FirstTH1[0].GetMean()
        stddev = FirstTH1[0].GetStdDev()
        latexName3 = "mean: "+'{:.2e}'.format(mean)
        latexName4= 'std dev: '+'{:.2e}'.format(stddev)
        DrawHists(FirstTH1, LegendName, ColorList,"p_{z} [GeV]", "Particles/bin", 0, 10, ymin, ymax, plotFolderNonLog+"/pz_"+particle, 1, 1, drawline, logy, latexName, latexName2, latexName3, leftLegend, doAtlas, doLumi, noRatio, do80, do59, drawPattern, logz, logx, latexName4)
        


        FirstTH1 = [hvx1, hvx2]
        ymax = FirstTH1[0].GetMaximum()*2
        mean = FirstTH1[0].GetMean()
        stddev = FirstTH1[0].GetStdDev()
        latexName3 = "mean: "+'{:.2e}'.format(mean)
        latexName4= 'std dev: '+'{:.2e}'.format(stddev)
        DrawHists(FirstTH1, LegendName, ColorList,"v_{x} [cm]", "Particles/bin", 0.0, 0.025, ymin, ymax, plotFolderNonLog+"/vx_"+particle, 1, 1, drawline, logy, latexName, latexName2, latexName3, leftLegend, doAtlas, doLumi, noRatio, do80, do59, drawPattern, logz, logx, latexName4)
        


        FirstTH1 = [hvy1, hvy2]
        ymax = FirstTH1[0].GetMaximum()*2
        mean = FirstTH1[0].GetMean()
        stddev = FirstTH1[0].GetStdDev()
        latexName3 = "mean: "+'{:.2e}'.format(mean)
        latexName4= 'std dev: '+'{:.2e}'.format(stddev)
        DrawHists(FirstTH1, LegendName, ColorList,"v_{y} [cm]", "Particles/bin", -0.01, 0.01, ymin, ymax, plotFolderNonLog+"/vy_"+particle, 1, 1, drawline, logy, latexName, latexName2, latexName3, leftLegend, doAtlas, doLumi, noRatio, do80, do59, drawPattern, logz, logx, latexName4)
        


        FirstTH1 = [hvz1, hvz2]
        ymax = FirstTH1[0].GetMaximum()*2
        mean = FirstTH1[0].GetMean()
        stddev = FirstTH1[0].GetStdDev()
        latexName3 = "mean: "+'{:.2e}'.format(mean)
        latexName4= 'std dev: '+'{:.2e}'.format(stddev)
        DrawHists(FirstTH1, LegendName, ColorList,"v_{z} [cm]", "Particles/bin", -0.005, 0.005, ymin, ymax, plotFolderNonLog+"/vz_"+particle, 1, 1, drawline, logy, latexName, latexName2, latexName3, leftLegend, doAtlas, doLumi, noRatio, do80, do59, drawPattern, logz, logx, latexName4)



        if particle!="electron":
            FirstTH1 = [ha01, ha02]
            ymax = FirstTH1[1].GetMaximum()*2
            mean = FirstTH1[0].GetMean()
            stddev = FirstTH1[0].GetStdDev()
            latexName3 = "mean: "+'{:.2e}'.format(mean)
            latexName4= 'std dev: '+'{:.2e}'.format(stddev)
            DrawHists(FirstTH1, LegendName, ColorList,"a_{0}", "Particles/bin", 5.0, 30.0, ymin, ymax, plotFolderNonLog+"/a0_"+particle, 1, 1, drawline, logy, latexName, latexName2, latexName3, leftLegend, doAtlas, doLumi, noRatio, do80, do59, drawPattern, logz, logx, latexName4)


    
    

if __name__=="__main__":
    main()