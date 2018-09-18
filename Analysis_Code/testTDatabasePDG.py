import ROOT
import networkx as nx
import matplotlib.pyplot as plt
import array
import copy
import math
import sys
def pt_addition(plot_vec_list, idx):
    for vec_dict in plot_vec_list:
        if vec_dict["idx"] == idx:
            px = vec_dict['x1']
            py = vec_dict['y1']
            px0, py0 = pt_addition(plot_vec_list, vec_dict["motheridx"])
            return px+px0, py+py0
    return 0, 0
def analyze_particles(t):
    #Reproducing the particle list...
    pdg = ROOT.TDatabasePDG()
    #met_phi = t.new_met_phi
    met_phi = t.pfmet_phi
    genps_p4 = []
    genps_id = []
    genps_motherid = []
    genps_motherp4 = []
    genps_isLastCopy = []
    genps_status = []
    
    for i in range(t.genqs_id.size()):
        genps_p4.append(t.genqs_p4.at(i))
        genps_id.append(t.genqs_id.at(i))
        genps_motherp4.append(t.genqs_motherp4.at(i))
        genps_motherid.append(t.genqs_motherid.at(i))
        genps_isLastCopy.append(t.genqs_isLastCopy.at(i))
        genps_status.append(t.genqs_status.at(i))
        
    for i in range(t.genleps_id.size()):
        genps_p4.append(t.genleps_p4.at(i))
        genps_id.append(t.genleps_id.at(i))
        genps_motherp4.append(t.genleps_motherp4.at(i))
        genps_motherid.append(t.genleps_motherid.at(i))
        genps_isLastCopy.append(t.genleps_isLastCopy.at(i))
        genps_status.append(t.genleps_status.at(i))    
    for i in range(t.gennus_id.size()):
        genps_p4.append(t.gennus_p4.at(i))
        genps_id.append(t.gennus_id.at(i))
        genps_motherp4.append(t.gennus_motherp4.at(i))
        genps_motherid.append(t.gennus_motherid.at(i))
        genps_isLastCopy.append(t.gennus_isLastCopy.at(i))
        genps_status.append(t.gennus_status.at(i))
    for i in range(t.genbosons_id.size()):
        genps_p4.append(t.genbosons_p4.at(i))
        genps_id.append(t.genbosons_id.at(i))
        genps_motherp4.append(t.genbosons_motherp4.at(i))
        genps_motherid.append(t.genbosons_motherid.at(i))
        genps_isLastCopy.append(t.genbosons_isLastCopy.at(i))
        genps_status.append(t.genbosons_status.at(i))
    for i in range(t.gensusy_id.size()):
        genps_p4.append(t.gensusy_p4.at(i))
        genps_id.append(t.gensusy_id.at(i))
        genps_motherp4.append(t.gensusy_motherp4.at(i))
        genps_motherid.append(t.gensusy_motherid.at(i))
        genps_isLastCopy.append(t.gensusy_isLastCopy.at(i))
        genps_status.append(t.gensusy_status.at(i))
    
    #Processing the gen_particles...
    genps_name = []
    genps_mothername = []
    genps_motheridx = [] 
    edges = []
    for i in range(len(genps_id)):
        p_name = pdg.GetParticle(genps_id[i]).GetName()
        genps_name.append(p_name)
        mother_name = pdg.GetParticle(genps_motherid[i]).GetName()
        genps_mothername.append(mother_name)
        genps_motheridx.append(-1)
        edges.append((-1,i))
        for j in range(len(genps_id)):
            if genps_id[j] == genps_motherid[i] and genps_p4[j] == genps_motherp4[i]:
                genps_motheridx[i] = j
                edges[i] = (j, i)
                break;
    plot_vec_list = []
    
    #for i in range(len(genps_id)):
    #    print("%.0f. "%i),
    #    print(pdg.GetParticle(genps_id[i]).GetName()),
    #    print(pdg.GetParticle(genps_motherid[i]).GetName()),
    #    tmp_phi = genps_p4[i].Phi()-met_phi 
    #    print(genps_p4[i].Pt()*math.cos(tmp_phi)),
    #    print(genps_p4[i].Pt()*math.sin(tmp_phi)),
    #    if genps_isLastCopy[i]:
    #        print("Last Copy."),
    #    print("Mother: %.0f "%genps_motheridx[i] ),
    #    print(genps_status[i])
    #print("Number of ISR jets:%.0f"%t.NISRjets)
    #sys.exit()
    for i in range(len(genps_id)):
        #print(genps_name[i]),
        tmp_ind = i
        if not(genps_isLastCopy[tmp_ind]):
            continue;
        print(" <= %s (%.0f)(s=%.0f)" %(genps_name[tmp_ind], tmp_ind,genps_status[tmp_ind])),
        while True:
            if genps_motheridx[tmp_ind] == -1:
                break;
            else:
                tmp_dict = {"name":genps_name[tmp_ind],"idx":tmp_ind,"motheridx":genps_motheridx[tmp_ind],"isLastCopy":genps_isLastCopy[tmp_ind]}
                tmp_dict["x0"] = 0
                tmp_dict["y0"] = 0
                pt = genps_p4[tmp_ind].Pt()
                phi =genps_p4[tmp_ind].Phi() - met_phi
                x =  pt*math.cos(phi)
                y = pt*math.sin(phi)
                tmp_dict["x1"] = x # genps_p4[tmp_ind].Px()
                tmp_dict["y1"] = y #genps_p4[tmp_ind].Py()
                flag_add = True
                for vec_dict in plot_vec_list:
                    if not(tmp_dict["isLastCopy"]):#Only considering the last copy
                        flag_add = False;
                        print("not last copy"),
                        break;      
                if flag_add: 
                    plot_vec_list.append(tmp_dict)
                    print("ADDED!!!!"),
                #else:
                #    break;
                tmp_ind = genps_motheridx[tmp_ind]
                print(" <= %s (%.0f)(s=%.0f)" %(genps_name[tmp_ind], tmp_ind,genps_status[tmp_ind])),
                
        print(genps_p4[i].Pt())            
    #Start pt addition
    #original_vec_list = plot_vec_list
    original_vec_list = copy.deepcopy(plot_vec_list)
    for i in range(len(plot_vec_list)):
        idx = plot_vec_list[i]["motheridx"]
        px, py = pt_addition(original_vec_list, idx)
        plot_vec_list[i]["x0"]+=px
        plot_vec_list[i]["x1"]+=px
        plot_vec_list[i]["y0"]+=py
        plot_vec_list[i]["y1"]+=py
    return plot_vec_list
        
    
if __name__ == "__main__":
    file_name = "../root_file_temp/Sicong_20180408/TChiWH_225_75.root"
    #file_name = "../root_file_temp/Sicong_20180408/ttbar_diLept_madgraph_pythia8_ext1_25ns_9.root"
    print(file_name)
    f = ROOT.TFile(file_name)
    t = f.Get("t")
    
    t.GetEntry(35635)
    #t.GetEntry(100513)
    plot_vec_list = analyze_particles(t)
    f.Close()
    
    max_x = max([max(abs(item["x0"]),abs(item["x1"])) for item in plot_vec_list])
    max_y = max([max(abs(item["y0"]),abs(item["y1"])) for item in plot_vec_list])
    axis_size = max(max_x,max_y)*1.2
    print(max_x, max_y, axis_size)
    
    #Start Drawing
    random_str = ""
    
    canvas = ROOT.TCanvas("can"+random_str,"can"+random_str, 800, 800)
    n = 2
    theta, r = array.array( 'd' ), array.array( 'd' )
    for ind in range( n ):
        theta.append( axis_size*ind )
        r.append( axis_size*ind)
    grP1 = ROOT.TGraphPolar(n, theta, r);
    grP1.SetTitle("");
    grP1.SetLineWidth(3);
    grP1.Draw("axis");

    gen_arr = ROOT.TArrow()
    gen_arr.SetLineWidth(3);
    gen_arr.SetAngle(45)
    gen_arr.SetFillColor(ROOT.kRed);
    gen_arr.SetLineColor(ROOT.kRed);
    
    latex = ROOT.TLatex();
    latex.SetTextAlign(22);
    latex.SetTextSize(0.02);
    
    for vec_dict in plot_vec_list:
        #print(vec_dict)
        gen_arr.DrawArrow(vec_dict["x0"]/axis_size,vec_dict["y0"]/axis_size,vec_dict["x1"]/axis_size,vec_dict["y1"]/axis_size, 0.01, "|>")
        latex.DrawLatex(vec_dict["x1"]/axis_size,vec_dict["y1"]/axis_size,vec_dict["name"]);
    canvas.Update()
    canvas.Print('test.png')
    canvas.Close()
