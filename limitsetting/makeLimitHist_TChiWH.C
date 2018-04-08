#include <fstream>
#include <iostream>

#include "TH1F.h"
#include "TH2F.h"
#include "TPad.h"
#include "TLegend.h"
#include "TCanvas.h"
#include "TColor.h"
#include "TLine.h"
#include "TLatex.h"
#include "TStyle.h"
#include "TFile.h"
#include "TBox.h"
#include "TGraph.h"
#include "TGraph2D.h"
//#include "tdrstyle_SUSY.C"

using namespace std;

int GetNumBins(const vector<double> &pts, double width){
  double pmin = *min_element(pts.cbegin(), pts.cend());
  double pmax = *max_element(pts.cbegin(), pts.cend());
  return max(1, min(500, static_cast<int>(ceil((pmax-pmin)/width))));
}

// code from Manuel Franco Sevilla to extract graphs from TH2 histograms
// https://github.com/CMS-SUS-XPAG/PlotsSMS/blob/0314f060280997093d827841b787c396dd64e27c/src/utilities.cpp#L24-L59
TGraph* getGraph(TH2* hobs, bool useLongest) {
  //hobs->Smooth();
  TGraph* graph = NULL;
  vector<double> vx, vy, vz;
  for(int binx=1; binx<=hobs->GetNbinsX(); ++binx){
    double x = hobs->GetXaxis()->GetBinCenter(binx);
    for(int biny=1; biny<=hobs->GetNbinsY(); ++biny){
      double y = hobs->GetYaxis()->GetBinCenter(biny);
      double z = hobs->GetBinContent(hobs->GetBin(binx,biny));
      vx.push_back(x);
      vy.push_back(y);
      vz.push_back(z);
    }
  }
    
  TGraph2D gsmooth("gsmooth", "", vx.size(), &vx.at(0), &vy.at(0), &vz.at(0));
  gsmooth.SetNpx(GetNumBins(vx, 1));
  gsmooth.SetNpy(GetNumBins(vy, 1));
  gsmooth.GetHistogram();
  TList *list = gsmooth.GetContourList(1.);
  TIter liter(list);
  // want longest contour in some cases and shortest in others.. have to set manually for each case when calling this function
  int max_points = 0;
  if (!useLongest) max_points = 991;
  for(int i = 0; i < list->GetSize(); ++i){
    TGraph *g = static_cast<TGraph*>(list->At(i));
    if(g == nullptr) continue;
    int n_points = g->GetN();
    //    cout<<"Contour with "<<n_points<<" points "<<endl;
    if((useLongest && n_points > max_points) || (!useLongest && n_points < max_points)){
      graph = g;
      max_points = n_points;
    }
  }

  return static_cast<TGraph*>(graph);
}

int makeLimitHist_TChiWH()
{

//  setTDRStyle();           
  gStyle->SetOptStat(0);
  TH1F * h_susyxsecs  = NULL;
  TFile * f_susyxsecs = NULL;

  //TString file_dir = "/home/users/siconglu/Run_Directory/CMSSW_8_1_0/src/WH_MET_limitsetting/scan40fbv9/";
  TString file_dir = "/home/users/siconglu/Run_Directory/CMSSW_8_1_0/src/WH_MET_limitsetting/scan_test/";
  f_susyxsecs = TFile::Open(file_dir+"xsec_susy_13tev.root","READ");
  h_susyxsecs = (TH1F*)f_susyxsecs->Get("h_xsec_c1n2")->Clone("h_susyxsecs");

  
  // More better palette
  const Int_t NRGBs = 5;
  const Int_t NCont = 255;
  
  double stops[] = {0.00, 0.34, 0.61, 0.84, 1.00};
  double red[]   = {0.50, 0.50, 1.00, 1.00, 1.00};
  double green[] = {0.50, 1.00, 1.00, 0.60, 0.50};
  double blue[]  = {1.00, 1.00, 0.50, 0.40, 0.50};
  TColor::CreateGradientColorTable(NRGBs, stops, red, green, blue, NCont);
  gStyle->SetNumberContours(NCont);
  
  TFile * f_rvalues = TFile::Open(file_dir+"r-values_tchwh.root","READ");  
   
  
  TH2F * massplane        = (TH2F*) f_rvalues->Get("hExp")   -> Clone("massplane");
  TH2F * massplane_obs    = (TH2F*) f_rvalues->Get("hObs")   -> Clone("massplane_obs");
  TH2F * massplane_obs_up = (TH2F*) f_rvalues->Get("hObs")   -> Clone("massplane_obs_up");
  TH2F * massplane_obs_dn = (TH2F*) f_rvalues->Get("hObs")   -> Clone("massplane_obs_dn");
  TH2F * massplane_exp_up = (TH2F*) f_rvalues->Get("hExp1p") -> Clone("massplane_exp_up");
  TH2F * massplane_exp_dn = (TH2F*) f_rvalues->Get("hExp1m") -> Clone("massplane_exp_dn");
  TH2F * massplane_exp_up2 = (TH2F*) f_rvalues->Get("hExp2p") -> Clone("massplane_exp_up2");
  TH2F * massplane_exp_dn2 = (TH2F*) f_rvalues->Get("hExp2m") -> Clone("massplane_exp_dn2");
  // TH2F * massplane_xsec   = new TH2F("massplane_xsec","", 27,25,1375,25,75.0,1325.0);

  TH2F * massplane_xsec   = (TH2F*) massplane_obs-> Clone("massplane_xsec");
  TH2F * efficiency       = (TH2F*) massplane    -> Clone("efficiency"    );

  TH2F * h_axis = new TH2F("h_axis","",650,100,650,350,0,350);

  double contourn[1];
  contourn[0] = 1.0;

  TH2F * contourplot = dynamic_cast<TH2F*>(massplane->Clone("contourplot"));

  h_axis->GetXaxis()->SetRangeUser(100,650);
  h_axis->GetYaxis()->SetRangeUser(0,300);

  h_axis->GetXaxis()->SetLabelSize(0.035);
  h_axis->GetXaxis()->SetNdivisions(508);
  h_axis->GetYaxis()->SetLabelSize(0.035);
  h_axis->GetXaxis()->SetTitle("m_{#tilde{#chi}^{#pm}_{1}} = m_{#tilde{#chi}^{0}_{2}} [GeV]");
  h_axis->GetYaxis()->SetTitle("m_{#tilde{#chi}^{0}_{1}} [GeV]");
  
  massplane_xsec->GetZaxis()->SetTitle("95% CL upper limit on #sigma [pb]");
  massplane_xsec->GetZaxis()->SetRangeUser(1e-3,10);
  massplane_xsec->GetZaxis()->SetLabelSize(0.035);

  TCanvas *c_massplane = new TCanvas("c_massplane", "", 800, 800);
  c_massplane->cd();
  TPad *padt = new TPad("p_tex", "p_tex", 0.0, 0.0, 1.0, 1.0);
  padt->SetTopMargin(0.08);
  padt->SetBottomMargin(0.16);
  padt->SetRightMargin(0.17);
  padt->SetLeftMargin(0.18);
  padt->Draw();
  padt->cd();
  padt->SetLogz();

  //edit here
  h_axis->Draw("axis");
  //  massplane_xsec->Draw("colz same");
  int bin_225_1;
  float bin_225_1_content;
  int bin_250_1;
  float bin_250_1_content;
  int bin_200_1;
  float bin_200_1_content;

  contourplot->SetContour(1, contourn);
  contourplot->SetLineWidth(4);
  contourplot->SetLineStyle(2);
  contourplot->SetLineColor(kRed);
  bin_200_1 = contourplot->FindBin(200,1);
  bin_200_1_content = contourplot->GetBinContent(bin_200_1);
  bin_225_1 = contourplot->FindBin(225,1);
  bin_225_1_content = contourplot->GetBinContent(bin_225_1);
  contourplot->Smooth();
  contourplot->SetBinContent(bin_225_1,bin_225_1_content);
  contourplot->SetBinContent(bin_200_1,bin_200_1_content);

  massplane_exp_up->SetContour(1, contourn);
  massplane_exp_up->SetLineWidth(2);
  massplane_exp_up->SetLineStyle(2);
  massplane_exp_up->SetLineColor(kRed);
  bin_225_1 = massplane_exp_up->FindBin(225,1);
  bin_225_1_content = massplane_exp_up->GetBinContent(bin_225_1);
  bin_200_1 = massplane_exp_up->FindBin(200,1);
  bin_200_1_content = massplane_exp_up->GetBinContent(bin_200_1);
  massplane_exp_up->Smooth();
  massplane_exp_up->SetBinContent(bin_225_1,bin_225_1_content);
  massplane_exp_up->SetBinContent(bin_200_1,bin_200_1_content);

  massplane_exp_dn->SetContour(1, contourn);
  massplane_exp_dn->SetLineWidth(2);
  massplane_exp_dn->SetLineStyle(2);
  massplane_exp_dn->SetLineColor(kRed);
  bin_200_1 = massplane_exp_dn->FindBin(200,1);
  bin_200_1_content = massplane_exp_dn->GetBinContent(bin_200_1);
  bin_225_1 = massplane_exp_dn->FindBin(225,1);
  bin_225_1_content = massplane_exp_dn->GetBinContent(bin_225_1);
  massplane_exp_dn->Smooth();
  massplane_exp_dn->SetBinContent(bin_225_1,bin_225_1_content);
  massplane_exp_dn->SetBinContent(bin_200_1,bin_200_1_content);

  massplane_exp_up2->SetContour(1, contourn);
  massplane_exp_up2->SetLineWidth(2);
  massplane_exp_up2->SetLineStyle(3);
  massplane_exp_up2->SetLineColor(kRed);
  massplane_exp_up2->Smooth();
  massplane_exp_dn2->SetContour(1, contourn);
  massplane_exp_dn2->SetLineWidth(2);
  massplane_exp_dn2->SetLineStyle(3);
  massplane_exp_dn2->SetLineColor(kRed);
  massplane_exp_dn2->Smooth();
  
  massplane_obs->SetContour(1, contourn);
  massplane_obs->SetLineWidth(4);
  massplane_obs->SetLineColor(kBlack);
  massplane_obs->SetLineStyle(1);
  bin_200_1 = massplane_obs->FindBin(200,1);
  bin_200_1_content = massplane_obs->GetBinContent(bin_200_1);
  bin_225_1 = massplane_obs->FindBin(225,1);
  bin_225_1_content = massplane_obs->GetBinContent(bin_225_1);
  bin_250_1 = massplane_obs->FindBin(250,1);
  bin_250_1_content = massplane_obs->GetBinContent(bin_250_1);
  massplane_obs->Smooth();
  massplane_obs->SetBinContent(bin_200_1,bin_200_1_content);
  massplane_obs->SetBinContent(bin_225_1,bin_225_1_content);
  massplane_obs->SetBinContent(bin_250_1,bin_250_1_content);

  massplane_obs_up->SetContour(1, contourn);
  massplane_obs_up->SetLineWidth(2);
  massplane_obs_up->SetLineColor(kBlack);
  bin_200_1 = massplane_obs_up->FindBin(200,1);
  bin_200_1_content = massplane_obs_up->GetBinContent(bin_200_1);
  bin_225_1 = massplane_obs_up->FindBin(225,1);
  bin_225_1_content = massplane_obs_up->GetBinContent(bin_225_1);
  bin_250_1 = massplane_obs_up->FindBin(250,1);
  bin_250_1_content = massplane_obs_up->GetBinContent(bin_250_1);
  massplane_obs_up->Smooth();
  massplane_obs_up->SetBinContent(bin_200_1,bin_200_1_content);
  massplane_obs_up->SetBinContent(bin_225_1,bin_225_1_content);
  massplane_obs_up->SetBinContent(bin_250_1,bin_250_1_content);

  massplane_obs_dn->SetContour(1, contourn);
  massplane_obs_dn->SetLineWidth(2);
  massplane_obs_dn->SetLineColor(kBlack);
  bin_200_1 = massplane_obs_dn->FindBin(200,1);
  bin_200_1_content = massplane_obs_dn->GetBinContent(bin_200_1);
  bin_225_1 = massplane_obs_dn->FindBin(225,1);
  bin_225_1_content = massplane_obs_dn->GetBinContent(bin_225_1);
  bin_250_1 = massplane_obs_dn->FindBin(250,1);
  bin_250_1_content = massplane_obs_dn->GetBinContent(bin_250_1);
  massplane_obs_dn->Smooth();
  massplane_obs_dn->SetBinContent(bin_200_1,bin_200_1_content);
  massplane_obs_dn->SetBinContent(bin_225_1,bin_225_1_content);
  massplane_obs_dn->SetBinContent(bin_250_1,bin_250_1_content);

  // multiply by susy xsec
  for( int binx = 1; binx <= massplane_xsec->GetNbinsX(); binx++ ){
  	for( int biny = 1; biny <= massplane_xsec->GetNbinsY(); biny++ ){
	  int mgluino = massplane_xsec->GetXaxis()->GetBinCenter(binx);
	  if (mgluino < 100) continue; // not in scan, no xsecs available
	  int truebin = massplane_xsec->GetBin(binx,biny);
	  // massplane_xsec->SetBinContent(truebin, massplane_xsec->GetBinContent(truebin)/(0.19175)*h_susyxsecs->GetBinContent(h_susyxsecs->FindBin(mgluino)));
	  double xsec = h_susyxsecs->GetBinContent(h_susyxsecs->FindBin(mgluino));
	  double xsec_relerr = h_susyxsecs->GetBinError(h_susyxsecs->FindBin(mgluino))/xsec;
	  massplane_xsec->SetBinContent(truebin, massplane_xsec->GetBinContent(truebin)*xsec);
	  massplane_obs_up->SetBinContent(truebin, massplane_obs->GetBinContent(truebin)*(1. + xsec_relerr));
	  massplane_obs_dn->SetBinContent(truebin, massplane_obs->GetBinContent(truebin)*(1. - xsec_relerr));
	}
  }

  massplane_xsec->Draw("samecolz");
////////////////  contourplot->Draw("samecont3");
  // // contourplot->Draw("colz");
  TGraph *gr1;
  massplane_obs->Draw("samecont3");
  massplane_obs_up->Draw("samecont3");
  massplane_obs_dn->Draw("samecont3");
  massplane_exp_up->Draw("samecont3");
  massplane_exp_dn->Draw("samecont3");
  
  contourplot->Draw("samecont3");

  // extract contours as graphs and save to file for aux material
  TFile* fg = new TFile("limits_TChiWH.root","RECREATE");
  fg->cd();
  TGraph* g_exp = getGraph(contourplot,0);
  g_exp->SetName("gExp");
  g_exp->Write();
  TGraph* g_obs = getGraph(massplane_obs,0);
  g_obs->SetName("gObs");
  g_obs->Write();
  TGraph* g_obs_up = getGraph(massplane_obs_up,0);
  g_obs_up->SetName("gObsUp");
  g_obs_up->Write();
  TGraph* g_obs_dn = getGraph(massplane_obs_dn,0);
  g_obs_dn->SetName("gObsDn");
  g_obs_dn->Write();
  // --- expected up has no exclusion, no contour
  // TGraph* g_exp_up = getGraph(massplane_exp_up,1);
  // g_exp_up->SetName("gExpUp");
  // g_exp_up->Write();
  TGraph* g_exp_dn = getGraph(massplane_exp_dn,1);
  g_exp_dn->SetName("gExpDn");
  g_exp_dn->Write();
  massplane_xsec->SetName("hObsXsec");
  massplane_xsec->Write();
  fg->Close();
  delete fg;
  
  TLine * diag_0 = new TLine(125,62,400,325);
  diag_0->SetLineWidth(20);
  diag_0->SetLineColor(kWhite);
  diag_0->SetLineStyle(1);
  diag_0->Draw("same");

  diag_0 = new TLine(75,16.5,400,325);
  diag_0->SetLineWidth(22);
  diag_0->SetLineColor(kWhite);
  diag_0->SetLineStyle(1);
  diag_0->Draw("same");

  //diag_0 = new TLine(1100,1150,2000,2050);
  diag_0 = new TLine(200,125,400,325);
  diag_0->SetLineWidth(21);
  diag_0->SetLineColor(kWhite);
  diag_0->SetLineStyle(1);
  diag_0->Draw("same");

  //diag_0 = new TLine(1100,1170,2000,2070);
  diag_0 = new TLine(100,25,450,370);
  diag_0->SetLineWidth(9);
  diag_0->SetLineColor(kWhite);
  diag_0->SetLineStyle(1);
  //diag_0->Draw("same");

  diag_0 = new TLine(1100,1190,2000,2090);
  diag_0->SetLineWidth(7);
  diag_0->SetLineColor(kWhite);
  diag_0->SetLineStyle(1);
  //diag_0->Draw("same");

  padt->RedrawAxis();

  TBox * box = new TBox(100,222,650,300);
  box->SetFillColor(kWhite);
  box->Draw("same");

  TLegend *l1 = new TLegend(0.18, 0.77, 0.65, 0.83);    
  l1->SetLineColor(kWhite);    
  l1->SetTextFont(42);    
  l1->SetTextSize(0.033);
  l1->SetShadowColor(kWhite);    
  l1->SetFillColor(kWhite);    
  l1->AddEntry(massplane_obs , "Observed limit, #pm 1 #sigma_{theory}"            , "l");
  l1->AddEntry(contourplot , "Expected limit, #pm 1 #sigma_{exp.}", "l");
  l1->Draw("same");

//  TLatex *clstex1 = NULL;
//  clstex1 = new TLatex(0.315,0.74, "(-1 s.d._{exp.} no exclusion)" );    
//  clstex1->SetNDC();    
//  clstex1->SetTextSize(0.032);    
//  clstex1->SetLineWidth(2);
//  clstex1->SetTextFont(42);    
//  clstex1->Draw();
  
  TLine * top_margin = new TLine(100,300,650,300);
  top_margin->SetLineWidth(4);
  top_margin->SetLineColor(kBlack);
  top_margin->SetLineStyle(1);
  top_margin->Draw("same");

  TLine * bot_margin = new TLine(100,222,650,222);
  bot_margin->SetLineWidth(4);
  bot_margin->SetLineColor(kBlack);
  bot_margin->SetLineStyle(1);
  bot_margin->Draw("same");

  TLine * lef_margin = new TLine(100,222,100,300);
  lef_margin->SetLineWidth(4);
  lef_margin->SetLineColor(kBlack);
  lef_margin->SetLineStyle(1);
  lef_margin->Draw("same");

  TLine * rig_margin = new TLine(650,222,650,300);
  rig_margin->SetLineWidth(4);
  rig_margin->SetLineColor(kBlack);
  rig_margin->SetLineStyle(1);
  rig_margin->Draw("same");

  // massplane_xsec->Draw("samecolz");
  // TLine * diag = new TLine(975,775,1575,1375);
  // diag->SetLineWidth(5);
  // diag->SetLineStyle(9);
  // diag->Draw("same");

  TLatex *prctex = NULL;
  prctex = new TLatex(0.215,0.88, "pp #rightarrow #tilde{#chi}^{#pm}_{1} #tilde{#chi}^{0}_{2};" );    
  prctex->SetNDC();    
  prctex->SetTextSize(0.032);    
  prctex->SetLineWidth(2);
  prctex->SetTextFont(42);    
  prctex->Draw();
  TLatex *prctex2 = NULL;
  prctex2 = new TLatex(0.4,0.88, "#tilde{#chi}^{#pm}_{1}#rightarrow W^{#pm} #tilde{#chi}_{1}^{0}, #tilde{#chi}^{0}_{2}#rightarrow H #tilde{#chi}_{1}^{0}" );    
  prctex2->SetNDC();    
  prctex2->SetTextSize(0.032);    
  prctex2->SetLineWidth(2);
  prctex2->SetTextFont(42);    
  prctex2->Draw();

  TLatex *clstex = NULL;
  clstex = new TLatex(0.215,0.84, "NLO + NLL exclusion" );    
  clstex->SetNDC();    
  clstex->SetTextSize(0.032);    
  clstex->SetLineWidth(2);
  clstex->SetTextFont(42);    
  clstex->Draw();


  TLatex *cmstex = NULL;
  cmstex = new TLatex(0.575,0.94, "35.9 fb^{-1} (13 TeV)" );    
  cmstex->SetNDC();    
  cmstex->SetTextSize(0.04);    
  cmstex->SetLineWidth(2);
  cmstex->SetTextFont(42);    
  cmstex->Draw();

  TLatex *cmstexbold = NULL;
  cmstexbold = new TLatex(0.18,0.94, "CMS" );    
  cmstexbold->SetNDC();    
  cmstexbold->SetTextSize(0.05);    
  cmstexbold->SetLineWidth(2);
  cmstexbold->SetTextFont(62);    
  cmstexbold->Draw();

  cmstexbold = new TLatex(0.29,0.94, "Internal" );    
  cmstexbold->SetNDC();    
  cmstexbold->SetTextSize(0.0375);    
  cmstexbold->SetLineWidth(2);
  cmstexbold->SetTextFont(52);    
  cmstexbold->Draw();
  
  TString plot_dir = "/home/users/siconglu/CMSTAS/software/niceplots/WH_Expected_Exclusion/";
  c_massplane->SaveAs(plot_dir+"TChiWHlnubb_Exclusion_13TeV_test_new.pdf");

  return 0;
}

