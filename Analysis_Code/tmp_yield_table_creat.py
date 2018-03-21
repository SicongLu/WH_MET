import ROOT
import numpy
import array
ROOT.gStyle.SetOptStat(0);
ROOT.gStyle.SetOptTitle(0);


bin_num = 3
xmin = -1
xmax = 2
var_name = "PassTrackVeto"
lumi = 35.9

from selection_criteria import get_cut_dict
cut_dict, current_cut_list,region_cut_dict = get_cut_dict()
condition_list = [cut_dict[item] for item in current_cut_list]
print(region_cut_dict.keys())



from create_file_list import get_files
MC_list = get_files()
MC = MC_list[6]
print(MC['name'])

new_location = "../root_file_temp/Sicong_20180228/"
total_yield = 0

sum_dict = {}
for file_name in MC['file_name_list']:
    file_name = new_location + file_name[file_name.rfind("/")+1:]
    print(file_name)
    f = ROOT.TFile(file_name)
    t = f.Get("t")
    yield_dict = {}
    for key, str_condition in region_cut_dict.iteritems():
        if not("CR0b" in key):
            continue;
        print(str_condition)
        #str_condition = "((HLT_SingleMu || HLT_SingleEl))"#&&(ngoodleps == 1)&&(nvetoleps == 1)&&(PassTrackVeto == 1)&&(PassTauVeto == 1)&&(ngoodjets == 2)&&(ngoodbtags == 0)&&((mbb > 90 && mbb < 150))&&(mct > 170)&&((pfmet > 125 && pfmet <=200))&&(mt_met_lep > 150)"
        cut_form = ROOT.TTreeFormula("weight"+str_condition,str_condition,t)
        
        lep1_tight_form = ROOT.TTreeFormula("lep1_tight_form"+lep1_tight,lep1_tight,t)
        lep2_tight_form = ROOT.TTreeFormula("lep2_tight_form"+lep2_tight,lep2_tight,t)
        lep1_veto_form = ROOT.TTreeFormula("lep1_tight_form"+lep1_veto,lep1_veto,t)
        lep2_veto_form = ROOT.TTreeFormula("lep2_tight_form"+lep2_veto,lep2_veto,t)
        
        resulted_event_num = 0
        print(t.GetEntries())
        for i in range(t.GetEntries()):
            t.GetEntry(i)
            if i%1e4 == 0:
                print(i)
            print(lep1_tight)
            ntightleps = lep1_tight_form.EvalInstance() + lep2_tight_form.EvalInstance()
            nvetoleps = lep2_veto_form.EvalInstance() + lep2_veto_form.EvalInstance()
            
            print("tight: %.0f good: %.0f"%(ntightleps, t.ngoodleps)) 
            if not( cut_form.EvalInstance()):
                continue;
            
            resulted_event_num += t.scale1fb
        resulted_event_num = resulted_event_num * 35.9
        str_condition = "("+str_condition+")*scale1fb*"+str(lumi)
#        myhist_name = "myhist"+key
#        myhist = ROOT.TH1F(myhist_name,myhist_name,bin_num,xmin,xmax);
#        t.Draw(var_name+">>"+myhist_name,str_condition,"goff")
#        resulted_event_num = myhist.Integral()
        cut_name = key
        yield_dict[cut_name] = resulted_event_num
        print(key+": %.5f   "%resulted_event_num),
        print(" ")
    f.Close()
    print(yield_dict)
    
    for key, value in yield_dict.iteritems():
        if key in sum_dict.keys():
            sum_dict[key]+=yield_dict[key]
        else:
            sum_dict[key]=yield_dict[key]
print(sum_dict) 