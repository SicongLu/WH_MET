import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
import ROOT
import csv
import math
import re
import sys
sys.path.insert(0, '/home/users/siconglu/CMSTAS/software/dataMCplotMaker/')
import dataMCplotMaker
class pandas_analyzer:
    def __init__(self):
        '''Set-up the common variables.'''
        print('Setting up analysis')
        self.lumi = 35.9
        self.old_features = ["mbb", "ngoodjets", "MT2W", "Mlb_closestb", "mct", "mt_met_lep",\
        "pfmet", "topness", "topnessMod","mindphi_met_j1_j2","scale1fb","ptbb","ngoodjets"]
        self.features = self.old_features
        #self.features_name_dict = {"mbb":"M_{bb}"}
        self.csv_location = "../csv_file_temp/"
        self.root_location = "../root_file_temp/Sicong_20180228/"
        self.plot_location = "/home/users/siconglu/CMSTAS/software/niceplots/WH_pandas_analysis/"
        
    def set_active_branch(self):
        '''Make a list of the active branches.'''
        self.active_branch_list = [] 
        for feature in self.features:
            if not('.' in feature or '(' in feature):
                self.active_branch_list.append(feature)
            else:
                split_list = re.split('.()',feature)
                split_list = [item for item in split_list if not(item == "")]
                for split in split_list:
                    self.active_branch_list.append(feature)            
    
    def root_to_df(self,file_name):
        '''Read dataframe frome .root files'''
        print('reading from file % s'%file_name)
        f = ROOT.TFile.Open(file_name)
        t = f.Get('t')
        t.SetBranchStatus("*",0)
        for branch in self.active_branch_list:
            t.SetBranchStatus(branch,1)
        nEntries = t.GetEntries()
        data = []
        print('reading %i rows'%nEntries)
        for entry in range(nEntries):
            if entry % 1e4 == 0:
                print ('processing entry %i' % entry)
            row = []
            t.GetEntry(entry)
            for feature in self.features:
                branch = getattr(t,feature)
                if '.vector<' in str(type(branch)):
                    vec = getattr(t,feature)
                    for value in vec[:4]:#Only get the first 4 indices
                        row.append(value)
                    for _ in range(4-len([value for value in vec[:4]])):
                        row.append(-999)
                else:
                    value = getattr(t,feature)
                    row.append(value)
            data.append(row)
        return pd.DataFrame(data, columns = self.features)
    def apply_mask(self, cut_str):
        '''Apply the mask to the temporary dataframe'''
        cut_str.replace("&&"," and ") #Make sure that cut_str is python-styled.
        cut_str.replace("||"," or ")
        self.tmp_df = self.tmp_df.query(cut_str)
        
    def read_df_from_root(self,file_name):
        '''Read data from root'''
        if not(".root" in file_name):
            file_name+=".root"
        self.tmp_df = self.root_to_df(self.root_location+file_name)
        self.tmp_df_name = file_name[:file_name.rfind(".")]
        print("Sample: "+self.tmp_df_name+" is saved in temporary data frame.")
        #print(self.tmp_df)

    def make_correlation_plot(self):
        '''Make correlation plot using the tmp_df'''
        print("Plotting the correlation of feature for current temp dataframe...")
        corr = self.tmp_df.corr()

        fig, ax = plt.subplots()
        corr_ax = ax.matshow(corr)
        fig.colorbar(corr_ax)
        plt.xticks(range(len(corr.columns)), corr.columns, rotation = 'vertical');
        plt.yticks(range(len(corr.columns)), corr.columns);
        #ax.yaxis.set_tick_params(rotation=90)
        correlation_location = self.plot_location + "correlation_plots/"
        if not os.path.exists(correlation_location):
            os.mkdir(correlation_location)
        fig_name = correlation_location + self.tmp_df_name+".png"
        plt.savefig(fig_name)

    def make_scatter_matrix(self, vars_list, no_dummy = True):
        '''Make scatter matrix plot using the tmp_df'''
        print("Plotting the scatter matrix of the following features:")
        print(vars_list)
        from pandas.plotting import scatter_matrix
        fig, ax = plt.subplots()
        fig_size = min(10, len(vars_list))
        fig_size = max(fig_size,8)
        scatter_df = self.tmp_df[vars_list]
        if no_dummy:
            for var in vars_list:
                scatter_df = scatter_df.query(var+">-999")
        
        scatter_matrix(scatter_df, alpha=0.2, figsize=(fig_size, fig_size), diagonal='kde')
        scatter_location = self.plot_location + "scatter_matricess/"
        if not os.path.exists(scatter_location):
            os.mkdir(scatter_location)
        fig_name = scatter_location + self.tmp_df_name+".png"
        plt.savefig(fig_name)
    
    def save_df_to_csv(self):
        '''Save the data to a .csv file fro later use.'''
        out_file = self.csv_location+self.tmp_df_name+".csv"
        print("Saving the temporary dataframe to .csv file to: \n "+out_file)
        self.tmp_df.to_csv(out_file, sep=' ')

    def read_df_from_csv(self,file_name):
        '''Directly read data from csv to save time.'''
        print('Reading temporary dataframe from file %s'%file_name)
        if not(".csv" in file_name):
            file_name += ".csv"
        self.tmp_df = pd.read_csv(self.csv_location+file_name,delimiter=' ',\
        na_values=[-999])
        self.tmp_df_name = file_name[:file_name.rfind(".")]