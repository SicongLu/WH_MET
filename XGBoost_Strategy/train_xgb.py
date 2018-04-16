'''
This should be a simple and quick module to test using xgboost to multi-classify
the different categories of processes.'''
import pandas as pd
import xgboost as xgb
import matplotlib.pyplot as plt
from sklearn import model_selection
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import LabelEncoder
from helpers import plot_overtrain, read_df_from_csv
class xgb_analyzer:
    def __init__(self):
        '''Set-up the common variables.'''
        print('Setting up analysis')
        self.lumi = 35.9
        self.old_features = ["mbb", "ngoodjets", "MT2W", "Mlb_closestb", "mct", "mt_met_lep",\
        "pfmet", "topness", "topnessMod","mindphi_met_j1_j2","scale1fb","ptbb"]
        self.features = self.old_features + ["weight"]
        #self.features_name_dict = {"mbb":"M_{bb}"}
        self.csv_location = "../csv_file_temp/"
        self.root_location = "../root_file_temp/Sicong_20180228/"
        self.root_out_location = "../root_file_temp/XGB_20180401/"
        self.plot_location = "/home/users/siconglu/CMSTAS/software/niceplots/WH_pandas_analysis/"
    def apply_preselection(self, tmp_df):
        '''Apply some basic prelection for the training samples.'''
        #1 lep+2 lep veto+2 btag+MET>100+MT>150.
        preselection_str = "lep1_tight == 1 && lep2_tight == 0 && lep2_veto == 0 && PassTrackVeto && PassTauVeto && nbtag_loose ==2 && nbtag_med >=1 && new_met>100&& new_mt>150" 
        preselection = (tmp_df["lep1_tight"]==1)&(tmp_df["lep2_tight"]==0)&(tmp_df["lep2_veto"]==0)\
        &(tmp_df["PassTrackVeto"]>0)&(tmp_df["PassTauVeto"]>0)\
        &(tmp_df["nbtag_loose"]==2)&(tmp_df["nbtag_med"]>=1)\
        &(tmp_df["new_met"]>100)&(tmp_df["new_mt"]>150)
        
        return tmp_df[preselection]
    def prepare_all_data_file(self):
        from create_file_list import get_files, getgrid, generate_scan_dict
        grid_list = generate_scan_dict()
        MC_list = get_files()
        sig_file_name_list = []#sig_file_name_list = ["TChiWH_700_1"]
        bkg_file_name_list = []#bkg_file_name_list = ["ttbar_diLept_madgraph_pythia8_25ns_1",]        
        for MC in MC_list[4:]+grid_list[0:0]:
            print(MC['name'])
            for file_name in MC['file_name_list']:
                file_name = file_name[file_name.rfind("/")+1:]
                file_name = file_name[:file_name.rfind(".")]
                #print(file_name)
                if "(" in MC['name']:
                    sig_file_name_list.append(file_name)
                else:
                    bkg_file_name_list.append(file_name)        
        df_list = []
        for file_name in sig_file_name_list:
            tmp_df = read_df_from_csv(file_name)
            tmp_df = self.apply_preselection(tmp_df)
            tmp_df["MC_ID"] = 1 #Denote signal with 1 bkg with 0.
            df_list.append(tmp_df)
        
        for file_name in bkg_file_name_list:
            tmp_df = read_df_from_csv(file_name) #Add a number n to read the first n rows.
            tmp_df = self.apply_preselection(tmp_df)
            tmp_df["MC_ID"] = 0
            df_list.append(tmp_df)
        self.df = pd.concat(df_list)
        self.label = self.df['MC_ID']
        
    def reweight_dataframe_uniformly(self):
        '''Reweight so that signal and background have the same total yield.'''
        sig_num = len(self.df[self.df['MC_ID']==1])
        bkg_num = len(self.df[self.df['MC_ID']==0])  
        self.df.loc[self.df['MC_ID'] == 1, 'weight'] = 1.0*sig_num/sig_num
        self.df.loc[self.df['MC_ID'] == 0, 'weight'] = 1.0*sig_num/bkg_num
        print("Reading: %.0f sig events, %.0f bkg events."%(sig_num, bkg_num))
    def reweight_dataframe(self):
        '''Reweight so that signal and background have the same total yield.'''
        sig_num = self.df.loc[self.df['MC_ID'] == 1, 'weight'].sum() 
        bkg_num = self.df.loc[self.df['MC_ID'] == 0, 'weight'].sum()
        print("Reading the yield: %.2f sig events, %.2f bkg events."%(sig_num, bkg_num))  
        self.df.loc[self.df['MC_ID'] == 1, 'weight'] *= 1.0*bkg_num/sig_num
        self.df.loc[self.df['MC_ID'] == 0, 'weight'] *= 1.0*bkg_num/bkg_num
        
    
    def xgb_training(self):
        '''Trim unnecessary variables.'''    
        self.used_var_list = ["ngoodjets","new_mct","new_mt","new_mbb","new_met","weight"]
        var_file = open("used_vars_list.txt","w")
        print("Using the following variables:")
        for var in self.used_var_list:
            var_file.write(var+"\n")
            print(var)
        for item in self.df.columns:
            if not(item in self.used_var_list):
                self.df = self.df.drop([item],axis=1)
        '''Separate Train and Test samples.'''
        X = self.df
        y = self.label.values
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.5, random_state=7)
        
        w_train = X_train["weight"].values
        w_test = X_test["weight"].values
        X_train = X_train.drop(['weight'],axis=1)
        X_test = X_test.drop(['weight'],axis=1)
        
        X_train = X_train.values
        X_test = X_test.values
        dtrain  = xgb.DMatrix(X_train, label=y_train, missing=-999.0, weight = w_train)
        dtest  = xgb.DMatrix(X_test, label=y_test, missing=-999.0, weight = w_test)
        
        dtrain.save_binary('train.buffer')
        dtest.save_binary('test.buffer')
        
        #Set-up training variables
        params = {"objective":"multi:softprob", "num_class": 2, "max_depth":5, "silent":1, "eta":0.01, \
        "n_estimators":1000}#,"min_child_weight":0.001 
        num_rounds = 1000
        watchlist = [(dtest,'test'),(dtrain,'train')]
        bst = xgb.train(params, dtrain, num_rounds, watchlist)
        bst.save_model("xgb_model_0412_uniform_weight.xgb")
        self.model = bst 
        self.all_data = [dtrain, dtest, y_train, y_test, w_train, w_test]
        y_train_pred = bst.predict(dtrain)
        y_test_pred =  bst.predict(dtest)
        plot_overtrain(y_train, y_test, y_train_pred, y_test_pred, w_train, w_test, full_path = "")

    def evaluate_prediction(self, bst, dtest):
        '''Evaluate the prediction'''
        y_pred = bst.predict(dtest)
        
        #xgb.plot_importance(self.bst)
        #plt.show()
        #xgb.plot_tree(bst, num_trees=2)
        #xgb.to_graphviz(bst, num_trees=2)
a = xgb_analyzer()
a.prepare_all_data_file()
a.reweight_dataframe_uniformly()
a.xgb_training()
