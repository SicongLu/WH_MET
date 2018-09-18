#Import packages and get data
import ROOT
import array
import os
os.nice(15)
import multiprocessing as mp
def get_scatter_hist(inputs):#(file_name, str_condition, x_name, y_name):
    [file_name, str_condition, x_name, y_name] = inputs
    print(file_name) 
    file_in = ROOT.TFile.Open(file_name);
    t = file_in.Get("t");
    t.Draw(y_name+":"+x_name, str_condition,"goff") #V1=Asym, V2=DeltaX
    
    X_array = t.GetV2();
    Y_array = t.GetV1();
    
    arr_len = t.GetSelectedRows()
    X_list = [X_array[i] for i in range(arr_len)]
    Y_list = [Y_array[i] for i in range(arr_len)]
    return [X_list, Y_list]


#Upon comparison, one finds the asym:DeltaX are approximiately independent of each other.
from selection_criteria import get_cut_dict, combine_cuts
cut_dict, current_cut_list,region_cut_dict = get_cut_dict()
region_str = "PSR3jet_met_225_mct225"
region_str = "SR2"
str_condition = region_cut_dict[region_str] + "&& ak4_htratiom > 0. && mindphi_met_j1_j2 > 0."
str_condition = str_condition.replace("ngoodjets30","ngoodjets")

#x_name = "mindphi_met_j1_j2"
#y_name = "ak4_htratiom"
x_name = "mindphi_met_j1_j2"
y_name = "ak4_htratiom"

from create_file_list import get_files

#Collect histograms
MC_list = get_files()
gr_list = []
name_list = []
#new_location = "../root_file_temp/Sicong_20180408/"
new_location = "../root_file_temp/Sicong_20180605/"

sample_index_list = [5, 6, 7, 8, 9, 10]
#sample_index_list = [5, 4, 3, 2, 1, 0]
sample_index_list = [5, 6]
col_ind = 1
draw_list = []
for MC in [MC_list[index] for index in sample_index_list]:
    MC_name = MC["name"]
    print(MC_name)
    file_name_list = MC["file_name_list"]
    X_all_list = []
    Y_all_list = []
    
    
    inputs_list = []
    for file_name in file_name_list:
        file_name = new_location + file_name[file_name.rfind("/")+1:]
        inputs_list.append([file_name, str_condition, x_name, y_name])
    #inputs_list = inputs_list[0:3]
    p = mp.Pool(processes=len(inputs_list))
    data = p.map(get_scatter_hist, inputs_list)
    p.close()
    for [X_list, Y_list] in data:
        X_all_list = X_all_list + X_list
        Y_all_list = Y_all_list + Y_list
    X_array = array.array("f",X_all_list)
    Y_array = array.array("f",Y_all_list)
    print(len(X_array))
    draw_list.append([X_array, Y_array, MC_name, col_ind])
    col_ind += 1;

c2 = ROOT.TCanvas("can2","can2",800,600);
c2.SetBorderMode(0);
[X_array, Y_array, MC_name, col_ind] = draw_list[0]
gr = ROOT.TGraph(len(X_array), X_array,Y_array);
gr.SetTitle("Scatter Plot: "+y_name+" VS "+x_name);
gr.GetYaxis().SetTitle(y_name)
gr.GetXaxis().SetTitle(x_name)
gr.GetYaxis().SetTitleOffset(1.3)
gr.Draw('A P')
c2.Modified()
c2.Update()
legend = ROOT.TLegend(0.7,0.6,0.9,0.9);
legend.SetHeader("Legend");
for draw in draw_list:
    [X_array, Y_array, MC_name, col_ind] = draw  
    tmp_gr = ROOT.TGraph(len(X_array), X_array,Y_array);
    gr2 = tmp_gr.Clone()
    gr_list.append(gr2)
    gr2.SetTitle("Scatter Plot: "+y_name+" VS "+x_name);
    print("Correlation Factor = %.4f"%gr2.GetCorrelationFactor())
    gr2.GetYaxis().SetTitle(y_name)
    gr2.GetXaxis().SetTitle(x_name)
    gr2.GetYaxis().SetTitleOffset(1.3)
    gr2.SetMarkerSize(0.8);
    gr2.SetMarkerStyle(8);
    gr2.SetMarkerColor(col_ind);
    
    gr2.Draw('p same')
    c2.Modified()
    c2.Update()    
    legend.AddEntry(gr2,MC_name,"p");

legend.Draw()
#c2.Draw()
c2.Show()
full_path = ''
#file_name = y_name+"_VS_"+x_name+"_signals_"+region_str
file_name = y_name+"_VS_"+x_name+"_"+region_str
c2.Print(full_path+file_name+'.png')
