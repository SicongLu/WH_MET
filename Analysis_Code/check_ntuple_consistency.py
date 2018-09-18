'''
This function intends to make sure that generated ntuples is consistent with
the previously generated ones.

To-do:
Fix the problem where the binning is incoherent...
'''
import ROOT
import numpy
import array
import math
import os
import time
import multiprocessing as mp
import random
os.nice(19)
ROOT.gStyle.SetOptStat(0);
ROOT.gStyle.SetOptTitle(0);
ROOT.gROOT.SetBatch(ROOT.kTRUE);

def get_all_branches(file_name):
    '''Get all branches in the specified file, and put in a list.
    In case there is LorentzVector in the branch, we need to compare the four
    components individually. 
    ''' 
    f = ROOT.TFile(file_name)
    t = f.Get("t")
    names = [b.GetName() for b in t.GetListOfBranches()]
    types = [b.GetClassName() for b in t.GetListOfBranches()]
    for i in range(len(types)):
        if "LorentzVector" in types[i]:
            for suffix in [".fCoordinates.M()",".fCoordinates.Pt()",".fCoordinates.Eta()"]:
                names.append(names[i]+suffix)
            names[i] = names[i]+".fCoordinates.Phi()"
    f.Close()
    return names
    
def draw_histo(file_name, var_name, xmin, xmax):
    '''It should return the normalized histogram for shape comparison.'''
    f = ROOT.TFile(file_name)
    t = f.Get("t")        
    str_condition = "1"
    rand_str = str(int(math.ceil(random.uniform(0, 1.)*1e6)))
    print(rand_str)
    names = [b.GetName() for b in t.GetListOfBranches()]
    if not(var_name in names):
        myhist = ROOT.TH1F("myhist"+rand_str,"myhist"+rand_str, 40, xmin, xmax);
        return myhist, xmin, xmax
    if xmin == 0 and xmax == 0:
        xmin =  t.GetMinimum(var_name)
        if xmin<-900: 
            xmin = 0
        xmax =  t.GetMaximum(var_name)
        if xmax < 2:
            xmax = 2;
        else:
            xmax = xmax*1.5 
    myhist = ROOT.TH1F("myhist"+rand_str,"myhist"+rand_str, 40, xmin, xmax);
    t.Draw(var_name+">>myhist"+rand_str,str_condition,"goff")
    if (myhist.Integral()!=0):
        myhist.Scale(1./myhist.Integral())
    myhist.SetDirectory(0); 
    f.Close()
    return myhist, xmin, xmax
    
from create_file_list import get_files
import sys
sys.path.insert(0, '/home/users/siconglu/CMSTAS/software/dataMCplotMaker/')
import dataMCplotMaker
def plot_comparison(var_name, plot_folder_name):
    #Remove special chars in var_name for naming the plot.
    tmp_var_name = var_name[:]
    char_str = "!@#$%^&*()[]{};:,./<>?\|`~-=_+"
    char_str = [char_str[i] for i in range(len(char_str))]
    for char in char_str:
        tmp_var_name = tmp_var_name.replace(char,"_")
    #Collect histograms
    name_list = ["New baby","Old baby"]
    hist_list = []
    xmin, xmax = 0, 0
    xmax_list = []
    xmin_list = []
    for file_name in file_list:
        hist, xmin, xmax = draw_histo(file_name, var_name, xmin, xmax)
        xmax_list.append(xmax)
        xmin_list.append(xmin)
        hist_list.append(hist) 
    #if hist_list[0].GetBinCenter(40)!=hist_list[1].GetBinCenter(40):
    #    print("Error!!!!! "+var_name)
    #    print(xmax_list)
    #    print(hist_list[0].GetBinCenter(40), hist_list[1].GetBinCenter(40))
    
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
            "noFill": True,
            "isLinear": True,
            "noStack": True,
            "noOverflow": False,
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
    color_list = [ROOT.kAzure, ROOT.kBlack, ROOT.kViolet, ROOT.kPink, ROOT.kOrange, ROOT.kSpring, ROOT.kTeal]
    dataMCplotMaker.dataMCplot(h_data, bgs=hist_list, titles=name_list, title="", colors=color_list[0:len(name_list)], opts=d_opts)
    
if __name__ == "__main__": 
    #Comparison Subjects: [old, new]
    global file_list
    file_list = ["/hadoop/cms/store/user/mliu/AutoTwopler_babies/onelepbabymaker_2017.v1/TTJets_TuneCP5_13TeV-amcatnloFXFX-pythia8_RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/skim/skim_369.root","/home/users/siconglu/WH_MET/root_file_temp/Mia_20180223/ttbar_diLept_madgraph_pythia8_ext1_25ns_1.root"]
    file_list = ["/hadoop/cms/store/user/mliu/AutoTwopler_babies/onelepbabymaker_2017.v1/ST_tW_top_5f_inclusiveDecays_TuneCP5_PSweights_13TeV-powheg-pythia8_RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/output/output_27.root","/home/users/siconglu/WH_MET/root_file_temp/Mia_20180223/t_tW_5f_powheg_pythia8_noHadDecays.root"]
    #file_list = ["/home/users/siconglu/WH_MET/root_file_temp/Mia_20180223/ttbar_singleLeptFromT_madgraph_pythia8_ext1_25ns.root","/home/users/siconglu/Mia_WH_Analysis/WHAnalysis/onelepbabymaker/output_sicheng_singlelep.root"]
    #file_list = ["/home/users/siconglu/WH_MET/root_file_temp/Mia_20180223/ttbar_diLept_madgraph_pythia8_ext1_25ns_1.root","/home/users/siconglu/Mia_WH_Analysis/WHAnalysis/onelepbabymaker/output.root"]
    #file_list = ["../root_file_temp/Sicong_20180408/TChiWH_700_1.root","../root_file_temp/Sicong_20180408/TChiWH_700_1_test.root"]
    
    new_file_name = file_list[0]
    names = get_all_branches(new_file_name)
    #names = ["NISRjets"]
    #names = names[:int(len(names)/10.)]
    plot_folder_name = "WH_Comparing_Babies_ttjets_0523_test/"
    plot_folder_name = "WH_Comparing_Babies_tW_0523/"
    
    processes = []
    num_cores = 20
    total_num = len(names)
    print("Total number of vars:%.0f"%total_num)
    start_time = time.time()
    for index in range(len(names)):
        var_name = names[index]
        p = mp.Process(target=plot_comparison, args=(var_name, plot_folder_name,))
        processes.append(p)
        if (index+1)%num_cores == 0 or index == len(names)-1:
            [x.start() for x in processes]
            print("Starting %.0f process simultaneously."%len(processes))
            [x.join() for x in processes]
            print("%.0f processes have been completed."%len(processes))
            current_time = time.time()
            print("Processing %.0f of %.0f"%(index+1, total_num))
            print("Expect to complete in %.2f miniutes"%(1.*(current_time-start_time)/(index+1)*(total_num-index-1)/60.))
            processes = []
