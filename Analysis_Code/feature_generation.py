'''
This scripts in tends to create relevant features to make future analysis faster.
'''
import ROOT
import numpy
import array
import math
import time
def feature_generate(file_name, file_name_out):
    '''
    This function shall create useful features to the designated .root file.
    Since there is some definition discrepancies. This shall be the most recent 
    definition of features like mct, mt, mbb, etc.
    Note that this function does not do any skimming, so it is rather slow!
    Do not run at work... unless there is a batch system.
    '''
    #Get Files
    print(file_name)
    f = ROOT.TFile(file_name)
    t = f.Get("t")
    f_out = ROOT.TFile(file_name_out, 'recreate' )

    #New features branches. MET related.
    new_met = array.array( 'f', [ 0 ] )
    new_met_phi = array.array( 'f', [ 0 ] )
    new_mt = array.array( 'f', [ 0 ] )
    
    #Btagging related
    nbtag_loose = array.array( 'i', [ 0 ] )
    nbtag_med = array.array( 'i', [ 0 ] )
    ptbb = array.array( 'f', [ 0 ] )
    new_mct = array.array( 'f', [ 0 ] )
    new_mbb = array.array( 'f', [ 0 ] )
    
    t_out = t.CloneTree(0)
    t_out.Branch( 'nbtag_loose', nbtag_loose, 'nbtag_loose/I' )
    t_out.Branch( 'nbtag_med', nbtag_med, 'nbtag_med/I' )
    t_out.Branch( 'new_met', new_met, 'new_met/F' )
    t_out.Branch( 'new_met_phi', new_met_phi, 'new_met_phi/F' )
    t_out.Branch( 'new_mt', new_mt, 'new_mt/F' )
    t_out.Branch( 'ptbb', ptbb, 'ptbb/F' )
    t_out.Branch( 'new_mct', new_mct, 'new_mct/F' )
    t_out.Branch( 'new_mbb', new_mbb, 'new_mbb/F' )
    
    #Note that the dijet system requires 2 pass loose btag and at least 1 pass med btag.
    BTAGWP = 0.5426; #Loose btag working point
    mBTAGWP = 0.8484; #Medium btag working point
    event_num = t.GetEntries()
    start_time = time.time()
    print("Total: %.0f events..." % (event_num))
    for i_evt in range(event_num):
        if i_evt % 10000 == 0 and i_evt != 0:
            current_time = time.time()
            minutes_left = 1.*(current_time - start_time)/i_evt*(event_num-i_evt)/60.
            print("Processing %.0f events..." % (i_evt))
            print("Estimated minutes left: %.1f..." % minutes_left)            
        t.GetEntry(i_evt)
        #Re-do the Met related:
        if "TChiWH_" in file_name:#For fastsim, it is recommended to use the new met. 
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
        else:
            new_met[0] = t.pfmet
            new_mt[0] = t.mt_met_lep
        
        #Reconstruction of the two b system.
        nbtag_loose[0] = 0
        nbtag_med[0] = 0
        ngoodjets = 0 #Local variable to check if the definition is consistent.
        bjet_index = []
        for i_jet in range(len(t.ak4pfjets_p4)):
            if not(t.ak4pfjets_p4.at(i_jet).Pt()>30 and \
            t.ak4pfjets_p4.at(i_jet).Eta()<2.4 and \
            t.ak4pfjets_loose_pfid.at(i_jet)): 
                continue;
            ngoodjets += 1;
            if t.ak4pfjets_CSV.at(i_jet)>mBTAGWP:
                nbtag_med[0]+=1
            if t.ak4pfjets_CSV.at(i_jet)>BTAGWP:
                nbtag_loose[0]+=1
                bjet_index.append(i_jet)
                if nbtag_loose[0] == 1: #First jet 
                    di_bjet = t.ak4pfjets_p4.at(i_jet)
                else: #Second jet
                    di_bjet = di_bjet + t.ak4pfjets_p4.at(i_jet)
        if len(bjet_index)<2: #If there is not enouth bjets
            if len(t.ak4pfjets_p4)<2: #If there is not enough jets
                new_mct[0] = -999
                new_mbb[0] = -999
            else:
                ptb1 = t.ak4pfjets_p4.at(0).Pt()
                ptb2 = t.ak4pfjets_p4.at(1).Pt()
                phib1 = t.ak4pfjets_p4.at(0).Phi()
                phib2 = t.ak4pfjets_p4.at(1).Phi()
                dphibb = abs(phib1-phib2)
                if dphibb>math.pi: dphibb = 2*math.pi-dphibb
                new_mct[0] = math.sqrt(2*ptb1*ptb2*(1+math.cos(dphibb)))
                new_mbb[0] = (t.ak4pfjets_p4.at(0)+t.ak4pfjets_p4.at(1)).M()
                ptbb[0] = (t.ak4pfjets_p4.at(0)+t.ak4pfjets_p4.at(1)).Pt()                
        else: #If there is sufficently many bjets.
            ptb1 = t.ak4pfjets_p4.at(bjet_index[0]).Pt()
            ptb2 = t.ak4pfjets_p4.at(bjet_index[1]).Pt()
            phib1 = t.ak4pfjets_p4.at(bjet_index[0]).Phi()
            phib2 = t.ak4pfjets_p4.at(bjet_index[1]).Phi()
            dphibb = abs(phib1-phib2)
            if dphibb>math.pi: dphibb = 2*math.pi-dphibb
            new_mct[0] = math.sqrt(2*ptb1*ptb2*(1+math.cos(dphibb)))
            new_mbb[0] = di_bjet.M()
            ptbb[0] = di_bjet.Pt()
        #Check consistency in the versions.
        #if ngoodjets!=t.ngoodjets and t.ngoodjets>=0:
        #    print("Inconsistency in ngoodjets, new: %.0f, old: %.of"%(ngoodjets, t.ngoodjets))            
        t_out.Fill()  
    t_out.AutoSave()
    f.Close()
    f_out.Close()
    return 0;
import os
def get_total_file_size(file_list):
    bytes_num = 0
    for file_path in file_list:
        bytes_num += os.path.getsize(file_path)
    return bytes_num

#Main Function
from create_file_list import get_files, getgrid, generate_scan_dict
grid_list = generate_scan_dict()
MC_list = get_files()

#Get the total file size in order to estimate the run time.
total_list = []
for MC in grid_list:#MC_list:
    total_list += MC["file_name_list"]
total_bytes_num = get_total_file_size(total_list)
print(total_bytes_num*1.0e-6)
print("Total file size to be processed: %.1f Mb"%(total_bytes_num*1.0e-6))
start_time = time.time()

file_location_out = "../root_file_temp/Sicong_20180408/"
processed_bytes_num = 0
for MC in grid_list:# MC_list[:]:
    MC_name = MC["name"]
    print(MC_name)
    file_name_list = MC["file_name_list"]
    for file_name in file_name_list:
        tmp_file_name = file_name[file_name.rfind("/")+1:]
        file_name_out = file_location_out + file_name[file_name.rfind("/")+1:]
        feature_generate(file_name, file_name_out)
        processed_bytes_num += os.path.getsize(file_name)
    
    current_time = time.time()
    print("Progress: %.1f percent processed"%(processed_bytes_num/total_bytes_num*100.))
    minutes_left = 1.*(current_time-start_time)/processed_bytes_num*(total_bytes_num-processed_bytes_num)/60.
    print("Estimated mintues left: %.1f"%minutes_left)
