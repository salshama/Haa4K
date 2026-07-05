# from https://github.com/mpresill/PlotsConfigurations/blob/matteo/Configurations/VBS_ZV/scripts/rebinning.py#L23-L66
# https://root.cern/doc/master/classTH1.html#a9eef6f499230b88582648892e5e4e2ce on rebin 
# requires python3 from key4hep stack sourcing, not cmsenv

import os
import ROOT
import shutil
from matplotlib import pyplot as plt
import numpy as np
import pandas as pd
import array
import sys
import os.path
import ntpath
import importlib
import copy
import re
import logging

def sorted_dict_values(dic: dict) -> list:
    ''''
    Sort values in the dictionary.
    '''
    keys = sorted(dic)
    return [dic[key] for key in keys]

def make_dir_if_not_exists(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)
        print(f"Directory created successfully.")
    else:
        print(f"Directory already exists.")

ana_tex     = "e^{+}e^{-} #rightarrow Z #rightarrow ZH, H #rightarrow aa"
energy      = 240
collider    = 'FCC-ee'
intLumi     = 10.8e6 #pb^-1

DIRECTORY 	= '/ceph/salshamaily/haa4K_FCCee/analysis/final_output/all_samples_mgp8sig_norwt_042026/'

# cut to rebin
CUTS = [
    "RecoKaonElecSel",
]

# variable to rebin
VARIABLE = "RecoHiggs_mass"

FILES = [
    'mgp8_ee_eeH_HAlpAlp_m1_ecm240',
    'mgp8_ee_eeH_HAlpAlp_m10_ecm240',
    'mgp8_ee_eeH_HAlpAlp_m30_ecm240',
    'mgp8_ee_eeH_HAlpAlp_m60_ecm240',
    
    'p8_ee_WW_ecm240',
    'p8_ee_Zqq_ecm240',
    'p8_ee_ZZ_ecm240',

    "wzp6_ee_tautauH_Htautau_ecm240",
    "wzp6_ee_tautauH_Hbb_ecm240",
    "wzp6_ee_tautauH_Hcc_ecm240",
    "wzp6_ee_tautauH_Hss_ecm240",
    "wzp6_ee_tautauH_Hgg_ecm240",
    "wzp6_ee_tautauH_HWW_ecm240",
    "wzp6_ee_tautauH_HZZ_ecm240",

    "wzp6_ee_nuenueZ_ecm240",
    "wzp6_ee_nunuH_Hbb_ecm240",
    "wzp6_ee_nunuH_Hcc_ecm240",
    "wzp6_ee_nunuH_Hss_ecm240",
    "wzp6_ee_nunuH_Hgg_ecm240",
    "wzp6_ee_nunuH_HWW_ecm240",
    "wzp6_ee_nunuH_HZZ_ecm240",

    "wzp6_ee_eeH_Htautau_ecm240",
    "wzp6_ee_eeH_Hbb_ecm240",
    "wzp6_ee_eeH_Hcc_ecm240",
    "wzp6_ee_eeH_Hss_ecm240",
    "wzp6_ee_eeH_Hgg_ecm240",
    "wzp6_ee_eeH_HWW_ecm240",
    "wzp6_ee_eeH_HZZ_ecm240",

    "wzp6_ee_mumuH_Hbb_ecm240",
    "wzp6_ee_mumuH_Hcc_ecm240",
    "wzp6_ee_mumuH_Hss_ecm240",
    "wzp6_ee_mumuH_Hgg_ecm240",
    "wzp6_ee_mumuH_HWW_ecm240",
    "wzp6_ee_mumuH_HZZ_ecm240",

    "wzp6_ee_bbH_Htautau_ecm240",
    "wzp6_ee_bbH_Hbb_ecm240",
    "wzp6_ee_bbH_Hcc_ecm240",
    "wzp6_ee_bbH_Hss_ecm240",
    "wzp6_ee_bbH_Hgg_ecm240",
    "wzp6_ee_bbH_HWW_ecm240",
    "wzp6_ee_bbH_HZZ_ecm240",

    "wzp6_ee_ccH_Htautau_ecm240",
    "wzp6_ee_ccH_Hbb_ecm240",
    "wzp6_ee_ccH_Hcc_ecm240",
    "wzp6_ee_ccH_Hss_ecm240",
    "wzp6_ee_ccH_Hgg_ecm240",
    "wzp6_ee_ccH_HWW_ecm240",
    "wzp6_ee_ccH_HZZ_ecm240",

    "wzp6_ee_ssH_Htautau_ecm240",
    "wzp6_ee_ssH_Hbb_ecm240",
    "wzp6_ee_ssH_Hcc_ecm240",
    "wzp6_ee_ssH_Hss_ecm240",
    "wzp6_ee_ssH_Hgg_ecm240",
    "wzp6_ee_ssH_HWW_ecm240",
    "wzp6_ee_ssH_HZZ_ecm240",

    "wzp6_ee_qqH_Htautau_ecm240",
    "wzp6_ee_qqH_Hbb_ecm240",
    "wzp6_ee_qqH_Hcc_ecm240",
    "wzp6_ee_qqH_Hss_ecm240",
    "wzp6_ee_qqH_Hgg_ecm240",
    "wzp6_ee_qqH_HWW_ecm240",
    "wzp6_ee_qqH_HZZ_ecm240",
]

LABELS = {
    "RecoKaonElecSel": "n_{kaons}=4 and n_{electrons}=2, charge_{kaons}=1, 0.2 < E_{kaons} < 0.7 GeV"
 }

backgrounds = [
    'p8_ee_WW_ecm240',
    'p8_ee_Zqq_ecm240',
    'p8_ee_ZZ_ecm240',
    
    "wzp6_ee_tautau_ecm240",
    "wzp6_ee_mumu_ecm240",
    "wzp6_ee_ee_Mee_30_150_ecm240",

    "wzp6_ee_tautauH_Htautau_ecm240",
    "wzp6_ee_tautauH_Hbb_ecm240",
    "wzp6_ee_tautauH_Hcc_ecm240",
    "wzp6_ee_tautauH_Hss_ecm240",
    "wzp6_ee_tautauH_Hgg_ecm240",
    "wzp6_ee_tautauH_HWW_ecm240",
    "wzp6_ee_tautauH_HZZ_ecm240",

    "wzp6_egamma_eZ_Zmumu_ecm240",
    "wzp6_egamma_eZ_Zee_ecm240",
    "wzp6_gammae_eZ_Zmumu_ecm240",
    "wzp6_gammae_eZ_Zee_ecm240",

    "wzp6_gaga_tautau_60_ecm240",
    "wzp6_gaga_mumu_60_ecm240",
    "wzp6_gaga_ee_60_ecm240",

    "wzp6_ee_nuenueZ_ecm240",
    "wzp6_ee_nunuH_Htautau_ecm240",
    "wzp6_ee_nunuH_Hbb_ecm240",
    "wzp6_ee_nunuH_Hcc_ecm240",
    "wzp6_ee_nunuH_Hss_ecm240",
    "wzp6_ee_nunuH_Hgg_ecm240",
    "wzp6_ee_nunuH_HWW_ecm240",
    "wzp6_ee_nunuH_HZZ_ecm240",

    "wzp6_ee_eeH_Htautau_ecm240",
    "wzp6_ee_eeH_Hbb_ecm240",
    "wzp6_ee_eeH_Hcc_ecm240",
    "wzp6_ee_eeH_Hss_ecm240",
    "wzp6_ee_eeH_Hgg_ecm240",
    "wzp6_ee_eeH_HWW_ecm240",
    "wzp6_ee_eeH_HZZ_ecm240",

    "wzp6_ee_mumuH_Htautau_ecm240",
    "wzp6_ee_mumuH_Hbb_ecm240",
    "wzp6_ee_mumuH_Hcc_ecm240",
    "wzp6_ee_mumuH_Hss_ecm240",
    "wzp6_ee_mumuH_Hgg_ecm240",
    "wzp6_ee_mumuH_HWW_ecm240",
    "wzp6_ee_mumuH_HZZ_ecm240",

    "wzp6_ee_bbH_Htautau_ecm240",
    "wzp6_ee_bbH_Hbb_ecm240",
    "wzp6_ee_bbH_Hcc_ecm240",
    "wzp6_ee_bbH_Hss_ecm240",
    "wzp6_ee_bbH_Hgg_ecm240",
    "wzp6_ee_bbH_HWW_ecm240",
    "wzp6_ee_bbH_HZZ_ecm240",

    "wzp6_ee_ccH_Htautau_ecm240",
    "wzp6_ee_ccH_Hbb_ecm240",
    "wzp6_ee_ccH_Hcc_ecm240",
    "wzp6_ee_ccH_Hss_ecm240",
    "wzp6_ee_ccH_Hgg_ecm240",
    "wzp6_ee_ccH_HWW_ecm240",
    "wzp6_ee_ccH_HZZ_ecm240",

    "wzp6_ee_ssH_Htautau_ecm240",
    "wzp6_ee_ssH_Hbb_ecm240",
    "wzp6_ee_ssH_Hcc_ecm240",
    "wzp6_ee_ssH_Hss_ecm240",
    "wzp6_ee_ssH_Hgg_ecm240",
    "wzp6_ee_ssH_HWW_ecm240",
    "wzp6_ee_ssH_HZZ_ecm240",

    "wzp6_ee_qqH_Htautau_ecm240",
    "wzp6_ee_qqH_Hbb_ecm240",
    "wzp6_ee_qqH_Hcc_ecm240",
    "wzp6_ee_qqH_Hss_ecm240",
    "wzp6_ee_qqH_Hgg_ecm240",
    "wzp6_ee_qqH_HWW_ecm240",
    "wzp6_ee_qqH_HZZ_ecm240",
]

blegend = {
    'p8_ee_WW_ecm240':	'ee \rightarrow WW',
    'p8_ee_Zqq_ecm240': 'ee \rightarrow Z \rightarrow qq',
    'p8_ee_ZZ_ecm240':	'ee \rightarrow ZZ',
    
    "wzp6_ee_tautau_ecm240":        "ee $\rightarrow$ $\tau$ $\tau$",
    "wzp6_ee_mumu_ecm240":            "ee $\rightarrow$ $\mu$ $\mu$",
    "wzp6_ee_ee_Mee_30_150_ecm240":    "ee $\rightarrow$ ee",

    "wzp6_ee_tautauH_Htautau_ecm240":    "ee $\rightarrow$ $\tau$ $\tau$ H $\rightarrow$ $\tau$ $\tau$",
    "wzp6_ee_tautauH_Hbb_ecm240":        "ee $\rightarrow$ $\tau$ $\tau$ H $\rightarrow$ bb",
    "wzp6_ee_tautauH_Hcc_ecm240":        "ee $\rightarrow$ $\tau$ $\tau$ H $\rightarrow$ cc",
    "wzp6_ee_tautauH_Hss_ecm240":        "ee $\rightarrow$ $\tau$ $\tau$ H $\rightarrow$ ss",
    "wzp6_ee_tautauH_Hgg_ecm240":        "ee $\rightarrow$ $\tau$ $\tau$ H $\rightarrow$ gg",
    "wzp6_ee_tautauH_HWW_ecm240":        "ee $\rightarrow$ $\tau$ $\tau$ H $\rightarrow$ WW",
    "wzp6_ee_tautauH_HZZ_ecm240":        "ee $\rightarrow$ $\tau$ $\tau$ H $\rightarrow$ ZZ",
    
    "wzp6_egamma_eZ_Zmumu_ecm240":    "e $\gamma$ $\rightarrow$ eZ $\rightarrow$ Z $\mu$ $\mu$",
    "wzp6_egamma_eZ_Zee_ecm240":    "e $\gamma$ $\rightarrow$ eZ $\rightarrow$ Zee",
    "wzp6_gammae_eZ_Zmumu_ecm240":    "e $\gamma$ e $\rightarrow$ eZ $\rightarrow$ Z $\mu$ $\mu$",
    "wzp6_gammae_eZ_Zee_ecm240":    "e $\gamma$ e $\rightarrow$ eZ $\rightarrow$ Zee",
    
    "wzp6_gaga_tautau_60_ecm240":    "gaga $\rightarrow$ $\tau$ $\tau$",
    "wzp6_gaga_mumu_60_ecm240":        "gaga $\rightarrow$ $\mu$ $\mu$",
    "wzp6_gaga_ee_60_ecm240":        "gaga $\rightarrow$ ee",
    
    "wzp6_ee_nuenueZ_ecm240":        "ee $\rightarrow$ $\nu$ $\nu$ eZ",
    "wzp6_ee_nunuH_Htautau_ecm240":    "ee $\rightarrow$ $\nu$ $\nu$ H $\rightarrow$ $\tau$ $\tau$",
    "wzp6_ee_nunuH_Hbb_ecm240":        "ee $\rightarrow$ $\nu$ $\nu$ H $\rightarrow$ bb",
    "wzp6_ee_nunuH_Hcc_ecm240":        "ee $\rightarrow$ $\nu$ $\nu$ H $\rightarrow$ cc",
    "wzp6_ee_nunuH_Hss_ecm240":        "ee $\rightarrow$ $\nu$ $\nu$ H $\rightarrow$ ss",
    "wzp6_ee_nunuH_Hgg_ecm240":        "ee $\rightarrow$ $\nu$ $\nu$ H $\rightarrow$ gg",
    "wzp6_ee_nunuH_HWW_ecm240":        "ee $\rightarrow$ $\nu$ $\nu$ H $\rightarrow$ WW",
    "wzp6_ee_nunuH_HZZ_ecm240":        "ee $\rightarrow$ $\nu$ $\nu$ H $\rightarrow$ ZZ",
    
    "wzp6_ee_eeH_Htautau_ecm240":    "ee $\rightarrow$ eeH $\rightarrow$ $\tau$ $\tau$",
    "wzp6_ee_eeH_Hbb_ecm240":        "ee $\rightarrow$ eeH $\rightarrow$ bb",
    "wzp6_ee_eeH_Hcc_ecm240":        "ee $\rightarrow$ eeH $\rightarrow$ cc",
    "wzp6_ee_eeH_Hss_ecm240":        "ee $\rightarrow$ eeH $\rightarrow$ ss",
    "wzp6_ee_eeH_Hgg_ecm240":        "ee $\rightarrow$ eeH $\rightarrow$ gg",
    "wzp6_ee_eeH_HWW_ecm240":        "ee $\rightarrow$ eeH $\rightarrow$ WW",
    "wzp6_ee_eeH_HZZ_ecm240":        "ee $\rightarrow$ eeH $\rightarrow$ ZZ",
    
    "wzp6_ee_mumuH_Htautau_ecm240":    "ee $\rightarrow$ $\mu$ $\mu$ H $\rightarrow$ $\tau$ $\tau$",
    "wzp6_ee_mumuH_Hbb_ecm240":        "ee $\rightarrow$ $\mu$ $\mu$ H $\rightarrow$ bb",
    "wzp6_ee_mumuH_Hcc_ecm240":        "ee $\rightarrow$ $\mu$ $\mu$ H $\rightarrow$ cc",
    "wzp6_ee_mumuH_Hss_ecm240":        "ee $\rightarrow$ $\mu$ $\mu$ H $\rightarrow$ ss",
    "wzp6_ee_mumuH_Hgg_ecm240":        "ee $\rightarrow$ $\mu$ $\mu$ H $\rightarrow$ gg",
    "wzp6_ee_mumuH_HWW_ecm240":        "ee $\rightarrow$ $\mu$ $\mu$ H $\rightarrow$ WW",
    "wzp6_ee_mumuH_HZZ_ecm240":        "ee $\rightarrow$ $\mu$ $\mu$ H $\rightarrow$ ZZ",
    
    "wzp6_ee_bbH_Htautau_ecm240":    "ee $\rightarrow$ bbH $\rightarrow$ $\tau$ $\tau$",
    "wzp6_ee_bbH_Hbb_ecm240":        "ee $\rightarrow$ bbH $\rightarrow$ bb",
    "wzp6_ee_bbH_Hcc_ecm240":        "ee $\rightarrow$ bbH $\rightarrow$ cc",
    "wzp6_ee_bbH_Hss_ecm240":        "ee $\rightarrow$ bbH $\rightarrow$ ss",
    "wzp6_ee_bbH_Hgg_ecm240":        "ee $\rightarrow$ bbH $\rightarrow$ gg",
    "wzp6_ee_bbH_HWW_ecm240":        "ee $\rightarrow$ bbH $\rightarrow$ WW",
    "wzp6_ee_bbH_HZZ_ecm240":        "ee $\rightarrow$ bbH $\rightarrow$ ZZ",
    
    "wzp6_ee_ccH_Htautau_ecm240":    "ee $\rightarrow$ ccH $\rightarrow$ $\tau$ $\tau$",
    "wzp6_ee_ccH_Hbb_ecm240":        "ee $\rightarrow$ ccH $\rightarrow$ bb",
    "wzp6_ee_ccH_Hcc_ecm240":        "ee $\rightarrow$ ccH $\rightarrow$ cc",
    "wzp6_ee_ccH_Hss_ecm240":        "ee $\rightarrow$ ccH $\rightarrow$ ss",
    "wzp6_ee_ccH_Hgg_ecm240":        "ee $\rightarrow$ ccH $\rightarrow$ gg",
    "wzp6_ee_ccH_HWW_ecm240":        "ee $\rightarrow$ ccH $\rightarrow$ WW",
    "wzp6_ee_ccH_HZZ_ecm240":        "ee $\rightarrow$ ccH $\rightarrow$ ZZ",
    
    "wzp6_ee_ssH_Htautau_ecm240":    "ee $\rightarrow$ ssH $\rightarrow$ $\tau$ $\tau$",
    "wzp6_ee_ssH_Hbb_ecm240":        "ee $\rightarrow$ ssH $\rightarrow$ bb",
    "wzp6_ee_ssH_Hcc_ecm240":        "ee $\rightarrow$ ssH $\rightarrow$ cc",
    "wzp6_ee_ssH_Hss_ecm240":        "ee $\rightarrow$ ssH $\rightarrow$ ss",
    "wzp6_ee_ssH_Hgg_ecm240":        "ee $\rightarrow$ ssH $\rightarrow$ gg",
    "wzp6_ee_ssH_HWW_ecm240":        "ee $\rightarrow$ ssH $\rightarrow$ WW",
    "wzp6_ee_ssH_HZZ_ecm240":        "ee $\rightarrow$ ssH $\rightarrow$ ZZ",
    
    "wzp6_ee_qqH_Htautau_ecm240":    "ee $\rightarrow$ qqH $\rightarrow$ $\tau$ $\tau$",
    "wzp6_ee_qqH_Hbb_ecm240":        "ee $\rightarrow$ qqH $\rightarrow$ bb",
    "wzp6_ee_qqH_Hcc_ecm240":        "ee $\rightarrow$ qqH $\rightarrow$ cc",
    "wzp6_ee_qqH_Hss_ecm240":        "ee $\rightarrow$ qqH $\rightarrow$ ss",
    "wzp6_ee_qqH_Hgg_ecm240":        "ee $\rightarrow$ qqH $\rightarrow$ gg",
    "wzp6_ee_qqH_HWW_ecm240":        "ee $\rightarrow$ qqH $\rightarrow$ WW",
    "wzp6_ee_qqH_HZZ_ecm240":        "ee $\rightarrow$ qqH $\rightarrow$ ZZ",
}

bcolors = {
    'p8_ee_WW_ecm240':	36,
    'p8_ee_Zqq_ecm240': 40,
    'p8_ee_ZZ_ecm240':	44,
    
    "wzp6_ee_tautau_ecm240": 36,
    "wzp6_ee_mumu_ecm240": 40,
    "wzp6_ee_ee_Mee_30_150_ecm240": 44,

    "wzp6_ee_tautauH_Htautau_ecm240": 36,
    "wzp6_ee_tautauH_Hbb_ecm240": 40,
    "wzp6_ee_tautauH_Hcc_ecm240": 44,
    "wzp6_ee_tautauH_Hss_ecm240": 36,
    "wzp6_ee_tautauH_Hgg_ecm240": 40,
    "wzp6_ee_tautauH_HWW_ecm240": 44,
    "wzp6_ee_tautauH_HZZ_ecm240": 36,

    "wzp6_egamma_eZ_Zmumu_ecm240": 36,
    "wzp6_egamma_eZ_Zee_ecm240": 40,
    "wzp6_gammae_eZ_Zmumu_ecm240": 44,
    "wzp6_gammae_eZ_Zee_ecm240": 36,

    "wzp6_gaga_tautau_60_ecm240": 36,
    "wzp6_gaga_mumu_60_ecm240": 40,
    "wzp6_gaga_ee_60_ecm240": 44,

    "wzp6_ee_nuenueZ_ecm240": 36,
    "wzp6_ee_nunuH_Htautau_ecm240": 40,
    "wzp6_ee_nunuH_Hbb_ecm240": 40,
    "wzp6_ee_nunuH_Hcc_ecm240": 44,
    "wzp6_ee_nunuH_Hss_ecm240": 36,
    "wzp6_ee_nunuH_Hgg_ecm240": 40,
    "wzp6_ee_nunuH_HWW_ecm240": 44,
    "wzp6_ee_nunuH_HZZ_ecm240": 36,

    "wzp6_ee_eeH_Htautau_ecm240": 36,
    "wzp6_ee_eeH_Hbb_ecm240": 40,
    "wzp6_ee_eeH_Hcc_ecm240": 44,
    "wzp6_ee_eeH_Hss_ecm240": 36,
    "wzp6_ee_eeH_Hgg_ecm240": 40,
    "wzp6_ee_eeH_HWW_ecm240": 44,
    "wzp6_ee_eeH_HZZ_ecm240": 36,

    "wzp6_ee_mumuH_Htautau_ecm240": 36,
    "wzp6_ee_mumuH_Hbb_ecm240": 40,
    "wzp6_ee_mumuH_Hcc_ecm240": 44,
    "wzp6_ee_mumuH_Hss_ecm240": 36,
    "wzp6_ee_mumuH_Hgg_ecm240": 40,
    "wzp6_ee_mumuH_HWW_ecm240": 44,
    "wzp6_ee_mumuH_HZZ_ecm240": 36,

    "wzp6_ee_bbH_Htautau_ecm240": 36,
    "wzp6_ee_bbH_Hbb_ecm240": 40,
    "wzp6_ee_bbH_Hcc_ecm240": 44,
    "wzp6_ee_bbH_Hss_ecm240": 36,
    "wzp6_ee_bbH_Hgg_ecm240": 40,
    "wzp6_ee_bbH_HWW_ecm240": 44,
    "wzp6_ee_bbH_HZZ_ecm240": 36,

    "wzp6_ee_ccH_Htautau_ecm240": 36,
    "wzp6_ee_ccH_Hbb_ecm240":		40,
    "wzp6_ee_ccH_Hcc_ecm240":		44,
    "wzp6_ee_ccH_Hss_ecm240":		36,
    "wzp6_ee_ccH_Hgg_ecm240":		40,
    "wzp6_ee_ccH_HWW_ecm240":		44,
    "wzp6_ee_ccH_HZZ_ecm240":		36,

    "wzp6_ee_ssH_Htautau_ecm240": 36,
    "wzp6_ee_ssH_Hbb_ecm240":		40,
    "wzp6_ee_ssH_Hcc_ecm240":		44,
    "wzp6_ee_ssH_Hss_ecm240":		36,
    "wzp6_ee_ssH_Hgg_ecm240":		40,
    "wzp6_ee_ssH_HWW_ecm240":		44,
    "wzp6_ee_ssH_HZZ_ecm240":		36,

    "wzp6_ee_qqH_Htautau_ecm240": 36,
    "wzp6_ee_qqH_Hbb_ecm240": 	40,
    "wzp6_ee_qqH_Hcc_ecm240":		44,
    "wzp6_ee_qqH_Hss_ecm240":		36,
    "wzp6_ee_qqH_Hgg_ecm240":		40,
    "wzp6_ee_qqH_HWW_ecm240":		44,
    "wzp6_ee_qqH_HZZ_ecm240":		36,
}

signals = [
    'mgp8_ee_eeH_HAlpAlp_m1_ecm240',
    'mgp8_ee_eeH_HAlpAlp_m10_ecm240',
    'mgp8_ee_eeH_HAlpAlp_m30_ecm240',
    'mgp8_ee_eeH_HAlpAlp_m60_ecm240',
]

slegend = {
    'mgp8_ee_eeH_HAlpAlp_m1_ecm240':	'M_{a} = 1.5 GeV',
    'mgp8_ee_eeH_HAlpAlp_m10_ecm240':	'M_{a} = 10 GeV',
    'mgp8_ee_eeH_HAlpAlp_m30_ecm240':	'M_{a} = 30 GeV',
    'mgp8_ee_eeH_HAlpAlp_m60_ecm240':	'M_{a} = 60 GeV',
}

scolors = {
    'mgp8_ee_eeH_HAlpAlp_m1_ecm240':	ROOT.kBlue-3,
    'mgp8_ee_eeH_HAlpAlp_m10_ecm240':	ROOT.kBlue-3,
    'mgp8_ee_eeH_HAlpAlp_m30_ecm240':	ROOT.kRed-3,
    'mgp8_ee_eeH_HAlpAlp_m60_ecm240':	ROOT.kGreen-3,
}

### note: The bin edges specified in xbins should correspond to bin edges in the original histogram ###
fir_bins			= np.arange(120,123,1.5)
sec_bins			= np.arange(123,127,1.7)
thi_bins			= np.arange(127,130,1.4)
asym_bins_shift		= np.concatenate([fir_bins,sec_bins, thi_bins])
nbins				= len(asym_bins_shift)-1

for CUT in CUTS:
    NEWFILE = "/ceph/salshamaily/haa4K_FCCee/samples/" + VARIABLE + "_" + CUT + "_rebinned.root"
    nf      = ROOT.TFile.Open(NEWFILE, "RECREATE")

    #rebin FILES and save content in NEWFILE
    for file in FILES:

        FILE    = DIRECTORY + file + '_' + CUT + '_histo.root'
        f       = ROOT.TFile.Open(FILE, "READ")
        hist    = f.Get(VARIABLE)

        print("Rebinning variable {}, {} from {} bins to {} bins\n".format(VARIABLE, FILE, hist.GetNbinsX(), nbins))
        
        hist_name = file + "_" + VARIABLE
        new_hist  = ROOT.TH1F(hist_name, "Reco Higgs mass", nbins, array.array('d', asym_bins_shift))
        
        #for each bin in the original distribution, sum until one interval is reached
        i = 0
        bin_content = 0
        for b in range(hist.GetNbinsX()):
            bin_content += hist.GetBinContent(b)
            if (hist.GetBinLowEdge(b) >= asym_bins_shift[i]): #check if the interval edge has already been reached and if we are over it
                new_hist.SetBinContent(i, bin_content)
                i += 1
                bin_content = 0
                if (i > nbins):
                    break
                    
        nf.cd()
        new_hist.Write()
        f.Close()

    nf.Close()

'''#plot the rebinned variable
NEWFILE_SF='/eos/user/s/sgiappic/combine/Reco_DR_norebin_selReco_gen_notracks_nohad_5M80_0.7cos_20MEpt.root' # name of the rebinned file
    
#extralab = LABELS[CUT]

canvas = ROOT.TCanvas("", "", 800, 800)

nsig = len(signals)
nbkg = 9 # change according to type of plots, 6 for grouped backgrounds

#legend coordinates and style
legsize = 0.06*nsig 
legsize2 = 0.04*nbkg
leg = ROOT.TLegend(0.16, 0.80 - legsize, 0.45, 0.74)
leg.SetFillColor(0)
leg.SetFillStyle(0)
leg.SetLineColor(0)
leg.SetShadowColor(0)
leg.SetTextSize(0.025)
leg.SetTextFont(42)

leg2 = ROOT.TLegend(0.70, 0.80 - legsize2, 0.88, 0.74)
leg2.SetFillColor(0)
leg2.SetFillStyle(0)
leg2.SetLineColor(0)
leg2.SetShadowColor(0)
leg2.SetTextSize(0.025)
leg2.SetTextFont(42)

#global arrays for histos and colors
histos = []
colors = []

#loop over files for signals and backgrounds and assign corresponding colors and titles
for s in signals:
    fin_SF = NEWFILE_SF
    #fin_DF = NEWFILE_DF
    with ROOT.TFile(fin_SF) as tf_SF:
        h = tf_SF.Get(s + "_" + VARIABLE)
        hh = copy.deepcopy(h)
        hh.SetDirectory(0)
   # with ROOT.TFile(fin_DF) as tf_DF:
    #    h1 = tf_DF.Get(s + "_" + VARIABLE)
    #    hh1 = copy.deepcopy(h1)
    #    hh1.SetDirectory(0)
    #hh.Add(hh1)
    histos.append(hh)
    colors.append(scolors[s])
    leg.AddEntry(histos[-1], slegend[s], "l")

#for b in backgrounds:
    #fin = f"{DIRECTORY}{b}_{cut}_histo.root"
    #with ROOT.TFile(fin) as tf:
        #h = tf.Get(variable)
        #hh = copy.deepcopy(h)
        #hh.SetDirectory(0)
    #histos.append(hh)
    #colors.append(bcolors[b])
    #leg2.AddEntry(histos[-1], blegend[b], "f")

if nbkg != 0:
    #add some backgrounds to the same histogram
    fin_SF = NEWFILE_SF
    #fin_DF = NEWFILE_DF
    with ROOT.TFile(fin_SF) as tf_SF:
        h = tf_SF.Get( "eenunu_" + VARIABLE)
        hh = copy.deepcopy(h)
        hh.SetDirectory(0)
    histos.append(hh)
    colors.append(bcolors["eenunu"])
    leg2.AddEntry(histos[-1], blegend["eenunu"], "f")

    with ROOT.TFile(fin_SF) as tf_SF:
        h = tf_SF.Get( "mumununu_" + VARIABLE)
        hh = copy.deepcopy(h)
        hh.SetDirectory(0)
    histos.append(hh)
    colors.append(bcolors["mumununu"])
    leg2.AddEntry(histos[-1], blegend["mumununu"], "f")

    with ROOT.TFile(fin_SF) as tf_SF:
        h = tf_SF.Get( "tatanunu_" + VARIABLE)
        hh = copy.deepcopy(h)
        hh.SetDirectory(0)
    histos.append(hh)
    colors.append(bcolors["tatanunu"])
    leg2.AddEntry(histos[-1], blegend["tatanunu"], "f")

    with ROOT.TFile(fin_SF) as tf_SF:
        h = tf_SF.Get( "llnunu_" + VARIABLE)
        hh = copy.deepcopy(h)
        hh.SetDirectory(0)
    histos.append(hh)
    colors.append(bcolors["llnunu"])
    leg2.AddEntry(histos[-1], blegend["llnunu"], "f")
    
    with ROOT.TFile(fin_SF) as tf_SF:
        h = tf_SF.Get( "p8_ee_Zee_ecm91_" + VARIABLE)
        hh = copy.deepcopy(h)
        hh.SetDirectory(0)
    with ROOT.TFile(fin_SF) as tf_SF:
        h1 = tf_SF.Get( "p8_ee_Zmumu_ecm91_" + VARIABLE)
        hh1 = copy.deepcopy(h1)
        hh1.SetDirectory(0)
    hh.Add(hh1)
    histos.append(hh)
    colors.append(bcolors["p8_ee_Zee_ecm91"])
    leg2.AddEntry(histos[-1], blegend["p8_ee_Zee_ecm91"], "f")

    with ROOT.TFile(fin_SF) as tf_SF:
        h = tf_SF.Get( "p8_ee_Ztautau_ecm91_" + VARIABLE)
        hh = copy.deepcopy(h)
        hh.SetDirectory(0)
    histos.append(hh)
    colors.append(bcolors["p8_ee_Ztautau_ecm91"])
    leg2.AddEntry(histos[-1], blegend["p8_ee_Ztautau_ecm91"], "f")

    with ROOT.TFile(fin_SF) as tf_SF:
        h = tf_SF.Get( "p8_ee_Zud_ecm91_" + VARIABLE)
        hh = copy.deepcopy(h)
        hh.SetDirectory(0)
    with ROOT.TFile(fin_SF) as tf_SF:
        h1 = tf_SF.Get( "p8_ee_Zss_ecm91_" + VARIABLE)
        hh1 = copy.deepcopy(h1)
        hh1.SetDirectory(0)
    hh.Add(hh1)
    histos.append(hh)
    colors.append(bcolors["p8_ee_Zud_ecm91"])
    leg2.AddEntry(histos[-1], blegend["p8_ee_Zud_ecm91"], "f")

    with ROOT.TFile(fin_SF) as tf_SF:
        h = tf_SF.Get( "p8_ee_Zcc_ecm91_" + VARIABLE)
        hh = copy.deepcopy(h)
        hh.SetDirectory(0)
    histos.append(hh)
    colors.append(bcolors["p8_ee_Zcc_ecm91"])
    leg2.AddEntry(histos[-1], blegend["p8_ee_Zcc_ecm91"], "f")

    with ROOT.TFile(fin_SF) as tf_SF:
        h = tf_SF.Get( "p8_ee_Zbb_ecm91_" + VARIABLE)
        hh = copy.deepcopy(h)
        hh.SetDirectory(0)
    histos.append(hh)
    colors.append(bcolors["p8_ee_Zbb_ecm91"])
    leg2.AddEntry(histos[-1], blegend["p8_ee_Zbb_ecm91"], "f")

    #drawing stack for backgrounds
    hStackBkg = ROOT.THStack("hStackBkg", "")
    hStackBkg.SetMinimum(1e-6)
    hStackBkg.SetMaximum(1e17)
    BgMCHistYieldsDic = {}
    for i in range(nsig, nsig+nbkg):
        h = histos[i]
        h.Scale(1.13) # scale lumi from 180 to 204
        h.SetLineWidth(1)
        h.SetLineColor(ROOT.kBlack)
        h.SetFillColor(colors[i])
        if h.Integral() > 0:
            BgMCHistYieldsDic[h.Integral()] = h
        else:
            BgMCHistYieldsDic[-1*nbkg] = h

    # sort stack by yields (smallest to largest)
    BgMCHistYieldsDic = sorted_dict_values(BgMCHistYieldsDic)
    for h in BgMCHistYieldsDic:
        hStackBkg.Add(h)

    #draw the histograms
    hStackBkg.Draw("HIST")

    # add the signal histograms
    for i in range(nsig):
        h = histos[i]
        h.Scale(1.13) # scale lumi from 180 to 204
        h.SetLineWidth(3)
        h.SetLineColor(colors[i])
        h.Draw("HIST SAME")

    hStackBkg.GetYaxis().SetTitle("Events")
    hStackBkg.GetXaxis().SetTitle("Reco #Delta R(l,l')")
    #hStackBkg.GetYaxis().SetTitleOffset(1.5)
    hStackBkg.GetXaxis().SetTitleOffset(1.2)
    #hStackBkg.GetXaxis().SetLimits(1, 1000)

else: 
        # add the signal histograms
    for i in range(nsig):
        h = histos[i]
        h.Scale(1.13) # scale lumi from 180 to 204
        h.SetLineWidth(3)
        h.SetLineColor(colors[i])
        if i == 0:
            h.Draw("HIST")
            h.GetYaxis().SetTitle("Events")
            h.GetXaxis().SetTitle(histos[i].GetXaxis().GetTitle())
            #h.GetXaxis().SetTitle("{}".format(variable))
            h.GetYaxis().SetRangeUser(1e-6,1e15)
            #h.GetYaxis().SetTitleOffset(1.5)
            h.GetXaxis().SetTitleOffset(1.2)
            #h.GetXaxis().SetLimits(1, 1000)
        else: 
            h.Draw("HIST SAME")

#labels around the plot
if 'ee' in collider:
    leftText = 'FCCAnalyses: FCC-ee Simulation (Delphes)'
rightText = f'#sqrt{{s}} = {energy} GeV, L={intLumi} ab^{{-1}}'

latex = ROOT.TLatex()
latex.SetNDC()

text = '#bf{#it{'+rightText+'}}'
latex.SetTextSize(0.03)
latex.DrawLatex(0.18, 0.84, text)

text = '#bf{#it{' + ana_tex + '}}'
latex.SetTextSize(0.03)
latex.DrawLatex(0.18, 0.80, text)

#text = '#bf{#it{' + extralab + '}}'
text = '#bf{#it{Two leptons, no photons, no other tracks, no neutral hadrons, 5<M(l,l)<80 GeV, p_{T,miss}>20 GeV, cos#theta>-0.7}}'
latex.SetTextSize(0.02)
latex.DrawLatex(0.18, 0.76, text)

leg.Draw()
leg2.Draw()

latex.SetTextAlign(31)
text = '#it{' + leftText + '}'
latex.SetTextSize(0.03)
latex.DrawLatex(0.92, 0.92, text)

# Set Logarithmic scales for both x and y axes
#canvas.SetLogx()
canvas.SetLogy()
canvas.SetTicks(1, 1)
canvas.SetLeftMargin(0.14)
canvas.SetRightMargin(0.08)
canvas.GetFrame().SetBorderSize(12)

canvas.RedrawAxis()
canvas.Modified()
canvas.Update()

#dir = "/eos/user/s/sgiappic/www/plots/" + CUT + "/"
#make_dir_if_not_exists(dir)

#canvas.SaveAs(dir + VARIABLE + "_rebinned.png")
#canvas.SaveAs(dir+ VARIABLE + "_rebinned.pdf")

canvas.SaveAs("/eos/user/s/sgiappic/www/paper/Reco_DR_rebinned_24july.png")
canvas.SaveAs("/eos/user/s/sgiappic/www/paper/Reco_DR_rebinned_24july.pdf")'''