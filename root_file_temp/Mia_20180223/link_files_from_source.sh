#Note that this needs to be checked, (with Dr Liu)
#Link the root file to this folder.
sig_dir=/nfs-7/userdata/mliu/tupler_babies/merged/onelepbabymaker/whsignoskim_moriond/ #Note that v1 is inapproriate as some of these (probably except 700) are skimmed
bkg_dir=/nfs-7/userdata/mliu/tupler_babies/merged/onelepbabymaker/moriond2017.v10/output/
#Signal
ln -s ${sig_dir}TChiWH*.root .
ln -s /nfs-7/userdata/mliu/tupler_babies/merged/onelepbabymaker/whsignoskim_moriond_v1/TChiWH_700_1.root . #Note that v1 is inapproriate as some of these (probably except 700) are skimmed
#BKG Cate #1: ttbar background
#Including ttbarDiLept, and tW->ll;
ln -s ${bkg_dir}ttbar_diLept*.root .
#BKG Cate #2 (together with #3): W + light jets(all flavors except b) LF (light flavor)
#BKG Cate #3: W boson in association with b-jets, called W+HF (heavy flavor)
ln -s ${bkg_dir}WJetsToLNu_madgraph_pythia8_25ns*.root .
ln -s ${bkg_dir}WJetsToLNu_HT800To1200*.root .
ln -s ${bkg_dir}extmerge/WJetsToLNu*.root .

#BKG Cate #4: WZ production, W->lep+nu, Z->bb
ln -s ${bkg_dir}WZTo1LNu2Q_amcnlo*.root .

#BKG Cate #5: Single lepton top, including SingleLeptFromTbar and SingleLeptFromT
#It also includes single top quark t- and s-channel production.
ln -s ${bkg_dir}ttbar_singleLeptFrom*.root .
ln -s ${bkg_dir}t_tch_4f_powheg_pythia8_inclDecays_25ns*.root .
ln -s ${bkg_dir}tbar_tch_4f_powheg_pythia8_inclDecays_25ns*.root .
ln -s ${bkg_dir}t_sch*.root .
#???
ln -s ${bkg_dir}extmerge/t_tbarW_5f_powheg_pythia8_noHadDecays*.root .
ln -s ${bkg_dir}extmerge/t_tW_5f_powheg_pythia8_noHadDecays*.root .

#BKG Cate #6: Rare backgrounds: Z+jets, WW/WZ/ZZ, ttW/Z, WWW/WWZ/WZZ/ZZZ, WH->lvbb;
ln -s ${bkg_dir}ttZ*.root .
ln -s ${bkg_dir}tZq*.root .
ln -s ${bkg_dir}ttW*.root .
ln -s ${bkg_dir}WWTo*powheg*.root .
ln -s ${bkg_dir}WZTo1L3Nu_amcnlo_pythia8_25ns*.root .
ln -s ${bkg_dir}WZTo3LNu_powheg_pythia8_25ns.root .
ln -s /nfs-6/userdata/mliu/onelepbabies/V80_7p65_v2/WZTo2L2Q_amcnlo_pythia8_25ns.root .
ln -s ${bkg_dir}ZZTo*.root .
ln -s ${bkg_dir}WminusH*.root .
ln -s ${bkg_dir}WplusH*.root .
ln -s ${bkg_dir}*WWW*.root .
ln -s ${bkg_dir}*WWZ*.root .
ln -s ${bkg_dir}*WZG*.root .
ln -s ${bkg_dir}*WZZ*.root .
ln -s ${bkg_dir}*ZZZ*.root .
ln -s ${bkg_dir}*WWG*.root .



