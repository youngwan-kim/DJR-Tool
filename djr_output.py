from ROOT import TFile,TTree,TH1D,TCanvas,TChain,TLegend,TCut,TPad
from ROOT import gStyle,gSystem,gDirectory
import os

gSystem.Load("libFWCoreFWLite")

def getDirNum(directory) :
    return directory.rsplit("/",1)[1].split("_")[1]

def SetCutOption(n,l_cut) :

    for i in range(0,5) :
        l_cut.append(TCut("GenEvent.nMEPartons()=={}".format(i)))

    if n == 0 :   # NLO with FxFx merging
        for i in range(0,len(l_cut)) :
            l_cut[i] = TCut("LHEEvent.npNLO()=={}".format(i))
    elif n == 1 : # LO with MLM ; default
        for i in range(0,len(l_cut)) :
            l_cut[i] = TCut("GenEvent.nMEPartons()=={}".format(i))
    elif n == 2 : # LO with MLM ; exclusing wbb/vbf type
        for i in range(0,len(l_cut)) :
            l_cut[i] = TCut("LHEEvent.nMEPartonsFiltered()=={}".format(i))

#initialize

tree = TChain("Events")
tree.Add("genVal.root")

l_cut = [] ; l_histo = []
SetCutOption(1,l_cut) # check option for FxFx/MLM
makeHistoList(l_histo)

tree.SetAlias("GenEvent","GenEventInfoProduct_generator__GEN.obj")
tree.SetAlias("LHEEvent","LHEEventProduct_externalLHEProducer__GEN.obj")

weight = TCut("GenEvent.weight()")
output = TFile("DJR_output_{}.root".format(getDirNum(os.getcwd())),"RECREATE")

for i in range(0,5) :
    output.cd()
    output.mkdir("djr{}{}".format(i,i+1))

output.cd()

#save histos to another root file

for i in range(0,5) :
    output.cd("djr{}{}".format(i,i+1))
    tmp_all = TH1D("all","",50,-0.5,3)
    tree.Draw("log10(GenEvent.DJRValues_[{}])>>all".format(i),weight,"goff")
    tmp_all = gDirectory.Get("all")
    tmp_all.Write()
    for j in range(0,5) :
        tmp = TH1D("djr{}".format(j),"",50,-0.5,3)
        tree.Draw("log10(GenEvent.DJRValues_[{}])>>djr{}".format(i,j),weight*l_cut[j],"goff")
        tmp = gDirectory.Get("djr{}".format(j))
        tmp.Write()


output.Close()
