import subprocess
import os
os.nice(19)
from create_old_file_list import get_files
MC_list = get_files()
#new_location = "../root_file_temp/Sicong_20180408/"
new_location = "../root_file_temp/Mia_20180223/"
runnings = []
core_num = 8
run_num = 0
for file_name in MC_list[6]["file_name_list"]:
    if "ttbar_diLept" in file_name:
        continue;
    run_list = ["root","-b","-q"]
    old_file_name = new_location + file_name[file_name.rfind("/")+1:]
    new_file_name = old_file_name.replace(".root","_1l.root")
    print(old_file_name, new_file_name)
    run_list.append("copytree_1lep.C(\"%s\",\"%s\")"%(old_file_name, new_file_name))
    p = subprocess.Popen(run_list)
    runnings.append(p)
    run_num+=1
    
    if run_num % core_num == 0:
        for p in runnings:
            p.wait()
        runnings = []
    
    run_list = ["root","-b","-q"]
    old_file_name = new_location + file_name[file_name.rfind("/")+1:]
    new_file_name = old_file_name.replace(".root","_2l.root")
    print(old_file_name, new_file_name)
    run_list.append("copytree_2lep.C(\"%s\",\"%s\")"%(old_file_name, new_file_name))
    p = subprocess.Popen(run_list)
    runnings.append(p)
    run_num+=1
    if run_num % core_num == 0:
        for p in runnings:
            p.wait()
        runnings = []
    
print("Submission Complete!!!")
for p in runnings:
    p.wait()