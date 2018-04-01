'''
This should be a simple and quick module to test using xgboost to multi-classify
the different categories of processes.'''
#Import
import pandas as pd
import xgboost as xgb
import matplotlib.pyplot as plt
from sklearn import model_selection
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import LabelEncoder
def read_df_from_csv(file_name):
    '''Directly read data from csv to save time.'''
    csv_location = "../csv_file_temp/"
    print('Reading temporary dataframe from file %s'%file_name)
    if not(".csv" in file_name):
        file_name += ".csv"
    tmp_df = pd.read_csv(csv_location+file_name,delimiter=' ')#, na_values=[-999]
    tmp_df_name = file_name[:file_name.rfind(".")]
    return tmp_df

#Filename
sig_file_name_list = ["TChiWH_700_1"]
bkg_file_name_list = ["ttbar_diLept_madgraph_pythia8_25ns_1"]
df_list = []

for file_name in sig_file_name_list:
    tmp_df = read_df_from_csv(file_name)
    #tmp_df = tmp_df[:24482]
    print(len(tmp_df.index))
    tmp_df["MC_ID"] = 1
    df_list.append(tmp_df)

for file_name in bkg_file_name_list:
    tmp_df = read_df_from_csv(file_name)
    #tmp_df = tmp_df[:24482]
    tmp_df["MC_ID"] = 0
    df_list.append(tmp_df)

df = pd.concat(df_list)
label = df['MC_ID']
df = df.drop(['MC_ID'],axis=1)
#Trim unnecessary variables.
used_var_list = ["ngoodjets","mct","mt_met_lep","mbb","pfmet","scale1fb"]
#,"MT2W"
print("Using the following variables:")
for item in df.columns:
    if not(item in used_var_list):
        df = df.drop([item],axis=1)

#Separate Train and Test samples.
X = df
y = label.values

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.33, random_state=7)

w_train = X_train["scale1fb"].values
w_test = X_test["scale1fb"].values

X_train = X_train.drop(['scale1fb'],axis=1)
X_test = X_test.drop(['scale1fb'],axis=1)

X_train = X_train.values
X_test = X_test.values

dtrain  = xgb.DMatrix(X_train, label=y_train, missing=-999.0, weight = w_train)
dtest  = xgb.DMatrix(X_test, label=y_test, missing=-999.0, weight = w_test)

dtrain.save_binary('train.buffer')

#Set-up training variables
params = {"objective":"binary:logistic", "max_depth":5, "silent":1, "eta":0.3, \
"n_estimators":10}#,"min_child_weight":0.001 
num_rounds = 100
watchlist = [(dtest,'test'),(dtrain,'train')]
bst = xgb.train(params, dtrain, num_rounds, watchlist)

#Evaluate the prediction
y_pred = bst.predict(dtest)
print(y_pred)
predictions = [round(value) for value in y_pred]
accuracy = accuracy_score(y_test, predictions)
print("Accuracy: %.4f%%" % (accuracy * 100.0))

xgb.plot_importance(bst)
plt.show()

#xgb.plot_tree(bst, num_trees=2)
#xgb.to_graphviz(bst, num_trees=2)