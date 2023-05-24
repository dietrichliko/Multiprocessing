#! /usr/bin/env python

from __future__ import print_function

import os
import math

import pickle
import cloudpickle
import concurrent.futures

import ROOT

MAX_WORKERS = 10
PATH = "/scratch-cbe/users/dietrich.liko/StopsCompressed/nanoTuples/compstops_UL18v9_nano_v10/Met/WJetsToLNu_HT200to400/"


class Sample:
    def __init__(self, path, wjet_pt):
        self.files = [os.path.join(path, n) for n in os.listdir(path)]
        self.wjet_pt = wjet_pt         


class Fill:
    def __init__(self, sample):
        self.sample = cloudpickle.dumps(sample)
        # self.sample = sample
        
    def __call__(self, i):
        sample = cloudpickle.loads(self.sample)
#        sample = self.sample
        file = ROOT.TFile(sample.files[i], "READ")
        h_l1_pt = ROOT.TH1D("l1_pt", "", 100, 0., 1000.)
        h_met_pt = ROOT.TH1D("met_pt", "", 100, 0., 1000.)
        h_wjet_pt = ROOT.TH1D("wjet_pt", "", 100, 0., 1000.)
        for j, event in enumerate(file.Events):
            if j % 10000 == 0:
                print("File", i, "Event", j)
            h_l1_pt.Fill(event.l1_pt)
            h_met_pt.Fill(event.met_pt)
            h_wjet_pt.Fill(sample.wjet_pt(event))
        return h_l1_pt, h_met_pt, h_wjet_pt
                
    
if __name__ == "__main__":
    wjet_sample = Sample(
        PATH,
        lambda x: x.l1_pt**2 + x.met_pt**2 + 2 * x.l1_pt * x.met_pt * math.cos(x.l1_phi - x.met_phi)
    )
    with concurrent.futures.ProcessPoolExecutor(max_workers=MAX_WORKERS) as executor:
        cp_sample = cloudpickle.dumps(wjet_sample)
        histos = None
        for result in executor.map(
            Fill(wjet_sample), range(len(wjet_sample.files))
        ):
            if histos is None:
                histos = result
            else:
                histos = [h+r for h, r in zip(histos, result)]
                
    file = ROOT.TFile("mp_fill.root", "RECREATE")
    for h in histos:
        h.Write()
    file.Close()
        