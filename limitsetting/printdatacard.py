# get number of yields in a bin
# print out data card
from ROOT import TH1F,TFile,TH3D
import os

#def printcard(masspoint,masspointinfo,binN,backgrounds,errors,selection):
def printcard(masspoint,binN,backgrounds,errors,selection):
    sigN,sigE = grabnumber(os.environ["analysis_output"]+'/wh_'+masspoint+'_'+selection+'_hists.root','h_lep_event_NEventsSROneBin_'+selection)
   # sigN,sigE = masspointinfo['yield'], masspointinfo['stat']  
    card = open('cardsop/datacard_tchwh_'+masspoint+'_'+str(binN)+'.txt','w')

    card.write("imax  1  number of channels\n")
    card.write("jmax  6  number of backgrounds\n")
    card.write("kmax  14  number of nuisance parameters\n")
    card.write("------------\n")
    card.write("# observations\n")
    card.write("bin        "+str(binN)+'\n')
    card.write("observation  " + str(9)+'\n')
    card.write("#now we list all expected number of events\n")
    bintoprint = str(binN)+' '
    card.write("bin "+7*bintoprint+'\n')
    card.write("process     sig       2l       1l       1ltop       wzbb   rare 1lH \n")
    card.write("process      0        1         2         3          4      5    6\n")
    binI = binN-1
    #card.write("rate " +str(sigN) +' ' + str(backgrounds['2l'][binI]) +' ' + str(backgrounds['1l'][binI])+' ' + str(backgrounds['1ltop'][binI])+' ' + str(backgrounds['wzbb'][binI])+' ' + str(backgrounds['rare'][binI])+ " "+str(backgrounds['1lH'][binI]))
    card.write("rate " +str(sigN[binI]) +' ' + str(backgrounds['2l'][binI]) +' ' + str(backgrounds['1l'][binI])+' ' + str(backgrounds['1ltop'][binI])+' ' + str(backgrounds['wzbb'][binI])+' ' + str(backgrounds['rare'][binI])+ " "+str(backgrounds['1lH'][binI]))
    card.write("\n------------\n")
    #card.write("SigStat"    +str(binI)+"  lnN " +str(sigE)+' - - - - - -\n')
    card.write("SigStat"    +str(binI)+"  lnN " +str(sigE[binI])+' - - - - - -\n')
    card.write("Bg2lStat"   +str(binI)+"  lnN - " +str(errors['2l'][binI])+'  -  -  -  - - \n')
    card.write("Bg1lStat"   +str(binI)+"  lnN - - " +str(errors['1l'][binI])+'   -  -  - - \n')
    card.write("Bg1ltopStat"+str(binI)+"  lnN - -  - " +str(errors['1ltop'][binI])+' -  - - \n')
    card.write("BgwzbbStat" +str(binI)+"  lnN - -  -  - " +str(errors['wzbb'][binI])+' - - \n')
    card.write("BgrareStat" +str(binI)+"  lnN - -  -  -  - " +str(errors['rare'][binI])+' - \n')
    card.write("Bg1lHStats" +str(binI)+"  lnN - -  -  -  -  - " +str(errors['1lH'][binI])+' \n')
    card.write("MCSystSig       lnN 1.15  -  -  -  - - - \n")
    card.write("MCSyst2l        lnN  -  1.30 -  -  - - - \n")
    card.write("MCSyst1l        lnN  -  - 1.20  -  - - - \n")
    card.write("MCSyst1ltop     lnN  -  - - 2.00   - - - \n")
    card.write("MCSystwzbb      lnN  -  - - - 1.30   - - \n")
    card.write("MCSystrare      lnN  -  - - - - 2.00   - \n")
    card.write("MCSyst1lH       lnN  -  - - - - - 1.70   \n")
    return 'cardsop/datacard_tchwh_'+masspoint+'_'+str(binN)+'.txt'

def getgrid():
    # this is just copied from a printout obtained from python grid.py
    grid = [[150, 1], [150, 24], [175, 1], [175, 25], [175, 49], [200, 1], [200, 25], [200, 50], [200, 74], [225, 1], [225, 25], [225, 50], [225, 75], [225, 99], [250, 1], [250, 25], [250, 50], [250, 75], [250, 100], [250, 124], [275, 1], [275, 25], [275, 50], [275, 75], [275, 100], [275, 125], [275, 149], [300, 1], [300, 25], [300, 50], [300, 75], [300, 100], [300, 125], [300, 150], [300, 174], [325, 1], [325, 25], [325, 50], [325, 75], [325, 100], [325, 125], [325, 150], [325, 175], [325, 199], [350, 1], [350, 25], [350, 50], [350, 75], [350, 100], [350, 125], [350, 150], [350, 175], [350, 200], [350, 224], [375, 1], [375, 25], [375, 50], [375, 75], [375, 100], [375, 125], [375, 150], [375, 175], [375, 200], [375, 225], [375, 249], [400, 1], [400, 25], [400, 50], [400, 75], [400, 100], [400, 125], [400, 150], [400, 175], [400, 200], [400, 225], [400, 250], [400, 274], [425, 1], [425, 25], [425, 50], [425, 75], [425, 100], [425, 125], [425, 150], [425, 175], [425, 200], [425, 225], [425, 250], [425, 275], [425, 299], [450, 1], [450, 25], [450, 50], [450, 75], [450, 100], [450, 125], [450, 150], [450, 175], [450, 200], [450, 225], [450, 250], [450, 275], [450, 300], [475, 1], [475, 25], [475, 50], [475, 75], [475, 100], [475, 125], [475, 150], [475, 175], [475, 200], [475, 225], [475, 250], [475, 275], [475, 300], [500, 1], [500, 25], [500, 50], [500, 75], [500, 100], [500, 125], [500, 150], [500, 175], [500, 200], [500, 225], [500, 250], [500, 275], [500, 300], [525, 1], [525, 25], [525, 50], [525, 75], [525, 100], [525, 125], [525, 150], [525, 175], [525, 200], [525, 225], [525, 250], [525, 275], [525, 300], [550, 1], [550, 25], [550, 50], [550, 75], [550, 100], [550, 125], [550, 150], [550, 175], [550, 200], [550, 225], [550, 250], [550, 275], [550, 300], [575, 1], [575, 25], [575, 50], [575, 75], [575, 100], [575, 125], [575, 150], [575, 175], [575, 200], [575, 225], [575, 250], [575, 275], [575, 300], [600, 1], [600, 25], [600, 50], [600, 75], [600, 100], [600, 125], [600, 150], [600, 175], [600, 200], [600, 225], [600, 250], [600, 275], [600, 300], [625, 1], [625, 25], [625, 50], [625, 75], [625, 100], [625, 125], [625, 150], [625, 175], [625, 200], [625, 225], [625, 250], [625, 275], [625, 300], [650, 1], [650, 25], [650, 50], [650, 75], [650, 100], [650, 125], [650, 150], [650, 175], [650, 200], [650, 225], [650, 250], [650, 275], [650, 300], [675, 1], [675, 25], [675, 50], [675, 75], [675, 100], [675, 125], [675, 150], [675, 175], [675, 200], [675, 225], [675, 250], [675, 275], [675, 300], [700, 1], [700, 25], [700, 50], [700, 75], [700, 100], [700, 125], [700, 150], [700, 175], [700, 200], [700, 225], [700, 250], [700, 275], [700, 300], [126, 1]]
    # need to printout a card called cards/points_TChiWH.txt
    points = open('cardsop/points_tchwh.txt','w') 
    for point in grid:
        points.write(str('tchwh_'+str(point[0])+'_'+str(point[1]))+'\n')
    return grid


def getsignalscan():
    histname="h_histscan"
    rootf = TFile(os.environ["analysis_output"]+"/SMS_tchwh_lnbb_SMS_SR_met100_mt150_mbb_mct150_twobtag_hists.root")
    scanhist = rootf.Get(histname)
    
    grid = getgrid() # print out the mass point string. 
    scandict = {} # make a dictionary for masspoints

    for mass in grid:
        xbin = scanhist.GetXaxis().FindBin(mass[0]) 
        ybin = scanhist.GetYaxis().FindBin(mass[1]) 
        string=str(mass[0])+'_'+str(mass[1])
        scandict[string]={'yield': scanhist.GetBinContent(xbin,ybin), 'stat': scanhist.GetBinError(xbin,ybin)} 
    return scandict   
 
def getsignalscanmultibin(bin,selection):
    histname="h_histscan"
    filename = "SMS_tchwh_lnbb_"+selection+"_hists.root"
    rootf = TFile(os.environ["analysis_output"]+"/"+filename)
    scanhist = rootf.Get(histname)
    
    grid = getgrid() # print out the mass point string. 
    scandict = {} # make a dictionary for masspoints

    for mass in grid:
        xbin = scanhist.GetXaxis().FindBin(mass[0]) 
        ybin = scanhist.GetYaxis().FindBin(mass[1]) 
        string=str(mass[0])+'_'+str(mass[1])
        scandict[string]={'yield': scanhist.GetBinContent(xbin,ybin,bin), 'stat': scanhist.GetBinError(xbin,ybin,bin)} 
         
def getbackgrounds(selection):  #hardcoded for WH
    hist_prefix = 'h_lep_event_NEventsSROneBin_'+selection
    backgrounds = {'2l':[],'1l':[],'1ltop':[],'wzbb':[],'rare':[]}
    errors = {'2l':[],'1l':[],'1ltop':[],'wzbb':[],'rare':[]}
    print "using inputs from:",os.environ["analysis_output"]
    backgrounds['2l'],errors['2l'] = grabnumber(os.environ["analysis_output"]+'/'+'tops_mad_'+selection+'_hists.root', hist_prefix.replace('lep','lep_dilep'))    
    backgrounds['1ltop'],errors['1ltop'] = grabnumber(os.environ["analysis_output"]+'/'+'tops_mad_'+selection+'_hists.root', hist_prefix.replace('lep','lep_onelep'))    
    backgrounds['1l'],errors['1l'] = grabnumber(os.environ["analysis_output"]+'/'+'ws_stitch_'+selection+'_hists.root',hist_prefix.replace('lep','lep_LF'))
    backgrounds['wzbb'],errors['wzbb'] = grabnumber(os.environ["analysis_output"]+'/'+'wzbb_'+selection+'_hists.root',hist_prefix)
    backgrounds['rare'],errors['rare'] = grabnumber(os.environ["analysis_output"]+'/'+'rare_'+selection+'_hists.root',hist_prefix)
    backgrounds['1lH'],errors['1lH'] = grabnumber(os.environ["analysis_output"]+'/'+'ws_stitch_'+selection+'_hists.root',hist_prefix.replace('lep','lep_HF'))
    print 'got backgrounds:', backgrounds
    print errors
    return backgrounds,errors
 
def grabnumber(filename,histname):
    rootf = TFile(filename)
    hist = rootf.Get(histname)
    contents = []
    errors = []

    for i in range(4):
        if(hist.GetBinContent(i+1)>0):contents.append(hist.GetBinContent(i+1)) 
        else:contents.append(0)
        if(hist.GetBinContent(i+1)>0):error = float(1+(hist.GetBinError(i+1)/hist.GetBinContent(i+1)))
        else: error = 0
        errors.append(error)
    return contents,errors

def combine(cards,masspoint):
    cardstocombine = ''
    for i,card in enumerate(cards):
       cardstocombine = cardstocombine+' ch%s'%(i+1)+'='+card
    cardstocombine = cardstocombine+'>'+"cards/combinedcards/"+masspoint+'.txt&'
    os.system("combineCards.py "+cardstocombine)
    return "cardsop/combinedcards/"+masspoint+'.txt'

def getSig(card):
    os.system("combine -M ProfileLikelihood --significance datacard.txt -t -1 --expectSignal=1".replace("datacard.txt",card))

def getLimit(card):
    os.system("combine -M Asymptotic --noFitAsimov datacard.txt".replace("datacard.txt",card))  
#    os.system(" ".replace("datacard.txt",card))  
    print "for masspoint:",card 

if __name__ == "__main__":
   #selection="SR_SROneBin_yield_mbb_mct150_mt150_met100_twobtag"
   selection="SR_SROneBin_yield_mbb_mct150_mt150_met100_twobtag"
   bkgs,err = getbackgrounds(selection) 
#   scandict = getsignalscan()
#
   cards = []
      
#   for k,kinfo in scandict.items():
#       card = printcard(k,kinfo,1,bkgs,err,selection)

#       cards.append(printcard(k,kinfo,1,bkgs,err,selection))
#       getLimit(card)
   masspoints = ["250_1","225_80","350_1","300_80"]
   for masspoint in masspoints:
       cards.append(printcard(masspoint,1,bkgs,err,selection))
   #    cards.append(printcard(masspoint,3,bkgs,err,selection))
   #    cards.append(printcard(masspoint,4,bkgs,err,selection))
#       card = combine(cards,masspoint) 
#       cards[:] = [] # empty the list of cards
#       getSig(card)
