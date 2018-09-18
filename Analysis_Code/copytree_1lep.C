void copytree_1lep(TString old_dir, TString new_dir) {
   //Get old file, old tree and set top branch address
   TFile *oldfile = new TFile(old_dir);
   TTree *oldtree = (TTree*)oldfile->Get("t");
   
   int is1lep;
   oldtree->SetBranchAddress("is1lep",&is1lep);

   //Create a new file + a clone of old tree in new file
   TFile *newfile = new TFile(new_dir,"recreate");
   TTree *newtree = oldtree->CloneTree(0);
   
   Long64_t nentries = oldtree->GetEntries();
   cout<<"Total Event #:"<<nentries<<endl;
   for (Long64_t i=0;i<nentries; i++) {
      if (i%10000 == 0) cout<<i<<endl;
      oldtree->GetEntry(i);
      if (is1lep) newtree->Fill();
   }
   newtree->AutoSave();
   delete oldfile;
   delete newfile;
}