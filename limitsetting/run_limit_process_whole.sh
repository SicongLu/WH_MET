#!/bin/bash
. ~/.bashrc_real
#new_cate="PSR3jet_met_200_mct225"
#new_cate="PSR3jet_met_200_mct275"

#new_cate="PSR3jet_met_225_mct225"
new_cate="PSR3jet_met_225_mct225_2vars"
#new_cate="original"
#new_cate="PSR3jet_met_200_mct225_xgb_0p2"
#new_cate="PSR3jet_met_200_mct200_xgb_0p4"
#new_cate="PSR3jet_met_200_mct200_xgb_0p2"
date_str="0426"

rm -r ../../Run_Directory/CMSSW_8_1_0/src/WH_MET_limitsetting/cards_${new_cate}_${date_str}/
rm -r ../../Run_Directory/CMSSW_8_1_0/src/WH_MET_limitsetting/scan_${new_cate}_${date_str}/
python qad_fast_print_cards.py $new_cate $date_str
. doLimits.sh $new_cate $date_str
root -b -q "makeLimitHist_TChiWH.C(\"$new_cate\",\"$date_str\")"