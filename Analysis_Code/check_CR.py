import ROOT
import numpy
import array
import math
import time
import multiprocessing as mp
import os
#os.nice(19)
ROOT.gStyle.SetOptStat(0);
ROOT.gStyle.SetOptTitle(0);
#To-do!!!!:
#Need to modify the code to include selection of 2lCR in the get_weight_str
#Also need to check which triglep1 or triglep2_sf should be used!!!
def get_weight_str(file_name, entry_num, if_dilep = False):
    '''Calculate the relevant weights'''
    #return "1"
    lumi = 35.9
    if "TChiWH" in file_name:
        f_scanSys = ROOT.TFile.Open("/nfs-7/userdata/mliu/tupler_babies/merged/onelepbabymaker/moriond2017.v13/output/SMS_tchiwh.root","READ") 
        h_scanSys = f_scanSys.Get("h_counterSMS").Clone("h_scanSys");
        h_scanN = f_scanSys.Get("histNEvts").Clone("h_scanN"); 
        nums = re.findall(r'\d+', file_name)
        c1mass, n1mass = int(nums[-2]), int(nums[-1])
        
        c1massbin = h_scanN.GetXaxis().FindBin(c1mass);
        n1massbin = h_scanN.GetYaxis().FindBin(n1mass);
        nevents = h_scanN.GetBinContent(c1massbin,n1massbin);
        f_scanSys.Close()
        str_condition = "1*xsec*0.58*0.3*1000*"+str(lumi)+"/"+str(nevents)#Problem on xsec
    elif "data" in file_name:
        return "1"
    else:
        str_condition = "1.0*scale1fb*"+str(lumi)
    if if_dilep:
        #trigeff_str = "(1-(1-triglep1)*(1-triglep2))"
        trigeff_str = "(triglep1+triglep2-triglep1*triglep2)"
    else:
        trigeff_str = "triglep1"
    str_condition += "*weight_PU*weight_lepSF*weight_btagsf"+"*"+trigeff_str
    #str_condition += "*weight_PU*weight_lepSF*weight_btagsf*trigeff"
    return str_condition

def draw_histo(file_name, var_name, str_condition, bin_num, xmin, xmax, if_dilep = False):
    #print(file_name, var_name, str_condition, bin_num, xmin, xmax)
    f = ROOT.TFile(file_name)
    t = f.Get("t")
    weight_str = get_weight_str(file_name, t.GetEntries(), if_dilep = False)
    str_condition_num = str_condition
    str_condition = "("+str_condition+")*"+weight_str
    myhist = ROOT.TH1F("myhist","myhist",bin_num,xmin,xmax);
    t.Draw(var_name+">>myhist",str_condition,"goff")
    myhist.SetDirectory(0);
    #ROOT.TH1.AddDirectory(ROOT.kFALSE);
    print("Integrated to:%.1f with %.1f events." %(t.GetEntries(str_condition),t.GetEntries(str_condition_num)))
    
    f.Close()
    return myhist
from create_file_list import get_files
def plot_comparison(var_name, xmin, xmax, bin_num, lumi, MC_multi, sample_index_list, plot_folder_name, str_condition):
    #Remove special chars in var_name:
    tmp_var_name = var_name[:]
    char_str = "!@#$%^&*()[]{};:,./<>?\|`~-=_+"
    char_str = [char_str[i] for i in range(len(char_str))]
    for char in char_str:
        tmp_var_name = tmp_var_name.replace(char,"_")
    #Collect histograms
    MC_list = get_files()
    hist_list = []
    name_list = []
    #new_location = "../root_file_temp/Sicong_20180408/"
    #new_location = "../root_file_temp/Sicong_20180605/"
    new_location = "../root_file_temp/Sicong_20180716/"
    for MC in [MC_list[index] for index in sample_index_list]:
        MC_name = MC["name"]
        file_name_list = MC["file_name_list"]
        sum_hist = ROOT.TH1F("sum_hist"+tmp_var_name+str(len(name_list)),"sum_hist",bin_num,xmin,xmax)
        #sum_hist.SetDirectory(0);  
        #ROOT.TH1.AddDirectory(ROOT.kFALSE);
        sum_dict = {}
        for file_name in file_name_list:
            file_name = new_location + file_name[file_name.rfind("/")+1:]
            hist = draw_histo(file_name, var_name, str_condition, bin_num, xmin, xmax, if_dilep = False)
            sum_hist.Add( sum_hist, hist, 1.0, 1.0 )
        
        hist_list.append(sum_hist)
        name_list.append(MC_name)
    for MC in [MC_list[index] for index in sample_index_list]:
        MC_name = MC["name"]
        if "(" in MC_name and "2l top" in name_list:
            index = name_list.index(MC_name)
            if (hist_list[index].Integral() == 0):
                continue;
            MC_multi = math.ceil(1.0*hist_list[name_list.index("2l top")].Integral()/hist_list[index].Integral())
            hist_list[index].Scale(MC_multi)
            name_list[index] += " x " + str(MC_multi)        
    import sys
    sys.path.insert(0, '/home/users/siconglu/CMSTAS/software/dataMCplotMaker/')
    import dataMCplotMaker
    
    if "data" in name_list:
        ind = name_list.index("data")
        h_data = hist_list[ind]
        hist_list = [hist_list[i] for i in range(len(hist_list)) if i != ind]
        name_list = [name_list[i] for i in range(len(name_list)) if i != ind]
    else:
        h_data = ROOT.TH1F("","",1,0,1)
    d_opts = {
            "poissonErrorsNoZeros": True,"systFillStyle":4050,
            "lumi": 35.9,
            "energy ": 13,
            "outputName": "/home/users/siconglu/CMSTAS/software/niceplots/"+plot_folder_name+tmp_var_name+".pdf",
            "yTitleOffset": -0.,
            "xAxisLabel": var_name,
            "yAxisLabel": "Events",
            "xAxisUnit": "GeV",
            "noFill": False,
            "isLinear": False,
            #"noStack": False,
            #"noOverflow": True,
            #"legendUp": -0.15,
            #"legendRight": -0.08,
            #"legendTaller": 0.15,
            "outOfFrame": True,
            "type": "Internal",
            #"noGrass": True,
            "darkColorLines": True,
            "makeTable": True,
            "makeJSON": True,
            #"flagLocation": "0.5,0.7,0.15", # add a US flag because 'merica
            }
    color_list = [ROOT.kOrange, ROOT.kSpring, ROOT.kTeal,ROOT.kAzure, ROOT.kViolet, ROOT.kPink, ROOT.kBlack]
    dataMCplotMaker.dataMCplot(h_data, bgs=hist_list, titles=name_list, title="", colors=color_list[0:len(name_list)], opts=d_opts)
    

#Basic Set-up
#Other relevant set-up
plot_dict_list = [
{"var_name":"ngoodjets", "xmin":0, "xmax":10, "bin_num": 10},\
{"var_name":"new_mct", "xmin":0, "xmax":500, "bin_num": 25},\
{"var_name":"new_met", "xmin":0, "xmax":500, "bin_num": 25},\
{"var_name":"new_mt", "xmin":0, "xmax":500, "bin_num": 25},\
{"var_name":"new_mbb", "xmin":0, "xmax":500, "bin_num": 50},\
{"var_name":"lep1_p4.fCoordinates.Pt()", "xmin":0, "xmax":500, "bin_num": 25},\
{"var_name":"ak4pfjets_leadbtag_p4.fCoordinates.Pt()", "xmin":0, "xmax":500, "bin_num": 25},\
#{"var_name":"triglep1", "xmin":0, "xmax":1.5, "bin_num": 25},\
#{"var_name":"triglep2", "xmin":0, "xmax":1.5, "bin_num": 25},\
#{"var_name":"(triglep1+triglep2-triglep1*triglep2)", "xmin":0, "xmax":1.5, "bin_num": 25},\
]

#Common set-up 
lumi = 35.9
#region_str = "PSR3jet_met_200_mct250"
#region_str = "PSR3jet_met_200_mct225"
region_str = "CR2l"
region_str = "CRMbb_inclusive"
region_str = "CR0b_inclusive"
plot_folder_name = "WH_CR_Distribution_20180719_"+region_str+"/"

sample_index_list = [6,7,8,9,10,11]
#sample_index_list = [6,11]
#sample_index_list = [6]
MC_multi = 10
#Cut-Conditions
from selection_criteria import get_cut_dict, combine_cuts
cut_dict, current_cut_list,region_cut_dict = get_cut_dict()
#Current Ordering of the cut-requirement: (Preselection)
str_condition = region_cut_dict[region_str]
if "CR0b" in region_str:
    str_condition = str_condition.replace(cut_dict["mt"],"new_mt>50")
elif "CRMbb" in region_str:
    str_condition = str_condition.replace(cut_dict["mctbb"],"new_mct>0")
tmp_str_condition = str_condition
print(str_condition)
#Plotting
num_cores = 12
total_num = len(plot_dict_list)
start_time = time.time()
processes = []
for plot_dict in plot_dict_list:
    if "CR2l" in region_str and not("new_mbb" in plot_dict["var_name"]):
        str_condition = "("+tmp_str_condition+")"+"&&"+cut_dict["m_bb"]
    else:
        str_condition = tmp_str_condition
    print(plot_dict)
    index = plot_dict_list.index(plot_dict)
    #plot_comparison(plot_dict["var_name"], plot_dict["xmin"], plot_dict["xmax"], plot_dict["bin_num"], lumi, MC_multi, sample_index_list, plot_folder_name)
    p = mp.Process(target=plot_comparison, args=(plot_dict["var_name"], plot_dict["xmin"], plot_dict["xmax"], plot_dict["bin_num"], lumi, MC_multi, sample_index_list, plot_folder_name,str_condition,))
    processes.append(p)
    if (index+1)%num_cores == 0 or index+1 == total_num:            
        [x.start() for x in processes]
        print("Starting %.0f process simultaneously."%len(processes))
        [x.join() for x in processes]
        print("%.0f processes have been completed."%len(processes))
        current_time = time.time()
        print("Processing %.0f of %.0f"%(index+1, total_num))
        print("Expect to complete in %.2f miniutes"%(1.*(current_time-start_time)/index*(total_num-index-1)/60.))
        processes = []


