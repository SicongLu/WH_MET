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
    
    
def get_cut_dict():
    '''The selection criteria is currently following:
    https://github.com/mialiu149/AnalysisLoopers2015/blob/master/sharedCode/WHSelection.cc
    '''
    lep1_tight, lep2_tight, lep1_veto, lep2_veto, ntight_lep_str, nveto_lep_str = get_lep_selection_str()
    cut_dict = {}
    cut_dict['passTrigger'] = "(HLT_SingleMu || HLT_SingleEl)"
    cut_dict['passOneLep'] = lep1_tight 
    cut_dict['passLepSel'] = "!("+lep2_veto+"||"+lep2_tight+")"
    cut_dict['passTwoLep'] = lep1_tight+"&&"+lep2_tight 
    
    cut_dict['PassTrackVeto'] = "PassTrackVeto == 1"
    cut_dict['PassTauVeto'] = "PassTauVeto == 1"
    cut_dict['inverted_PassTrackVeto'] = "PassTrackVeto == 0"
    cut_dict['inverted_PassTauVeto'] = "PassTauVeto == 0"
    
    cut_dict['ngoodjets'] = "ngoodjets == 2"
    cut_dict['3goodjets'] = "ngoodjets == 3"
    cut_dict['2ormoregoodjets'] = "ngoodjets >= 2"
    
    cut_dict['goodbtags'] = "nbtag_loose == 2 && nbtag_med >= 1"
    cut_dict['zerobtags'] = "nbtag_loose == 0" 
    
    #cut_dict['m_bb'] =  "(mbb > 90 && mbb < 150)"
    cut_dict['m_bb'] =  "(new_mbb > 90 && new_mbb < 150)"
    #cut_dict['m_bb'] =  "(new_mbb > 90 && new_mbb < 150)"
    #cut_dict['inverted_m_bb'] =  "!(mbb > 90 && mbb < 150)"
    cut_dict['inverted_m_bb'] =  "!(new_mbb > 90 && new_mbb < 150)"
    
    cut_dict['event_met_pt'] =  "(pfmet > 125)"
    cut_dict['event_met_pt_med'] =  "(pfmet > 125 && pfmet <=200)"
    cut_dict['event_met_pt_high'] =  "(pfmet > 200)"
    
    #cut_dict['mt'] =  "mt_met_lep > 150"
    cut_dict['mt'] =  "new_mt > 150"
    
    cut_dict['mctbb'] =  "new_mct > 170"
    #cut_dict['mctbb'] =  "mct > 170"
    
    #Current Ordering of the cut-requirement: (Preselection)
    current_cut_list = ["passTrigger", "passOneLep", "passLepSel", "PassTrackVeto",\
     "PassTauVeto", "ngoodjets", "goodbtags", "m_bb", "mctbb", "event_met_pt", "mt"]
    
    region_cut_dict = {}
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
    CR2l_list_1 = ["passTrigger", "passOneLep", "passLepSel", "inverted_PassTrackVeto",\
    "inverted_PassTauVeto", "ngoodjets", "goodbtags", "event_met_pt_high", "mt"]
    CR2l_condition_list_1 = [cut_dict[item] for item in CR2l_list_1]
    CR2l_cut_1 = combine_cuts(CR2l_condition_list_1)
    
    CR2l_list_2 = ["passTrigger", "passTwoLep", "PassTrackVeto",\
    "PassTauVeto", "ngoodjets", "goodbtags", "event_met_pt_high", "mt"]
    CR2l_condition_list_2 = [cut_dict[item] for item in CR2l_list_2]
    CR2l_cut_2 = combine_cuts(CR2l_condition_list_2)
    
    CR2l_cut = "("+CR2l_cut_1+")||("+CR2l_cut_2+")"
    #region_cut_dict["CR2l"] = CR2l_cut
    
    #CR0b
    CR0b1_list = ["passTrigger", "passOneLep", "passLepSel", "PassTrackVeto",\
    "PassTauVeto", "ngoodjets", "zerobtags", "m_bb", "mctbb", "event_met_pt_med", "mt"]
    CR0b1_condition_list = [cut_dict[item] for item in CR0b1_list]
    CR0b1_cut = combine_cuts(CR0b1_condition_list)   #str_condition = "("+str_condition+")*"+scale_str
    
    CR0b2_list = ["passTrigger", "passOneLep", "passLepSel", "PassTrackVeto",\
    "PassTauVeto", "ngoodjets", "zerobtags", "m_bb", "mctbb", "event_met_pt_high", "mt"]
    CR0b2_condition_list = [cut_dict[item] for item in CR0b2_list]
    CR0b2_cut = combine_cuts(CR0b2_condition_list)
    
    region_cut_dict["CR0b1"] = CR0b1_cut
    region_cut_dict["CR0b2"] = CR0b2_cut
    
    #CRMbb
    CRMbb1_list = ["passTrigger", "passOneLep", "passLepSel", "PassTrackVeto",\
    "PassTauVeto", "ngoodjets", "goodbtags", "inverted_m_bb", "mctbb", "event_met_pt_med", "mt"]
    CRMbb1_condition_list = [cut_dict[item] for item in CRMbb1_list]
    CRMbb1_cut = combine_cuts(CRMbb1_condition_list)   #str_condition = "("+str_condition+")*"+scale_str
    
    CRMbb2_list = ["passTrigger", "passOneLep", "passLepSel", "PassTrackVeto",\
    "PassTauVeto", "ngoodjets", "goodbtags", "inverted_m_bb", "mctbb", "event_met_pt_high", "mt"]
    CRMbb2_condition_list = [cut_dict[item] for item in CRMbb2_list]
    CRMbb2_cut = combine_cuts(CRMbb2_condition_list)
    
    region_cut_dict["CRMbb1"] = CRMbb1_cut
    region_cut_dict["CRMbb2"] = CRMbb2_cut
    
    #Proposed SR 
    PSR_list = ["passTrigger", "passOneLep", "passLepSel", "PassTrackVeto",\
    "PassTauVeto", "3goodjets", "goodbtags", "m_bb", "event_met_pt_high", "mt"]
    PSR_condition_list = [cut_dict[item] for item in PSR_list]
    PSR_cut = combine_cuts(PSR_condition_list)
    
#    region_cut_dict["3jet_met_200_mct200"] = PSR_cut + "&& mct > 200"
    region_cut_dict["3jet_met_200_mct225"] = PSR_cut + "&& mct > 225"
    region_cut_dict["3jet_met_200_mct250"] = PSR_cut + "&& mct > 250"
#    region_cut_dict["3jet_met_200_mct275"] = PSR_cut + "&& mct > 275"
#    region_cut_dict["3jet_met_200_mct300"] = PSR_cut + "&& mct > 300"
        
    
    PSR_list = ["passTrigger", "passOneLep", "passLepSel", "PassTrackVeto",\
    "PassTauVeto", "3goodjets", "goodbtags", "m_bb", "event_met_pt", "mt"]
    PSR_condition_list = [cut_dict[item] for item in PSR_list]
    PSR_cut = combine_cuts(PSR_condition_list)

#    region_cut_dict["3jet_mct200"] = PSR_cut + "&& mct > 200"
#    region_cut_dict["3jet_mct225"] = PSR_cut + "&& mct > 225"
#    region_cut_dict["3jet_mct250"] = PSR_cut + "&& mct > 250"
    region_cut_dict["3jet_mct275"] = PSR_cut + "&& mct > 275"
    region_cut_dict["3jet_mct300"] = PSR_cut + "&& mct > 300"
#    region_cut_dict["3jet_mct350"] = PSR_cut + "&& mct > 350"
    
    xgb_list = ["passTrigger", "passOneLep", "passLepSel", "PassTrackVeto",\
    "PassTauVeto"]
    xgb_condition_list = [cut_dict[item] for item in xgb_list]
    xgb_cut = combine_cuts(xgb_condition_list)
    
#    region_cut_dict["xgb0p6"] = PSR_cut + "&& xgb_proba > 0.6"
#    region_cut_dict["xgb0p7"] = PSR_cut + "&& xgb_proba > 0.7"
#    region_cut_dict["xgb0p8"] = PSR_cut + "&& xgb_proba > 0.8"
#    region_cut_dict["xgb0p9"] = PSR_cut + "&& xgb_proba > 0.9"
#    region_cut_dict["xgb0p95"] = PSR_cut + "&& xgb_proba > 0.94"
#    region_cut_dict["xgb0p97"] = PSR_cut + "&& xgb_proba > 0.97"
    
    return cut_dict, current_cut_list, region_cut_dict

#BTAGWP, compared to ak4pfjets_CSV[i_jet]
BTAGWP = 0.5426; #Loose btag working point
mBTAGWP = 0.8484; #Medium btag working point
#Note that the b-jet must satisify the following requirements:
i_jet = 0;
jet_requirement =  "ak4pfjets_p4().at(%.0f).Pt() > 30 && fabs(ak4pfjets_p4().at(%.0f).Eta()) < 2.4 && ak4pfjets_loose_pfid().at(%.0f)" %(i_jet, i_jet, i_jet)
#Dummy value set-up
dummy_value = -999

