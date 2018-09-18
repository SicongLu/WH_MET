'''
Quick and Dirty method to get a simple expected exclusion area.
'''
from ROOT import TH1F,TFile
import os
from math import sqrt
import pandas as pd

def printcard(masspoint,masspointinfo,binN,backgrounds,errors, bin_name ,carddir):
  
    sigN,sigE = masspointinfo['yield'], masspointinfo['stat']  
    cardname = carddir+'/datacard_'+str(binN)+'_tchwh_'+masspoint+'.txt'
    card = open(cardname,'w')
    card.write("imax  1  number of channels\n")
    card.write("jmax  6  number of backgrounds\n")
    card.write("kmax  *  number of nuisance parameters\n")
    card.write("------------\n")
    card.write("# observations\n")
    card.write("bin        "+bin_name+'\n')
    card.write("observation  " +str(8)+'\n') # str(backgrounds['data'])
    card.write("#now we list all expected number of events\n")
    bintoprint = bin_name+' '
    card.write("bin "+7*bintoprint+'\n')
    card.write("process     sig       2ltop       WLF       1ltop       wzbb   rare WHF \n")
    card.write("process      0        1         2         3          4      5    6\n")
    binI = binN-1
    card.write("rate " +str(sigN) +' ' + str(backgrounds['2l'][binI]) +' ' + str(backgrounds['1l'][binI])+' ' + str(backgrounds['1ltop'][binI])+' ' + str(backgrounds['wzbb'][binI])+' ' + str(backgrounds['rare'][binI])+ " "+str(backgrounds['1lH'][binI]))
    card.write("\n------------\n")
    card.write("SigStat"    +str(binI)+"  lnN " +str(sigE)+' - - - - - -\n')
    card.write("Bg2lStat"   +str(binI)+"  lnN - " +str(errors['2l'][binI])+'  -  -  -  - - \n')
    card.write("Bg1lStat"   +str(binI)+"  lnN - - " +str(errors['1l'][binI])+'   -  -  - - \n')
    card.write("Bg1ltopStat"+str(binI)+"  lnN - -  - " +str(errors['1ltop'][binI])+' -  - - \n')
    card.write("BgwzbbStat" +str(binI)+"  lnN - -  -  - " +str(errors['wzbb'][binI])+' - - \n')
    card.write("BgrareStat" +str(binI)+"  lnN - -  -  -  - " +str(errors['rare'][binI])+' - \n')
    card.write("Bg1lHStats" +str(binI)+"  lnN - -  -  -  -  - " +str(errors['1lH'][binI])+' \n')
    #card.write("MCSystSig       lnN 1.15  -  -  -  - - - \n")
    card.write("Sigsyslumi         lnN 1.062  -  -  -  - - - \n")
    card.write('Sigsysbtagsf       lnN '+str(masspointinfo['sysbtagsf'])+'  - - - - - -   \n')
    card.write('Sigsysscale        lnN '+str(masspointinfo['sysscale'])+'  - - - - - -   \n')
    card.write('Sigsyslepsf        lnN '+str(masspointinfo['syslepsf'])+'  - - - - - -   \n')
    card.write('Sigsysmet          lnN '+str(masspointinfo['sysmet'])+'  - - - - - -   \n')
    card.write('Sigsystrig         lnN '+str(masspointinfo['systrig'])+'  - - - - - -   \n')
    card.write('Sigsysjec          lnN '+str(masspointinfo['sysjec'])+'  - - - - - -   \n')
    card.write("MCSyst2ltop        lnN  -  1.20 -  -  - - - \n")
    card.write("MCSystWLF          lnN  -  - 1.20  -  - - - \n")
    card.write("MCSyst1ltop        lnN  -  - - 2.00   - - - \n")
    card.write("MCSystwzbb         lnN  -  - - - 1.30   - - \n")
    card.write("MCSystrare         lnN  -  - - - - 1.50   - \n")
    card.write("MCSystWHF          lnN  -  - - - - - 1.70   \n")

    return 'cards/datacard_'+str(binN)+'_tchwh_'+masspoint+'.txt'
def getgrid():
    grid = [[150, 1], [150, 24], \
    [175, 1], [175, 25], [175, 49], \
    [200, 1], [200, 25], [200, 50], [200, 74], \
    [225, 1], [225, 25], [225, 50], [225, 75], [225, 99], \
    [250, 1], [250, 25], [250, 50], [250, 75], [250, 100], [250, 124], \
    [275, 1], [275, 25], [275, 50], [275, 75], [275, 100], [275, 125], [275, 149], \
    [300, 1], [300, 25], [300, 50], [300, 75], [300, 100], [300, 125], [300, 150], [300, 174], \
    [325, 1], [325, 25], [325, 50], [325, 75], [325, 100], [325, 125], [325, 150], [325, 175], [325, 199], \
    [350, 1], [350, 25], [350, 50], [350, 75], [350, 100], [350, 125], [350, 150], [350, 175], [350, 200], [350, 224], \
    [375, 1], [375, 25], [375, 50], [375, 75], [375, 100], [375, 125], [375, 150], [375, 175], [375, 200], [375, 225], [375, 249], \
    [400, 1], [400, 25], [400, 50], [400, 75], [400, 100], [400, 125], [400, 150], [400, 175], [400, 200], [400, 225], [400, 250], [400, 274], \
    [425, 1], [425, 25], [425, 50], [425, 75], [425, 100], [425, 125], [425, 150], [425, 175], [425, 200], [425, 225], [425, 250], [425, 275], [425, 299], \
    [450, 1], [450, 25], [450, 50], [450, 75], [450, 100], [450, 125], [450, 150], [450, 175], [450, 200], [450, 225], [450, 250], [450, 275], [450, 300], \
    [475, 1], [475, 25], [475, 50], [475, 75], [475, 100], [475, 125], [475, 150], [475, 175], [475, 200], [475, 225], [475, 250], [475, 275], [475, 300], \
    [500, 1], [500, 25], [500, 50], [500, 75], [500, 100], [500, 125], [500, 150], [500, 175], [500, 200], [500, 225], [500, 250], [500, 275], [500, 300], \
    [525, 1], [525, 25], [525, 50], [525, 75], [525, 100], [525, 125], [525, 150], [525, 175], [525, 200], [525, 225], [525, 250], [525, 275], [525, 300], \
    [550, 1], [550, 25], [550, 50], [550, 75], [550, 100], [550, 125], [550, 150], [550, 175], [550, 200], [550, 225], [550, 250], [550, 275], [550, 300], \
    [575, 1], [575, 25], [575, 50], [575, 75], [575, 100], [575, 125], [575, 150], [575, 175], [575, 200], [575, 225], [575, 250], [575, 275], [575, 300], \
    [600, 1], [600, 25], [600, 50], [600, 75], [600, 100], [600, 125], [600, 150], [600, 175], [600, 200], [600, 225], [600, 250], [600, 275], [600, 300], \
    [625, 1], [625, 25], [625, 50], [625, 75], [625, 100], [625, 125], [625, 150], [625, 175], [625, 200], [625, 225], [625, 250], [625, 275], [625, 300], \
    [650, 1], [650, 25], [650, 50], [650, 75], [650, 100], [650, 125], [650, 150], [650, 175], [650, 200], [650, 225], [650, 250], [650, 275], [650, 300], \
    [675, 1], [675, 25], [675, 50], [675, 75], [675, 100], [675, 125], [675, 150], [675, 175], [675, 200], [675, 225], [675, 250], [675, 275], [675, 300], \
    [700, 1], [700, 25], [700, 50], [700, 75], [700, 100], [700, 125], [700, 150], [700, 175], [700, 200], [700, 225], [700, 250], [700, 275], [700, 300], \
    #[126, 1]
    ]
    # need to printout a card called cards/points_TChiWH.txt
    points = open('cards/points_tchwh.txt','w') 
    for point in grid:
        points.write(str('tchwh_'+str(point[0])+'_'+str(point[1]))+'\n')
    return grid
def getsignalscan(signalfile,nzbins):
    # open  files
    histname="h_histscan"
    rootf = TFile(os.environ["analysis_output"]+"/"+signalfile)
    rootf_jecup = TFile(os.environ["analysis_output"]+"/"+signalfile.replace("lnbb","lnbb_jecup"))
    rootf_jecdn = TFile(os.environ["analysis_output"]+"/"+signalfile.replace("lnbb","lnbb_jecdn"))
    # grab 2d histograms with yields.
    scanhist = rootf.Get(histname)
    scanhist_jecup = rootf_jecup.Get(histname)
    scanhist_jecdn = rootf_jecdn.Get(histname)
    scanhist_btagsfup = rootf.Get('h_histscan_btagsfup')
    scanhist_btagsfdn = rootf.Get('h_histscan_btagsfdn')
    scanhist_genmet   = rootf.Get('h_histscan_genmet')
    scanhist_lepsfup  = rootf.Get('h_histscan_lepsfup') 
    scanhist_lepsfdn  = rootf.Get('h_histscan_lepsfdn') 
    scanhist_scaleup  = rootf.Get('h_histscan_scaleup') 
    scanhist_scaledn  = rootf.Get('h_histscan_scaledn') 
    scanhist_trigup  = rootf.Get('h_histscan_trigup') 
    scanhist_trigdn  = rootf.Get('h_histscan_trigdn') 
    
    grid = getgrid() # print out the mass point string. 
    scandicts = [] # make a dictionary for masspoints
    
    for zbin in range(1,nzbins+1):
        scandict={}
        for mass in grid:
           # find the mass points and name for the datacard
            xbin = scanhist.GetXaxis().FindBin(mass[0]) 
            ybin = scanhist.GetYaxis().FindBin(mass[1])         
            namestring=str(mass[0])+'_'+str(mass[1]) 
           # genmet resolution uncertainties.
            recoyield = scanhist.GetBinContent(xbin,ybin,zbin)
            recoerror = scanhist.GetBinError(xbin,ybin,zbin)
            genyield = scanhist_genmet.GetBinContent(xbin,ybin,zbin)
            generror = scanhist_genmet.GetBinError(xbin,ybin,zbin)
            averagedyield = (recoyield+genyield)/2
            averageerror  = sqrt(recoerror*recoerror+generror*generror)/2
           # calculate relative uncertainties
            centralyield = recoyield
            meterror = abs(recoyield-genyield)/2
            sysbtagsf = 0
            syslepsf=0
            sysscale=0
            systrig=0
            sysjec=0
            if centralyield:
               btagup = scanhist_btagsfup.GetBinContent(xbin,ybin,zbin)
               btagdn = scanhist_btagsfdn.GetBinContent(xbin,ybin,zbin)
               sysbtagsf = max(abs(btagup-centralyield)/centralyield,abs(btagdn-centralyield)/centralyield)+1
               lepup = scanhist_lepsfup.GetBinContent(xbin,ybin,zbin) 
               lepdn = scanhist_lepsfdn.GetBinContent(xbin,ybin,zbin) 
               syslepsf = max(abs(lepup-centralyield)/centralyield,abs(lepdn-centralyield)/centralyield) +1
               sysscale = max(scanhist_scaleup.GetBinContent(xbin,ybin)/centralyield,scanhist_scaledn.GetBinContent(xbin,ybin)/centralyield)
               trigup = scanhist_trigup.GetBinContent(xbin,ybin,zbin) 
               trigdn = scanhist_trigdn.GetBinContent(xbin,ybin,zbin) 
               systrig  =max(abs(trigup-centralyield)/centralyield,abs(trigdn-centralyield)/centralyield)+1
               jecup = scanhist_jecup.GetBinContent(xbin,ybin,zbin)
               jecdn = scanhist_jecdn.GetBinContent(xbin,ybin,zbin)
               sysjec = max(abs(jecup-centralyield)/centralyield,abs(jecdn-centralyield)/centralyield)+1 
               scandict[namestring]={'yield': averagedyield, 'stat': recoerror/centralyield+1, 'sysmet':meterror/centralyield+1
                              ,'sysbtagsf':sysbtagsf ,'syslepsf':syslepsf, 'sysscale':sysscale, 'systrig':systrig, 'sysjec':sysjec}
            else:
                 scandict[namestring]={'yield': averagedyield, 'stat': 1, 'sysmet': 1,'sysbtagsf':sysbtagsf ,'syslepsf':syslepsf, 'sysscale':sysscale, 'systrig':systrig, 'sysjec':sysjec}
        scandicts.append(scandict)      
    return scandicts    
    

def combine(cards,masspoint):
    cardstocombine = ''
    for i,card in enumerate(cards):
       cardstocombine = cardstocombine+' ch%s'%(i+1)+'='+card
    cardstocombine = cardstocombine+'>'+"cards/combinedcards/"+masspoint+'.txt&'
    os.system("combineCards.py "+cardstocombine)
    return "cards/combinedcards/"+masspoint+'.txt'

def get_temp_syst(mass_chargino, mass_lsp, in_dict):
    syst_location = "/home/users/siconglu/Run_Directory/CMSSW_8_1_0/src/WH_MET_limitsetting/cards_40fb_v8/"
    syst_list =['sysmet','sysbtagsf' ,'syslepsf', 'sysscale', 'systrig', 'sysjec'] 
    f1 = open(syst_location+"datacard_1_tchwh_%.0f_%.0f.txt"%(mass_chargino, mass_lsp),"r")
    for line in f1:
        for syst in syst_list:
            if not(syst in line): continue;
            nums = line.split(" ")
            nums = [item for item in nums if not(item == "")]
            value = float(nums[2])
            if in_dict[syst]<value:
                in_dict[syst] = value
    f1.close()
    f2 = open(syst_location+"datacard_2_tchwh_%.0f_%.0f.txt"%(mass_chargino, mass_lsp),"r")
    for line in f2:
        for syst in syst_list:
            if not(syst in line): continue;
            nums = line.split(" ")
            nums = [item for item in nums if not(item == "")]
            value = float(nums[2])
            if in_dict[syst]<value:
                in_dict[syst] = value
    return in_dict    
        
    
    
def str2yield(tmp_str):
    num_list = tmp_str.split(" +- ")
    num_yield = float(num_list[0])
    num_stats = float(num_list[1])
    #Need to scale it by luminosity
    num_yield = num_yield*(lumi/35.9)
    num_stats = num_stats*(lumi/35.9)
    
    return num_yield, num_stats
def test_get_scan(yield_file, SR_list = ["SR1", "SR2"]):
    '''Directly read data from csv.'''
    backgrounds = {'2l':[],'1l':[],'1ltop':[],'wzbb':[],'rare':[]}
    errors = {'2l':[],'1l':[],'1ltop':[],'wzbb':[],'rare':[]}
    
    df = pd.read_csv(yield_file)
    bkg_row_name = {"2l":"2l top", "1ltop":"1l top", "1l":"W+LF/W+HF", "wzbb":"WZ","rare":"rare"}#,"data":"data"
    bkg_list = bkg_row_name.keys()
    for SR in SR_list: #For each signal region
        for bkg in bkg_list: #For each background category
            tmp_str = df[SR][df[' '] == bkg_row_name[bkg]].values[0]
            y, s = str2yield(tmp_str)
            if y != 0:
                s = 1.0*s/y+1
            else:
                s = 1.0+s
            backgrounds[bkg].append(y)
            errors[bkg].append(s)
    zero_list = [0 for i in range(len(errors['1l']))] #1l now includes both W+LF/W+HF
    backgrounds['1lH'],errors['1lH'] = zero_list, zero_list #manually add it... 
    
    grid = getgrid()
    scandicts = []
    for SR in SR_list: #For each signal region
        scandict = {}
        for mass in grid:
            mass_chargino = mass[0]
            mass_lsp = mass[1]
            MC_name = "(%.0f, %.0f)"%(mass_chargino,mass_lsp)
            tmp_str = df[SR][df[' '] == MC_name].values[0]
            
            y, s = str2yield(tmp_str)
            if y != 0:
                s = 1.0*s/y+1
            else:
                s = 1.0+s
            namestring=str(mass[0])+'_'+str(mass[1])
            scandict[namestring]={'yield': y, 'stat': s, 'sysmet': 0,'sysbtagsf':0 ,'syslepsf':0, 'sysscale':0, 'systrig':0, 'sysjec':0}
            scandict[namestring] = get_temp_syst(mass_chargino, mass_lsp, scandict[namestring])
            
        scandicts.append(scandict)
    
    print 'got backgrounds:', backgrounds
    print errors
    
    return scandicts, backgrounds,errors
import sys
if __name__ == "__main__":
   # specify selection here to get a set of backgrounds
   version='0'
   lumi_str = sys.argv[1]
   date_str = sys.argv[2]
   SR_list = sys.argv[3:]
   
   global lumi
   lumi = float(lumi_str.replace("p","."))
   new_cate_str = lumi_str
   for SR in SR_list:
       new_cate_str+="_"+SR
   print(lumi, date_str, SR_list)
   print(new_cate_str)
   
   zbins = len(SR_list)
   selection=""
   carddir = "../../Run_Directory/CMSSW_8_1_0/src/WH_MET_limitsetting/cards_"+new_cate_str+"_"+date_str+"/"#%version#_3jets
   yield_file = "../Analysis_Code/table_of_yield_04_12_sub.csv"
   yield_file = "../Analysis_Code/table_of_yield_07_06_MET_binning.csv"
   #yield_file = "../Analysis_Code/table_of_yield_04_26_SR_lumi_80fb.csv"
   scandicts, bkgs,err = test_get_scan(yield_file, SR_list = SR_list)
 
   # output directory for cards
    ### check if output cards exist
   if os.path.isdir(carddir): 
       overwritedir = raw_input("cards directory already exist, overwrite? (y/n)")
       if overwritedir is "y":
          print "will overwrite cards in "+carddir
       else:
          dirname = raw_input("name the output directory for cards")
          if dirname is not carddir:
             os.mkdir(dirname)
   else: 
       os.mkdir(carddir)
       print "will save cards in %s"%carddir

   cards = []
   sys ={'stat':[] , 'sysscale':[] , 'yield':[] , 'sysbtagsf':[] , 'syslepsf': [], 'sysmet':[],'systrig':[],'sysjec':[]} 

   for zbin in range(1,zbins+1):
       print zbin
       for k,kinfo in scandicts[zbin-1].items():
           card = printcard(k,kinfo,zbin,bkgs,err,SR_list[zbin-1],carddir)
