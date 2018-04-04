import ROOT

file_name = "../root_file_temp/Grid_20180404/Grid_Merged.root"
f = ROOT.TFile(file_name)
t = f.Get("t")
t.SetBranchStatus("*",0)
t.SetBranchStatus("mass_chargino",1)
t.SetBranchStatus("mass_lsp",1)
#mass_chargino, mass_lsp = 0, 0
read_list = []
nEntries= t.GetEntries()
f_txt = open("entry_mass_list.txt","w")
for i in range(nEntries):
    if i % 1e4 == 0: print("Reading %.0f with a total of %.0f1"%(i,nEntries))
    t.GetEntry(i)
    read_list.append([i, t.mass_chargino, t.mass_lsp])
    f_txt.write("%.0f %.0f %.0f\n"%(i, t.mass_chargino, t.mass_lsp))

f_txt.close()
f.Close()
read_list = sorted(read_list, key = lambda x: (x[1], x[2]))

import pickle
with open('entry_mass_list.pkl', 'w') as f_pickle: 
    pickle.dump([read_list], f_pickle)

# Getting back the objects:
import pickle
with open('entry_mass_list.pkl', 'r') as f_pickle:  
    [read_list] = pickle.load(f_pickle)

grid_chargino = 0
grid_lsp = 0
file_name = "%.0f_%.0f.txt"%(grid_chargino, grid_lsp)
out_dir = "../root_file_temp/Grid_20180404/entry_location/"
f_small = open(file_name, 'w')
for line in read_list:
    [entry_num, mass_chargino, mass_lsp] = line
    if not(grid_chargino == mass_chargino and grid_lsp == mass_lsp):
        f_small.close()
        grid_chargino, grid_lsp = mass_chargino, mass_lsp
        file_name = out_dir+"%.0f_%.0f.txt"%(grid_chargino, grid_lsp)
        print(file_name) 
        f_small = open(file_name, 'w')
        f_small.write("%.0f\n"%(entry_num))
    else:
        f_small.write("%.0f\n"%(entry_num))
f_small.close()



