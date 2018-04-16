import ROOT
import pandas as pd
def read_df_from_csv(file_name, nrows = False):
    '''Directly read data from csv to save time.'''
    csv_location = "../csv_file_temp/"
    print('Reading temporary dataframe from file %s'%file_name)
    if not(".csv" in file_name):
        file_name += ".csv"
    if not(nrows):
        tmp_df = pd.read_csv(csv_location+file_name,delimiter=' ')#, na_values=[-999]
    else:
        tmp_df = pd.read_csv(csv_location+file_name,delimiter=' ', nrows=nrows)#, na_values=[-999]
    tmp_df_name = file_name[:file_name.rfind(".")]
    return tmp_df
def plot_overtrain(y_train, y_test, y_train_pred, y_test_pred, w_train, w_test, full_path = ""):
    print("Generating the overtrain plot.")
    
    ROOT.gStyle.SetOptStat(0);
    ROOT.gStyle.SetOptTitle(0);
    ROOT.gROOT.SetBatch()
    
    h_sig_train = ROOT.TH1F("h_sig_train","h_sig_train",50,0,1)
    h_bkg_train = ROOT.TH1F("h_bkg_train","h_bkg_train",50,0,1)
    h_sig_test = ROOT.TH1F("h_sig_test","h_sig_test",50,0,1)
    h_bkg_test = ROOT.TH1F("h_bkg_test","h_bkg_test",50,0,1)
    
    for i in range(len(y_train)):
        if y_train[i] == 1:
            h_sig_train.Fill(y_train_pred[i][1],w_train[i])
        else:
            h_bkg_train.Fill(y_train_pred[i][1],w_train[i])
    for i in range(len(y_test)):
        if y_test[i] == 1:
            h_sig_test.Fill(y_test_pred[i][1],w_test[i])
        else:
            h_bkg_test.Fill(y_test_pred[i][1],w_test[i])
    
    canvas = ROOT.TCanvas("Overtrain", "Overtrain",800,600)
    canvas.SetBorderMode(0);
    canvas.SetBorderSize(2);
    canvas.SetLeftMargin(0.16);
    canvas.SetRightMargin(0.05);
    canvas.SetTopMargin(0.05);
    canvas.SetBottomMargin(0.16);
    canvas.SetFrameBorderMode(0);
    canvas.SetLogy();
    
    yaxis = h_sig_train.GetYaxis()
    xaxis = h_sig_train.GetXaxis()
    yaxis.SetTitle("Fraction of Events")
    yaxis.SetTitleSize(0.05); yaxis.SetTitleFont(42); yaxis.SetTitleOffset(1.4);
    yaxis.SetLabelFont(42); yaxis.SetLabelSize(0.05)
    
    xaxis.SetTitle("xgb Probability")
    xaxis.SetTitleSize(0.05); xaxis.SetTitleFont(42); xaxis.SetTitleOffset(1.4);
    xaxis.SetLabelFont(42); xaxis.SetLabelSize(0.05)
    
    h_sig_train.SetFillStyle(3010); h_bkg_train.SetFillStyle(3010);
    h_sig_train.SetFillColor(ROOT.kRed); h_bkg_train.SetFillColor(ROOT.kBlue);
    
    h_sig_test.SetMarkerSize(1); h_bkg_test.SetMarkerSize(1);
    h_sig_test.SetMarkerStyle(20); h_bkg_test.SetMarkerStyle(20);
    h_sig_test.SetMarkerColor(ROOT.kRed); h_bkg_test.SetMarkerColor(ROOT.kBlue);
    
    print(h_sig_train.Integral()); print(h_bkg_train.Integral())
    h_sig_train.Scale(1./h_sig_train.Integral())
    h_bkg_train.Scale(1./h_bkg_train.Integral())
    h_sig_test.Scale(1./h_sig_test.Integral())
    h_bkg_test.Scale(1./h_bkg_test.Integral())
    
    h_sig_train.SetMaximum(h_sig_train.GetMaximum()*2);
    h_sig_train.SetMinimum(0);
    
    h_sig_train.Draw('hist '); h_bkg_train.Draw('hist same')
    h_sig_test.Draw('p same'); h_bkg_test.Draw('p same')
    #lat = ROOT.TLatex(); lat.DrawLatexNDC(0.5,0.88,'Test XGBoost Training')
    leg = ROOT.TLegend(0.6,0.62,0.8,0.78)
    leg.AddEntry(h_sig_train,'SIG train','F')
    leg.AddEntry(h_bkg_train,'BKG train','F')
    leg.AddEntry(h_sig_test,'SIG test','P')
    leg.AddEntry(h_bkg_test,'BKG test','P')
    
    leg.SetLineColor(0); leg.SetShadowColor(0); leg.SetFillStyle(0); leg.SetFillColor(0);
    leg.SetTextSize(0.03)
    leg.Draw()
        
    canvas.Update()
    file_name = "overtrain"
    canvas.Print(full_path+file_name+'.png')
    canvas.Print(full_path+file_name+'.pdf')
    out_file = ROOT.TFile.Open('histograms.root','RECREATE')
    h_sig_train.Write()
    h_bkg_train.Write()
    h_sig_test.Write()
    h_bkg_test.Write()
    out_file.Close()
