from ROOT import TFile,TTree,TH1D,TCanvas,TChain,TLegend,TCut,TPad
from ROOT import gStyle,gSystem,gDirectory

#gSystem.Load("libFWCoreFWLite")

def SetCutOption(n,l_cut) :

    for i in range(0,5) :
        l_cut.append(TCut("GenEventInfoProduct_generator__GEN.obj.nMEPartons()=={}".format(i)))
 
    if n == 0 :   # NLO with FxFx merging
        for i in range(0,len(l_cut)) :
            l_cut[i] = TCut("LHEEventProduct_externalLHEProducer__GEN.obj.npNLO()=={}".format(i))
    elif n == 1 : # LO with MLM ; default
        for i in range(0,len(l_cut)) :
            l_cut[i] = TCut("LHEEventProduct_externalLHEProducer__GEN.obj.nMEPartons()=={}".format(i))
    elif n == 2 : # LO with MLM ; exclusing wbb/vbf type 
        for i in range(0,len(l_cut)) :
            l_cut[i] = TCut("LHEEventProduct_externalLHEProducer__GEN.obj.nMEPartonsFiltered()=={}".format(i)) 

#initialize 

tree = TChain("Events")
tree.Add("test.root")

l_cut = [] 
SetCutOption(1,l_cut) # check option for FxFx/MLM

#tree.SetAlias("GenEvent","GenEventInfoProduct_generator__GEN.obj")
#tree.SetAlias("LHEEvent","LHEEventProduct_externalLHEProducer__GEN.obj")

weight = TCut("GenEventInfoProduct_generator__GEN.obj.weight()")
output = TFile("output.root","RECREATE")

for i in range(0,5) : 
    output.cd()
    output.mkdir("djr{}{}".format(i,i+1))

output.cd()

#save histos to another root file

for i in range(0,5) :
    output.cd("djr{}{}".format(i,i+1))
    tmp_all = TH1D("all","",50,-0.5,3)
    tree.Draw("log10(GenEventInfoProduct_generator__GEN.obj.DJRValues_[{}])>>all".format(i),weight,"goff")
    tmp_all = gDirectory.Get("all")
    tmp_all.Write()
    for j in range(0,5) : 
        tmp = TH1D("djr{}".format(j),"",50,-0.5,3)
        tree.Draw("log10(GenEventInfoProduct_generator__GEN.obj.DJRValues_[{}])>>djr{}".format(i,j),weight*l_cut[j],"goff")
        tmp = gDirectory.Get("djr{}".format(j))
        tmp.Write()
        

output.Close()
