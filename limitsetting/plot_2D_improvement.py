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
new_result_dict = get_limits(region_name = "PSR3jet_met_225_mct225_0426")


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
'''

canvas.SetBorderMode(0);
canvas.SetBorderSize(2);
canvas.SetTickx(1);
canvas.SetTicky(1);
canvas.SetLeftMargin(0.16);
canvas.SetRightMargin(0.05);
canvas.SetTopMargin(0.05);
canvas.SetBottomMargin(0.16);
canvas.SetFrameBorderMode(0);

ROOT.gROOT.LoadMacro('/global/homes/b/btamadio/atlasstyle/AtlasStyle.C')
ROOT.gROOT.LoadMacro('/global/homes/b/btamadio/atlasstyle/AtlasLabels.C')
ROOT.SetAtlasStyle()
ROOT.gROOT.SetBatch()
ROOT.gStyle.SetPaintTextFormat("0.2f");

h_improvement.GetYaxis().SetTitle("m_{#tilde{#chi}_{1}^{0}} [GeV]")
h_improvement.GetYaxis().SetTitleSize(0.05)
h_improvement.GetYaxis().SetTitleFont(42)
h_improvement.GetYaxis().SetTitleOffset(1.4)
h_improvement.GetYaxis().SetLabelFont(42)
h_improvement.GetYaxis().SetLabelSize(0.05)    

h_improvement.GetXaxis().SetTitle("m_{#tilde{g}} [GeV]")
h_improvement.GetXaxis().SetTitleSize(0.05)
h_improvement.GetXaxis().SetTitleFont(42)
h_improvement.GetXaxis().SetTitleOffset(1.4)
h_improvement.GetXaxis().SetLabelFont(42)
h_improvement.GetXaxis().SetLabelSize(0.05)

###############################
h_improvement.SetContour(2); # number of contours
h_improvement.SetContourLevel(0, 0.04); # contour of CL_s = 0.05
h_improvement.SetContourLevel(1, 0.05); # contour of CL_s = 0.05
h_improvement.Draw("CONT LIST same");
canvas.Update()
conts0 = ROOT.gROOT.GetListOfSpecials().FindObject("contours")
contLevel3 = conts0.At(1);
curv3 = contLevel3.At(0);
x_buff = curv3.GetX()
y_buff = curv3.GetY()
n = curv3.GetN()#x_buff.SetSize(n) #y_buff.SetSize(n)
x = [x_buff[i] for i in range(n)]
y = [y_buff[i] for i in range(n)]
upper_x = [x[i] for i in range(n) if y[i]>600]
upper_i = [i for i in range(n) if y[i]>600]
lower_x = [x[i] for i in range(n) if y[i]<=600]
lower_i = [i for i in range(n) if y[i]<=600]
i_min = lower_i[lower_x.index(min(lower_x))]
i_max = upper_i[upper_x.index(min(upper_x))]
print(i_min,i_max)
if i_max<i_min:
    i_max, i_min = i_min, i_max 
x = x[i_min:i_max]
y = y[i_min:i_max]
x.append(y[-1])
y.append(y[-1])
x.append(0)
y.append(0)
x.append(x[0])
y.append(y[0])

x_obs = array.array('f',x)
y_obs = array.array('f',y)
ROOT.gPad.GetListOfPrimitives().Remove(h);
ROOT.gPad.Update();
#####################################
h_up.SetContour(2); # number of contours
h_up.SetContourLevel(0, 0.04); # contour of CL_s = 0.05
h_up.SetContourLevel(1, 0.05); # contour of CL_s = 0.05
h_up.Draw("CONT LIST same");
canvas.Update()
conts0 = ROOT.gROOT.GetListOfSpecials().FindObject("contours")
contLevel3 = conts0.At(1);
curv3 = contLevel3.At(0);
x_buff = curv3.GetX()
y_buff = curv3.GetY()
n = curv3.GetN()#x_buff.SetSize(n) #y_buff.SetSize(n)
x = [x_buff[i] for i in range(n)]
y = [y_buff[i] for i in range(n)]
upper_x = [x[i] for i in range(n) if y[i]>600]
upper_i = [i for i in range(n) if y[i]>600]
lower_x = [x[i] for i in range(n) if y[i]<=600]
lower_i = [i for i in range(n) if y[i]<=600]
i_min = lower_i[lower_x.index(min(lower_x))]
i_max = upper_i[upper_x.index(min(upper_x))]
print(i_min,i_max)
if i_max<i_min:
    i_max, i_min = i_min, i_max 
x = x[i_min:i_max]
y = y[i_min:i_max]
x.append(y[-1])
y.append(y[-1])
x.append(0)
y.append(0)
x.append(x[0])
y.append(y[0])

x_up = array.array('f',x)
y_up = array.array('f',y)
ROOT.gPad.GetListOfPrimitives().Remove(h_up);
ROOT.gPad.Update();
#####################################
h_down.SetContour(2); # number of contours
h_down.SetContourLevel(0, 0.04); # contour of CL_s = 0.05
h_down.SetContourLevel(1, 0.05); # contour of CL_s = 0.05
h_down.Draw("CONT LIST same");
canvas.Update()
conts0 = ROOT.gROOT.GetListOfSpecials().FindObject("contours")
contLevel3 = conts0.At(1);
curv3 = contLevel3.At(0);
x_buff = curv3.GetX()
y_buff = curv3.GetY()
n = curv3.GetN()#x_buff.SetSize(n) #y_buff.SetSize(n)
x = [x_buff[i] for i in range(n)]
y = [y_buff[i] for i in range(n)]
upper_x = [x[i] for i in range(n) if y[i]>600]
upper_i = [i for i in range(n) if y[i]>600]
lower_x = [x[i] for i in range(n) if y[i]<=600]
lower_i = [i for i in range(n) if y[i]<=600]
i_min = lower_i[lower_x.index(min(lower_x))]
i_max = upper_i[upper_x.index(min(upper_x))]
print(i_min,i_max)
if i_max<i_min:
    i_max, i_min = i_min, i_max 
x = x[i_min:i_max]
y = y[i_min:i_max]
x.append(y[-1])
y.append(y[-1])
x.append(0)
y.append(0)
x.append(x[0])
y.append(y[0])

x_down = array.array('f',x)
y_down = array.array('f',y)
ROOT.gPad.GetListOfPrimitives().Remove(h_down);
ROOT.gPad.Update();

#####################################
h_med.SetContour(2); # number of contours
h_med.SetContourLevel(0, 0.04); # contour of CL_s = 0.05
h_med.SetContourLevel(1, 0.05); # contour of CL_s = 0.05
h_med.Draw("CONT LIST same");
canvas.Update()
conts0 = ROOT.gROOT.GetListOfSpecials().FindObject("contours")
contLevel3 = conts0.At(1);
curv3 = contLevel3.At(0);
x_buff = curv3.GetX()
y_buff = curv3.GetY()
n = curv3.GetN()#x_buff.SetSize(n) #y_buff.SetSize(n)
x = [x_buff[i] for i in range(n)]
y = [y_buff[i] for i in range(n)]
upper_x = [x[i] for i in range(n) if y[i]>600]
upper_i = [i for i in range(n) if y[i]>600]
lower_x = [x[i] for i in range(n) if y[i]<=600]
lower_i = [i for i in range(n) if y[i]<=600]
i_min = lower_i[lower_x.index(min(lower_x))]
i_max = upper_i[upper_x.index(min(upper_x))]
print(i_min,i_max)
if i_max<i_min:
    i_max, i_min = i_min, i_max 
x = x[i_min:i_max]
y = y[i_min:i_max]
x.append(y[-1])
y.append(y[-1])
x.append(0)
y.append(0)
x.append(x[0])
y.append(y[0])

x_med = array.array('f',x)
y_med = array.array('f',y)
ROOT.gPad.GetListOfPrimitives().Remove(h_med);
ROOT.gPad.Update();
########################
h_1p.SetContour(2); # number of contours
h_1p.SetContourLevel(0, 0.04); # contour of CL_s = 0.05
h_1p.SetContourLevel(1, 0.05); # contour of CL_s = 0.05
h_1p.Draw("CONT LIST same");
canvas.Update()
conts0 = ROOT.gROOT.GetListOfSpecials().FindObject("contours")
contLevel3 = conts0.At(1);
curv3 = contLevel3.At(0);
x_buff = curv3.GetX()
y_buff = curv3.GetY()
n = curv3.GetN()#x_buff.SetSize(n) #y_buff.SetSize(n)
x = [x_buff[i] for i in range(n)]
y = [y_buff[i] for i in range(n)]
upper_x = [x[i] for i in range(n) if y[i]>600]
upper_i = [i for i in range(n) if y[i]>600]
lower_x = [x[i] for i in range(n) if y[i]<=600]
lower_i = [i for i in range(n) if y[i]<=600]
i_min = lower_i[lower_x.index(min(lower_x))]
i_max = upper_i[upper_x.index(min(upper_x))]
print(i_min,i_max)
if i_max<i_min:
    i_max, i_min = i_min, i_max 
x = x[i_min:i_max]
y = y[i_min:i_max]
x.append(y[-1])
y.append(y[-1])
x.append(0)
y.append(0)
x.append(x[0])
y.append(y[0])

x_1p = array.array('f',x)
y_1p = array.array('f',y)
ROOT.gPad.GetListOfPrimitives().Remove(h_1p);
ROOT.gPad.Update();
########################
h_1m.SetContour(2); # number of contours
h_1m.SetContourLevel(0, 0.04); # contour of CL_s = 0.05
h_1m.SetContourLevel(1, 0.05); # contour of CL_s = 0.05
h_1m.Draw("CONT LIST same");
canvas.Update()
conts0 = ROOT.gROOT.GetListOfSpecials().FindObject("contours")
contLevel3 = conts0.At(1);
curv3 = contLevel3.At(0);
x_buff = curv3.GetX()
y_buff = curv3.GetY()
n = curv3.GetN()#x_buff.SetSize(n) #y_buff.SetSize(n)
x = [x_buff[i] for i in range(n)]
y = [y_buff[i] for i in range(n)]
upper_x = [x[i] for i in range(n) if y[i]>600]
upper_i = [i for i in range(n) if y[i]>600]
lower_x = [x[i] for i in range(n) if y[i]<=600]
lower_i = [i for i in range(n) if y[i]<=600]
i_min = lower_i[lower_x.index(min(lower_x))]
i_max = upper_i[upper_x.index(min(upper_x))]
print(i_min,i_max)
if i_max<i_min:
    i_max, i_min = i_min, i_max 
x = x[i_min:i_max]
y = y[i_min:i_max]
x.append(y[-1])
y.append(y[-1])
x.append(0)
y.append(0)
x.append(x[0])
y.append(y[0])

x_1m = array.array('f',x)
y_1m = array.array('f',y)
ROOT.gPad.GetListOfPrimitives().Remove(h_1m);
ROOT.gPad.Update();

e1m_limit.SetFillColor(ROOT.kYellow)

h_improvement.GetXaxis().SetRangeUser(700,2200)
h_improvement.GetYaxis().SetRangeUser(50,2200)
#h_improvement.SetMaximum(2200)
#h_improvement.SetMinimum(50)
h_improvement.Draw("axis");
e1m_limit.Draw("F same")
e1p_limit.Draw("F same")
#e1m_limit.Draw("L same")
#e1p_limit.Draw("L same")
med_limit.Draw("L same")
obs_limit.Draw("L same")
obs_up_limit.Draw("L same")
obs_down_limit.Draw("L same")
#h_improvement.Draw("text45");
canvas.Update()

run_1_x = [ 889,   893.4,   897.9,   899.4,   901,   902.5,   908.1,   912.5,   930.6,   937.5,   953,   962.5,   975.9,   987.5,   996.1,   1012,   1013,   1035,   1038,   1041,  1038,   1034,   1028,   1022,   1027,   1012,   993,   987.5,   962.5,   937.5,   922.1,   912.5,   887.5,   862.5,   859,   837.5,   822.7,   812.5]
run_1_y = [   65.62,   96.88,   128.1,   159.4,   190.6,   221.9,   253.1,   257.6,   284.4,   294,   315.6,   328.7,   346.9,   362.5,   378.1,   407.7,   409.4,   440.6,   454.1,  471.9,   488.1,   503.1,   534.4,   565.6,   596.9,   618.7,   628.1,   629.7,   640.1,   652,   659.4,   664,   676.1,   688.1,   690.6,   708.9,   721.9,   731.3]

run_1_x = array.array('f',run_1_x)
run_1_y = array.array('f',run_1_y)

run_1_limit = ROOT.TGraph(len(run_1_x),run_1_x,run_1_y)
run_1_limit.SetLineWidth(3)
run_1_limit.SetLineStyle(5)
run_1_limit.SetLineColor(13)
run_1_limit.Draw("L same")


forbid = ROOT.TGraph(4,array.array('f',[0, 2200, 0, 0]),array.array('f',[0, 2200, 2200,0]))
forbid.SetLineWidth(3)
forbid.SetLineColor(ROOT.kGray)
forbid.SetFillColor(ROOT.kWhite)
forbid.Draw("F same")
forbid.Draw("L same")

ROOT.ATLASLabel(0.55,0.81,' Internal',0.05,0.115,1)
lat = ROOT.TLatex()
lat.DrawLatexNDC(0.55,0.88,'#sqrt{s} = 13 TeV, 36.1 fb^{-1}')
#lat.DrawLatexNDC(0.19,0.7,'region: 5jSRb')

tex = ROOT.TLatex(900,1000,"#color[12]{#scale[0.55]{#tilde{g}#rightarrow qq#tilde{#chi}_{1}^{0} forbidden}}");
tex.SetTextFont(42);
tex.SetTextAngle(24);
tex.SetLineWidth(2);
tex.Draw();

leg = ROOT.TLegend(0.17,0.71,0.47,0.92)
leg.AddEntry(obs_limit,'Obs Limit','L')
leg.AddEntry(obs_down_limit,'#pm 1#sigma_{theory}^{SUSY} Obs Limit','L')
leg.AddEntry(med_limit,'Exp Limit (#pm 1#sigma_{exp})','LF')
leg.AddEntry(run_1_limit,'Run 1 Limit','L')
leg.AddEntry(0,'#scale[0.65]{All limits at 95% CL}',"")
leg.SetLineColor(0)
leg.SetTextSize(0.03)
leg.SetShadowColor(0)
leg.SetFillStyle(0)
leg.SetFillColor(0)
leg.Draw()

tex_pro = ROOT.TLatex(700,2250,"#scale[0.5]{#tilde{g}-#tilde{g} production, #tilde{g}#rightarrowqq#tilde{#chi}_{1}^{0}, #tilde{#chi}_{1}^{0}#rightarrow qqq}");
tex_pro.SetTextFont(42);
tex_pro.SetLineWidth(2);
tex_pro.Draw();
h_improvement.Draw("axis same");
#h_improvement.Draw("text45");
canvas.Update()


full_path = ''

canvas.Print(full_path+file_name+'.C')
canvas.Print(full_path+file_name+'.png')
canvas.Print(full_path+file_name+'.pdf')
canvas.Print(full_path+file_name+'.eps')
full_path = '/global/project/projectdirs/atlas/www/multijet/RPV/siconglu/09_26_RPV10_Plots/'
canvas.Print(full_path+file_name+'.C')
canvas.Print(full_path+file_name+'.png')
canvas.Print(full_path+file_name+'.pdf')
canvas.Print(full_path+file_name+'.eps')

import pickle
with open('Curves.pickle', 'w') as f:  
    pickle.dump([x_obs,y_obs, x_up, y_up,x_down, y_down,x_med, y_med, x_1p, y_1p, x_1m, y_1m], f)

'''