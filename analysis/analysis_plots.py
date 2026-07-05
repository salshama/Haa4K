import ROOT
import colorsys

# global parameters
intLumi		= 10.8e6 #pb^-1

###If scaleSig=0 or scaleBack=0, we don't apply any additional scaling, on top of the normalization to cross section and integrated luminosity, as defined in finalSel.py
###If scaleSig or scaleBack is not defined, plots will be normalized to 1
# scaleSig		= 0.
# scaleBack		= 0.
ana_tex			= "e^{+}e^{-} #rightarrow Z #rightarrow ZH, H #rightarrow aa"
delphesVersion	= '3.4.2'
energy			= 240
collider 		= 'FCC-ee'
inputDir 		= '/ceph/salshamaily/haa4K_FCCee/analysis/final_output/only_signal_mgp8sig_norwt_062026/'
outdir			= '/ceph/salshamaily/haa4K_FCCee/analysis/plots_output/only_signal_mgp8sig_norwt_062026/'
formats			= ['png','pdf']
yaxis			= ['log']
stacksig		= ['nostack']
stackbkg		= ['stack']
# legendCoord	= [0.68,0.76,0.96,0.88]
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
	
	# JETS
# 	"Jets_kt2_e",		
# 	"Jets_kt2_mass",	
# 	"Jets_kt2_p",		
# 	"Jets_kt2_pt",		
# 	"Jets_kt2_px",		
# 	"Jets_kt2_py",		
# 	"Jets_kt2_pz",		
# 	"Jets_kt2_eta",		
# 	"Jets_kt2_theta",	
# 	"Jets_kt2_phi",
# 	"n_Jets_kt2_constituents",
# 	"n_Jets_kt2_charged_constituents",
# 	"n_Jets_kt2_neutral_constituents",
# 	"n_Jets_kt2",
	
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
	
	"RecoEmiss_e",
	"RecoEmiss_mass",
	"RecoEmiss_p",
	"RecoEmiss_pt",
	"RecoEmiss_px",
	"RecoEmiss_py",
	"RecoEmiss_pz",
	
	"RecoIP_Lxyz",
]

selections	= {}
extralabel	= {}
colors 		= {}
legend 		= {}
plots  		= {}

selections['HAlpAlp']			= ["RecoKaonElecSel", "RecoHiggsMassCut"]
extralabel['RecoKaonElecSel']	= "Reco kaon and lepton selection"
extralabel['RecoHiggsMassCut']	= "Higgs mass > 120 GeV"
plots['HAlpAlp']				= {'signal': {}, 'backgrounds': {}}

###############
# BACKGROUNDS #
###############
# bkg_proc = {
# 	# key               : (sample name,                       color,             				legend text)
# 	'eeWW':             ('p8_ee_WW_ecm240',                   ROOT.TColor.GetColor('#d9f0d3'), 'ee #rightarrow WW'),
# 	'eeZqq':            ('p8_ee_Zqq_ecm240',                  ROOT.TColor.GetColor('#1b7837'), 'ee #rightarrow Z #rightarrow qq'),
# 	'eeZZ':             ('p8_ee_ZZ_ecm240',                   ROOT.TColor.GetColor('#7fbf7b'), 'ee #rightarrow ZZ'),
# 
# 	'eetautau':         ('wzp6_ee_tautau_ecm240',              ROOT.kRed+1, 'ee #rightarrow #tau^{+}#tau^{-}'),
# 	'eemumu':           ('wzp6_ee_mumu_ecm240',                ROOT.kRed+2, 'ee #rightarrow #mu^{+}#mu^{-}'),
# 	'eeMee':            ('wzp6_ee_ee_Mee_30_150_ecm240',       ROOT.kRed+3, 'ee #rightarrow ee, 30<M_{ee}<150 GeV'),
# 
# 	'eeHtautau':        ('wzp6_ee_tautauH_Htautau_ecm240',     ROOT.kBlue+1, '#tau#tau H, H #rightarrow #tau#tau'),
# 	'eeHbb':            ('wzp6_ee_tautauH_Hbb_ecm240',         ROOT.kBlue+2, '#tau#tau H, H #rightarrow b#bar{b}'),
# 	'eeHcc':            ('wzp6_ee_tautauH_Hcc_ecm240',         ROOT.kBlue-1, '#tau#tau H, H #rightarrow c#bar{c}'),
# 	'eeHss':            ('wzp6_ee_tautauH_Hss_ecm240',         ROOT.kBlue-2, '#tau#tau H, H #rightarrow s#bar{s}'),
# 	'eeHgg':            ('wzp6_ee_tautauH_Hgg_ecm240',         ROOT.kBlue-3, '#tau#tau H, H #rightarrow gg'),
# 	'eeHWW':            ('wzp6_ee_tautauH_HWW_ecm240',         ROOT.kBlue-4, '#tau#tau H, H #rightarrow WW'),
# 	'eeHZZ':            ('wzp6_ee_tautauH_HZZ_ecm240',         ROOT.kBlue+3, '#tau#tau H, H #rightarrow ZZ'),
# 
# 	'egammaZmumu':      ('wzp6_egamma_eZ_Zmumu_ecm240',        ROOT.kGreen+1, 'e#gamma #rightarrow eZ, Z #rightarrow #mu#mu'),
# 	'egammaZee':        ('wzp6_egamma_eZ_Zee_ecm240',          ROOT.kGreen+2, 'e#gamma #rightarrow eZ, Z #rightarrow ee'),
# 	'gammaeZmumu':      ('wzp6_gammae_eZ_Zmumu_ecm240',        ROOT.kGreen+3, '#gamma e #rightarrow eZ, Z #rightarrow #mu#mu'),
# 	'gammaeZee':        ('wzp6_gammae_eZ_Zee_ecm240',          ROOT.kGreen-2, '#gamma e #rightarrow eZ, Z #rightarrow ee'),
# 
# 	'gagatautau':       ('wzp6_gaga_tautau_60_ecm240',         ROOT.kSpring-7, '#gamma#gamma #rightarrow #tau#tau'),
# 	'gagamumu':         ('wzp6_gaga_mumu_60_ecm240',           ROOT.kSpring+3, '#gamma#gamma #rightarrow #mu#mu'),
# 	'gagaee':           ('wzp6_gaga_ee_60_ecm240',             ROOT.kSpring+9, '#gamma#gamma #rightarrow ee'),
# 
# 	'eenuenueZ':        ('wzp6_ee_nuenueZ_ecm240',             ROOT.kOrange+1, 'ee #rightarrow #nu_{e}#bar{#nu}_{e}Z'),
# 	'eenunuHtautau':    ('wzp6_ee_nunuH_Htautau_ecm240',       ROOT.kOrange+2, '#nu#nu H, H #rightarrow #tau#tau'),
# 	'eenunuHbb':        ('wzp6_ee_nunuH_Hbb_ecm240',           ROOT.kOrange-1, '#nu#nu H, H #rightarrow b#bar{b}'),
# 	'eenunuHcc':        ('wzp6_ee_nunuH_Hcc_ecm240',           ROOT.kOrange-2, '#nu#nu H, H #rightarrow c#bar{c}'),
# 	'eenunuHss':        ('wzp6_ee_nunuH_Hss_ecm240',           ROOT.kOrange-3, '#nu#nu H, H #rightarrow s#bar{s}'),
# 	'eenunuHgg':        ('wzp6_ee_nunuH_Hgg_ecm240',           ROOT.kOrange-4, '#nu#nu H, H #rightarrow gg'),
# 	'eenunuHWW':        ('wzp6_ee_nunuH_HWW_ecm240',           ROOT.kOrange+3, '#nu#nu H, H #rightarrow WW'),
# 	'eenunuHZZ':        ('wzp6_ee_nunuH_HZZ_ecm240',           ROOT.kOrange-6, '#nu#nu H, H #rightarrow ZZ'),
# 
# 	'eemumuHtautau':    ('wzp6_ee_mumuH_Htautau_ecm240',       ROOT.kYellow+1, '#mu#mu H, H #rightarrow #tau#tau'),
# 	'eemumuHbb':        ('wzp6_ee_mumuH_Hbb_ecm240',           ROOT.kYellow+2, '#mu#mu H, H #rightarrow b#bar{b}'),
# 	'eemumuHcc':        ('wzp6_ee_mumuH_Hcc_ecm240',           ROOT.kYellow-1, '#mu#mu H, H #rightarrow c#bar{c}'),
# 	'eemumuHss':        ('wzp6_ee_mumuH_Hss_ecm240',           ROOT.kYellow-2, '#mu#mu H, H #rightarrow s#bar{s}'),
# 	'eemumuHgg':        ('wzp6_ee_mumuH_Hgg_ecm240',           ROOT.kYellow-7, '#mu#mu H, H #rightarrow gg'),
# 	'eemumuHWW':        ('wzp6_ee_mumuH_HWW_ecm240',           ROOT.kYellow-9, '#mu#mu H, H #rightarrow WW'),
# 	'eemumuHZZ':        ('wzp6_ee_mumuH_HZZ_ecm240',           ROOT.kYellow+3, '#mu#mu H, H #rightarrow ZZ'),
# 
# 	'eebbHtautau':      ('wzp6_ee_bbH_Htautau_ecm240',         ROOT.kMagenta+1, 'b#bar{b} H, H #rightarrow #tau#tau'),
# 	'eebbHbb':          ('wzp6_ee_bbH_Hbb_ecm240',             ROOT.kMagenta+2, 'b#bar{b} H, H #rightarrow b#bar{b}'),
# 	'eebbHcc':          ('wzp6_ee_bbH_Hcc_ecm240',             ROOT.kMagenta-1, 'b#bar{b} H, H #rightarrow c#bar{c}'),
# 	'eebbHss':          ('wzp6_ee_bbH_Hss_ecm240',             ROOT.kMagenta-2, 'b#bar{b} H, H #rightarrow s#bar{s}'),
# 	'eebbHgg':          ('wzp6_ee_bbH_Hgg_ecm240',             ROOT.kMagenta-3, 'b#bar{b} H, H #rightarrow gg'),
# 	'eebbHWW':          ('wzp6_ee_bbH_HWW_ecm240',             ROOT.kMagenta-4, 'b#bar{b} H, H #rightarrow WW'),
# 	'eebbHZZ':          ('wzp6_ee_bbH_HZZ_ecm240',             ROOT.kMagenta+3, 'b#bar{b} H, H #rightarrow ZZ'),
# 
# 	'eeccHtautau':      ('wzp6_ee_ccH_Htautau_ecm240',         ROOT.kViolet+1, 'c#bar{c} H, H #rightarrow #tau#tau'),
# 	'eeccHbb':          ('wzp6_ee_ccH_Hbb_ecm240',             ROOT.kViolet+2, 'c#bar{c} H, H #rightarrow b#bar{b}'),
# 	'eeccHcc':          ('wzp6_ee_ccH_Hcc_ecm240',             ROOT.kViolet-1, 'c#bar{c} H, H #rightarrow c#bar{c}'),
# 	'eeccHss':          ('wzp6_ee_ccH_Hss_ecm240',             ROOT.kViolet-2, 'c#bar{c} H, H #rightarrow s#bar{s}'),
# 	'eeccHgg':          ('wzp6_ee_ccH_Hgg_ecm240',             ROOT.kViolet-3, 'c#bar{c} H, H #rightarrow gg'),
# 	'eeccHWW':          ('wzp6_ee_ccH_HWW_ecm240',             ROOT.kViolet-4, 'c#bar{c} H, H #rightarrow WW'),
# 	'eeccHZZ':          ('wzp6_ee_ccH_HZZ_ecm240',             ROOT.kViolet+3, 'c#bar{c} H, H #rightarrow ZZ'),
# 
# 	'eessHtautau':      ('wzp6_ee_ssH_Htautau_ecm240',         ROOT.kCyan+1, 's#bar{s} H, H #rightarrow #tau#tau'),
# 	'eessHbb':          ('wzp6_ee_ssH_Hbb_ecm240',             ROOT.kCyan+2, 's#bar{s} H, H #rightarrow b#bar{b}'),
# 	'eessHcc':          ('wzp6_ee_ssH_Hcc_ecm240',             ROOT.kCyan-1, 's#bar{s} H, H #rightarrow c#bar{c}'),
# 	'eessHss':          ('wzp6_ee_ssH_Hss_ecm240',             ROOT.kCyan-2, 's#bar{s} H, H #rightarrow s#bar{s}'),
# 	'eessHgg':          ('wzp6_ee_ssH_Hgg_ecm240',             ROOT.kCyan-3, 's#bar{s} H, H #rightarrow gg'),
# 	'eessHWW':          ('wzp6_ee_ssH_HWW_ecm240',             ROOT.kCyan-4, 's#bar{s} H, H #rightarrow WW'),
# 	'eessHZZ':          ('wzp6_ee_ssH_HZZ_ecm240',             ROOT.kCyan+3, 's#bar{s} H, H #rightarrow ZZ'),
# 
# 	'eeqqHtautau':      ('wzp6_ee_qqH_Htautau_ecm240',         ROOT.kTeal+1, 'q#bar{q} H, H #rightarrow #tau#tau'),
# 	'eeqqHbb':          ('wzp6_ee_qqH_Hbb_ecm240',             ROOT.kTeal+2, 'q#bar{q} H, H #rightarrow b#bar{b}'),
# 	'eeqqHcc':          ('wzp6_ee_qqH_Hcc_ecm240',             ROOT.kTeal-1, 'q#bar{q} H, H #rightarrow c#bar{c}'),
# 	'eeqqHss':          ('wzp6_ee_qqH_Hss_ecm240',             ROOT.kTeal-2, 'q#bar{q} H, H #rightarrow s#bar{s}'),
# 	'eeqqHgg':          ('wzp6_ee_qqH_Hgg_ecm240',             ROOT.kTeal-3, 'q#bar{q} H, H #rightarrow gg'),
# 	'eeqqHWW':          ('wzp6_ee_qqH_HWW_ecm240',             ROOT.kTeal-4, 'q#bar{q} H, H #rightarrow WW'),
# 	'eeqqHZZ':          ('wzp6_ee_qqH_HZZ_ecm240',             ROOT.kTeal+3, 'q#bar{q} H, H #rightarrow ZZ'),
# }
# 
# for key, (sample, color, leg) in bkg_proc.items():
# 	plots['HAlpAlp']['backgrounds'][key] = [sample]
# 	colors[key] = color
# 	legend[key] = leg

# placeholder so no empty bkg list
plots['HAlpAlp']['backgrounds']['placeholder'] = ['mgp8_ee_eeH_HAlpAlp_m0p1_cah1em2_ecm240']
colors['placeholder'] = ROOT.kGray
legend['placeholder'] = 'placeholder'

###########
# SIGNALS #
###########
masses          = ['10p0']
mass_labels     = {'0p05': '0.05', '0p1': '0.1', '0p5': '0.5', '1p0': '1', '1p5': '1.5', '5p0': '5', '10p0': '10', '20p0': '20', '30p0': '30'}

couplings       = ['cah1em1', 'cah1em2', 'cah1em3', 'cah1em4', 'cah1em5', 'cah1em6']
coupling_labels = {c: f'10^{{-{i+1}}}' for i, c in enumerate(couplings)}

finalstates     		= {'ee': 'e^{+}e^{-}', 'mumu': '#mu^{+}#mu^{-}'}#, 'qq': 'q#bar{q}'}
finalstate_basecolor	= {'ee': '#2b8cbe', 'mumu': '#fdae6b'}#, 'qq': '#762a83'

def _hex_to_rgb01(hexcode):
	hexcode = hexcode.lstrip('#')
	return tuple(int(hexcode[i:i+2], 16) / 255.0 for i in (0, 2, 4))

for fs, fs_tex in finalstates.items():
	base_r, base_g, base_b = _hex_to_rgb01(finalstate_basecolor[fs])
	base_h, base_s, base_v = colorsys.rgb_to_hsv(base_r, base_g, base_b)

	for i, mass in enumerate(masses):
		# small hue nudge per mass so overlapping mass points are distinguishable
		hue = (base_h + 0.01 * i) % 1.0

		for n, cah in enumerate(couplings):
			key    		= f"{fs}H_m{mass}_{cah}"
			sample 		= f"mgp8_ee_{fs}H_HAlpAlp_m{mass}_{cah}_ecm240"
			legend[key] = f"Z #rightarrow {fs_tex}, m_{{a}}={mass_labels[mass]} GeV, cah={coupling_labels[cah]}"

			# coupling controls shade within the same hue
			val 		= 0.35 + 0.55 * (n / (len(couplings) - 1))
			r, g, b 	= colorsys.hsv_to_rgb(hue, base_s, val)
			colors[key] = ROOT.TColor.GetColor(r, g, b)
			plots['HAlpAlp']['signal'][key] = [sample]