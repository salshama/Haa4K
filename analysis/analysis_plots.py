import ROOT

# global parameters
intLumi		= 108e6 #pb^-1

###If scaleSig=0 or scaleBack=0, we don't apply any additional scaling, on top of the normalization to cross section and integrated luminosity, as defined in finalSel.py
###If scaleSig or scaleBack is not defined, plots will be normalized to 1
# scaleSig		= 0.
# scaleBack		= 0.
ana_tex			= "e^{+}e^{-} #rightarrow Z, Z #rightarrow ZH, Z #rightarrow e^{+}e^{-}, H #rightarrow psps"
delphesVersion	= '3.4.2'
energy			= 240
collider 		= 'FCC-ee'
inputDir 		= '/ceph/salshamaily/h4k_FCCee/analysis/final_output/all_samples_102025/'
outdir			= '/ceph/salshamaily/h4k_FCCee/analysis/plots_output/all_samples_102025'
formats			= ['png', 'pdf']
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
	"Jets_kt2_e",		
	"Jets_kt2_mass",	
	"Jets_kt2_p",		
	"Jets_kt2_pt",		
	"Jets_kt2_px",		
	"Jets_kt2_py",		
	"Jets_kt2_pz",		
	"Jets_kt2_eta",		
	"Jets_kt2_theta",	
	"Jets_kt2_phi",
	"n_Jets_kt2_constituents",
	"n_Jets_kt2_charged_constituents",
	"n_Jets_kt2_neutral_constituents",
	"n_Jets_kt2",
	
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
]

selections = {}
# selections['HAlpAlp']	= ["NoCut"]
selections['Hpsps']		= ["NoCut"]
selections['eeWW']		= ["NoCut"]
selections['ee_Zqq']	= ["NoCut"]
selections['ee_ZZ']		= ["NoCut"]

extralabel 			= {}
extralabel['NoCut']	= "No cut"

colors 				= {}
# colors['HAlpAlp']	= ROOT.kRed-5
colors['Hpsps']		= ROOT.kBlue-5
colors['eeWW']		= ROOT.kMagenta-5
colors['eeZqq']		= ROOT.kRed-5
colors['eeZZ']		= ROOT.kGreen-5

plots = {}
plots['Hpsps'] = {'signal':{
					'Hpsps':['p8_ee_eeH_Hpsps_ecm240']},
				
				'backgrounds':{
					'eeWW':['pp8_ee_WW_ecm240'],
					'eeZqq':['p8_ee_Zqq_ecm240'],
					'eeZZ':['p8_ee_ZZ_ecm240'],}}

legend 				= {}
# legend['HAlpAlp']	= 'HAlpAlp'
legend['Hpsps']		= 'Hpsps'
legend['eeWW'] 		= 'eeWW'
legend['eeZZ'] 		= 'eeZZ'
legend['eeZqq'] 	= 'eeZqq'
