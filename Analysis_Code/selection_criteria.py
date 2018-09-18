'''
This section intends to provide a comprehensive definition of relevant cut-requirement.
One shall try to mimic the naming convention from Dr Mia Liu.
'''
def combine_cuts(cut_list):
    cut_str = ""
    str_condition = "1"
    for i in range(len(cut_list)):
        str_condition += "&&"
        str_condition += "("+cut_list[i]+")"
    return str_condition

def get_lep_selection_str():
    '''Do the lepton selection definition, the naming convention follows Dr Miaoyuan Liu.
    https://github.com/mialiu149/AnalysisLoopers2015/blob/master/sharedCode/EventTypeSel.cc
    '''
    pdg_id_el = 11
    pdg_id_mu = 13
    
    sel_pt_el = 30
    sel_pt_mu = 25
    veto_pt_el = 5         
    veto_pt_mu = 5
    
    sel_eta_el = 1.442
    sel_eta_mu = 2.1
    veto_eta_el = 2.4
    veto_eta_mu = 2.4
    
    sel_miniRelIso_el  = 0.1;
    sel_miniRelIso_mu  = 0.1;
    veto_miniRelIso_el = 0.2;
    veto_miniRelIso_mu = 0.2;
    
    #Tight
    lep1el_str = "abs(lep1_pdgid)==%.0f && lep1_p4.Pt()>%.0f && fabs(lep1_p4.Eta())<%.3f && lep1_MiniIso < %.2f"\
    %(pdg_id_el, sel_pt_el, sel_eta_el,sel_miniRelIso_el) \
    +"&& lep1_passMediumID && lep1_relIso*lep1_p4.Pt() < 5"
    
    lep1mu_str = "abs(lep1_pdgid)==%.0f && lep1_p4.Pt()>%.0f && fabs(lep1_p4.Eta())<%.3f && lep1_MiniIso < %.2f"\
    %(pdg_id_mu, sel_pt_mu, sel_eta_mu,sel_miniRelIso_mu) \
    +"&& lep1_passTightID && lep1_relIso*lep1_p4.Pt() < 5"
    
    lep2el_str = lep1el_str.replace("lep1","lep2")
    lep2mu_str = lep1mu_str.replace("lep1","lep2")
    
    lep1_tight = "("+lep1el_str+")||("+lep1mu_str+")"
    lep2_tight = "("+lep2el_str+")||("+lep2mu_str+")"
    
    #Veto
    lep1el_str = "abs(lep1_pdgid) == %.0f && lep1_p4.Pt()>%.0f && abs(lep1_p4.Eta())<%.3f && lep1_MiniIso < %.2f"\
    %(pdg_id_el, veto_pt_el, veto_eta_el,veto_miniRelIso_el) +" && lep1_passVeto "
    lep1mu_str = "abs(lep1_pdgid) == %.0f && lep1_p4.Pt()>%.0f && abs(lep1_p4.Eta())<%.3f && lep1_MiniIso < %.2f"\
    %(pdg_id_mu, veto_pt_mu, veto_eta_mu,veto_miniRelIso_mu) +" && lep1_passVeto"
    lep2el_str = lep1el_str.replace("lep1","lep2")
    lep2mu_str = lep1mu_str.replace("lep1","lep2")
    
    lep1_veto = "("+lep1el_str+")||("+lep1mu_str+")"
    lep2_veto = "("+lep2el_str+")||("+lep2mu_str+")"
    
    #Sum
    ntight_lep_str = "("+lep1_tight+")+("+lep2_tight+")"
    nveto_lep_str = "("+lep1_veto+")+("+lep2_veto+")"
    
    return lep1_tight, lep2_tight, lep1_veto, lep2_veto, ntight_lep_str, nveto_lep_str
    
    
def get_cut_dict(if_new_sample = False):
    '''The selection criteria is currently following:
    https://github.com/mialiu149/AnalysisLoopers2015/blob/master/sharedCode/WHSelection.cc
    '''
    lep1_tight, lep2_tight, lep1_veto, lep2_veto, ntight_lep_str, nveto_lep_str = get_lep_selection_str()
    cut_dict = {}
    cut_dict['passTrigger'] = "(HLT_SingleMu || HLT_SingleEl)"
    cut_dict['passOneLep'] = "lep1_tight"
    cut_dict['passLepSel'] = "!(lep2_veto||lep2_tight)"
    cut_dict['passTwoLep'] = "(lep2_veto||lep2_tight)"

    cut_dict['PassTrackVeto'] = "PassTrackVeto"
    cut_dict['PassTauVeto'] = "PassTauVeto"
    cut_dict['inverted_PassTrackVeto'] = "!(PassTrackVeto)" 
    cut_dict['inverted_PassTauVeto'] = "!(PassTauVeto)"
    cut_dict['Hadronic_Tau'] = "!(PassTauVeto && PassTrackVeto)"
    
    #if_new_sample = False #The new sample lower the pt cut to 25
    if_new_vars = True #Use the variable that is renewed for fastsim...
    if if_new_sample:
        cut_dict['ngoodjets'] = "ngoodjets30 == 2"
        cut_dict['3goodjets'] = "ngoodjets30 == 3"
    else:
        cut_dict['ngoodjets'] = "ngoodjets == 2"
        cut_dict['3goodjets'] = "ngoodjets == 3"
    cut_dict['4moregoodjets'] = "ngoodjets >= 4" #Remove if it is checked to be useless.
    cut_dict['2ormoregoodjets'] = "ngoodjets >= 2"
    
    cut_dict['goodbtags'] = "nbtag_loose >= 2 && nbtag_med >= 1"
    cut_dict['zerobtags'] = "nbtag_loose == 0" 
    
    cut_dict['one_ak4jet'] = "ngoodjets30 <= 1"
    cut_dict['one_ak8jet'] = "ak8GoodPFJets >= 1"
    cut_dict['ak8jetpt600'] = "ak8pfjets_p4[0].Pt() >= 600"
    cut_dict['ak8jetpt500'] = "ak8pfjets_p4[0].Pt() >= 500"
    cut_dict['ak8jetpt400'] = "ak8pfjets_p4[0].Pt() >= 400"
    cut_dict['ak8jetpt300'] = "ak8pfjets_p4[0].Pt() >= 300"
    cut_dict['ak8jet_hbb'] = "ak8pfjets_deep_rawdisc_hbb[0] >= 0.5"
    
    cut_dict['2jet_recover'] = "!(ak8GoodPFJets >= 1 && ak8pfjets_deep_rawdisc_hbb[0] >= 0.5) && ngoodjets30 <= 2 && ngoodjets > 1"
    cut_dict['2jet_recover_new'] = "!(ak8GoodPFJets >= 1 && ak8pfBoostedDoubleSecondaryVertexAK8BJetTags[0] >= 0.5) && ngoodjets30 <= 2 && ngoodjets > 1"
    
    if if_new_vars:
        cut_dict['m_bb'] =  "(new_mbb > 90 && new_mbb < 150)"
        cut_dict['m_bb_csv_rank'] =  "(new_mbb_csv_rank > 90 && new_mbb_csv_rank < 150)"
        cut_dict['inverted_m_bb'] =  "!(new_mbb > 90 && new_mbb < 150)"
        cut_dict['event_met_pt'] =  "new_met > 125"
        cut_dict['event_met_pt_med'] =  "(new_met > 125 && new_met <=200)"
        cut_dict['event_met_pt_high'] =  "(new_met > 200)"
        cut_dict['mt'] =  "new_mt > 150"
        cut_dict['mctbb'] =  "new_mct > 170"
        cut_dict['mctbb_csv_rank'] =  "new_mct_csv_rank > 170"
        cut_dict['mctbb_csv_rank225'] =  "new_mct_csv_rank > 225"
    else:
        cut_dict['m_bb'] =  "(mbb > 90 && mbb < 150)"
        cut_dict['inverted_m_bb'] =  "!(mbb > 90 && mbb < 150)"
        cut_dict['event_met_pt'] =  "(pfmet > 125)"
        cut_dict['event_met_pt_med'] =  "(pfmet > 125 && pfmet <=200)"
        cut_dict['event_met_pt_high'] =  "(pfmet > 200)"
        cut_dict['mt'] =  "mt_met_lep > 150"
        cut_dict['mctbb'] =  "mct > 170"

    cut_dict["2vars"] = "ak4_htratiom < 0.3 && mindphi_met_j1_j2 > 1"
    
    #Current Ordering of the cut-requirement: (Preselection)
    current_cut_list = ["passTrigger", "passOneLep", "passLepSel", "PassTrackVeto",\
     "PassTauVeto", "ngoodjets", "goodbtags", "m_bb", "mctbb", "event_met_pt", "mt"]
    
    Pre_cut_list = ["passTrigger", "passOneLep", "passLepSel", "PassTrackVeto",\
     "PassTauVeto",   "event_met_pt", "mt"]#"goodbtags","m_bb", "mctbb",
    region_cut_dict = {}
    
    Pre_condition_list = [cut_dict[item] for item in Pre_cut_list]
    Pre_cut = combine_cuts(Pre_condition_list)
    
    region_cut_dict["Preselection"] = Pre_cut
    #Definition of Signal Region (SR1, SR2) and Control Region (CR2l, CR0b, CRMbb)
    SR1_list = ["passTrigger", "passOneLep", "passLepSel", "PassTrackVeto",\
    "PassTauVeto", "ngoodjets", "goodbtags", "m_bb", "mctbb", "event_met_pt_med", "mt"]
    SR1_condition_list = [cut_dict[item] for item in SR1_list]
    SR1_cut = combine_cuts(SR1_condition_list)   #str_condition = "("+str_condition+")*"+scale_str
    
    SR2_list = ["passTrigger", "passOneLep", "passLepSel", "PassTrackVeto",\
    "PassTauVeto", "ngoodjets", "goodbtags", "m_bb", "mctbb", "event_met_pt_high", "mt"]
    SR2_condition_list = [cut_dict[item] for item in SR2_list]
    SR2_cut = combine_cuts(SR2_condition_list)
    
    region_cut_dict["SR1"] = SR1_cut
    region_cut_dict["SR2"] = SR2_cut
    
    #CR2l
    CR2l_list_1 = ["passTrigger", "passOneLep", "passLepSel", "Hadronic_Tau",\
    "ngoodjets", "goodbtags", "event_met_pt", "mt"]
    CR2l_condition_list_1 = [cut_dict[item] for item in CR2l_list_1]
    CR2l_cut_1 = combine_cuts(CR2l_condition_list_1)

    CR2l_list_2 = ["passTrigger", "passTwoLep", "ngoodjets", "goodbtags", "event_met_pt", "mt"]
    CR2l_condition_list_2 = [cut_dict[item] for item in CR2l_list_2]
    CR2l_cut_2 = combine_cuts(CR2l_condition_list_2)
    
    CR2l_cut = "("+CR2l_cut_1+")||("+CR2l_cut_2+")"
    #region_cut_dict["CR2l"] = CR2l_cut
    region_cut_dict["CR2l"] = CR2l_cut
    #region_cut_dict["CR2l_1"] = CR2l_cut_1
    
    #CR0b
    CR0b1_list = ["passTrigger", "passOneLep", "passLepSel", "PassTrackVeto",\
    "PassTauVeto", "ngoodjets", "zerobtags", "m_bb", "mctbb", "event_met_pt_med", "mt"]
    CR0b1_condition_list = [cut_dict[item] for item in CR0b1_list]
    CR0b1_cut = combine_cuts(CR0b1_condition_list)   
    
    CR0b2_list = ["passTrigger", "passOneLep", "passLepSel", "PassTrackVeto",\
    "PassTauVeto", "ngoodjets", "zerobtags", "m_bb", "mctbb", "event_met_pt_high", "mt"]
    CR0b2_condition_list = [cut_dict[item] for item in CR0b2_list]
    CR0b2_cut = combine_cuts(CR0b2_condition_list)
    
    region_cut_dict["CR0b1"] = CR0b1_cut
    region_cut_dict["CR0b2"] = CR0b2_cut
    region_cut_dict["CR0b_inclusive"] = "("+CR0b1_cut+")||("+CR0b2_cut+")"
    
    #CRMbb
    CRMbb1_list = ["passTrigger", "passOneLep", "passLepSel", "PassTrackVeto",\
    "PassTauVeto", "ngoodjets", "goodbtags", "inverted_m_bb", "mctbb", "event_met_pt_med", "mt"]
    CRMbb1_condition_list = [cut_dict[item] for item in CRMbb1_list]
    CRMbb1_cut = combine_cuts(CRMbb1_condition_list)   
    
    CRMbb2_list = ["passTrigger", "passOneLep", "passLepSel", "PassTrackVeto",\
    "PassTauVeto", "ngoodjets", "goodbtags", "inverted_m_bb", "mctbb", "event_met_pt_high", "mt"]
    CRMbb2_condition_list = [cut_dict[item] for item in CRMbb2_list]
    CRMbb2_cut = combine_cuts(CRMbb2_condition_list)
    
    region_cut_dict["CRMbb1"] = CRMbb1_cut
    region_cut_dict["CRMbb2"] = CRMbb2_cut
    region_cut_dict["CRMbb_inclusive"] = "("+CRMbb1_cut+")||("+CRMbb2_cut+")"
    
    #CR3j_2l
    CR3j_2l_list_1 = ["passTrigger", "passOneLep", "passLepSel", "Hadronic_Tau",\
    "3goodjets", "goodbtags", "event_met_pt", "mt"]
    CR3j_2l_condition_list_1 = [cut_dict[item] for item in CR3j_2l_list_1]
    CR3j_2l_cut_1 = combine_cuts(CR3j_2l_condition_list_1)

    CR3j_2l_list_2 = ["passTrigger", "passTwoLep", "3goodjets", "goodbtags", "event_met_pt", "mt"]
    CR3j_2l_condition_list_2 = [cut_dict[item] for item in CR3j_2l_list_2]
    CR3j_2l_cut_2 = combine_cuts(CR3j_2l_condition_list_2)
    
    CR3j_2l_cut = "("+CR3j_2l_cut_1+")||("+CR3j_2l_cut_2+")"
    #region_cut_dict["CR3j_2l"] = CR3j_2l_cut
    region_cut_dict["CR3j_2l"] = CR3j_2l_cut
    #region_cut_dict["CR3j_2l_1"] = CR3j_2l_cut_1
    
    #CR3j_0b
    CR3j_0b1_list = ["passTrigger", "passOneLep", "passLepSel", "PassTrackVeto",\
    "PassTauVeto", "3goodjets", "zerobtags", "m_bb", "mctbb", "event_met_pt_med", "mt"]
    CR3j_0b1_condition_list = [cut_dict[item] for item in CR3j_0b1_list]
    CR3j_0b1_cut = combine_cuts(CR3j_0b1_condition_list)   
    
    CR3j_0b2_list = ["passTrigger", "passOneLep", "passLepSel", "PassTrackVeto",\
    "PassTauVeto", "3goodjets", "zerobtags", "m_bb", "mctbb", "event_met_pt_high", "mt"]
    CR3j_0b2_condition_list = [cut_dict[item] for item in CR3j_0b2_list]
    CR3j_0b2_cut = combine_cuts(CR3j_0b2_condition_list)
    
    region_cut_dict["CR3j_0b1"] = CR3j_0b1_cut
    region_cut_dict["CR3j_0b2"] = CR3j_0b2_cut
    region_cut_dict["CR3j_0b_inclusive"] = "("+CR3j_0b1_cut+")||("+CR3j_0b2_cut+")"
    
    #CR3j_Mbb
    CR3j_Mbb1_list = ["passTrigger", "passOneLep", "passLepSel", "PassTrackVeto",\
    "PassTauVeto", "3goodjets", "goodbtags", "inverted_m_bb", "mctbb", "event_met_pt_med", "mt"]
    CR3j_Mbb1_condition_list = [cut_dict[item] for item in CR3j_Mbb1_list]
    CR3j_Mbb1_cut = combine_cuts(CR3j_Mbb1_condition_list)   
    
    CR3j_Mbb2_list = ["passTrigger", "passOneLep", "passLepSel", "PassTrackVeto",\
    "PassTauVeto", "3goodjets", "goodbtags", "inverted_m_bb", "mctbb", "event_met_pt_high", "mt"]
    CR3j_Mbb2_condition_list = [cut_dict[item] for item in CR3j_Mbb2_list]
    CR3j_Mbb2_cut = combine_cuts(CR3j_Mbb2_condition_list)
    
    region_cut_dict["CR3j_Mbb1"] = CR3j_Mbb1_cut
    region_cut_dict["CR3j_Mbb2"] = CR3j_Mbb2_cut
    region_cut_dict["CR3j_Mbb_inclusive"] = "("+CR3j_Mbb1_cut+")||("+CR3j_Mbb2_cut+")"
        
    #Proposed SR 
    PSR_list = ["passTrigger", "passOneLep", "passLepSel", "PassTrackVeto",\
    "PassTauVeto", "3goodjets", "goodbtags", "m_bb", "event_met_pt_high", "mt"]
    PSR_condition_list = [cut_dict[item] for item in PSR_list]
    PSR_cut = combine_cuts(PSR_condition_list)
    
    region_cut_dict["PSR3jet_met_200_mct200"] = PSR_cut + "&& new_mct > 200"
    region_cut_dict["PSR3jet_met_200_mct225"] = PSR_cut + "&& new_mct > 225"
    region_cut_dict["PSR3jet_met_200_mct250"] = PSR_cut + "&& new_mct > 250"
    region_cut_dict["PSR3jet_met_200_mct275"] = PSR_cut + "&& new_mct > 275"
    region_cut_dict["PSR3jet_met_200_mct225_xgb_0p4"] = PSR_cut + "&& new_mct > 225"+"&& xgb_proba>0.4"
    region_cut_dict["PSR3jet_met_200_mct225_xgb_0p2"] = PSR_cut + "&& new_mct > 225"+"&& xgb_proba>0.2"
    region_cut_dict["PSR3jet_met_200_mct200_xgb_0p4"] = PSR_cut + "&& new_mct > 200"+"&& xgb_proba>0.4"
    region_cut_dict["PSR3jet_met_200_mct200_xgb_0p2"] = PSR_cut + "&& new_mct > 200"+"&& xgb_proba>0.2"
        
    #Test even higher met...
    region_cut_dict["PSR3jet_met_225_mct225"] = PSR_cut + "&& new_met > 225 && new_mct > 225"
    region_cut_dict["PSR3jet_met_225_mct225_2vars"] = region_cut_dict["PSR3jet_met_225_mct225"] + "&&"+ cut_dict["2vars"]
    region_cut_dict["PSR3jet_met_200_mct225_2vars"] = region_cut_dict["PSR3jet_met_200_mct225"] + "&&"+ cut_dict["2vars"]
    
    #Test the mct included with the ISR:
    
    PSR_list = ["passTrigger", "passOneLep", "passLepSel", "PassTrackVeto",\
    "PassTauVeto", "3goodjets", "goodbtags", "m_bb_csv_rank", "event_met_pt", "mt"]
    PSR_condition_list = [cut_dict[item] for item in PSR_list]
    PSR_cut = combine_cuts(PSR_condition_list)
    region_cut_dict["PSR3jet_met_125_mct200_ISR"] = PSR_cut + "&& new_mct_csv_rank > 200"
    region_cut_dict["PSR3jet_met_125_mct225_ISR"] = PSR_cut + "&& new_mct_csv_rank > 225"
    region_cut_dict["PSR3jet_met_125_mct250_ISR"] = PSR_cut + "&& new_mct_csv_rank > 250"
    region_cut_dict["PSR3jet_met_125_mct275_ISR"] = PSR_cut + "&& new_mct_csv_rank > 275"
    
    PSR_list = ["passTrigger", "passOneLep", "passLepSel", "PassTrackVeto",\
    "PassTauVeto", "3goodjets", "goodbtags", "m_bb_csv_rank", "event_met_pt_high", "mt"]
    PSR_condition_list = [cut_dict[item] for item in PSR_list]
    PSR_cut = combine_cuts(PSR_condition_list)
    region_cut_dict["PSR3jet_met_200_mct200_ISR"] = PSR_cut + "&& new_mct_csv_rank > 200"
    region_cut_dict["PSR3jet_met_200_mct225_ISR"] = PSR_cut + "&& new_mct_csv_rank > 225"
    region_cut_dict["PSR3jet_met_200_mct250_ISR"] = PSR_cut + "&& new_mct_csv_rank > 250"
    region_cut_dict["PSR3jet_met_200_mct275_ISR"] = PSR_cut + "&& new_mct_csv_rank > 275"
    region_cut_dict["PSR3jet_met_225_mct225_ISR"] = PSR_cut + "&& new_met > 225 && new_mct_csv_rank > 225"
    region_cut_dict["PSR3jet_met_225_mct225_2vars_ISR"] = region_cut_dict["PSR3jet_met_225_mct225_ISR"] + "&&"+ cut_dict["2vars"]

    PSR_list = ["passTrigger", "passOneLep", "passLepSel", "PassTrackVeto",\
    "PassTauVeto", "3goodjets", "goodbtags", "m_bb", "event_met_pt", "mt"]
    PSR_condition_list = [cut_dict[item] for item in PSR_list]
    PSR_cut = combine_cuts(PSR_condition_list)
    region_cut_dict["PSR3jet_mct275"] = PSR_cut + "&& new_mct > 275"
    region_cut_dict["PSR3jet_mct300"] = PSR_cut + "&& new_mct > 300"
    
    #Proposed SR 1 fat jet
    PSR_list = ["passTrigger", "passOneLep", "passLepSel", "PassTrackVeto",\
    "PassTauVeto", "one_ak4jet","one_ak8jet", "event_met_pt_high", "mt"]#"m_bb",
    PSR_condition_list = [cut_dict[item] for item in PSR_list]
    PSR_cut = combine_cuts(PSR_condition_list)

    region_cut_dict["PSR1jet_met_200_pt_300"] = PSR_cut+"&&"+cut_dict['ak8jetpt300']
    region_cut_dict["PSR1jet_met_200_pt_300_hbb"] = PSR_cut+"&&"+cut_dict['ak8jetpt300']+"&&ak8pfjets_deep_rawdisc_hbb[0]>0.5"
    region_cut_dict["PSR1jet_met_200_pt_300_hbb0p9"] = PSR_cut+"&&"+cut_dict['ak8jetpt300']+"&&ak8pfjets_deep_rawdisc_hbb[0]>0.9"
    
    region_cut_dict["PSR1jet_met_200_pt_400"] = PSR_cut+"&&"+cut_dict['ak8jetpt400']
    region_cut_dict["PSR1jet_met_200_pt_400_hbb"] = PSR_cut+"&&"+cut_dict['ak8jetpt400']+"&&ak8pfjets_deep_rawdisc_hbb[0]>0.5"
    region_cut_dict["PSR1jet_met_200_pt_400_hbb0p9"] = PSR_cut+"&&"+cut_dict['ak8jetpt400']+"&&ak8pfjets_deep_rawdisc_hbb[0]>0.9"
    
    region_cut_dict["PSR1jet_met_200_pt_500"] = PSR_cut+"&&"+cut_dict['ak8jetpt500']
    region_cut_dict["PSR1jet_met_200_pt_500_hbb"] = PSR_cut+"&&"+cut_dict['ak8jetpt500']+"&&ak8pfjets_deep_rawdisc_hbb[0]>0.5"
    region_cut_dict["PSR1jet_met_200_pt_500_hbb0p9"] = PSR_cut+"&&"+cut_dict['ak8jetpt500']+"&&ak8pfjets_deep_rawdisc_hbb[0]>0.9"
    
    region_cut_dict["PSR1jet_met_200_pt_600"] = PSR_cut+"&&"+cut_dict['ak8jetpt600']
    region_cut_dict["PSR1jet_met_200_pt_600_hbb"] = PSR_cut+"&&"+cut_dict['ak8jetpt600']+"&&ak8pfjets_deep_rawdisc_hbb[0]>0.5"
    region_cut_dict["PSR1jet_met_200_pt_600_hbb0p9"] = PSR_cut+"&&"+cut_dict['ak8jetpt600']+"&&ak8pfjets_deep_rawdisc_hbb[0]>0.9"
 

    #Proposed Non-Orthogonal 1 fat jet region
    PSR_list = ["passTrigger", "passOneLep", "passLepSel", "PassTrackVeto",\
    "PassTauVeto", "one_ak8jet", "event_met_pt_high"]#"m_bb",#, "mt"
    PSR_condition_list = [cut_dict[item] for item in PSR_list]
    PSR_cut = combine_cuts(PSR_condition_list)
    
    region_cut_dict["PSR1jet_inclusive_met_200_pt_600"] = PSR_cut+"&&"+cut_dict['ak8jetpt600']
    region_cut_dict["PSR1jet_inclusive_met_200_pt_600_hbb"] = PSR_cut+"&&"+cut_dict['ak8jetpt600']+"&&ak8pfjets_deep_rawdisc_hbb[0]>0.5"
    region_cut_dict["PSR1jet_inclusive_met_200_pt_600_hbb0p9"] = PSR_cut+"&&"+cut_dict['ak8jetpt600']+"&&ak8pfjets_deep_rawdisc_hbb[0]>0.9"
    
    region_cut_dict["PSR1jet_inclusive_met_200_pt_500"] = PSR_cut+"&&"+cut_dict['ak8jetpt500']
    region_cut_dict["PSR1jet_inclusive_met_200_pt_500_hbb"] = PSR_cut+"&&"+cut_dict['ak8jetpt500']+"&&ak8pfjets_deep_rawdisc_hbb[0]>0.5"
    region_cut_dict["PSR1jet_inclusive_met_200_pt_500_hbb0p9"] = PSR_cut+"&&"+cut_dict['ak8jetpt500']+"&&ak8pfjets_deep_rawdisc_hbb[0]>0.9"
    
    region_cut_dict["PSR1jet_inclusive_met_200_pt_400"] = PSR_cut+"&&"+cut_dict['ak8jetpt400']
    region_cut_dict["PSR1jet_inclusive_met_200_pt_400_hbb"] = PSR_cut+"&&"+cut_dict['ak8jetpt400']+"&&ak8pfjets_deep_rawdisc_hbb[0]>0.5"
    region_cut_dict["PSR1jet_inclusive_met_200_pt_400_hbb0p9"] = PSR_cut+"&&"+cut_dict['ak8jetpt400']+"&&ak8pfjets_deep_rawdisc_hbb[0]>0.9"
    
    #Proposed 2 jet recoverable region
    PSR_list = ["passTrigger", "passOneLep", "passLepSel", "PassTrackVeto",\
    "PassTauVeto", "2jet_recover", "goodbtags", "mt", "m_bb"]#, "mctbb", "event_met_pt_high"
    PSR_condition_list = [cut_dict[item] for item in PSR_list]
    PSR_cut = combine_cuts(PSR_condition_list)
    region_cut_dict["PSR1jet_recover_2jet"] = PSR_cut
    region_cut_dict["PSR1jet_recover_2jet_met_200_mct170"] = PSR_cut + "&& new_mct > 170"+"&& new_met>200"
    region_cut_dict["PSR1jet_recover_2jet_met_200_mct225"] = PSR_cut + "&& new_mct > 225"+"&& new_met>200"
    region_cut_dict["PSR1jet_recover_2jet_met_250_mct170"] = PSR_cut + "&& new_mct > 170"+"&& new_met>250"
    region_cut_dict["PSR1jet_recover_2jet_met_250_mct220"] = PSR_cut + "&& new_mct > 225"+"&& new_met>250"
    
    #Proposed Binned 2jet region
    BSR2_list = ["passTrigger", "passOneLep", "passLepSel", "PassTrackVeto",\
    "PassTauVeto", "ngoodjets", "goodbtags", "m_bb", "mctbb", "mt"]
    BSR2_condition_list = [cut_dict[item] for item in BSR2_list]
    BSR2_cut = combine_cuts(BSR2_condition_list)
    
    region_cut_dict["BSR2_MET_250"] = BSR2_cut+"&& new_met >= 250"
    region_cut_dict["BSR2_MET_300"] = BSR2_cut+"&& new_met >= 300"
    region_cut_dict["BSR2_MET_350"] = BSR2_cut+"&& new_met >= 350"
    region_cut_dict["BSR2_MET_400"] = BSR2_cut+"&& new_met >= 400"
    region_cut_dict["BSR2_MET_450"] = BSR2_cut+"&& new_met >= 450"
    region_cut_dict["BSR2_MET_500"] = BSR2_cut+"&& new_met >= 500"
    region_cut_dict["BSR2_MET_100_200"] = BSR2_cut+"&& new_met >= 100 && new_met < 200"
    region_cut_dict["BSR2_MET_200_300"] = BSR2_cut+"&& new_met >= 200 && new_met < 300"
    region_cut_dict["BSR2_MET_300_400"] = BSR2_cut+"&& new_met >= 300 && new_met < 400"
    region_cut_dict["BSR2_MET_400_500"] = BSR2_cut+"&& new_met >= 400 && new_met < 500"
    
    region_cut_dict["BSR2_MET_100_300"] = BSR2_cut+"&& new_met >= 100 && new_met < 300"
    region_cut_dict["BSR2_MET_200_400"] = BSR2_cut+"&& new_met >= 200 && new_met < 400"
    region_cut_dict["BSR2_MET_300_500"] = BSR2_cut+"&& new_met >= 300 && new_met < 500"
    
    region_cut_dict["BSR2_MET_100_150"] = BSR2_cut+"&& new_met >= 100 && new_met < 150"
    region_cut_dict["BSR2_MET_150_200"] = BSR2_cut+"&& new_met >= 150 && new_met < 200"
    region_cut_dict["BSR2_MET_200_250"] = BSR2_cut+"&& new_met >= 200 && new_met < 250"
    region_cut_dict["BSR2_MET_250_300"] = BSR2_cut+"&& new_met >= 250 && new_met < 300"
    region_cut_dict["BSR2_MET_300_350"] = BSR2_cut+"&& new_met >= 300 && new_met < 350"
    region_cut_dict["BSR2_MET_350_400"] = BSR2_cut+"&& new_met >= 350 && new_met < 400"
    region_cut_dict["BSR2_MET_400_450"] = BSR2_cut+"&& new_met >= 400 && new_met < 450"
    region_cut_dict["BSR2_MET_450_500"] = BSR2_cut+"&& new_met >= 450 && new_met < 500"
        
    #Proposed Binned 3jet region
    BSR3_list = ["passTrigger", "passOneLep", "passLepSel", "PassTrackVeto",\
    "PassTauVeto", "3goodjets", "goodbtags", "m_bb_csv_rank","mctbb_csv_rank225", "mt"]
    
    BSR3_condition_list = [cut_dict[item] for item in BSR3_list]
    BSR3_cut = combine_cuts(BSR3_condition_list)
    
    region_cut_dict["BSR3_MET_250"] = BSR3_cut+"&& new_met >= 250"
    region_cut_dict["BSR3_MET_300"] = BSR3_cut+"&& new_met >= 300"
    region_cut_dict["BSR3_MET_350"] = BSR3_cut+"&& new_met >= 350"
    region_cut_dict["BSR3_MET_400"] = BSR3_cut+"&& new_met >= 400"
    region_cut_dict["BSR3_MET_450"] = BSR3_cut+"&& new_met >= 450"
    region_cut_dict["BSR3_MET_500"] = BSR3_cut+"&& new_met >= 500"
    region_cut_dict["BSR3_MET_100_200"] = BSR3_cut+"&& new_met >= 100 && new_met < 200"
    region_cut_dict["BSR3_MET_200_300"] = BSR3_cut+"&& new_met >= 200 && new_met < 300"
    region_cut_dict["BSR3_MET_300_400"] = BSR3_cut+"&& new_met >= 300 && new_met < 400"
    region_cut_dict["BSR3_MET_400_500"] = BSR3_cut+"&& new_met >= 400 && new_met < 500"
    
    region_cut_dict["BSR3_MET_100_300"] = BSR3_cut+"&& new_met >= 100 && new_met < 300"
    region_cut_dict["BSR3_MET_200_400"] = BSR3_cut+"&& new_met >= 200 && new_met < 400"
    region_cut_dict["BSR3_MET_300_500"] = BSR3_cut+"&& new_met >= 300 && new_met < 500"
    
    region_cut_dict["BSR3_MET_100_150"] = BSR3_cut+"&& new_met >= 100 && new_met < 150"
    region_cut_dict["BSR3_MET_150_200"] = BSR3_cut+"&& new_met >= 150 && new_met < 200"
    region_cut_dict["BSR3_MET_200_250"] = BSR3_cut+"&& new_met >= 200 && new_met < 250"
    region_cut_dict["BSR3_MET_250_300"] = BSR3_cut+"&& new_met >= 250 && new_met < 300"
    region_cut_dict["BSR3_MET_300_350"] = BSR3_cut+"&& new_met >= 300 && new_met < 350"
    region_cut_dict["BSR3_MET_350_400"] = BSR3_cut+"&& new_met >= 350 && new_met < 400"
    region_cut_dict["BSR3_MET_400_450"] = BSR3_cut+"&& new_met >= 400 && new_met < 450"
    region_cut_dict["BSR3_MET_450_500"] = BSR3_cut+"&& new_met >= 450 && new_met < 500"
    
    #Proposed Binned 3jet region with 2var
    BSR3_2vars_list = ["passTrigger", "passOneLep", "passLepSel", "PassTrackVeto",\
    "PassTauVeto", "3goodjets", "goodbtags", "m_bb_csv_rank","mctbb_csv_rank225", "mt","2vars"]
    
    BSR3_2vars_condition_list = [cut_dict[item] for item in BSR3_2vars_list]
    BSR3_2vars_cut = combine_cuts(BSR3_2vars_condition_list)
    
    region_cut_dict["BSR3_2vars_MET_250"] = BSR3_2vars_cut+"&& new_met >= 250"
    region_cut_dict["BSR3_2vars_MET_300"] = BSR3_2vars_cut+"&& new_met >= 300"
    region_cut_dict["BSR3_2vars_MET_350"] = BSR3_2vars_cut+"&& new_met >= 350"
    region_cut_dict["BSR3_2vars_MET_400"] = BSR3_2vars_cut+"&& new_met >= 400"
    region_cut_dict["BSR3_2vars_MET_450"] = BSR3_2vars_cut+"&& new_met >= 450"
    region_cut_dict["BSR3_2vars_MET_500"] = BSR3_2vars_cut+"&& new_met >= 500"
    region_cut_dict["BSR3_2vars_MET_100_200"] = BSR3_2vars_cut+"&& new_met >= 100 && new_met < 200"
    region_cut_dict["BSR3_2vars_MET_200_300"] = BSR3_2vars_cut+"&& new_met >= 200 && new_met < 300"
    region_cut_dict["BSR3_2vars_MET_300_400"] = BSR3_2vars_cut+"&& new_met >= 300 && new_met < 400"
    region_cut_dict["BSR3_2vars_MET_400_500"] = BSR3_2vars_cut+"&& new_met >= 400 && new_met < 500"
    
    region_cut_dict["BSR3_2vars_MET_100_300"] = BSR3_2vars_cut+"&& new_met >= 100 && new_met < 300"
    region_cut_dict["BSR3_2vars_MET_200_400"] = BSR3_2vars_cut+"&& new_met >= 200 && new_met < 400"
    region_cut_dict["BSR3_2vars_MET_300_500"] = BSR3_2vars_cut+"&& new_met >= 300 && new_met < 500"
    
    region_cut_dict["BSR3_2vars_MET_100_150"] = BSR3_2vars_cut+"&& new_met >= 100 && new_met < 150"
    region_cut_dict["BSR3_2vars_MET_150_200"] = BSR3_2vars_cut+"&& new_met >= 150 && new_met < 200"
    region_cut_dict["BSR3_2vars_MET_200_250"] = BSR3_2vars_cut+"&& new_met >= 200 && new_met < 250"
    region_cut_dict["BSR3_2vars_MET_250_300"] = BSR3_2vars_cut+"&& new_met >= 250 && new_met < 300"
    region_cut_dict["BSR3_2vars_MET_300_350"] = BSR3_2vars_cut+"&& new_met >= 300 && new_met < 350"
    region_cut_dict["BSR3_2vars_MET_350_400"] = BSR3_2vars_cut+"&& new_met >= 350 && new_met < 400"
    region_cut_dict["BSR3_2vars_MET_400_450"] = BSR3_2vars_cut+"&& new_met >= 400 && new_met < 450"
    region_cut_dict["BSR3_2vars_MET_450_500"] = BSR3_2vars_cut+"&& new_met >= 450 && new_met < 500"
    #One 30GeV jet with multiple 20 GeV jets.#Need to change the b-tagging requirement.
    
    
    #Proposed SR 1 fat jet
    PSR_list = ["passTrigger", "passOneLep", "passLepSel", "PassTrackVeto",\
    "PassTauVeto", "one_ak4jet","one_ak8jet", "event_met_pt_high", "mt"]#"m_bb",
    PSR_condition_list = [cut_dict[item] for item in PSR_list]
    PSR_cut = combine_cuts(PSR_condition_list)

    region_cut_dict["PSR1jet_new_met_200_pt_300"] = PSR_cut+"&&"+cut_dict['ak8jetpt300']
    region_cut_dict["PSR1jet_new_met_200_pt_300_hbb"] = PSR_cut+"&&"+cut_dict['ak8jetpt300']+"&&ak8pfBoostedDoubleSecondaryVertexAK8BJetTags[0]>0.5"
    region_cut_dict["PSR1jet_new_met_200_pt_300_hbb0p7"] = PSR_cut+"&&"+cut_dict['ak8jetpt300']+"&&ak8pfBoostedDoubleSecondaryVertexAK8BJetTags[0]>0.7"
    region_cut_dict["PSR1jet_new_met_200_pt_300_hbb0p9"] = PSR_cut+"&&"+cut_dict['ak8jetpt300']+"&&ak8pfBoostedDoubleSecondaryVertexAK8BJetTags[0]>0.9"
    
    region_cut_dict["PSR1jet_new_met_200_pt_400"] = PSR_cut+"&&"+cut_dict['ak8jetpt400']
    region_cut_dict["PSR1jet_new_met_200_pt_400_hbb"] = PSR_cut+"&&"+cut_dict['ak8jetpt400']+"&&ak8pfBoostedDoubleSecondaryVertexAK8BJetTags[0]>0.5"
    region_cut_dict["PSR1jet_new_met_200_pt_400_hbb0p7"] = PSR_cut+"&&"+cut_dict['ak8jetpt400']+"&&ak8pfBoostedDoubleSecondaryVertexAK8BJetTags[0]>0.7"
    region_cut_dict["PSR1jet_new_met_200_pt_400_hbb0p9"] = PSR_cut+"&&"+cut_dict['ak8jetpt400']+"&&ak8pfBoostedDoubleSecondaryVertexAK8BJetTags[0]>0.9"
    
    region_cut_dict["PSR1jet_new_met_200_pt_500"] = PSR_cut+"&&"+cut_dict['ak8jetpt500']
    region_cut_dict["PSR1jet_new_met_200_pt_500_hbb"] = PSR_cut+"&&"+cut_dict['ak8jetpt500']+"&&ak8pfBoostedDoubleSecondaryVertexAK8BJetTags[0]>0.5"
    region_cut_dict["PSR1jet_new_met_200_pt_500_hbb0p9"] = PSR_cut+"&&"+cut_dict['ak8jetpt500']+"&&ak8pfBoostedDoubleSecondaryVertexAK8BJetTags[0]>0.9"
    
    region_cut_dict["PSR1jet_new_met_200_pt_600"] = PSR_cut+"&&"+cut_dict['ak8jetpt600']
    region_cut_dict["PSR1jet_new_met_200_pt_600_hbb"] = PSR_cut+"&&"+cut_dict['ak8jetpt600']+"&&ak8pfBoostedDoubleSecondaryVertexAK8BJetTags[0]>0.5"
    region_cut_dict["PSR1jet_new_met_200_pt_600_hbb0p9"] = PSR_cut+"&&"+cut_dict['ak8jetpt600']+"&&ak8pfBoostedDoubleSecondaryVertexAK8BJetTags[0]>0.9"
 

    #Proposed Non-Orthogonal 1 fat jet region
    PSR_list = ["passTrigger", "passOneLep", "passLepSel", "PassTrackVeto",\
    "PassTauVeto", "one_ak8jet", "event_met_pt_high"]#"m_bb",#, "mt"
    PSR_condition_list = [cut_dict[item] for item in PSR_list]
    PSR_cut = combine_cuts(PSR_condition_list)
    
    region_cut_dict["PSR1jet_new_inclusive_met_200_pt_600"] = PSR_cut+"&&"+cut_dict['ak8jetpt600']
    region_cut_dict["PSR1jet_new_inclusive_met_200_pt_600_hbb"] = PSR_cut+"&&"+cut_dict['ak8jetpt600']+"&&ak8pfBoostedDoubleSecondaryVertexAK8BJetTags[0]>0.5"
    region_cut_dict["PSR1jet_new_inclusive_met_200_pt_600_hbb0p9"] = PSR_cut+"&&"+cut_dict['ak8jetpt600']+"&&ak8pfBoostedDoubleSecondaryVertexAK8BJetTags[0]>0.9"
    
    region_cut_dict["PSR1jet_new_inclusive_met_200_pt_500"] = PSR_cut+"&&"+cut_dict['ak8jetpt500']
    region_cut_dict["PSR1jet_new_inclusive_met_200_pt_500_hbb"] = PSR_cut+"&&"+cut_dict['ak8jetpt500']+"&&ak8pfBoostedDoubleSecondaryVertexAK8BJetTags[0]>0.5"
    region_cut_dict["PSR1jet_new_inclusive_met_200_pt_500_hbb0p9"] = PSR_cut+"&&"+cut_dict['ak8jetpt500']+"&&ak8pfBoostedDoubleSecondaryVertexAK8BJetTags[0]>0.9"
    
    region_cut_dict["PSR1jet_new_inclusive_met_200_pt_400"] = PSR_cut+"&&"+cut_dict['ak8jetpt400']
    region_cut_dict["PSR1jet_new_inclusive_met_200_pt_400_hbb"] = PSR_cut+"&&"+cut_dict['ak8jetpt400']+"&&ak8pfBoostedDoubleSecondaryVertexAK8BJetTags[0]>0.5"
    region_cut_dict["PSR1jet_new_inclusive_met_200_pt_400_hbb0p9"] = PSR_cut+"&&"+cut_dict['ak8jetpt400']+"&&ak8pfBoostedDoubleSecondaryVertexAK8BJetTags[0]>0.9"
    
    #Proposed 2 jet recoverable region
    PSR_list = ["passTrigger", "passOneLep", "passLepSel", "PassTrackVeto",\
    "PassTauVeto", "2jet_recover_new", "goodbtags", "mt", "m_bb"]#, "mctbb", "event_met_pt_high"
    PSR_condition_list = [cut_dict[item] for item in PSR_list]
    PSR_cut = combine_cuts(PSR_condition_list)
    region_cut_dict["PSR1jet_new_recover_2jet"] = PSR_cut
    region_cut_dict["PSR1jet_new_recover_2jet_met_200_mct170"] = PSR_cut + "&& new_mct > 170"+"&& new_met>200"
    region_cut_dict["PSR1jet_new_recover_2jet_met_200_mct225"] = PSR_cut + "&& new_mct > 225"+"&& new_met>200"
    region_cut_dict["PSR1jet_new_recover_2jet_met_250_mct170"] = PSR_cut + "&& new_mct > 170"+"&& new_met>250"
    region_cut_dict["PSR1jet_new_recover_2jet_met_250_mct220"] = PSR_cut + "&& new_mct > 225"+"&& new_met>250"
    
    return cut_dict, current_cut_list, region_cut_dict

def get_weight_formula():
    '''Give the weight formula for different types of events.'''
    weight_form = {}
    weight_form["normal_sig"] = ""
    weight_form["normal_bkg"] = ""
    weight_form["xgb_sig"] = "weight"
    weight_form["xgb_bkg"] = "weight"

def save_for_later():
    #Proposed SR with 4 jets
    PSR_list = ["passTrigger", "passOneLep", "passLepSel", "PassTrackVeto",\
    "PassTauVeto", "4moregoodjets", "goodbtags", "m_bb", "event_met_pt_high", "mt"]
    PSR_condition_list = [cut_dict[item] for item in PSR_list]
    region_cut_dict["PSR4jet_met_200_mct200"] = PSR_cut + "&& new_mct > 200"
    region_cut_dict["PSR4jet_met_200_mct225"] = PSR_cut + "&& new_mct > 225"
    region_cut_dict["PSR4jet_met_200_mct250"] = PSR_cut + "&& new_mct > 250"
    region_cut_dict["PSR4jet_met_200_mct275"] = PSR_cut + "&& new_mct > 275"
    region_cut_dict["PSR4jet_met_200_mct300"] = PSR_cut + "&& new_mct > 300"    
    PSR_cut = combine_cuts(PSR_condition_list)
    
    #Proposed SR with 4 jets
    PSR_list = ["passTrigger", "passOneLep", "passLepSel", "PassTrackVeto",\
    "PassTauVeto", "4moregoodjets", "goodbtags", "m_bb", "event_met_pt", "mt"]
    PSR_condition_list = [cut_dict[item] for item in PSR_list]
    region_cut_dict["PSR4jet_met_125_mct200"] = PSR_cut + "&& new_mct > 200"
    region_cut_dict["PSR4jet_met_125_mct225"] = PSR_cut + "&& new_mct > 225"
    region_cut_dict["PSR4jet_met_125_mct250"] = PSR_cut + "&& new_mct > 250"
    region_cut_dict["PSR4jet_met_125_mct275"] = PSR_cut + "&& new_mct > 275"
    region_cut_dict["PSR4jet_met_125_mct300"] = PSR_cut + "&& new_mct > 300"    
    PSR_cut = combine_cuts(PSR_condition_list)
    
    xgb_list = ["passTrigger", "passOneLep", "passLepSel", "PassTrackVeto", "PassTauVeto", "goodbtags"]
    #preselection_str = "lep1_tight == 1 && lep2_tight == 0 && lep2_veto == 0 && PassTrackVeto && PassTauVeto && nbtag_loose ==2 && nbtag_med >=1 && new_met>100&& new_mt>150"
    xgb_condition_list = [cut_dict[item] for item in xgb_list]
    xgb_cut = combine_cuts(xgb_condition_list) + "&& new_met>100 && new_mt>150"
    
    region_cut_dict["xgb0p6"] = xgb_cut + "&& xgb_proba > 0.6"
    region_cut_dict["xgb0p7"] = xgb_cut + "&& xgb_proba > 0.7"
    region_cut_dict["xgb0p8"] = xgb_cut + "&& xgb_proba > 0.8"+"&& xgb_proba <= 0.9"
    region_cut_dict["xgb0p9"] = xgb_cut + "&& xgb_proba > 0.9"+"&& xgb_proba <= 0.91"
    region_cut_dict["xgb0p91"] = xgb_cut + "&& xgb_proba > 0.91"+"&& xgb_proba <= 0.92"
    region_cut_dict["xgb0p92"] = xgb_cut + "&& xgb_proba > 0.92"+"&& xgb_proba <= 0.93"
    region_cut_dict["xgb0p93"] = xgb_cut + "&& xgb_proba > 0.93"+"&& xgb_proba <= 0.94"
    region_cut_dict["xgb0p94"] = xgb_cut + "&& xgb_proba > 0.94"+"&& xgb_proba <= 0.95"
    region_cut_dict["xgb0p95"] = xgb_cut + "&& xgb_proba > 0.95"+"&& xgb_proba <= 0.96"
    region_cut_dict["xgb0p96"] = xgb_cut + "&& xgb_proba > 0.96"+"&& xgb_proba <= 0.97"
    region_cut_dict["xgb0p97"] = xgb_cut + "&& xgb_proba > 0.97"+"&& xgb_proba <= 0.972"
    region_cut_dict["xgb0p972"] = xgb_cut + "&& xgb_proba > 0.972"+"&& xgb_proba <= 0.974"
    region_cut_dict["xgb0p974"] = xgb_cut + "&& xgb_proba > 0.974"+"&& xgb_proba <= 0.976"
    region_cut_dict["xgb0p976"] = xgb_cut + "&& xgb_proba > 0.976"+"&& xgb_proba <= 0.978"
    region_cut_dict["xgb0p978"] = xgb_cut + "&& xgb_proba > 0.978"+"&& xgb_proba <= 0.980"
    region_cut_dict["xgb0p98"] = xgb_cut + "&& xgb_proba > 0.980"+"&& xgb_proba <= 0.982"
    region_cut_dict["xgb0p982"] = xgb_cut + "&& xgb_proba > 0.982"+"&& xgb_proba <= 0.984"
    region_cut_dict["xgb0p984"] = xgb_cut + "&& xgb_proba > 0.984"+"&& xgb_proba <= 0.986"
    region_cut_dict["xgb0p986"] = xgb_cut + "&& xgb_proba > 0.986"+"&& xgb_proba <= 0.988"
    region_cut_dict["xgb0p988"] = xgb_cut + "&& xgb_proba > 0.988"+"&& xgb_proba <= 1.00"
#BTAGWP, compared to ak4pfjets_CSV[i_jet]
BTAGWP = 0.5426; #Loose btag working point
mBTAGWP = 0.8484; #Medium btag working point
#Note that the b-jet must satisify the following requirements:
i_jet = 0;
jet_requirement =  "ak4pfjets_p4().at(%.0f).Pt() > 30 && fabs(ak4pfjets_p4().at(%.0f).Eta()) < 2.4 && ak4pfjets_loose_pfid().at(%.0f)" %(i_jet, i_jet, i_jet)
#Dummy value set-up
dummy_value = -999

