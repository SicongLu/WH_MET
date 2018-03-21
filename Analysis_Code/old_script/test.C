#include <iostream>
#include <vector>
#include <string> 
#include "TCanvas.h"
#include "TChain.h"
#include "TFile.h"
#include "TList.h"
#include "TRandom3.h"
#include "TTree.h"
#include "TTreeIndex.h"

/*
Modified by Sicong, July 2017
*/

void test(){

  char inputfile[300];
  sprintf(inputfile,"../root_file_temp/Mia_20180223/TChiWH_350_100.root");

  TFile *input = TFile::Open(inputfile);
  TTree* output = (TTree*)input->Get("t");
  vector<bool> *ak4pfjets_passMEDbtag = 0;
  output->SetBranchAddress( "ak4pfjets_passMEDbtag", &ak4pfjets_passMEDbtag );
  for (Long64_t ievt=0; ievt<10;ievt++) {
    if (ievt%1000 == 0) std::cout << "--- ... Processing event: " << ievt << std::endl;
    output->GetEntry(ievt);
    cout<<ak4pfjets_passMEDbtag->at(1)<<ak4pfjets_passMEDbtag->at(0)<<endl;
  }
return; }