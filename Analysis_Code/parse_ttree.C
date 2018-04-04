#include <iostream>
#include <fstream>
#include <string>
#include <dirent.h>
#include <time.h>
using namespace std;

int parse_one_grid(string txt_file_name){
    std::string tmp;
    int grid_chargino, grid_lsp;
    char c;
    std::stringstream ss(txt_file_name);
    ss >> grid_chargino >> c >> grid_lsp>>tmp;
    cout<<grid_chargino<<"   "<<grid_lsp<<endl;

    TFile *oldfile;
    oldfile = new TFile("../root_file_temp/Grid_20180404/Grid_Merged.root");
    TTree *oldtree = (TTree*)oldfile->Get("t");
    Long64_t nentries = oldtree->GetEntries();
    
    ostringstream x_convert;
    x_convert << grid_chargino;
    string s1 = x_convert.str();
    x_convert.str("");
    x_convert.clear();
    x_convert << grid_lsp;
    string s2 = x_convert.str();
    string tmp_str = "../root_file_temp/Grid_20180404/TChiWH_"+s1+"_"+s2+".root";
    TString file_name = tmp_str;
    cout<<file_name<<endl;
    
    TFile *newfile = new TFile(file_name,"recreate");
    TTree *newtree = oldtree->CloneTree(0);
    
    ifstream fs("../root_file_temp/Grid_20180404/entry_location/"+txt_file_name);
    int i;
    int total_num = 0;
    while (fs >> i) {
        oldtree->GetEntry(i);
        newtree->Fill();
        total_num++;
    }    
    cout<<"Total number of entries:"<<total_num<<endl;
    newtree->AutoSave();
    delete oldfile;
    delete newfile;
    fs.close();

    return EXIT_SUCCESS;
}

void parse_ttree(){
    string path = "../root_file_temp/Grid_20180404/entry_location/";
    DIR*    dir;
    dirent* pdir;
    dir = opendir(path.c_str());
    
    int processed = 0;
    int total = 234;
    time_t seconds, new_seconds, initial_seconds;
    initial_seconds = time (NULL);
    while (pdir = readdir(dir)) {
        string txt_file_name = pdir->d_name;
        if (txt_file_name.find(".txt") != std::string::npos){            
            seconds = time (NULL);
            
            cout<<txt_file_name<<endl;
            parse_one_grid(txt_file_name);
            processed++;
        
            new_seconds = time (NULL);
            cout<<"Minutes since last loop: "<<(new_seconds - seconds)/60.<<endl;
            cout<<"Minutes remaining..."<<(new_seconds - initial_seconds)/60.*(total-processed)/processed<<endl;
        }
        
    }
    
}

