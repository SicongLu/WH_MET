#Link the root file to this folder.
sig_dir=/nfs-7/userdata/mliu/tupler_babies/merged/onelepbabymaker/whsignoskim_moriond_v1/
bkg_dir=/nfs-7/userdata/mliu/tupler_babies/merged/onelepbabymaker/moriond2017.v10/output/

ln -s ${sig_dir}TChiWH*.root .
ln -s ${bkg_dir}ttbar*.root .




