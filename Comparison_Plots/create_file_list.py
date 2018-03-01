import glob
import os
def get_files():
    file_location = "../root_file_temp/Mia_20180223/"
    MC_list = []
    
    #file_name_list = [os.path.abspath(path) for path in file_name_list]
    #MC signal points
    name = "(225, 75)"
    file_name_list = glob.glob(file_location+"TChiWH_225_75.root")
    MC_list.append({"name":name,"file_name_list":file_name_list})
    
    name = "(250, 1)"
    file_name_list = glob.glob(file_location+"TChiWH_250_1.root")
    MC_list.append({"name":name,"file_name_list":file_name_list})
    
    name = "(350, 100)"
    file_name_list = glob.glob(file_location+"TChiWH_225_75.root")
    MC_list.append({"name":name,"file_name_list":file_name_list})
    
    name = "(500, 1)"
    file_name_list = glob.glob(file_location+"TChiWH_225_75.root")
    MC_list.append({"name":name,"file_name_list":file_name_list})
    
    name = "(500, 125)"
    file_name_list = glob.glob(file_location+"TChiWH_225_75.root")
    MC_list.append({"name":name,"file_name_list":file_name_list})
    
    name = "(700, 1)"
    file_name_list = glob.glob(file_location+"TChiWH_225_75.root")
    MC_list.append({"name":name,"file_name_list":file_name_list})
    
    #MC background
    name = "2l top"
    file_name_list = glob.glob(file_location+"ttbar_diLept*.root")
    MC_list.append({"name":name,"file_name_list":file_name_list})
    
    name = "1l top"
    file_name_list = glob.glob(file_location+"ttbar_singleLeptFrom*.root")
    MC_list.append({"name":name,"file_name_list":file_name_list})
    return MC_list

