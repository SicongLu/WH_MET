from selection_criteria import get_cut_dict, combine_cuts
cut_dict, current_cut_list,region_cut_dict = get_cut_dict()

import ROOT

from create_file_list import get_files, get_tmp_files
MC_list = get_tmp_files()
hist_list = []
name_list = []
new_location = "../root_file_temp/Sicong_20180422/"
str_condition = cut_dict["passTrigger"]#region_cut_dict["SR2"]
str_condition += "&&" + cut_dict["passOneLep"]
str_condition += "&&" + cut_dict["passLepSel"]
str_condition += "&&" + cut_dict["PassTrackVeto"]
str_condition += "&&" + cut_dict["PassTauVeto"]
str_condition_1jet = "((ngoodjets == 1 && ak4pfjets_p4[0].fCoordinates.Pt()>=30) ||"+\
"(ngoodjets >= 2 && ak4pfjets_p4[0].fCoordinates.Pt()>=30 && ak4pfjets_p4[1].fCoordinates.Pt()<30))"
#str_condition += "&&"+str_condition_1jet+"&& ak8pfjets_p4[0].fCoordinates.Pt()>=400"
#str_condition += "&&" + cut_dict["event_met_pt"]
#str_condition += "&&" + cut_dict["mt"]

str_condition_2jet = "((ngoodjets == 2 && ak4pfjets_p4[1].fCoordinates.Pt()>=30) ||"+\
"(ngoodjets >= 3 && ak4pfjets_p4[1].fCoordinates.Pt()>=30 && ak4pfjets_p4[2].fCoordinates.Pt()<30))"
#
str_condition_2jet_lowered = "((ngoodjets == 2 && ak4pfjets_p4[0].fCoordinates.Pt()>=30 && ak4pfjets_p4[1].fCoordinates.Pt()>=20 && ak4pfjets_p4[1].fCoordinates.Pt()<40))"# ||"+\
#"(ngoodjets >= 3 && ak4pfjets_p4[0].fCoordinates.Pt()>=30 && ak4pfjets_p4[1].fCoordinates.Pt()>=20  ))"# && ak4pfjets_p4[2].fCoordinates.Pt()<20
str_condition += "&&" + str_condition_2jet_lowered
#str_condition += "&&" + cut_dict["goodbtags"]
#str_condition += "&&" + cut_dict["m_bb"]
#str_condition += "&&" + cut_dict["mctbb"]
#str_condition += "&&" + cut_dict["event_met_pt_high"]
#str_condition += "&&" + cut_dict["mt"]
 
for MC in MC_list:
    MC_name = MC["name"]
    file_name_list = MC["file_name_list"]
    file_name = file_name_list[0]
    file_name = new_location + file_name[file_name.rfind("/")+1:]
    f = ROOT.TFile(file_name)
    t = f.Get("t")
    event_num = t.GetEntries(str_condition)
    print(MC_name, event_num)
    f.Close()



#('new (700,1)',  2.38 
#('new (700,100)' 2.24 
#('new (700,150)' 2.30 
#('new (600,1)',  4.09 
#('new (600,100)' 3.86
#('new (600,150)' 3.81

#('new (700,1)', 1111L) 0.00214
#('new (700,100)', 1079L)0.002
#('new (700,150)', 1181L) 0.0019
#('new (600,1)', 940L) 0.004
#('new (600,100)', 904L)
#('new (600,150)', 838L)

#The new region: ak8>600
#('new (700,1)', 369L) about 1 event...
#('new (700,100)', 323L)
#('new (700,150)', 315L)
#('new (600,1)', 235L)
#('new (600,100)', 171L)
#('new (600,150)', 153L)
#('new 2l top', 0L)
#('new 1l top', 0L)

#The new region: ak8>450
#('new (700,1)', 668L)
#('new (700,100)', 676L)
#('new (700,150)', 647L)
#('new (600,1)', 484L)
#('new (600,100)', 415L)
#('new (600,150)', 372L)
#('new 2l top', 1L)
#('new 1l top', 2L)

#The new region: ak8>450 + met>125+mt>150
#('new (700,1)', 479L)
#('new (700,100)', 486L)
#('new (700,150)', 454L)
#('new (600,1)', 334L)
#('new (600,100)', 289L)
#('new (600,150)', 262L)
#('new 2l top', 0L)
#('new 1l top', 0L)


