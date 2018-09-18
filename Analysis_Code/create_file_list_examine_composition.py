import glob
import os
def get_test_files():
    '''Get the path to the MC files.'''
    file_location = "../root_file_temp/Mia_20180223/"
    MC_list = []
        
    #MC background
    #Cate #1
    name = "2l top"
    file_name_list = glob.glob(file_location+"ttbar_diLept*.root")
    MC_list.append({"name":name,"file_name_list":file_name_list})
    
    #Cate #2/3
    name = "W+LF/W+HF"
    file_name_list = glob.glob(file_location+"WJetsToLNu_*.root")
    MC_list.append({"name":name,"file_name_list":file_name_list})
    
    #Cate #4
    name = "WZ"
    file_name_list = glob.glob(file_location+"WZTo1LNu2Q_amcnlo*.root")
    MC_list.append({"name":name,"file_name_list":file_name_list})
    
    #Cate #5
    name = "1l top"
    file_name_list = glob.glob(file_location+"ttbar_singleLeptFrom*.root")
    MC_list.append({"name":"1l ttbar","file_name_list":file_name_list})
    file_name_list = glob.glob(file_location+"t_tch_4f_powheg_pythia8*.root")
    file_name_list += glob.glob(file_location+"tbar_tch_4f_powheg_pythia8*.root")
    file_name_list += glob.glob(file_location+"t_sch*.root")
    MC_list.append({"name":"1l tch,sch","file_name_list":file_name_list})
    file_name_list = glob.glob(file_location+"t_tbarW_5f_powheg_pythia8*.root")#???
    file_name_list += glob.glob(file_location+"t_tW_5f_powheg_pythia8*.root")#???
    MC_list.append({"name":"1l tW","file_name_list":file_name_list})
    
    #Cate #6: Z+jets, WW/WZ/ZZ, ttW/Z, WWW/WWZ/WZZ/ZZZ, WH->lvbb;
    name = "rare"
    file_name_list = glob.glob(file_location+"ttZ*.root")
    file_name_list += glob.glob(file_location+"tZq*.root")
    file_name_list += glob.glob(file_location+"ttW*.root")
    file_name_list += glob.glob(file_location+"WWTo*powheg*.root")
    file_name_list += glob.glob(file_location+"WZTo1L3Nu_amcnlo_pythia8_25ns*.root")
    file_name_list += glob.glob(file_location+"WZTo3LNu_powheg_pythia8_25ns.root")
    file_name_list += glob.glob(file_location+"WZTo2L2Q_amcnlo_pythia8_25ns.root")
    file_name_list += glob.glob(file_location+"ZZTo*.root")
    file_name_list += glob.glob(file_location+"WminusH*.root")
    file_name_list += glob.glob(file_location+"WplusH*.root")
    file_name_list += glob.glob(file_location+"*WWW*.root")
    file_name_list += glob.glob(file_location+"*WWZ*.root")
    file_name_list += glob.glob(file_location+"*WZG*.root")
    file_name_list += glob.glob(file_location+"*WZZ*.root")
    file_name_list += glob.glob(file_location+"*ZZZ*.root") 
    file_name_list += glob.glob(file_location+"*WWG*.root")
    MC_list.append({"name":name,"file_name_list":file_name_list})
    
    name = "data"
    file_name_list = glob.glob(file_location+"data_single_electron_Run2016*.root")
    file_name_list += glob.glob(file_location+"data_single_muon_Run2016*.root")
    MC_list.append({"name":name,"file_name_list":file_name_list})
    
    return MC_list
