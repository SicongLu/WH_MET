import glob
import os
def get_files():
    '''Get the path to the MC files.'''
    file_location = "../root_file_temp/Mia_20180223/"
    MC_list = []
    
    #Standard, no skimmed, MC signal points
    name = "(225, 75)"
    file_name_list = glob.glob(file_location+"TChiWH_225_75.root")
    MC_list.append({"name":name,"file_name_list":file_name_list})
    
    name = "(250, 1)"
    file_name_list = glob.glob(file_location+"TChiWH_250_1.root")
    MC_list.append({"name":name,"file_name_list":file_name_list})
    
    name = "(350, 100)"
    file_name_list = glob.glob(file_location+"TChiWH_350_100.root")
    MC_list.append({"name":name,"file_name_list":file_name_list})
    
    name = "(500, 1)"
    file_name_list = glob.glob(file_location+"TChiWH_500_1.root")
    MC_list.append({"name":name,"file_name_list":file_name_list})
    
    name = "(500, 125)"
    file_name_list = glob.glob(file_location+"TChiWH_500_125.root")
    MC_list.append({"name":name,"file_name_list":file_name_list})
    
    name = "(700, 1)"
    file_name_list = glob.glob(file_location+"TChiWH_700_1.root")
    MC_list.append({"name":name,"file_name_list":file_name_list})
    
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
    file_name_list += glob.glob(file_location+"t_tch_4f_powheg_pythia8*.root")
    file_name_list += glob.glob(file_location+"tbar_tch_4f_powheg_pythia8*.root")
    file_name_list += glob.glob(file_location+"t_sch*.root")
    file_name_list += glob.glob(file_location+"t_tbarW_5f_powheg_pythia8*.root")#???
    file_name_list += glob.glob(file_location+"t_tW_5f_powheg_pythia8*.root")#???
    MC_list.append({"name":name,"file_name_list":file_name_list})
    
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
    
    
    return MC_list

def getgrid():
    '''Define the grids.'''
    grid = [[150, 1], [150, 24], \
    [175, 1], [175, 25], [175, 49], \
    [200, 1], [200, 25], [200, 50], [200, 74], \
    [225, 1], [225, 25], [225, 50], [225, 75], [225, 99], \
    [250, 1], [250, 25], [250, 50], [250, 75], [250, 100], [250, 124], \
    [275, 1], [275, 25], [275, 50], [275, 75], [275, 100], [275, 125], [275, 149], \
    [300, 1], [300, 25], [300, 50], [300, 75], [300, 100], [300, 125], [300, 150], [300, 174], \
    [325, 1], [325, 25], [325, 50], [325, 75], [325, 100], [325, 125], [325, 150], [325, 175], [325, 199], \
    [350, 1], [350, 25], [350, 50], [350, 75], [350, 100], [350, 125], [350, 150], [350, 175], [350, 200], [350, 224], \
    [375, 1], [375, 25], [375, 50], [375, 75], [375, 100], [375, 125], [375, 150], [375, 175], [375, 200], [375, 225], [375, 249], \
    [400, 1], [400, 25], [400, 50], [400, 75], [400, 100], [400, 125], [400, 150], [400, 175], [400, 200], [400, 225], [400, 250], [400, 274], \
    [425, 1], [425, 25], [425, 50], [425, 75], [425, 100], [425, 125], [425, 150], [425, 175], [425, 200], [425, 225], [425, 250], [425, 275], [425, 299], \
    [450, 1], [450, 25], [450, 50], [450, 75], [450, 100], [450, 125], [450, 150], [450, 175], [450, 200], [450, 225], [450, 250], [450, 275], [450, 300], \
    [475, 1], [475, 25], [475, 50], [475, 75], [475, 100], [475, 125], [475, 150], [475, 175], [475, 200], [475, 225], [475, 250], [475, 275], [475, 300], \
    [500, 1], [500, 25], [500, 50], [500, 75], [500, 100], [500, 125], [500, 150], [500, 175], [500, 200], [500, 225], [500, 250], [500, 275], [500, 300], \
    [525, 1], [525, 25], [525, 50], [525, 75], [525, 100], [525, 125], [525, 150], [525, 175], [525, 200], [525, 225], [525, 250], [525, 275], [525, 300], \
    [550, 1], [550, 25], [550, 50], [550, 75], [550, 100], [550, 125], [550, 150], [550, 175], [550, 200], [550, 225], [550, 250], [550, 275], [550, 300], \
    [575, 1], [575, 25], [575, 50], [575, 75], [575, 100], [575, 125], [575, 150], [575, 175], [575, 200], [575, 225], [575, 250], [575, 275], [575, 300], \
    [600, 1], [600, 25], [600, 50], [600, 75], [600, 100], [600, 125], [600, 150], [600, 175], [600, 200], [600, 225], [600, 250], [600, 275], [600, 300], \
    [625, 1], [625, 25], [625, 50], [625, 75], [625, 100], [625, 125], [625, 150], [625, 175], [625, 200], [625, 225], [625, 250], [625, 275], [625, 300], \
    [650, 1], [650, 25], [650, 50], [650, 75], [650, 100], [650, 125], [650, 150], [650, 175], [650, 200], [650, 225], [650, 250], [650, 275], [650, 300], \
    [675, 1], [675, 25], [675, 50], [675, 75], [675, 100], [675, 125], [675, 150], [675, 175], [675, 200], [675, 225], [675, 250], [675, 275], [675, 300], \
    [700, 1], [700, 25], [700, 50], [700, 75], [700, 100], [700, 125], [700, 150], [700, 175], [700, 200], [700, 225], [700, 250], [700, 275], [700, 300], \
    #[126, 1] Not sure wh
    ]
    return grid
def generate_scan_dict():
    '''Put the grid in the same format as other background MC files.'''
    grid = getgrid()
    grid_list = []
    for point in grid:
        tmp_dict = {}
        tmp_dict["name"] = "(%.0f, %.0f)"%(point[0], point[1])
        tmp_dict["file_name_list"] = ["TChiWH_%.0f_%.0f.root"%(point[0], point[1])]
        grid_list.append(tmp_dict)
        
    return grid_list