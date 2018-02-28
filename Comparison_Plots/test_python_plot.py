import sys
sys.path.insert(0, '/home/users/siconglu/CMSTAS/software/dataMCplotMaker/')
import dataMCplotMaker
import ROOT

h_data = ROOT.TH1F("data", "", 7, 0, 7)
h_wz = h_data.Clone("wz")
h_ttz = h_data.Clone("ttz")

h_wz.FillRandom("gaus",5)
h_ttz.FillRandom("gaus",10)

for i in range(10): h_data.Fill(0)
for i in range(2): h_data.Fill(1)

d_opts = {
        "poissonErrorsNoZeros": True,
        "lumi": 36.8,
        "outputName": "plots/test.pdf",
        "xAxisLabel": "Njets",
        "noXaxisUnit": True,
        "percentageInBox": True,
        "isLinear": True,
        "legendUp": -0.15,
        "legendRight": -0.08,
        "outOfFrame": True,
        "legendTaller": 0.15,
        "yTitleOffset": -0.5,
        "type": "Internal",
        "noGrass": True,
        "darkColorLines": True,
        "makeTable": True,
        "makeJSON": True,
        "flagLocation": "0.5,0.7,0.15", # add a US flag because 'merica
        }

dataMCplotMaker.dataMCplot(h_data, bgs=[h_wz,h_ttz], titles=["WZ","t#bar{t}Z"], title="test", colors=[ROOT.kGreen+2,ROOT.kBlue-1], opts=d_opts)
os.system("ic " + d_opts["outputName"])