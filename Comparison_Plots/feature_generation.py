'''
This scripts in tends to create relevant features to make future analysis faster.
'''
import ROOT
import numpy
import array
ROOT.gStyle.SetOptStat(0);
ROOT.gStyle.SetOptTitle(0);

def feature_generate(file_name, file_name_out):
    '''
    This function shall create useful features to the designated .root file. 
    '''
    #Get Files
    print(file_name)
    f = ROOT.TFile(file_name)
    t = f.Get("t")
    f_out = ROOT.TFile(file_name_out, 'recreate' )
    
#    #Only read in relevant variables to increase the speed.
#    cut_var_list = ["ngoodleps","nvetoleps","PassTrackVeto","PassTauVeto","ngoodjets",\
#    "ngoodbtags","mbb","mct","pfmet","mt_met_lep","ak4pfjets_passMEDbtag",\
#    "ak4pfjets_CSV"]
#    plot_var_list = ["scale1fb","ak4pfjets_leadMEDbjet_p4"]
#    used_var_list = cut_var_list + plot_var_list
#    LV_var_list = ["ak4pfjets_p4"]
#    #Set the branch status
#    t.SetBranchStatus("*",0)
#    for used_var in used_var_list:
#        t.SetBranchStatus(used_var,1)
#    #For Math.LorentzVector we need more branches inside
#    LV_suffix_list = [".fCoordinates.fX",".fCoordinates.fY",".fCoordinates.fZ",\
#    ".fCoordinates.fT"] #For those that are Math.LorentzVector
#    for LV_var in LV_var_list:
#        for LV_suffix in LV_suffix_list:       
#            t.SetBranchStatus(LV_var+LV_suffix,1)
            
    #Histogram_list
    pt_hist = ROOT.TH1F("pt_hist","pt_hist",20,0,400)
    pt_hist.SetDirectory(0);
    ROOT.TH1.AddDirectory(ROOT.kFALSE); 
    form_passMEDbtag_list = []
    for i in range(12):
        form_passMEDbtag_list.append(ROOT.TTreeFormula("ak4pfjets_passMEDbtag_%d"%i,\
        "ak4pfjets_passMEDbtag[%d]"%i,t))   
    
    #maxn = 10
    #n = array( 'i', [ 0 ] )
    #d = array( 'f', maxn*[ 0. ] )
    #t.Branch( 'mynum', n, 'mynum/I' )
    #t.Branch( 'myval', d, 'myval[mynum]/F' )
    
    ptbb = array.array( 'f', [ 0 ] )
    
    t_out = t.CloneTree(0)
    t_out.Branch( 'ptbb', ptbb, 'ptbb/F' )
        
    event_num = t.GetEntries()
    print("Total: %.0f events..." % (event_num))
    for i_evt in range(event_num):
        if i_evt % 10000 == 0:
            print("Processing %.0f events..." % (i_evt))
        t.GetEntry(i_evt)
        
        #Reconstruction 
        lead_btag_jet = t.ak4pfjets_leadMEDbjet_p4
        
        jet_list = t.ak4pfjets_p4
        jet_num = len(jet_list)                                                            
        if not(t.ngoodbtags == 2):
            ptbb[0] = -9999
            t_out.Fill()    
            continue;
        for i_jet in range(jet_num):
            if (form_passMEDbtag_list[i_jet].GetNdata() > 0): 
            #It is a temporary solution to a known issue in ROOT, see appendix for details 
                jet_btag_bool = form_passMEDbtag_list[i_jet].EvalInstance()
            if jet_btag_bool == 0:
                continue;
            second_btag_jet = jet_list[i_jet]
        di_bjet = lead_btag_jet+second_btag_jet
        ptbb[0] = di_bjet.Pt()
        t_out.Fill()
            
    t_out.AutoSave()
    f.Close()
    f_out.Close()
    #Print Efficiency Table
    return 0;
#Main Function
from create_file_list import get_files
MC_list = get_files()
file_location_out = "../root_file_temp/Sicong_20180228/"

for MC in MC_list[0:7]:
    MC_name = MC["name"]
    file_name_list = MC["file_name_list"]
    for file_name in file_name_list[0:1]:
        file_name_out = file_location_out + file_name[file_name.rfind("/")+1:]
        feature_generate(file_name, file_name_out)

