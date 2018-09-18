#https://root.cern.ch/root/html534/guides/users-guide/Graphics.html#drawing-objects
import ROOT
import numpy
import array
import math
import os
os.nice(15)
ROOT.gStyle.SetOptStat(0);
#ROOT.gStyle.SetOptTitle(0);
ROOT.gROOT.SetBatch(ROOT.kTRUE);#Suppress Canvas

from testTDatabasePDG import analyze_particles

def scan_tree(file_name, str_condition):
    f = ROOT.TFile(file_name)
    t = f.Get("t")
    weight_form = ROOT.TTreeFormula("weight",str_condition,t)
    
    BTAGWP = 0.5426; #Loose btag working point
    mBTAGWP = 0.8484; #Medium btag working point
    
    process_name = file_name[file_name.find("Sicong"):]
    process_name = process_name[process_name.find("/")+1:process_name.find(".")]
    print("Total Number of events in %s: %.0f"%(process_name, t.GetEntries()))
    selected_num = 0
    total_num = 10
    
    for i in range(t.GetEntries()):
        if i % 1e4 == 0: print(i)
        t.GetEntry(i)
        weight = weight_form.EvalInstance()
        if weight == 0:
            continue ;
        ht_raio = t.ak4_htratiom
        min_deltaphi = t.mindphi_met_j1_j2
        print(ht_raio, min_deltaphi)
        random_str = process_name+"_"+str(selected_num)
        canvas = ROOT.TCanvas("can"+random_str,"can"+random_str, 1600, 1600)
        pad1 = ROOT.TPad("pad1"+random_str,"pad1"+random_str, 0, 0.5, 0.5, 1.)
        pad1.SetBottomMargin(0); 
        pad1.Draw()
        pad1.cd();
        
        pT_list = [t.pfmet, t.lep1_p4.Pt(), t.ak4pfjets_p4.at(0).Pt()]
        axis_size = max(pT_list)
        #axis_size = 1000.
        tmp_array = array.array("d",[0.])
        n = 2
        theta, r = array.array( 'd' ), array.array( 'd' )
        for ind in range( n ):
            theta.append( axis_size*ind )
            r.append( axis_size*ind)
        grP1 = ROOT.TGraphPolar(n, theta, r);
        grP1.SetTitle("");
        grP1.SetLineWidth(3);
        grP1.Draw("axis");
        #Daw Met:
        print(t.pfmet)
        met_arr = ROOT.TArrow(0., 0., t.pfmet/axis_size, 0., 0.025,"|>") 
        met_arr.SetFillColor(ROOT.kRed);
        met_arr.SetLineColor(ROOT.kRed);
        met_arr.SetLineWidth(3);
        met_arr.SetAngle(45)
        met_arr.Draw("")
        #Jet
        jet_arr = ROOT.TArrow()
        jet_arr.SetLineWidth(3);
        jet_arr.SetAngle(45)
        jet_arr.SetFillColor(ROOT.kYellow);
        jet_arr.SetLineColor(ROOT.kYellow);
        
        jet_arr_med = ROOT.TArrow()
        jet_arr_med.SetLineWidth(3);
        jet_arr_med.SetAngle(45)
        jet_arr_med.SetFillColor(ROOT.kAzure);
        jet_arr_med.SetLineColor(ROOT.kAzure);
        
        jet_arr_loose = ROOT.TArrow()
        jet_arr_loose.SetLineWidth(3);
        jet_arr_loose.SetAngle(45)
        jet_arr_loose.SetFillColor(ROOT.kCyan);
        jet_arr_loose.SetLineColor(ROOT.kCyan);
        
        for jet_i in range(len(t.ak4pfjets_p4)):
            pt = t.ak4pfjets_p4.at(jet_i).Pt()
            phi = t.ak4pfjets_p4.at(jet_i).Phi() - t.pfmet_phi
            x =  pt*math.cos(phi)/axis_size
            y = pt*math.sin(phi)/axis_size
            if t.ak4pfjets_CSV.at(jet_i)>mBTAGWP:
                jet_arr_med.DrawArrow(0.,0.,x,y, 0.01, "|>")
            elif t.ak4pfjets_CSV>BTAGWP:
                jet_arr_loose.DrawArrow(0.,0.,x,y, 0.01, "|>")
            else:
                jet_arr.DrawArrow(0.,0.,x,y, 0.01, "|>")
        
        #Photon
        ph_arr = ROOT.TArrow()
        ph_arr.SetLineWidth(3);
        ph_arr.SetAngle(45)
        ph_arr.SetFillColor(ROOT.kOrange);
        ph_arr.SetLineColor(ROOT.kOrange);
        
        for ph_i in range(len(t.ph_pt)):
            pt = t.ph_pt.at(jet_i)
            phi = t.ph_phi.at(ph_i).Phi() - t.pfmet_phi
            x =  pt*math.cos(phi)/axis_size
            y = pt*math.sin(phi)/axis_size
            ph_arr.DrawArrow(0.,0.,x,y, 0.01, "|>")
        
        #Lepton
        lep_arr = ROOT.TArrow()
        lep_arr.SetLineWidth(3);
        lep_arr.SetAngle(45)
        pt = t.lep1_p4.Pt()
        phi = t.lep1_p4.Phi() - t.pfmet_phi
        x =  pt*math.cos(phi)/axis_size
        y = pt*math.sin(phi)/axis_size
        lep_arr.SetFillColor(ROOT.kSpring);
        lep_arr.SetLineColor(ROOT.kSpring);
        lep_arr.DrawArrow(0.,0.,x,y, 0.01, "|>")
        axis_size_1 = axis_size
        pad1.Update()
        canvas.Update()
        canvas.cd()
        
        pad2 = ROOT.TPad("pad2"+random_str,"pad2"+random_str, 0.5, 0.5, 1., 1.)
        pad2.SetBottomMargin(0.15); 
        pad2.Draw()
        pad2.cd();
        X_array = array.array("d",[t.mindphi_met_j1_j2])
        Y_array = array.array("d",[t.ak4_htratiom])
        gr = ROOT.TGraph(len(X_array), X_array,Y_array);
        gr.SetTitle(random_str);
        gr.GetYaxis().SetTitle("ak4_htratiom")
        gr.GetXaxis().SetTitle("mindphi_met_j1_j2")
        gr.GetYaxis().SetTitleOffset(1.3)
        gr.GetYaxis().SetRangeUser(0., 1.1)
        gr.GetXaxis().SetLimits(0., 3.5)
        gr.SetMarkerStyle(22)
        gr.SetMarkerSize(1)
        gr.SetMarkerColor(ROOT.kRed)

        gr.Draw('A P')
        legend = ROOT.TLegend(0.4,0.55,0.9,0.9);
        legend.SetHeader("Entry #: %.0f"%i, "C")
        legend.AddEntry(met_arr,"Missing E_{T}","l");
        legend.AddEntry(lep_arr,"Lepton, p_{T}","l");
        legend.AddEntry(jet_arr_med,"med b-jet, p_{T}","l");
        legend.AddEntry(jet_arr_loose,"loose b-jet, p_{T}","l");
        legend.AddEntry(jet_arr,"other jet, p_{T}","l");        
        legend.AddEntry(ph_arr,"photon, p_{T}","l");
        legend.Draw('same')

        pad2.Update()
        canvas.cd();
        
        pad3 = ROOT.TPad("pad3"+random_str,"pad3"+random_str, 0., 0., 0.5, 0.5)
        pad3.SetBottomMargin(0.);
        pad3.Draw()
        plot_vec_list = analyze_particles(t)
        pad3.cd();
        max_x = max([max(abs(item["x0"]),abs(item["x1"])) for item in plot_vec_list])
        max_y = max([max(abs(item["y0"]),abs(item["y1"])) for item in plot_vec_list])
        axis_size = max(max_x,max_y)
        n = 2
        theta, r = array.array( 'd' ), array.array( 'd' )
        for ind in range( n ):
            theta.append( axis_size*ind )
            r.append( axis_size*ind)
        grP3 = ROOT.TGraphPolar(n, theta, r);
        grP3.SetTitle("");
        grP3.SetLineWidth(3);
        grP3.Draw("axis");
    
        gen_arr = ROOT.TArrow()
        gen_arr.SetLineWidth(3);
        gen_arr.SetAngle(45)
        gen_arr.SetFillColor(ROOT.kRed);
        gen_arr.SetLineColor(ROOT.kRed);
        
        latex = ROOT.TLatex();
        latex.SetTextAlign(22);
        latex.SetTextSize(0.02);
        
        for vec_dict in plot_vec_list:
            gen_arr.DrawArrow(vec_dict["x0"]/axis_size,vec_dict["y0"]/axis_size,vec_dict["x1"]/axis_size,vec_dict["y1"]/axis_size, 0.01, "|>")
        for vec_dict in plot_vec_list:
            latex.DrawLatex(vec_dict["x1"]/axis_size,vec_dict["y1"]/axis_size,vec_dict["name"]);
        pad3.Update()
        
        canvas.cd();
        pad4 = ROOT.TPad("pad3"+random_str,"pad3"+random_str, 0.5, 0., 1, 0.5)
        pad4.SetBottomMargin(0.);
        pad4.Draw();
        pad4.cd();
        out_vec_list = [] #Select only the child-less particles
        for vec_dict in plot_vec_list:
            flag_out = True
            for vec_dict2 in plot_vec_list:
                if vec_dict2["motheridx"] == vec_dict["idx"]:
                    flag_out = False;
                    break;
            if flag_out:
                out_vec_list.append(vec_dict)
        max_dx = max([abs(item["x0"]-item["x1"]) for item in out_vec_list])
        max_dy = max([abs(item["y0"]-item["y1"]) for item in out_vec_list])
        axis_size = max(max_dx,max_dy)
        n = 2
        theta, r = array.array( 'd' ), array.array( 'd' )
        for ind in range( n ):
            theta.append( axis_size*ind )
            r.append( axis_size*ind)
        grP4 = ROOT.TGraphPolar(n, theta, r);
        grP4.SetTitle("");
        grP4.SetLineWidth(3);
        grP4.Draw("axis");
        
        out_gen_arr = ROOT.TArrow()
        out_gen_arr.SetLineWidth(3);
        out_gen_arr.SetAngle(45)
        out_gen_arr.SetFillColor(ROOT.kRed);
        out_gen_arr.SetLineColor(ROOT.kRed);
        
        latex = ROOT.TLatex();
        latex.SetTextAlign(22);
        latex.SetTextSize(0.02);
                
        for vec_dict in out_vec_list:
            x, y = (vec_dict["x1"]-vec_dict["x0"])/axis_size, (vec_dict["y1"]-vec_dict["y0"])/axis_size 
            out_gen_arr.DrawArrow(0., 0., x, y, 0.01, "|>")
        for vec_dict in out_vec_list:
            x, y = (vec_dict["x1"]-vec_dict["x0"])/axis_size, (vec_dict["y1"]-vec_dict["y0"])/axis_size
            latex.DrawLatex(x, y, vec_dict["name"]);
        pad4.Update()
        
        canvas.Update()
        #plot_dir = "/home/users/siconglu/CMSTAS/software/niceplots/WH_Analyze_HTratio_pfmet/"
        plot_dir = "/home/users/siconglu/CMSTAS/software/niceplots/WH_Analyze_old_2jet_region/"
        #plot_dir = ""
        canvas.Print(plot_dir+random_str+'.png')
        canvas.Close()
        selected_num += 1
        if selected_num>=total_num:
            break;
        
    f.Close()
    return 0
import multiprocessing as mp
from selection_criteria import get_cut_dict, combine_cuts
if __name__ == "__main__":
    cut_dict, current_cut_list,region_cut_dict = get_cut_dict()
    region_str = "PSR3jet_met_225_mct225"
    region_str = "SR2"
    #region_str = "PSR1jet_met_200_pt_600"
    str_condition = region_cut_dict[region_str] + "&& ak4_htratiom > 0. && mindphi_met_j1_j2 > 0."
    from create_file_list import get_files

    MC_list = get_files()
    #new_location = "../root_file_temp/Sicong_20180408/"
    new_location = "../root_file_temp/Sicong_20180605/"

    process_ind = 0
    num_cores = 20
    processes = []
    all_list = MC_list[0:11] 
    #all_list = MC_list[13:]
    for MC in all_list:
        for file_name in MC["file_name_list"]:
            file_name_record = file_name
            file_name = new_location + file_name[file_name.rfind("/")+1:]
            p = mp.Process(target=scan_tree, args=(file_name, str_condition,))
            #if "ttbar_diLept_madgraph_pythia8_ext1_25ns_9" in file_name: 
            processes.append(p)
            process_ind+=1
            if (process_ind)%num_cores == 0 or (MC == all_list[-1] and file_name_record == MC["file_name_list"][-1]):            
                [x.start() for x in processes]
                print("Starting %.0f process simultaneously."%len(processes))
                [x.join() for x in processes]
                processes = []
    

