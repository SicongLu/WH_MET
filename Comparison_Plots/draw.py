import ROOT
import numpy
import array
ROOT.gStyle.SetOptStat(0);
ROOT.gStyle.SetOptTitle(0);

def draw_histo(file_name, var_name, str_condition, bin_num, xmin, xmax):
    #print(file_name, var_name, str_condition, bin_num, xmin, xmax)
    f = ROOT.TFile(file_name)
    t = f.Get("t")
    
    myhist = ROOT.TH1F("myhist","myhist",bin_num,xmin,xmax);
    t.Draw(var_name+">>myhist",str_condition,"goff")
    print(myhist.Integral())
    myhist.SetDirectory(0);
    #ROOT.TH1.AddDirectory(ROOT.kFALSE); 
    
    f.Close()
    return myhist

#Basic Set-up
bin_num = 20
xmin = 0
xmax = 300
var_name = "mbb"
lumi = 35.9
str_condition = "ngoodleps == 1 && nvetoleps == 1 && PassTrackVeto == 1 && PassTauVeto == 1 && ngoodjets == 2 && ngoodbtags ==2 && mct >= 170 && pfmet >= 125 && mt_met_lep >= 150"
str_condition = "("+str_condition+")*scale1fb*"+str(lumi)
file_name = "/home/users/siconglu/WH_MET/root_file_temp/Mia_20180223/TChiWH_225_75.root"
#myhist = draw_histo(file_name, var_name, str_condition, bin_num, xmin, xmax)

from create_file_list import get_files
MC_list = get_files()
hist_list = []
name_list = []
for MC in MC_list[5:8]:
    MC_name = MC["name"]
    file_name_list = MC["file_name_list"]
    
    sum_hist = ROOT.TH1F("sum_hist"+str(len(name_list)),"sum_hist",bin_num,xmin,xmax)
    #sum_hist.SetDirectory(0);  
    #ROOT.TH1.AddDirectory(ROOT.kFALSE);
    sum_dict = {}
    for file_name in file_name_list:
        hist = draw_histo(file_name, var_name, str_condition, bin_num, xmin, xmax)
        sum_hist.Add( sum_hist, hist, 1.0, 1.0 )
        
    if "(" in MC_name:
        sum_hist.Scale(50)
        MC_name += " x 50" 
    hist_list.append(sum_hist)
    name_list.append(MC_name)
    
import sys
sys.path.insert(0, '/home/users/siconglu/CMSTAS/software/dataMCplotMaker/')
import dataMCplotMaker

h_data = ROOT.TH1F("","",1,0,1)
d_opts = {
        "poissonErrorsNoZeros": True,
        "lumi": 35.9,
        "energy ": 13,
        "outputName": "plots/test.pdf",
        "yTitleOffset": 0.0,
        "xAxisLabel": "m_{bb}",
        "yAxisLabel": "Events",
        "xAxisUnit": "GeV",
        "noFill": "GeV",
        "isLinear": True,
        #"legendUp": -0.15,
        #"legendRight": -0.08,
        #"legendTaller": 0.15,
        "outOfFrame": True,
        "type": "Internal",
        #"noGrass": True,
        "darkColorLines": True,
        "makeTable": True,
        "makeJSON": True
        #"flagLocation": "0.5,0.7,0.15", # add a US flag because 'merica
        }
color_list = [ROOT.kOrange, ROOT.kSpring, ROOT.kTeal,ROOT.kAzure, ROOT.kViolet, ROOT.kPink, ROOT.kBlack]
dataMCplotMaker.dataMCplot(h_data, bgs=hist_list, titles=name_list, title="", colors=color_list[0:len(name_list)], opts=d_opts)



