#include "TFile.h"
#include "TString.h"
#include <fstream>
#include <iostream>

void draw_susy_xsecs_13tev() {
  
  gStyle->SetPadTopMargin(0.08);
  gStyle->SetPadBottomMargin(0.12);
  gStyle->SetPadLeftMargin(0.15);
  gStyle->SetPadRightMargin(0.05);
    
  TFile* fin = new TFile("xsec_susy_13tev_graphs.root");

  TCanvas* c = new TCanvas("c","c");
  c->SetLogy();
  
  TH2F* h_axes = new TH2F("h_axes",";Mass [GeV]; #sigma, 13 TeV [pb]",500,100,1800,1000,1e-3,400);
  h_axes->GetYaxis()->SetTitleOffset(1.15);
  h_axes->Draw();
  
  TGraphErrors* g_xsec_gluino = (TGraphErrors*) fin->Get("g_xsec_gluino");
  g_xsec_gluino->SetFillColor(kRed);
  g_xsec_gluino->Draw("3 same");

  TGraphErrors* g_xsec_squark = (TGraphErrors*) fin->Get("g_xsec_squark");
  g_xsec_squark->SetFillColor(kBlue);
  g_xsec_squark->Draw("3 same");

  TGraphErrors* g_xsec_stop = (TGraphErrors*) fin->Get("g_xsec_stop");
  g_xsec_stop->SetFillColor(kGreen+2);
  g_xsec_stop->Draw("3 same");

  TGraphErrors* g_xsec_c1n2 = (TGraphErrors*) fin->Get("g_xsec_c1n2");
  g_xsec_c1n2->SetFillColor(kMagenta);
  g_xsec_c1n2->Draw("3 same");

  TGraphErrors* g_xsec_c1c1 = (TGraphErrors*) fin->Get("g_xsec_c1c1");
  g_xsec_c1c1->SetFillColor(kOrange+1);
  g_xsec_c1c1->Draw("3 same");

  TGraphErrors* g_xsec_slep = (TGraphErrors*) fin->Get("g_xsec_slep");
  g_xsec_slep->SetFillColor(kCyan+1);
  g_xsec_slep->Draw("3 same");

  //  TLegend* leg = new TLegend(0.72,0.59,0.90,0.89);
  //TLegend* leg = new TLegend(0.55,0.67,0.90,0.89);
  TLegend* leg = new TLegend(0.55,0.57,0.90,0.89);
  leg->AddEntry(g_xsec_gluino,"#tilde{g}#tilde{g}","f");
  leg->AddEntry(g_xsec_squark,"#tilde{q}#tilde{q}","f");
  leg->AddEntry(g_xsec_stop,"#tilde{t}#tilde{t}","f");
  leg->AddEntry(g_xsec_c1n2,"#tilde{#chi}_{1}^{#pm}#tilde{#chi}_{2}^{0}","f");
  leg->AddEntry(g_xsec_c1c1,"#tilde{#chi}_{1}^{#pm}#tilde{#chi}_{1}^{#mp}","f");
  leg->AddEntry(g_xsec_slep,"#tilde{l}^{#pm}_{L}#tilde{l}^{#mp}_{L}","f");
  leg->SetNColumns(2);
  leg->SetEntrySeparation(0.35);
  leg->Draw("same");

  c->SaveAs("c_xsec_susy_13tev_ewk.eps");
  c->SaveAs("c_xsec_susy_13tev_ewk.pdf");
}
