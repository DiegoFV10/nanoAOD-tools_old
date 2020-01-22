import ROOT
import math
from array import array
from PhysicsTools.NanoAODTools.postprocessing.tools import *
from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection, Object, Event
from PhysicsTools.NanoAODTools.postprocessing.framework.treeReaderArrayTools import *
from PhysicsTools.NanoAODTools.postprocessing.framework.preskimming import preSkim
print "PhysicsTools implemented"

from preliminary_tools import *
print "Agostino's tools implemented"

from topreco import *
print "Andrea's tools implemented"

inputpath = "/eos/home-a/adeiorio/Wprime/nosynch/"
inpfiles = ["Wprime_4000_RH"
            #,"TT_Mtt-700to1000"
            #,"WJets"
            #,"QCD_Pt_600to800_1"
            #,"SingleMuon_Run2016G_1"
]

print "input pathed"



#ROOT.gROOT.SetStyle('Plain')
#ROOT.gStyle.SetPalette(1)   
ROOT.gStyle.SetOptStat(0)
ROOT.gROOT.SetBatch()        # don't pop up canvases
ROOT.TH1.SetDefaultSumw2()
#ROOT.TGaxis.SetMaxDigits(3)
print "root setted"

def bjet_filter(jets): #returns a collection of only b-gen jets (to use only for MC samples)
    return list(filter(lambda x : x.partonFlavour == -5 or x.partonFlavour == 5, jets))

def sameflav_filter(jets, flav): #returns a collection of only b-gen jets (to use only for MC samples)
    return list(filter(lambda x : x.partonFlavour == flav, jets))

HLTrig = True
for inpfile in inpfiles:
    filetoopen = inputpath + inpfile
    infile = ROOT.TFile.Open(filetoopen + ".root")
    tree = InputTree(infile.Events)
    print '%s opened' %(filetoopen)
    
    #histo booking
    nbins_edges = 15
    nbins = 60
    nmin = 0
    nmax = 2400
    wnbins = 80
    wnmin = 0
    wnmax = 10000
    
    #edges = array('f',[0., 20., 40., 60., 80., 100., 130., 160., 190., 230., 270., 320., 360., 400., 700., 1000.])
    
    h_mclepton_pt = {'electron': ROOT.TH1F("MC_Electron_pt", "MC_Electron_pt", nbins, nmin, nmax),
                     'muon': ROOT.TH1F("MC_Muon_pt", "MC_Muon_pt", nbins, nmin, nmax)
                     }
    
    h_mclepton_eta = {'electron': ROOT.TH1F("MC_Electron_eta", "MC_Electron_eta", nbins, nmin, nmax),
                      'muon': ROOT.TH1F("MC_Muon_eta", "MC_Muon_eta", nbins, nmin, nmax)
                      }
    h_mcbjet_pt = {'Wbjet_ev2': ROOT.TH1F("MC_ev2_Wbjet_pt", "MC_ev2_Wbjet_pt", nbins, nmin, nmax),
                   'topbjet_ev2': ROOT.TH1F("MC_ev2_topbjet_pt", "MC_ev2_topbjet_pt", nbins, nmin, nmax),
                   'Wbjet': ROOT.TH1F("MC_Wbjet_pt", "MC_Wbjet_pt", nbins, nmin, nmax),
                   'topbjet': ROOT.TH1F("MC_topbjet_pt", "MC_topbjet_pt", nbins, nmin, nmax)
                   }
    h_mcWprime_mass = {'all': ROOT.TH1F("Lep_MC_Wprime_mass", "Lep_MC_Wprime_mass", wnbins, wnmin, wnmax),
                       'ev2': ROOT.TH1F("Lep_MC_ev2_Wprime_mass", "Lep_MC_ev2_Wprime_mass", wnbins, wnmin, wnmax),
                       'ele_all': ROOT.TH1F("Ele_MC_Wprime_mass", "Ele_MC_Wprime_mass", wnbins, wnmin, wnmax),
                       'ele_ev2': ROOT.TH1F("Ele_MC_ev2_Wprime_mass", "Ele_MC_ev2_Wprime_mass", wnbins, wnmin, wnmax),
                       'mu_all': ROOT.TH1F("Mu_MC_Wprime_mass", "Mu_MC_Wprime_mass", wnbins, wnmin, wnmax),
                       'mu_ev2': ROOT.TH1F("Mu_MC_ev2_Wprime_mass", "Mu_MC_ev2_Wprime_mass", wnbins, wnmin, wnmax)
                       }
    h_mcWprime_tmass = {'all': ROOT.TH1F("Lep_MC_Wprime_transverse_mass", "Lep_MC_Wprime_transverse_mass", wnbins, wnmin, wnmax),
                       'ev2': ROOT.TH1F("Lep_MC_ev2_Wprime_transverse_mass", "Lep_MC_ev2_Wprime_transverse_mass", wnbins, wnmin, wnmax),
                       'ele_all': ROOT.TH1F("Ele_MC_Wprime_transverse_mass", "Ele_MC_Wprime_transverse_mass", wnbins, wnmin, wnmax),
                       'ele_ev2': ROOT.TH1F("Ele_MC_ev2_Wprime_transverse_mass", "Ele_MC_ev2_Wprime_transverse_mass", wnbins, wnmin, wnmax),
                       'mu_all': ROOT.TH1F("Mu_MC_Wprime_transverse_mass", "Mu_MC_Wprime_transverse_mass", wnbins, wnmin, wnmax),
                       'mu_ev2': ROOT.TH1F("Mu_MC_ev2_Wprime_transverse_mass", "Mu_MC_ev2_Wprime_transverse_mass", wnbins, wnmin, wnmax)
                       }
    h_sameflav_bjet_deltaR = ROOT.TH1F("Same_Flavour_bjet_DeltaR", "Same_Flavour_bjet_DeltaR", 80, 0, 4)
    h_met_q = {'pt': ROOT.TH1F("met_ptransv", "MET_pt", nbins, nmin, nmax),
               'Et': ROOT.TH1F("met_Etransv", "MET_Et", 100, 0, 4000),
             'phi': ROOT.TH1F("met_ptransv", "MET_phi", 80, 0, 4),
             'pt_ev2': ROOT.TH1F("met_pt_ev2", "MET_pt_ev2", nbins, nmin, nmax),
             'Et_ev2': ROOT.TH1F("met_Et_ev2", "MET_Et_ev2", 100, 0, 4000),
             'phi_ev2': ROOT.TH1F("met_pt_ev2", "MET_phi_ev2", 80, 0, 4)
             }
    if not HLTrig:
        for value in h_mclepton_pt.values():
            old_title = value.GetTitle()
            old_name = value.GetName()
            new_title = 'unHLT_' + old_title
            new_name = 'unHLT_' + old_name
            value.SetTitle(new_title)
            value.SetName(new_name)
        for value in h_mclepton_eta.values():
            old_title = value.GetTitle()
            old_name = value.GetName()
            new_title = 'unHLT_' + old_title
            new_name = 'unHLT_' + old_name
            value.SetTitle(new_title)
            value.SetName(new_name)
        for value in h_mcbjet_pt.values():
            old_title = value.GetTitle()
            old_name = value.GetName()
            new_title = 'unHLT_' + old_title
            new_name = 'unHLT_' + old_name
            value.SetTitle(new_title)
            value.SetName(new_name)
            old_title = value.GetTitle()
        for value in h_mcWprime_mass.values():
            old_title = value.GetTitle()
            old_name = value.GetName()
            new_title = 'unHLT_' + old_title
            new_name = 'unHLT_' + old_name
            value.SetTitle(new_title)
            value.SetName(new_name)
            
    #preselection
    badflag = 0
    badevt = 0
    HLTriggered = 0
    LepTriggered = 0
    JetTriggered = 0
    m2bjetev = 0
    nmctruth_ev = 0
    nentries = tree.GetEntries()
    print 'n entries: %i' %(nentries)

    for i in xrange(0,tree.GetEntries()):
        last = False

        if i == (nentries-1):
            last = True
        
        event = Event(tree,i)
        electrons = Collection(event, "Electron")
        muons = Collection(event, "Muon")
        jets = Collection(event, "Jet")
        fatjets = Collection(event, "FatJet")
        genpart = Collection(event, "GenPart")
        PV = Object(event, "PV")
        met = Object(event, "MET")
        HLT = Object(event, "HLT")
        Flag = Object(event, 'Flag')
        #it will be an ele or a muon, use isEle and isMu to recover lepton flavour
        lepton = None
        lepton_p4 = None
        mclepton = None
        mclepton_p4 = None
        MET = {'metPx': met.pt*ROOT.TMath.Cos(met.phi),
               'metPy': met.pt*ROOT.TMath.Sin(met.phi)
           }

        if last:
            print 'all object extracted'

        if not pass_MET(Flag):
            badflag += 1
            continue

        goodEvt, isMu, isEle = presel(PV, muons, electrons, jets)

        if goodEvt and isMu and isEle:
            #print str(goodEvt) + ' ' + str(isMu) + ' ' + str(isEle)
            print 'presel algo not properly working here'
            continue
        
        if not goodEvt:
            badevt += 1
            continue

        #HLTriggering + mclepton finding
        if isMu:
            if HLTrig and not (HLT.Mu50 or HLT.TkMu50):
                continue
            lepton = muons[0]
            mctfound = False
            for muon in muons:
                if (muon.genPartFlav == 1 or muon.genPartFlav == 15) and not mctfound:
                    mclepton = muon
                    mctfound = True
                    if mclepton.genPartIdx == -1:
                        print 'MCTruth reconstruction not properly working - lepton step'
                        continue
    

        if isEle:
            if HLTrig and not HLT.Ele115_CaloIdVT_GsfTrkIdT:
                continue
            lepton = electrons[0]
            mctfound = False
            for electron in electrons:
                if (electron.genPartFlav == 1 or electron.genPartFlav == 15) and not mctfound:
                    mclepton = electron
                    mctfound = True
                    if mclepton.genPartIdx == -1:
                        print 'MCTruth reconstruction not properly working - lepton step'
                        continue
    
        if lepton is None:
            continue
        else:
            HLTriggered += 1
            #print 'HLTriggered'

        recotop = TopUtilities()
        #MCtruth event reconstruction
        
        mctop_p4 = None
        mctop_p4t = None
        mcpromptbjet_p4 = None
        mctopbjet_p4 = None
        mcpromptbjet_p4t = None
        bjetcheck = True
        bjets = bjet_filter(jets)
        if len(bjets)>2:
            #print 'Warning! More than 2 bjet from MCTruth in ev #%i' %i
            bjetcheck = False
            m2bjetev += 1
        '''
        else:
            for bjet in bjets:
                if bjet.partonFlavour == 5:
                    h_mcbjet_pt['bjet'].Fill(bjet.pt)
                else:
                    h_mcbjet_pt['antibjet'].Fill(bjet.pt)
        '''
        
        if mclepton is not None:
            nmctruth_ev += 1
            mclepton_p4 = ROOT.TLorentzVector()
            mclepton_p4.SetPtEtaPhiM(mclepton.pt, mclepton.eta, mclepton.phi, mclepton.mass)
            if isMu:
                h_mclepton_pt['muon'].Fill(mclepton.pt)
            elif isEle:
                h_mclepton_pt['electron'].Fill(mclepton.pt)
            
            MCWprime_p4 = ROOT.TLorentzVector()

            topgot = False
            Wpgot = False

            bottjets = sameflav_filter(bjets, 5)
            abottjets = sameflav_filter(bjets, -5)

            if len(bottjets)>1:
                for i in reversed(range(len(bottjets))):
                    for j in range(i):
                        dR = deltaR(bottjets[i].eta, bottjets[i].phi, bottjets[j].eta, bottjets[j].phi)
                        h_sameflav_bjet_deltaR.Fill(dR)

            if len(abottjets)>1:
                for i in reversed(range(len(abottjets))):
                    for j in range(i):
                        dR = deltaR(abottjets[i].eta, abottjets[i].phi, abottjets[j].eta, abottjets[j].phi)
                        h_sameflav_bjet_deltaR.Fill(dR)

            #if bjetcheck:
             
            for bjet in bjets:
                bjet_p4 = ROOT.TLorentzVector()
                bjet_p4.SetPtEtaPhiM(bjet.pt, bjet.eta, bjet.phi, bjet.mass)

                if abs(bjet.partonFlavour)!=5:
                    print 'bfilter not properly working'
                    continue
            
                blepflav = genpart[mclepton.genPartIdx].pdgId*bjet.partonFlavour

                if blepflav < 0 and not topgot:
                    mctop_p4 = recotop.top4Momentum(mclepton_p4, bjet_p4, MET['metPx'], MET['metPy'])
                    mclepton_p4t = copy.deepcopy(mclepton_p4)
                    mclepton_p4t.SetPz(0.)
                    mctopbjet_p4 = bjet_p4
                    bjet_p4t = copy.deepcopy(bjet_p4)
                    bjet_p4t.SetPz(0.)
                    met_p4t = ROOT.TLorentzVector()
                    met_p4t.SetPtEtaPhiM(met.pt, 0., met.phi, 0)
                    mctop_p4t = mclepton_p4t + bjet_p4t + met_p4t
                    if mctop_p4t.Pz() !=0:
                        print 'p3'
                        mctop_p4t.SetPz(0.)
                    topgot = True
                elif blepflav > 0 and not Wpgot:
                    mcpromptbjet_p4 = bjet_p4
                    mcpromptbjet_p4t = copy.deepcopy(bjet_p4)
                    mcpromptbjet_p4t.SetPz(0.)
                    Wpgot = True
            
            if topgot and Wpgot:
                MCWprime_p4 = mctop_p4 + mcpromptbjet_p4
                MCWprime_p4t = mctop_p4t + mcpromptbjet_p4t
                if True:#MCWprime_p4.M() > 6000:#Wpmass filter
                    h_mcbjet_pt['topbjet'].Fill(mctopbjet_p4.Pt())
                    h_mcbjet_pt['Wbjet'].Fill(mcpromptbjet_p4.Pt())
                    h_met_q['pt'].Fill(met.pt)
                    h_met_q['Et'].Fill(met.sumEt)
                    h_met_q['phi'].Fill(met.phi)
                    if bjetcheck:
                        h_mcbjet_pt['topbjet_ev2'].Fill(mctopbjet_p4.Pt())
                        h_mcbjet_pt['Wbjet_ev2'].Fill(mcpromptbjet_p4.Pt())                    
                        h_met_q['pt_ev2'].Fill(met.pt)
                        h_met_q['Et_ev2'].Fill(met.sumEt)
                        h_met_q['phi_ev2'].Fill(met.phi)

                        h_mcWprime_mass['all'].Fill(MCWprime_p4.M())
                        h_mcWprime_tmass['all'].Fill(MCWprime_p4t.M())
                        if isEle:
                            h_mcWprime_mass['ele_all'].Fill(MCWprime_p4.M())
                            h_mcWprime_tmass['ele_all'].Fill(MCWprime_p4t.M())
                        elif isMu:
                            h_mcWprime_mass['mu_all'].Fill(MCWprime_p4.M())
                            h_mcWprime_tmass['mu_all'].Fill(MCWprime_p4t.M())
                        if bjetcheck:
                            h_mcWprime_mass['ev2'].Fill(MCWprime_p4.M())
                            h_mcWprime_tmass['ev2'].Fill(MCWprime_p4t.M())
                            if isEle:
                                h_mcWprime_mass['ele_ev2'].Fill(MCWprime_p4.M())
                                h_mcWprime_tmass['ele_ev2'].Fill(MCWprime_p4t.M())
                            elif isMu:
                                h_mcWprime_mass['mu_ev2'].Fill(MCWprime_p4.M())
                                h_mcWprime_tmass['mu_ev2'].Fill(MCWprime_p4t.M())
        #LepTriggering

        if isMu:
            if not (lepton.tightId or lepton.pt > 50):
                continue
            else:
                LepTriggered += 1

        if isEle:
            if not (lepton.mvaFall17V2noIso_WP90 or lepton.pt > 50):
                continue
            else:
                LepTriggered += 1
            

        #JetTriggering
        goodjets = get_Jet(jets, 35)
        if len(goodjets)<1:
            continue
        else:
            JetTriggered += 1
    
    
    #histo printing and saving
    
    for value in h_mclepton_pt.values():
        print_hist(inpfile, value)
        save_hist(inpfile, value)
    
    for value in h_mcbjet_pt.values():
        print_hist(inpfile, value)
        save_hist(inpfile, value)
    
    for value in h_mcWprime_mass.values():
        print_hist(inpfile, value)
        save_hist(inpfile, value)

    for value in h_mcWprime_tmass.values():
        print_hist(inpfile, value)
        save_hist(inpfile, value)

    for value in h_met_q.values():
        print_hist(inpfile, value)
        save_hist(inpfile, value)
    
    print_hist(inpfile, h_sameflav_bjet_deltaR)
    save_hist(inpfile, h_sameflav_bjet_deltaR)
    
    print 'Total events: %d     ||     Bad MET flag events %d     ||     Bad events %d      ||     Events with more than 2 mcbjets %d' %(tree.GetEntries(), badflag, badevt, m2bjetev)
        #tree.Scan("GenPart_genPartIdxMother:GenPart_pdgId")#, "GenPart_pdgId==-11 || GenPart_pdgId==11")
        #tree.Scan("Muon_genPartIdx", "(HLT_Mu50 || HLT_TkMu50 || HLT_Ele115_CaloIdVT_GsfTrkIdT) && Muon_genPartIdx == -1")
        #tree.Scan("GenPart_pdgId[GenPart_genPartIdxMother[Electron_genPartIdx]]:GenPart_pdgId[Electron_genPartIdx]:GenPart_pdgId[GenPart_genPartIdxMother[Muon_genPartIdx]]:GenPart_pdgId[Muon_genPartIdx]", "(Electron_genPartIdx != (-1) && Muon_genPartIdx != (-1) && (GenPart_pdgId[GenPart_genPartIdxMother[Electron_genPartIdx]] == GenPart_pdgId[Electron_genPartIdx] || GenPart_pdgId[GenPart_genPartIdxMother[Muon_genPartIdx]] == GenPart_pdgId[Muon_genPartIdx]))")


