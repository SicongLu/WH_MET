import ROOT
import numpy
import array
import math
ROOT.gStyle.SetOptStat(0);
ROOT.gStyle.SetOptTitle(0);
def delta_R(v1, v2):
    dphi = abs(v1.Phi()-v2.Phi())
    if dphi>math.pi: dphi = 2*math.pi - dphi
    deta = abs(v1.Eta()-v2.Eta())
    dR = numpy.sqrt(dphi*dphi+deta*deta)
    return dR
def draw_histo_2D(file_name, str_condition, var_dict1,var_dict2):
    #print(file_name, var_name, str_condition, bin_num, xmin, xmax)
    BTAGWP = 0.5426; #Loose btag working point
    mBTAGWP = 0.8484; #Medium btag working point
    #
    f = ROOT.TFile(file_name)
    t = f.Get("t")
    myhist = ROOT.TH2F("myhist","myhist",\
    var_dict1["bin_num"],var_dict1["xmin"],var_dict1["xmax"],\
    var_dict2["bin_num"],var_dict2["xmin"],var_dict2["xmax"]);
    print(var_dict1["var_name"])
    print("dR" in var_dict1["var_name"] or "sublead" in var_dict1["var_name"])
    if not("dR" in var_dict1["var_name"] or "sublead" in var_dict1["var_name"]):
        t.Draw(var_dict2["var_name"]+":"+var_dict1["var_name"]+">>myhist",str_condition,"goff")
    elif var_dict1["var_name"] == "dR_bb_gen":
        weight_form = ROOT.TTreeFormula("weight",str_condition,t)
        for i in range(t.GetEntries()):
            if i % 1e4 == 0: print(i)
            t.GetEntry(i)
            dR_bb = -999
            weight = weight_form.EvalInstance()
            #if weight == 0:
            #    continue
            v1 = 0
            m_id = t.genqs_motherid
            for i in range(len(m_id)):
                if t.genqs_motherid.at(i) == 25:
                    if v1 == 0: v1 = t.genqs_p4.at(i)
                    else: v2 = t.genqs_p4.at(i)
            if v1 == v2:
                continue;
            dR_bb = delta_R(v1,v2)          
            value = -999
            for i in range(len(t.genbosons_id)):
                if t.genbosons_id.at(i) == 25:
                    value = t.genbosons_p4.at(i).Pt()
            myhist.Fill(dR_bb, value, weight)
    elif var_dict1["var_name"] == "sublead_bjet_pt":
        weight_form = ROOT.TTreeFormula("weight",str_condition,t)
        for i in range(t.GetEntries()):
            if i % 1e4 == 0: print(i)
            t.GetEntry(i)
            weight = weight_form.EvalInstance()
            if weight == 0:
                continue
            lead_btag_vec = t.ak4pfjets_leadbtag_p4
            sub_lead_btag_pt = 1
            for i_jet in range(len(t.ak4pfjets_p4)):
                #if not(t.ak4pfjets_p4.at(i_jet).Pt()>30 and \
                #t.ak4pfjets_p4.at(i_jet).Eta()<2.4 and \
                #t.ak4pfjets_loose_pfid.at(i_jet)): 
                #    continue;
                if t.ak4pfjets_CSV.at(i_jet)>BTAGWP and not(t.ak4pfjets_CSV.at(i_jet) == lead_btag_vec):
                    sub_lead_btag_pt = t.ak4pfjets_p4.at(i_jet).Pt()
            for i in range(len(t.genbosons_id)):
                if t.genbosons_id.at(i) == 25:
                    value = t.genbosons_p4.at(i).Pt()
            myhist.Fill(sub_lead_btag_pt, value, weight)
    print(myhist.Integral())
    myhist.SetDirectory(0);
    #ROOT.TH1.AddDirectory(ROOT.kFALSE); 
    
    f.Close()
    return myhist
from create_file_list import get_files
def flatten_var_name(var_name):
    #Remove special chars in var_name:
    tmp_var_name = var_name[:]
    char_str = "!@#$%^&*()[]{};:,./<>?\|`~-=_+"
    char_str = [char_str[i] for i in range(len(char_str))]
    for char in char_str:
        tmp_var_name = tmp_var_name.replace(char,"_")
    return tmp_var_name
def plot_comparison(var_dict1, var_dict2, lumi, MC_multi, sample_index, plot_folder_name):
    #Collect histograms
    MC_list = get_files()
    new_location = "../root_file_temp/Sicong_20180228/"
    MC = MC_list[sample_index]
    MC_name = MC["name"]
    #Collecting the plot
    file_name_list = MC["file_name_list"]

    sum_hist = ROOT.TH2F("sum_hist","sum_hist",\
    var_dict1["bin_num"],var_dict1["xmin"],var_dict1["xmax"],\
    var_dict2["bin_num"],var_dict2["xmin"],var_dict2["xmax"])
    #sum_hist.SetDirectory(0);  
    #ROOT.TH1.AddDirectory(ROOT.kFALSE);
    sum_dict = {}
    for file_name in file_name_list:
        file_name = new_location + file_name[file_name.rfind("/")+1:]
        print(file_name)
        hist = draw_histo_2D(file_name, str_condition, var_dict1, var_dict2)
        sum_hist.Add( sum_hist, hist, 1.0, 1.0 )
    if "(" in MC_name:
        sum_hist.Scale(MC_multi)
        MC_name += " x " + str(MC_multi) 
        
    ROOT.gStyle.SetOptStat(0);
    ROOT.gStyle.SetOptTitle(0);
    canvas = ROOT.TCanvas("can","can",800,800)
    canvas.SetBorderMode(0);
    canvas.SetBorderSize(2);
    canvas.SetTickx(1);
    canvas.SetTicky(1);
    canvas.SetLeftMargin(0.1);
    canvas.SetRightMargin(0.1);
    canvas.SetTopMargin(0.1);
    canvas.SetBottomMargin(0.1);
    canvas.SetFrameBorderMode(0);
    sum_hist.Draw("colz")
    canvas.Update()
    canvas.SetTitle(MC_name)
    sum_hist.GetXaxis().SetTitle(var_dict1["var_name"]);
    sum_hist.GetYaxis().SetTitle(var_dict2["var_name"]); 
    
    outputName = "/home/users/siconglu/CMSTAS/software/niceplots/"+plot_folder_name+\
    flatten_var_name(var_dict1["var_name"])+"VS"+flatten_var_name(var_dict2["var_name"])+".pdf"
    canvas.Print(outputName)
    
    

#Basic Set-up
#Other relevant set-up
plot_dict_list = [\
{"var_name":"mct", "xmin":0, "xmax":800, "bin_num": 40},\
{"var_name":"ptbb", "xmin":20, "xmax":800, "bin_num": 40},\
{"var_name":"genbosons_p4.fCoordinates.Pt()*(genbosons_id==25)", "xmin":25, "xmax":800, "bin_num": 40},\
{"var_name":"dR_bb", "xmin":0, "xmax":5, "bin_num": 20},\
{"var_name":"dR_bb_gen", "xmin":0, "xmax":4, "bin_num": 40},\
{"var_name":"sublead_bjet_pt", "xmin":0, "xmax":200, "bin_num": 40},\
{"var_name":"mbb", "xmin":0, "xmax":300, "bin_num": 20},\
{"var_name":"ngoodjets", "xmin":0, "xmax":10, "bin_num": 10},\
{"var_name":"genbosons_id", "xmin":15, "xmax":30, "bin_num": 15},\
{"var_name":"genbosons_p4.fCoordinates.M()", "xmin":50, "xmax":150, "bin_num": 25},\
{"var_name":"genbosons_p4.fCoordinates.M()*(genbosons_id==25)", "xmin":50, "xmax":150, "bin_num": 25},\
{"var_name":"pfmet", "xmin":0, "xmax":600, "bin_num": 30},\
{"var_name":"mt_met_lep", "xmin":10, "xmax":600, "bin_num": 20},\
{"var_name":"MT2W", "xmin":20, "xmax":600, "bin_num": 20},\
{"var_name":"Mlb_closestb", "xmin":10, "xmax":300, "bin_num": 20},\
{"var_name":"topness", "xmin":-10, "xmax":10, "bin_num": 20},\
{"var_name":"topnessMod", "xmin":-10, "xmax":10, "bin_num": 20},\
{"var_name":"mindphi_met_j1_j2", "xmin":0, "xmax":5, "bin_num": 20},\
{"var_name":"mbb*(ptbb>100)", "xmin":50, "xmax":200, "bin_num": 20},\
{"var_name":"mbb*(ptbb>200)", "xmin":50, "xmax":200, "bin_num": 20},\
{"var_name":"mbb*(ptbb>300)", "xmin":50, "xmax":200, "bin_num": 20},\
{"var_name":"mbb*(ptbb>400)", "xmin":50, "xmax":200, "bin_num": 20},\
{"var_name":"mbb*(ptbb>450)", "xmin":50, "xmax":200, "bin_num": 20},\
{"var_name":"mbb*(ptbb>500)", "xmin":50, "xmax":200, "bin_num": 20},\
]

#Common set-up 
lumi = 35.9
plot_folder_name = "WH_Analysis_Correlations_1jet/"
sample_index_list = [5]

MC_multi = 5
#Cut-Conditions
from selection_criteria import get_cut_dict, combine_cuts
cut_dict, current_cut_list,region_cut_dict = get_cut_dict()
#Current Ordering of the cut-requirement: (Preselection)
current_cut_list = ["passTrigger", "passOneLep", "passLepSel", "PassTrackVeto",\
"PassTauVeto", "event_met_pt", "mt"]
#"PassTauVeto","3goodjets", "goodbtags", "m_bb", "event_met_pt", "mt"]
#"PassTauVeto","ngoodjets", "goodbtags", "m_bb", "mctbb", "event_met_pt", "mt"]
#"PassTauVeto","3goodjets", "goodbtags", "m_bb", "mctbb", "event_met_pt", "mt"]
current_condition_list = [cut_dict[item] for item in current_cut_list]
str_condition = combine_cuts(current_condition_list)
#str_condition = "("+str_condition+"&& ngoodjets == 1)*scale1fb*"+str(lumi)
str_condition = "("+str_condition+"&& ngoodjets == 1)*scale1fb*"+str(lumi)
#Plotting
for sample_index in sample_index_list:
#    plot_comparison(plot_dict_list[0], plot_dict_list[2], lumi, MC_multi, sample_index, plot_folder_name)
#    plot_comparison(plot_dict_list[0], plot_dict_list[1], lumi, MC_multi, sample_index, plot_folder_name)
#    plot_comparison(plot_dict_list[1], plot_dict_list[2], lumi, MC_multi, sample_index, plot_folder_name)
#    plot_comparison(plot_dict_list[4], plot_dict_list[2], lumi, MC_multi, sample_index, plot_folder_name)
    plot_comparison(plot_dict_list[5], plot_dict_list[2], lumi, MC_multi, sample_index, plot_folder_name)

