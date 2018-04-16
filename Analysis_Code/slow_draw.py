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
    #t.Draw(var_name+">>myhist",str_condition,"goff")
    weight_form = ROOT.TTreeFormula("weight",str_condition,t)
    for i in range(t.GetEntries()):
        if i % 1e4 == 0: print(i)
        t.GetEntry(i)
        dR_bb = -999
        weight = weight_form.EvalInstance()
        if weight == 0:
            continue        
        gen_p4_list = t.genqs_p4
        gen_pT_list = [p4.Pt() for p4 in gen_p4_list] 
        gen_pT_list = sorted(gen_pT_list, reverse=True)
        
        p4_list = t.ak4pfjets_p4
        pT_list = [p4.Pt() for p4 in p4_list] 
        pT_list = sorted(pT_list, reverse=True)
        if var_name == "genqs_1st_pT":
            if len(gen_pT_list)>=1:
                value = gen_pT_list[0]
            else:
                value = -999
        elif var_name == "genqs_2nd_pT":
            if len(gen_pT_list)>=2:
                value = gen_pT_list[1]
            else:
                value = -999
        elif var_name == "ak4pf_1st_pT":
            if len(pT_list)>=1:
                value = pT_list[0]
            else:
                value = -999
        elif var_name == "ak4pf_2nd_pT":
            if len(pT_list)>=2:
                value = pT_list[1]
            else:
                value = -999

        myhist.Fill(value, weight)
    
    print(myhist.Integral())
    myhist.SetDirectory(0);
    #ROOT.TH1.AddDirectory(ROOT.kFALSE); 
    
    f.Close()
    return myhist
from create_file_list import get_files
def plot_comparison(var_name, xmin, xmax, bin_num, lumi, MC_multi, sample_index_list, plot_folder_name):
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
    new_location = "../root_file_temp/Sicong_20180408/"
    for MC in [MC_list[index] for index in sample_index_list]:
        MC_name = MC["name"]
        file_name_list = MC["file_name_list"]
        if not("(" in MC_name) and "genbosons_id==25" in var_name:
            continue
        sum_hist = ROOT.TH1F("sum_hist"+tmp_var_name+str(len(name_list)),"sum_hist",bin_num,xmin,xmax)
        #sum_hist.SetDirectory(0);  
        #ROOT.TH1.AddDirectory(ROOT.kFALSE);
        sum_dict = {}
        for file_name in file_name_list:
            file_name = new_location + file_name[file_name.rfind("/")+1:]
            print(file_name)
            hist = draw_histo(file_name, var_name, str_condition, bin_num, xmin, xmax)
            sum_hist.Add( sum_hist, hist, 1.0, 1.0 )
            
        if "(" in MC_name:
            sum_hist.Scale(MC_multi)
            MC_name += " x " + str(MC_multi) 
        hist_list.append(sum_hist)
        name_list.append(MC_name)
        
    import sys
    sys.path.insert(0, '/home/users/siconglu/CMSTAS/software/dataMCplotMaker/')
    import dataMCplotMaker

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
            "noOverflow": True,
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
{"var_name":"genqs_1st_pT", "xmin":0, "xmax":1000, "bin_num": 25},\
{"var_name":"genqs_2nd_pT", "xmin":0, "xmax":1000, "bin_num": 25},\
{"var_name":"ak4pf_1st_pT", "xmin":0, "xmax":1000, "bin_num": 25},\
{"var_name":"ak4pf_2nd_pT", "xmin":0, "xmax":1000, "bin_num": 25},\
]

#Common set-up 
lumi = 35.9
#plot_folder_name = "WH_Comparison_20180321_alljets/"
plot_folder_name = "WH_Comparison_20180411_1jet/"
#plot_folder_name = "WH_Comparison_20180315_2jet/"

sample_index_list = [1, 2, 3, 4, 5, 6]
sample_index_list = [4,5,6,7,8,9,10]
sample_index_list = [4,5]
MC_multi = 300
#MC_multi = 5
#Cut-Conditions
from selection_criteria import get_cut_dict, combine_cuts
cut_dict, current_cut_list,region_cut_dict = get_cut_dict()
#Current Ordering of the cut-requirement: (Preselection)
#current_cut_list = ["passTrigger", "passOneLep", "passLepSel", "PassTrackVeto",\
#"PassTauVeto", "ngoodjets","goodbtags", "m_bb", "event_met_pt", "mt"]
current_cut_list = ["passTrigger", "passOneLep", "passLepSel", "PassTrackVeto",\
"PassTauVeto", "event_met_pt", "mt"]

current_condition_list = [cut_dict[item] for item in current_cut_list]
str_condition = combine_cuts(current_condition_list)
str_condition +="&& ngoodjets == 1"
#str_condition +="&& ngoodjets == 2"
str_condition = "("+str_condition+")*scale1fb*"+str(lumi)
#Plotting
for plot_dict in plot_dict_list:
    print(plot_dict)
    plot_comparison(plot_dict["var_name"], plot_dict["xmin"], plot_dict["xmax"], plot_dict["bin_num"], lumi, MC_multi, sample_index_list, plot_folder_name)


