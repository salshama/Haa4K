import ROOT

# global parameters
intLumi		= 10.8e6 #pb^-1

###If scaleSig=0 or scaleBack=0, we don't apply any additional scaling, on top of the normalization to cross section and integrated luminosity, as defined in finalSel.py
###If scaleSig or scaleBack is not defined, plots will be normalized to 1
# scaleSig		= 0.
# scaleBack		= 0.
ana_tex			= "e^{+}e^{-} #rightarrow Z, Z #rightarrow ZH, Z #rightarrow e^{+}e^{-}, H #rightarrow psps"
delphesVersion	= '3.4.2'
energy			= 240
collider 		= 'FCC-ee'
inputDir 		= '/ceph/salshamaily/h4k_FCCee/analysis/final_output/all_samples_112025/'
outdir			= '/ceph/salshamaily/h4k_FCCee/analysis/plots_output/all_samples_112025/'
formats			= ['png', 'pdf']
yaxis			= ['log', 'lin']
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

	#MC mu
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
	
	# RECO IND e-
	"Electron_0_m",
	"Electron_0_e",	
	"Electron_0_p",
	"Electron_0_pt",
	"Electron_0_px",
	"Electron_0_py",
	"Electron_0_pz",
	"Electron_0_eta",
	"Electron_0_phi",
	
	"Electron_1_m",
	"Electron_1_e",	
	"Electron_1_p",
	"Electron_1_pt",
	"Electron_1_px",
	"Electron_1_py",
	"Electron_1_pz",
	"Electron_1_eta",
	"Electron_1_phi",
	
	"RecoEmiss_e",
	"RecoEmiss_mass",
	"RecoEmiss_p",
	"RecoEmiss_pt",
	"RecoEmiss_px",
	"RecoEmiss_py",
	"RecoEmiss_pz",
	
	"RecoIP_Lxyz",
]

selections 			= {}
selections['Hpsps'] = ["NoCut", "KinematicCut"]

extralabel					= {}
extralabel['NoCut'] 		= "No Cut"
extralabel['KinematicCut']	= "Higgs mass > 120 GeV"

colors 				= {}
colors['HAlpAlp']	= ROOT.kGray+2
colors['Hpsps']		= ROOT.kBlack

colors['eeWW']		= ROOT.kPink+1
colors['eeZqq']		= ROOT.kPink+2
colors['eeZZ']		= ROOT.kPink+3

colors['eetautau']	= ROOT.kRed+1  
colors['eemumu']	= ROOT.kRed+2    
colors['eeMee']		= ROOT.kRed+3
          
colors['eeHtautau'] = ROOT.kBlue+1
colors['eeHbb']		= ROOT.kBlue+2
colors['eeHcc']		= ROOT.kBlue-1
colors['eeHss']		= ROOT.kBlue-2
colors['eeHgg']		= ROOT.kBlue-3
colors['eeHWW']		= ROOT.kBlue-4
colors['eeHZZ']		= ROOT.kBlue+3

colors['egammaZmumu']	= ROOT.kGreen+1
colors['egammaZee']		= ROOT.kGreen+2
colors['gammaeZmumu']	= ROOT.kGreen+3
colors['gammaeZee']		= ROOT.kGreen-2

colors['gagatautau']	= ROOT.kSpring-7
colors['gagamumu']		= ROOT.kSpring+3
colors['gagaee']		= ROOT.kSpring+9

colors['eenuenueZ']		= ROOT.kOrange+1
colors['eenunuHtautau']	= ROOT.kOrange+2
colors['eenunuHbb']		= ROOT.kOrange-1
colors['eenunuHcc']		= ROOT.kOrange-2
colors['eenunuHss']		= ROOT.kOrange-3
colors['eenunuHgg']		= ROOT.kOrange-4
colors['eenunuHWW']		= ROOT.kOrange+3
colors['eenunuHZZ']		= ROOT.kOrange-6

colors['eemumuHtautau']	= ROOT.kYellow+1
colors['eemumuHbb']		= ROOT.kYellow+2
colors['eemumuHcc']		= ROOT.kYellow-1
colors['eemumuHss']		= ROOT.kYellow-2
colors['eemumuHgg']		= ROOT.kYellow-7
colors['eemumuHWW']		= ROOT.kYellow-9
colors['eemumuHZZ']		= ROOT.kYellow+3

colors['eebbHtautau']	= ROOT.kMagenta+1
colors['eebbHbb']		= ROOT.kMagenta+2
colors['eebbHcc']		= ROOT.kMagenta-1
colors['eebbHss']		= ROOT.kMagenta-2
colors['eebbHgg']		= ROOT.kMagenta-3
colors['eebbHWW']		= ROOT.kMagenta-4
colors['eebbHZZ']		= ROOT.kMagenta+3

colors['eeccHtautau']	= ROOT.kViolet+1
colors['eeccHbb']		= ROOT.kViolet+2
colors['eeccHcc']		= ROOT.kViolet-1
colors['eeccHss']		= ROOT.kViolet-2
colors['eeccHgg']		= ROOT.kViolet-3
colors['eeccHWW']		= ROOT.kViolet-4
colors['eeccHZZ']		= ROOT.kViolet+3

colors['eessHtautau']	= ROOT.kCyan+1
colors['eessHbb']		= ROOT.kCyan+2
colors['eessHcc']		= ROOT.kCyan-1
colors['eessHss']		= ROOT.kCyan-2
colors['eessHgg']		= ROOT.kCyan-3
colors['eessHWW']		= ROOT.kCyan-4
colors['eessHZZ']		= ROOT.kCyan+3

colors['eeqqHtautau']	= ROOT.kTeal+1
colors['eeqqHbb']		= ROOT.kTeal+2
colors['eeqqHcc']		= ROOT.kTeal-1
colors['eeqqHss']		= ROOT.kTeal-2
colors['eeqqHgg']		= ROOT.kTeal-3
colors['eeqqHWW']		= ROOT.kTeal-4
colors['eeqqHZZ']		= ROOT.kTeal+3

plots 			= {}
plots['Hpsps'] = {'signal':{
					'Hpsps':['p8_ee_eeH_Hpsps_ecm240'],
					'HAlpAlp':['mgp8_ee_eeH_HAlpAlp'],},
				
				'backgrounds':{
					'eeWW':['p8_ee_WW_ecm240'],
					'eeZqq':['p8_ee_Zqq_ecm240'],
					'eeZZ':['p8_ee_ZZ_ecm240'],
					
					'eetautau':['wzp6_ee_tautau_ecm240'],
					'eemumu':['wzp6_ee_mumu_ecm240'],
					'eeMee':['wzp6_ee_ee_Mee_30_150_ecm240'],
					
					'eeHtautau':['wzp6_ee_tautauH_Htautau_ecm240'],
					'eeHbb':['wzp6_ee_tautauH_Hbb_ecm240'],
					'eeHcc':['wzp6_ee_tautauH_Hcc_ecm240'],
					'eeHss':['wzp6_ee_tautauH_Hss_ecm240'],
					'eeHgg':['wzp6_ee_tautauH_Hgg_ecm240'],
					'eeHWW':['wzp6_ee_tautauH_HWW_ecm240'],
					'eeHZZ':['wzp6_ee_tautauH_HZZ_ecm240'],
					
					'egammaZmumu':['wzp6_egamma_eZ_Zmumu_ecm240'],
					'egammaZee':['wzp6_egamma_eZ_Zee_ecm240'],
					'gammaeZmumu':['wzp6_gammae_eZ_Zmumu_ecm240'],
					'gammaeZee':['wzp6_gammae_eZ_Zee_ecm240'],
					
					'gagatautau':['wzp6_gaga_tautau_60_ecm240'],
					'gagamumu':['wzp6_gaga_mumu_60_ecm240'],
					'gagaee':['wzp6_gaga_ee_60_ecm240'],
					
					'eenuenueZ':['wzp6_ee_nuenueZ_ecm240'],
					'eenunuHtautau':['wzp6_ee_nunuH_Htautau_ecm240'],
					'eenunuHbb':['wzp6_ee_nunuH_Hbb_ecm240'],
					'eenunuHcc':['wzp6_ee_nunuH_Hcc_ecm240'],
					'eenunuHss':['wzp6_ee_nunuH_Hss_ecm240'],
					'eenunuHgg':['wzp6_ee_nunuH_Hgg_ecm240'],
					'eenunuHWW':['wzp6_ee_nunuH_HWW_ecm240'],
					'eenunuHZZ':['wzp6_ee_nunuH_HZZ_ecm240'],
					
					'eemumuHtautau':['wzp6_ee_mumuH_Htautau_ecm240'],
					'eemumuHbb':['wzp6_ee_mumuH_Hbb_ecm240'],
					'eemumuHcc':['wzp6_ee_mumuH_Hcc_ecm240'],
					'eemumuHss':['wzp6_ee_mumuH_Hss_ecm240'],
					'eemumuHgg':['wzp6_ee_mumuH_Hgg_ecm240'],
					'eemumuHWW':['wzp6_ee_mumuH_HWW_ecm240'],
					'eemumuHZZ':['wzp6_ee_mumuH_HZZ_ecm240'],
					
					'eebbHtautau':['wzp6_ee_bbH_Htautau_ecm240'],
					'eebbHbb':['wzp6_ee_bbH_Hbb_ecm240'],
					'eebbHcc':['wzp6_ee_bbH_Hcc_ecm240'],
					'eebbHss':['wzp6_ee_bbH_Hss_ecm240'],
					'eebbHgg':['wzp6_ee_bbH_Hgg_ecm240'],
					'eebbHWW':['wzp6_ee_bbH_HWW_ecm240'],
					'eebbHZZ':['wzp6_ee_bbH_HZZ_ecm240'],
					
					'eeccHtautau':['wzp6_ee_ccH_Htautau_ecm240'],
					'eeccHbb':['wzp6_ee_ccH_Hbb_ecm240'],
					'eeccHcc':['wzp6_ee_ccH_Hcc_ecm240'],
					'eeccHss':['wzp6_ee_ccH_Hss_ecm240'],
					'eeccHgg':['wzp6_ee_ccH_Hgg_ecm240'],
					'eeccHWW':['wzp6_ee_ccH_HWW_ecm240'],
					'eeccHZZ':['wzp6_ee_ccH_HZZ_ecm240'],
					
					'eessHtautau':['wzp6_ee_ssH_Htautau_ecm240'],
					'eessHbb':['wzp6_ee_ssH_Hbb_ecm240'],
					'eessHcc':['wzp6_ee_ssH_Hcc_ecm240'],
					'eessHss':['wzp6_ee_ssH_Hss_ecm240'],
					'eessHgg':['wzp6_ee_ssH_Hgg_ecm240'],
					'eessHWW':['wzp6_ee_ssH_HWW_ecm240'],
					'eessHZZ':['wzp6_ee_ssH_HZZ_ecm240'],
					
					'eeqqHtautau':['wzp6_ee_qqH_Htautau_ecm240'],
					'eeqqHbb':['wzp6_ee_qqH_Hbb_ecm240'],
					'eeqqHcc':['wzp6_ee_qqH_Hcc_ecm240'],
					'eeqqHss':['wzp6_ee_qqH_Hss_ecm240'],
					'eeqqHgg':['wzp6_ee_qqH_Hgg_ecm240'],
					'eeqqHWW':['wzp6_ee_qqH_HWW_ecm240'],
					'eeqqHZZ':['wzp6_ee_qqH_HZZ_ecm240']}}

legend 					= {}

legend['HAlpAlp']		= 'HAlpAlp'
legend['Hpsps']			= 'Hpsps'

legend['eeWW'] 			= 'eeWW'
legend['eeZZ'] 			= 'eeZZ'
legend['eeZqq'] 		= 'eeZqq'

legend['eetautau']  	= 'eetautau'
legend['eemumu']		= 'eemumu'
legend['eeMee']			= 'eeMee'

legend['eeHtautau'] 	= 'eeHtautau'
legend['eeHbb'] 		= 'eeHbb'
legend['eeHcc'] 		= 'eeHcc'
legend['eeHss'] 		= 'eeHss'
legend['eeHgg'] 		= 'eeHgg'
legend['eeHWW'] 		= 'eeHWW'
legend['eeHZZ'] 		= 'eeHZZ'

legend['egammaZmumu']	= 'egammaZmumu'
legend['egammaZee'] 	= 'egammaZee'
legend['gammaeZmumu'] 	= 'gammaeZmumu'
legend['gammaeZee'] 	= 'gammaeZee'

legend['gagatautau']	= 'gagatautau'
legend['gagamumu']		= 'gagamumu'
legend['gagaee']		= 'gagaee'

legend['eenuenueZ']		= 'eenuenueZ'
legend['eenunuHtautau']	= 'eenunuHtautau'
legend['eenunuHbb']		= 'eenunuHbb'
legend['eenunuHcc']		= 'eenunuHcc'
legend['eenunuHss']		= 'eenunuHss'
legend['eenunuHgg']		= 'eenunuHgg'
legend['eenunuHWW']		= 'eenunuHWW'
legend['eenunuHZZ']		= 'eenunuHZZ'

legend['eemumuHtautau']	= 'eemumuHtautau'
legend['eemumuHbb']		= 'eemumuHbb'
legend['eemumuHcc']		= 'eemumuHcc'
legend['eemumuHss']		= 'eemumuHss'
legend['eemumuHgg']		= 'eemumuHgg'
legend['eemumuHWW']		= 'eemumuHWW'
legend['eemumuHZZ']		= 'eemumuHZZ'

legend['eebbHtautau']	= 'eebbHtautau'
legend['eebbHbb']		= 'eebbHbb'
legend['eebbHcc']		= 'eebbHcc'
legend['eebbHss']		= 'eebbHss'
legend['eebbHgg']		= 'eebbHgg'
legend['eebbHWW']		= 'eebbHWW'
legend['eebbHZZ']		= 'eebbHZZ'

legend['eeccHtautau']	= 'eeccHtautau'
legend['eeccHbb']		= 'eeccHbb'
legend['eeccHcc']		= 'eeccHcc'
legend['eeccHss']		= 'eeccHss'
legend['eeccHgg']		= 'eeccHgg'
legend['eeccHWW']		= 'eeccHWW'
legend['eeccHZZ']		= 'eeccHZZ'

legend['eessHtautau']	= 'eessHtautau'
legend['eessHbb']		= 'eessHbb'
legend['eessHcc']		= 'eessHcc'
legend['eessHss']		= 'eessHss'
legend['eessHgg']		= 'eessHgg'
legend['eessHWW']		= 'eessHWW'
legend['eessHZZ']		= 'eessHZZ'

legend['eeqqHtautau']	= 'eeqqHtautau'
legend['eeqqHbb']		= 'eeqqHbb'
legend['eeqqHcc']		= 'eeqqHcc'
legend['eeqqHss']		= 'eeqqHss'
legend['eeqqHgg']		= 'eeqqHgg'
legend['eeqqHWW']		= 'eeqqHWW'
legend['eeqqHZZ']		= 'eeqqHZZ'