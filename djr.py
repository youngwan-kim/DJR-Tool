from ROOT import TFile,TTree,TH1D,TCanvas,TChain,TLegend,TCut,TPad
from ROOT import gStyle,gSystem

l_hmult = []

def setcanvas(c1,pad) :

    c1.SetLeftMargin(0.0)
    c1.SetTopMargin(0.0)
    c1.SetRightMargin(0.0)
    c1.SetBottomMargin(0.0)

    pad.append(TPad("pad0","pad",0,0.67,0.5,1.0))
    pad.append(TPad("pad1","pad",0.5,0.67,1.0,1.0))
    pad.append(TPad("pad2","pad",0,0.33,0.5,0.67))
    pad.append(TPad("pad3","pad",0.5,0.33,1.0,0.67))
    pad.append(TPad("pad4","pad",0.,0.,0.5,0.33))

    for i in range(0,5) :
        pad[i].Draw()


def setLegend(legend, hall, l_hmult) :

    legend.SetTextSize(0.050)
    legend.SetBorderSize(0)
    legend.SetTextFont(62)
    legend.SetLineColor(0)
    legend.SetLineStyle(1)
    legend.SetLineWidth(1)
    legend.SetFillColor(0)
    legend.SetFillStyle(1001)

    legend.AddEntry(hall,"all partons")

    for i in range(0,len(l_hmult)) :
        legend.AddEntry(l_hmult[i],"{} partons".format(i))

def setMultiColor(l_hmult) :
    l_hmult[0].SetLineColor(600)
    l_hmult[1].SetLineColor(629)
    l_hmult[2].SetLineColor(419)
    l_hmult[3].SetLineColor(810)
    l_hmult[4].SetLineColor(30)

def setHists(l_hmult,name) :

    for i in range(0,5) :
        l_hmult.append(TH1D("hmult{}_{}".format(i,name),"",nbins,xlow,xhigh))
        l_hmult[i].SetLineStyle(2)

def makeplot(name, tree, weight, drawstring, xlabel, nbins, xlow, xhigh, typeMC) :

    l_mult = []
    for i in range(0,5) :
        l_mult.append(TCut("GenEvent.nMEPartons()=={}".format(i)))
 
    if typeMC == 0 :   # NLO with FxFx merging
        for i in range(0,len(l_mult)) :
            l_mult[i] = TCut("LHEEvent.npNLO()=={}".format(i))
    elif typeMC == 1 : # LO with MLM ; default
        for i in range(0,len(l_mult)) :
            l_mult[i] = TCut("GenEvent.nMEPartons()=={}".format(i))
    elif typeMC == 2 : # LO with MLM ; exclusing wbb/vbf type 
        for i in range(0,len(l_mult)) :
            l_mult[i] = TCut("LHEEvent.nMEPartonsFiltered()=={}".format(i))
    
    hall = TH1D("hall_{}".format(name),"",nbins,xlow,xhigh)
    
    #setHists(l_hmult,name)
    for i in range(0,5) :
        l_hmult.append(TH1D("hmult{}_{}".format(i,name),"",nbins,xlow,xhigh))
        l_hmult[i].SetLineStyle(2)

    hall.SetLineColor(921) ; hall.SetLineWidth(2) 
    setMultiColor(l_hmult)

    tree.Draw("{}>>{}".format(drawstring,hall.GetName()),weight,"goff")
    for i in range(0,5) :
        tree.Draw("{}>>{}".format(drawstring,l_hmult[i].GetName()),weight*l_mult[i],"goff")

    hall.GetXaxis().SetTitle(xlabel)
    legend = TLegend(0.67,0.87-4*0.06,0.87,0.87)
    setLegend(legend,hall,l_hmult)

    hall.Draw("e&hist")
    for i in range(0,5) :
        l_hmult[i].Draw("e&hist&same")

    gStyle.SetOptStat(0)
    legend.Draw()

def plotdjr(infile, printfile) :

    gSystem.Load("libFWCoreFWLite.so")

    tree = TChain("Events")
    tree.Add(infile)

    tree.SetAlias("GenEvent","GenEventInfoProduct_generator__GEN.obj")
    tree.SetAlias("LHEEvent","LHEEventProduct_externalLHEProducer__GEN.obj")

    weight = TCut("GenEvent.weight()")
    nbins = 50 ; djrmin = -0.5 ; djrmax = 3 
    typeMC = 1 

    c1 = TCanvas("c1","c1",800,600)
    pad = []
    setcanvas(c1,pad)

    for i in range(0,5) :
        pad[i].cd()
        makeplot("djr{}".format(i),tree,weight,
                 "log10(GenEvent.DJRValues_[{}])".format(i),
                 "DJR {}->{}".format(i,i+1),nbins,djrmin,djrmax,typeMC)
    
    c1.Print(printfile)


plotdjr("DJR_Q30v2.root","test.pdf")
                  


    





    



