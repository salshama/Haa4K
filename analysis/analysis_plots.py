import os
import ROOT
import colorsys

# global parameters
intLumi			= 10.8e6 #pb^-1

###If scaleSig=0 or scaleBack=0, we don't apply any additional scaling, on top of the normalization to cross section and integrated luminosity, as defined in finalSel.py
###If scaleSig or scaleBack is not defined, plots will be normalized to 1
# scaleSig		= 0.
# scaleBack		= 0.
ana_tex			= "e^{+}e^{-} #rightarrow Z #rightarrow ZH, H #rightarrow aa"
delphesVersion	= '3.4.2'
energy			= 240
collider 		= 'FCC-ee'
inputDir 		= '/ceph/salshamaily/haa4K_FCCee/analysis/final_output/all_samples_mgp8sig_norwt_082026/'
outdir			= '/ceph/salshamaily/haa4K_FCCee/analysis/plots_output/all_samples_mgp8sig_norwt_082026/'
formats			= ['png','pdf']
yaxis			= ['log']
stacksig		= ['nostack']
stackbkg		= ['stack']
legendCoord		= [0.68,0.55,0.96,0.88]
# plotStatUnc	= True ### to include statistical uncertainty ###
splitLeg		= True ### to split legend for backgrounds and signals ###

variables = [

	# MC k+
	"n_GenKplus",
	"GenKplus_e",
	"GenKplus_mass",
	"GenKplus_pt",
	"GenKplus_p",
	"GenKplus_px",
	"GenKplus_py",
	"GenKplus_pz",
	"GenKplus_eta",
	"GenKplus_theta",
	"GenKplus_phi",
	"GenKplus_charge",

	# MC gamma
	"n_FSGenPhoton",
	"FSGenPhoton_e",
	"FSGenPhoton_pt",
	"FSGenPhoton_p",
	"FSGenPhoton_px",
	"FSGenPhoton_py",
	"FSGenPhoton_pz",
	"FSGenPhoton_eta",
	"FSGenPhoton_theta",
	"FSGenPhoton_phi",

	# MC e-
	"n_FSGenElectron",
	"FSGenElectron_e",
	"FSGenElectron_mass",
	"FSGenElectron_pt",
	"FSGenElectron_p",
	"FSGenElectron_px",
	"FSGenElectron_py",
	"FSGenElectron_pz",
	"FSGenElectron_eta",
	"FSGenElectron_theta",
	"FSGenElectron_phi",
	"FSGenElectron_charge",

	# MC mu
	"n_FSGenMuon",
	"FSGenMuon_e",
	"FSGenMuon_mass",
	"FSGenMuon_pt",
	"FSGenMuon_p",
	"FSGenMuon_px",
	"FSGenMuon_py",
	"FSGenMuon_pz",
	"FSGenMuon_eta",
	"FSGenMuon_theta",
	"FSGenMuon_phi",
	"FSGenMuon_charge",

	# RECO k+
	"n_RecoKplus",
	"RecoKplus_e",
	"RecoKplus_mass",
	"RecoKplus_p",
	"RecoKplus_pt",
	"RecoKplus_px",
	"RecoKplus_py",
	"RecoKplus_pz",
	"RecoKplus_charge",

	# RECO gamma
	"n_RecoPhotons",
	"RecoPhoton_e",
	"RecoPhoton_p",
	"RecoPhoton_pt",
	"RecoPhoton_px",
	"RecoPhoton_py",
	"RecoPhoton_pz",

	# RECO e-
	"n_RecoElectrons",
	"RecoElectron_e",
	"RecoElectron_mass",
	"RecoElectron_p",
	"RecoElectron_pt",
	"RecoElectron_px",
	"RecoElectron_py",
	"RecoElectron_pz",
	"RecoElectron_charge",

	# RECO mu
	"n_RecoMuons",
	"RecoMuon_e",
	"RecoMuon_mass",
	"RecoMuon_p",
	"RecoMuon_pt",
	"RecoMuon_px",
	"RecoMuon_py",
	"RecoMuon_pz",
	"RecoMuon_charge",

	# RECO lepton
	"n_RecoLeptons",
	"RecoLepton_e",
	"RecoLepton_mass",
	"RecoLepton_p",
	"RecoLepton_pt",
	"RecoLepton_px",
	"RecoLepton_py",
	"RecoLepton_pz",
	"RecoLepton_charge",

	# RECO H
	"RecoHiggs_e",
	"RecoHiggs_mass",
	"RecoHiggs_p",
	"RecoHiggs_pt",
	"RecoHiggs_px",
	"RecoHiggs_py",
	"RecoHiggs_pz",
	"RecoHiggs_eta",
	"RecoHiggs_phi",

	# RECO IND k+
	"Kplus_0_m",
	"Kplus_0_e",
	"Kplus_0_p",
	"Kplus_0_pt",
	"Kplus_0_px",
	"Kplus_0_py",
	"Kplus_0_pz",
	"Kplus_0_eta",
	"Kplus_0_phi",

	"Kplus_1_m",
	"Kplus_1_e",
	"Kplus_1_p",
	"Kplus_1_pt",
	"Kplus_1_px",
	"Kplus_1_py",
	"Kplus_1_pz",
	"Kplus_1_eta",
	"Kplus_1_phi",

	"Kplus_2_m",
	"Kplus_2_e",
	"Kplus_2_p",
	"Kplus_2_pt",
	"Kplus_2_px",
	"Kplus_2_py",
	"Kplus_2_pz",
	"Kplus_2_eta",
	"Kplus_2_phi",

	"Kplus_3_m",
	"Kplus_3_e",
	"Kplus_3_p",
	"Kplus_3_pt",
	"Kplus_3_px",
	"Kplus_3_py",
	"Kplus_3_pz",
	"Kplus_3_eta",
	"Kplus_3_phi",

	# RECO Z
	"RecoZ_e",
	"RecoZ_mass",
	"RecoZ_p",
	"RecoZ_pt",
	"RecoZ_px",
	"RecoZ_py",
	"RecoZ_pz",
	"RecoZ_eta",
	"RecoZ_phi",

	# RECO IND lepton
	"Lepton_0_m",
	"Lepton_0_e",
	"Lepton_0_p",
	"Lepton_0_pt",
	"Lepton_0_px",
	"Lepton_0_py",
	"Lepton_0_pz",
	"Lepton_0_eta",
	"Lepton_0_phi",

	"Lepton_1_m",
	"Lepton_1_e",
	"Lepton_1_p",
	"Lepton_1_pt",
	"Lepton_1_px",
	"Lepton_1_py",
	"Lepton_1_pz",
	"Lepton_1_eta",
	"Lepton_1_phi",

	# RECO IND alp
	"alp_0_m",
	"alp_0_e",
	"alp_0_p",
	"alp_0_pt",
	"alp_0_px",
	"alp_0_py",
	"alp_0_pz",
	"alp_0_eta",
	"alp_0_phi",

	"alp_1_m",
	"alp_1_e",
	"alp_1_p",
	"alp_1_pt",
	"alp_1_px",
	"alp_1_py",
	"alp_1_pz",
	"alp_1_eta",
	"alp_1_phi",

	"RecoEmiss_e",
	"RecoEmiss_mass",
	"RecoEmiss_p",
	"RecoEmiss_pt",
	"RecoEmiss_px",
	"RecoEmiss_py",
	"RecoEmiss_pz",

	"RecoIP_Lxyz",
]

selections = {}
selections['HAlpAlp'] = ["RecoKaonElecSel", "RecoHiggsMassCut"]

extralabel = {}
extralabel["RecoKaonElecSel"] = "n_{K^{#pm}} = 4, n_{leptons} = 2"
extralabel["RecoHiggsMassCut"] = "m_{H} > 120 GeV"

##########
# SIGNAL #
##########

#   ALL_MASSES = ["0p05","0p1","0p5","1p0","1p5","5p0",
#                 "10p0","20p0","30p0","40p0","50p0","60p0"]
#   ALL_CTAUS  = ["1mm","10mm","1m","2m"]

masses = ["10p0", "30p0", "60p0"]
ctaus  = ["1mm", "1m"]

def _hex_from_hls(h_deg, l, s=0.65):
    h = (h_deg % 360) / 360.0
    r, g, b = colorsys.hls_to_rgb(h, l, s)
    return f"#{int(round(r*255)):02x}{int(round(g*255)):02x}{int(round(b*255)):02x}"

SIGNAL_HUE = 130  # green

def signal_color_hex(index, n_total):
    lightness = 0.20 + 0.55 * (index / (n_total - 1)) if n_total > 1 else 0.35
    return _hex_from_hls(SIGNAL_HUE, lightness, s=0.70)

colors = {}
legend = {}
plots = {}

plots['HAlpAlp'] = {'signal': {}, 'backgrounds': {}}

n_signal_total = len(masses) * len(ctaus)
idx = 0
for m in masses:
    for c in ctaus:
        key = f"ee_llH_HAlpAlp_m{m}_ctau{c}"
        proc_ee   = f"mgp8_ee_eeH_HAlpAlp_m{m}_ecm240_ctau{c}"
        proc_mumu = f"mgp8_ee_mumuH_HAlpAlp_m{m}_ecm240_ctau{c}"
        plots['HAlpAlp']['signal'][key] = [proc_ee, proc_mumu]
        colors[key] = ROOT.TColor.GetColor(signal_color_hex(idx, n_signal_total))
        legend[key] = f"e^{{+}}e^{{-}}#rightarrow l^{{+}}l^{{-}}H, m_{{a}}={m.replace('p','.')} GeV, c#tau={c}"
        idx += 1

#### Alternative: keep e/mu channels separate (2x the legend rows) ####

# idx = 0
# for m in masses:
#     for c in ctaus:
#         hexcode = signal_color_hex(idx, n_signal_total)
#
#         key_ee = f"ee_eeH_HAlpAlp_m{m}_ctau{c}"
#         proc_ee = f"mgp8_ee_eeH_HAlpAlp_m{m}_ecm240_ctau{c}"
#         plots['HAlpAlp']['signal'][key_ee] = [proc_ee]
#         colors[key_ee] = ROOT.TColor.GetColor(hexcode)
#         legend[key_ee] = f"e^{{+}}e^{{-}}#rightarrow e^{{+}}e^{{-}}H, m_{{a}}={m.replace('p','.')} GeV, c#tau={c}"
#
#         key_mumu = f"ee_mumuH_HAlpAlp_m{m}_ctau{c}"
#         proc_mumu = f"mgp8_ee_mumuH_HAlpAlp_m{m}_ecm240_ctau{c}"
#         plots['HAlpAlp']['signal'][key_mumu] = [proc_mumu]
#         colors[key_mumu] = ROOT.TColor.GetColor(hexcode)
#         legend[key_mumu] = f"e^{{+}}e^{{-}}#rightarrow #mu^{{+}}#mu^{{-}}H, m_{{a}}={m.replace('p','.')} GeV, c#tau={c}"
#         idx += 1

##############
# BACKGROUND #
##############

bkg_groups = {
    "WW":       ["p8_ee_WW_ecm240"],
    "ZZ":       ["p8_ee_ZZ_ecm240"],
    "Zqq":      ["p8_ee_Zqq_ecm240"],
    "Ztautau":  ["wzp6_ee_tautau_ecm240"],
    "Zmumu":    ["wzp6_ee_mumu_ecm240"],
    "Zee":      ["wzp6_ee_ee_Mee_30_150_ecm240"],
    "eeZ":      ["wzp6_egamma_eZ_Zmumu_ecm240", "wzp6_egamma_eZ_Zee_ecm240",
                 "wzp6_gammae_eZ_Zmumu_ecm240", "wzp6_gammae_eZ_Zee_ecm240"],
    "gaga":     ["wzp6_gaga_tautau_60_ecm240", "wzp6_gaga_mumu_60_ecm240",
                 "wzp6_gaga_ee_60_ecm240"],
    "nuenueZ":  ["wzp6_ee_nuenueZ_ecm240"],
}

zh_prefixes = ["tautauH", "nunuH", "eeH", "mumuH", "bbH", "ccH", "ssH", "qqH"]
zh_hdecays  = ["Htautau", "Hbb", "Hcc", "Hss", "Hgg", "HWW", "HZZ"]
bkg_groups["ZH_other"] = [
    f"wzp6_ee_{prefix}_{hdecay}_ecm240"
    for prefix in zh_prefixes
    for hdecay in zh_hdecays
]

petroff10_hex = [
    "#3f90da",  # blue
    "#ffa90e",  # amber
    "#bd1f01",  # red
    "#94a4a2",  # grey
    "#832db6",  # purple
    "#a96b59",  # brown
    "#e76300",  # orange
    "#b9ac70",  # khaki
    "#717581",  # grey
    "#92dadd",  # teal
]

bkg_colors_hex = dict(zip(bkg_groups.keys(), petroff10_hex))

bkg_colors_hex['ZZ'], bkg_colors_hex['Zqq'] = bkg_colors_hex['Zqq'], bkg_colors_hex['ZZ']

bkg_colors_hex['nuenueZ']  = "#b9ac70"
bkg_colors_hex['ZH_other'] = "#717581"

bkg_legend_labels = {
    "WW":       "e^{+}e^{-} #rightarrow WW",
    "ZZ":       "e^{+}e^{-} #rightarrow ZZ",
    "Zqq":      "e^{+}e^{-} #rightarrow Z #rightarrow q#bar{q}",
    "Ztautau":  "e^{+}e^{-} #rightarrow Z #rightarrow #tau^{+}#tau^{-}",
    "Zmumu":    "e^{+}e^{-} #rightarrow Z #rightarrow #mu^{+}#mu^{-}",
    "Zee":      "e^{+}e^{-} #rightarrow Z #rightarrow e^{+}e^{-}",
    "eeZ":      "e#gamma/#gamma e #rightarrow eZ",
    "gaga":     "#gamma#gamma #rightarrow f#bar{f}",
    "nuenueZ":  "e^{+}e^{-} #rightarrow #nu_{e}#bar{#nu}_{e}Z",
    "ZH_other": "Other",
}

plots['HAlpAlp']['backgrounds'] = bkg_groups
for key, hexcode in bkg_colors_hex.items():
    colors[key] = ROOT.TColor.GetColor(hexcode)
for key, label in bkg_legend_labels.items():
    legend[key] = label