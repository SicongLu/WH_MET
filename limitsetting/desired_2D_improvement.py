import numpy as np
import ROOT
import math
import array
import pickle
import glob
import copy
from create_file_list import getgrid
grid_list = getgrid()

def get_limits(region_name = "PSR3jet_met_225_mct225_0426"):
    
    file_location = "/home/users/siconglu/Run_Directory/CMSSW_8_1_0/src/WH_MET_limitsetting/scan_"+region_name+"/log/"
    result_dict = {}
    
    for point in grid_list:
        mass_chargino = point[0]
        mass_lsp = point[1]
        txt_file_name = file_location + "limit_tchwh_%.0f_%.0f.log"%(mass_chargino, mass_lsp)
        f_txt = open(txt_file_name, "r")
        limit_names = [
        "Observed Limit",
        "Expected  2.5%",
        "Expected 16.0%",
        "Expected 50.0%",
        "Expected 84.0%",
        "Expected 97.5%",]
        tmp_dict = {}
        for line in f_txt:
            for name in limit_names:
                if name in line:
                    nums = line.split("<")
                    tmp_dict[name] = float(nums[-1])
        
        result_dict[str(point)] = copy.deepcopy(tmp_dict)
        #print(tmp_dict)
        f_txt.close()
    return result_dict
region_name = "test_04_13"       
old_result_dict = get_limits(region_name)
region_name = "PSR3jet_met_225_mct225_0426"
region_name = "PSR3jet_met_225_mct225_2vars_ISR_0608"
new_result_dict = get_limits(region_name )


h_improvement = ROOT.TH2F('h_improvement','Improvement', int((700-0)/25.),0,700,int((350/25.)), 0,350)
for point in grid_list: 
    bin_x = h_improvement.GetXaxis().FindBin(point[0])
    bin_y = h_improvement.GetYaxis().FindBin(point[1])
    
    ratio = 100.0*(1-new_result_dict[str(point)]["Expected 50.0%"]/old_result_dict[str(point)]["Expected 50.0%"])
    #print(bin_x, bin_y, ratio)
    h_improvement.SetBinContent(bin_x, bin_y, ratio)
    
ROOT.gROOT.SetBatch()
ROOT.gStyle.SetOptStat(0);
#ROOT.gStyle.SetOptTitle(0);

ROOT.gStyle.SetPaintTextFormat("0.1f");

can_name = 'can'
canvas = ROOT.TCanvas(can_name,can_name,800,600)
h_improvement.Draw("text45")


h_improvement.GetXaxis().SetTitle("m_{#tilde{#chi}_{1}^{#pm}} = m_{#tilde{#chi}_{2}^{0}} [GeV]")
h_improvement.GetXaxis().SetTitleSize(0.05)
h_improvement.GetXaxis().SetTitleFont(42)
h_improvement.GetXaxis().SetTitleOffset(0.8)
h_improvement.GetXaxis().SetLabelFont(42)
h_improvement.GetXaxis().SetLabelSize(0.05)

h_improvement.GetYaxis().SetTitle("m_{#tilde{#chi}_{1}^{0}} [GeV]")
h_improvement.GetYaxis().SetTitleSize(0.05)
h_improvement.GetYaxis().SetTitleFont(42)
h_improvement.GetYaxis().SetTitleOffset(0.8)
h_improvement.GetYaxis().SetLabelFont(42)
h_improvement.GetYaxis().SetLabelSize(0.05)    




canvas.Update()


full_path = ''
file_name = "SR_improvements_"+region_name
canvas.Print(full_path+file_name+'.png')


h_improvement.Draw("colz")
canvas.Update()
file_name = "SR_improvements_"+region_name+"_color"
canvas.Print(full_path+file_name+'.png')


canvas.Show()
