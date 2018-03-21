'''
This scripts in tends to create relevant features to make future analysis faster.
'''
import ROOT
import numpy
import array
import math
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
    new_mct = array.array( 'f', [ 0 ] )
    new_mbb = array.array( 'f', [ 0 ] )
    new_met = array.array( 'f', [ 0 ] )
    new_met_phi = array.array( 'f', [ 0 ] )
    new_mt = array.array( 'f', [ 0 ] )
    nbtag_loose = array.array( 'i', [ 0 ] )
    nbtag_med = array.array( 'i', [ 0 ] )
    
    t_out = t.CloneTree(0)
    t_out.Branch( 'ptbb', ptbb, 'ptbb/F' )
    t_out.Branch( 'new_mct', new_mct, 'new_mct/F' )
    t_out.Branch( 'new_met', new_met, 'new_met/F' )
    t_out.Branch( 'new_met_phi', new_met_phi, 'new_met_phi/F' )
    t_out.Branch( 'new_mt', new_mt, 'new_mt/F' )
    t_out.Branch( 'new_mbb', new_mbb, 'new_mbb/F' )
    t_out.Branch( 'nbtag_loose', nbtag_loose, 'nbtag_loose/I' )
    t_out.Branch( 'nbtag_med', nbtag_med, 'nbtag_med/I' )
    
    #Note that the dijet system requires 2 pass loose btag and at least 1 pass med btag.
    BTAGWP = 0.5426; #Loose btag working point
    mBTAGWP = 0.8484; #Medium btag working point
    event_num = t.GetEntries()
    print("Total: %.0f events..." % (event_num))
    n_err_mct = 0
    for i_evt in range(event_num):
        if i_evt % 10000 == 0:
            print("Processing %.0f events..." % (i_evt))
        t.GetEntry(i_evt)
        
        #Reconstruction
        nbtag_loose[0] = 0
        nbtag_med[0] = 0
        ngoodjet_pt_eta = 0
        bjet_index = []
        for i_jet in range(len(t.ak4pfjets_p4)):
            if not(t.ak4pfjets_p4.at(i_jet).Pt()>30 and \
            t.ak4pfjets_p4.at(i_jet).Eta()<2.4 and \
            t.ak4pfjets_loose_pfid.at(i_jet)): 
                continue;
            ngoodjet_pt_eta += 1
            if t.ak4pfjets_CSV.at(i_jet)>mBTAGWP:
                nbtag_med[0]+=1
            if t.ak4pfjets_CSV.at(i_jet)>BTAGWP:
                nbtag_loose[0]+=1
                bjet_index.append(i_jet)
                if nbtag_loose[0] == 1:
                    di_bjet = t.ak4pfjets_p4.at(i_jet)
                else:
                    di_bjet = di_bjet + t.ak4pfjets_p4.at(i_jet)
        #New MET
        new_met[0] = 1/2.*(t.pfmet+t.genmet)
        pfmet_vec = ROOT.TVector3()
        pfmet_vec.SetPtEtaPhi(t.pfmet, 0, t.pfmet_phi)
        genmet_vec = ROOT.TVector3()
        genmet_vec.SetPtEtaPhi(t.genmet, 0, t.genmet_phi)
        
        new_met_vec = 1/2.*(pfmet_vec+genmet_vec)
        new_met[0] = new_met_vec.Pt()
        new_met_phi[0]  = new_met_vec.Phi()
        
        mt_dphi = t.lep1_p4.Phi() -new_met_phi[0]
        if mt_dphi>math.pi: mt_dphi = 2*math.pi - mt_dphi 
        
        new_mt[0] = 2*math.sqrt(t.lep1_p4.Pt()*new_met[0])*abs(math.sin(mt_dphi/2.))
        if len(bjet_index)<2:
            new_mct[0] = -999
            new_mbb[0] = -999
        else:
            ptb1 = t.ak4pfjets_p4.at(bjet_index[0]).Pt()
            ptb2 = t.ak4pfjets_p4.at(bjet_index[1]).Pt()
            phib1 = t.ak4pfjets_p4.at(bjet_index[0]).Phi()
            phib2 = t.ak4pfjets_p4.at(bjet_index[1]).Phi()
            dphibb = abs(phib1-phib2)
            if dphibb>math.pi: dphibb = 2*math.pi-dphibb
            new_mct[0] = math.sqrt(2*ptb1*ptb2*(1+math.cos(dphibb)))
            new_mbb[0] = di_bjet.M()

                  
        if ngoodjet_pt_eta!=t.ngoodjets and t.ngoodjets>=0:
            print("Error! ngoodjets!!!")
            print(ngoodjet_pt_eta, t.ngoodjets)
        if (nbtag_loose[0] == 2 and nbtag_med[0] >=1 and ngoodjet_pt_eta == 2):
            ptbb[0] = di_bjet.Pt()
        else:
            ptbb[0] = -999
        t_out.Fill()
    print("n_err_mct%.0f"%n_err_mct)  
    t_out.AutoSave()
    f.Close()
    f_out.Close()
    return 0;
#Main Function
from create_file_list import get_files
MC_list = get_files()
file_location_out = "../root_file_temp/Sicong_20180228/"
for MC in MC_list:#[6:]:
    MC_name = MC["name"]
    if not(MC_name == "rare"):    continue;
    print(MC_name)
    file_name_list = MC["file_name_list"]
    
    for file_name in file_name_list:
        tmp_file_name = file_name[file_name.rfind("/")+1:]
        if not( "WZTo2L" in tmp_file_name):
            continue;
        file_name_out = file_location_out + file_name[file_name.rfind("/")+1:]
        feature_generate(file_name, file_name_out)
