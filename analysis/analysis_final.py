#Input directory where the files produced at the stage1 level are
inputDir = "/ceph/salshamaily/h4k_FCCee/samples"

#Output directory where the files produced at the final-selection level are
outputDir = "/ceph/salshamaily/h4k_FCCee/analysis/final_output/all_samples_112025"

#Integrated luminosity for scaling number of events (required only if setting doScale to true)
intLumi = 10.8e6 #pb^-1

#Scale event yields by intLumi and cross section (optional)
# if scaling, both the number of events in the table and in the histograms will be scaled
doScale = True

#Save event yields in a table (optional)
saveTabular = True

#produces ROOT TTrees, default is False
doTree = False

# list of processes
processList = {
	"mgp8_ee_eeH_HAlpAlp":		{},
	"p8_ee_eeH_Hpsps_ecm240":	{},
	
	"p8_ee_WW_ecm240":			{},
	"p8_ee_Zqq_ecm240":			{},
	"p8_ee_ZZ_ecm240":			{},
	
	"wzp6_ee_tautau_ecm240":		{},
    "wzp6_ee_mumu_ecm240":			{},
    "wzp6_ee_ee_Mee_30_150_ecm240":	{},

    "wzp6_ee_tautauH_Htautau_ecm240":	{},
    "wzp6_ee_tautauH_Hbb_ecm240":		{},
    "wzp6_ee_tautauH_Hcc_ecm240":		{},
    "wzp6_ee_tautauH_Hss_ecm240":		{},
    "wzp6_ee_tautauH_Hgg_ecm240":		{},
    "wzp6_ee_tautauH_HWW_ecm240":		{},
    "wzp6_ee_tautauH_HZZ_ecm240":		{},

    "wzp6_egamma_eZ_Zmumu_ecm240":	{},
    "wzp6_egamma_eZ_Zee_ecm240":	{},
    "wzp6_gammae_eZ_Zmumu_ecm240":	{},
    "wzp6_gammae_eZ_Zee_ecm240":	{},

    "wzp6_gaga_tautau_60_ecm240":	{},
    "wzp6_gaga_mumu_60_ecm240":		{},
    "wzp6_gaga_ee_60_ecm240":		{},

    "wzp6_ee_nuenueZ_ecm240":		{},
    "wzp6_ee_nunuH_Htautau_ecm240":	{},
    "wzp6_ee_nunuH_Hbb_ecm240":		{},
    "wzp6_ee_nunuH_Hcc_ecm240":		{},
    "wzp6_ee_nunuH_Hss_ecm240":		{},
    "wzp6_ee_nunuH_Hgg_ecm240":		{},
    "wzp6_ee_nunuH_HWW_ecm240":		{},
    "wzp6_ee_nunuH_HZZ_ecm240":		{},

    "wzp6_ee_eeH_Htautau_ecm240":	{},
    "wzp6_ee_eeH_Hbb_ecm240":		{},
    "wzp6_ee_eeH_Hcc_ecm240":		{},
    "wzp6_ee_eeH_Hss_ecm240":		{},
    "wzp6_ee_eeH_Hgg_ecm240":		{},
    "wzp6_ee_eeH_HWW_ecm240":		{},
    "wzp6_ee_eeH_HZZ_ecm240":		{},

    "wzp6_ee_mumuH_Htautau_ecm240":	{},
    "wzp6_ee_mumuH_Hbb_ecm240":		{},
    "wzp6_ee_mumuH_Hcc_ecm240":		{},
    "wzp6_ee_mumuH_Hss_ecm240":		{},
    "wzp6_ee_mumuH_Hgg_ecm240":		{},
    "wzp6_ee_mumuH_HWW_ecm240":		{},
    "wzp6_ee_mumuH_HZZ_ecm240":		{},

    "wzp6_ee_bbH_Htautau_ecm240":	{},
    "wzp6_ee_bbH_Hbb_ecm240":		{},
    "wzp6_ee_bbH_Hcc_ecm240":		{},
    "wzp6_ee_bbH_Hss_ecm240":		{},
    "wzp6_ee_bbH_Hgg_ecm240":		{},
    "wzp6_ee_bbH_HWW_ecm240":		{},
    "wzp6_ee_bbH_HZZ_ecm240":		{},

    "wzp6_ee_ccH_Htautau_ecm240":	{},
    "wzp6_ee_ccH_Hbb_ecm240":		{},
    "wzp6_ee_ccH_Hcc_ecm240":		{},
    "wzp6_ee_ccH_Hss_ecm240":		{},
    "wzp6_ee_ccH_Hgg_ecm240":		{},
    "wzp6_ee_ccH_HWW_ecm240":		{},
    "wzp6_ee_ccH_HZZ_ecm240":		{},

    "wzp6_ee_ssH_Htautau_ecm240":	{},
    "wzp6_ee_ssH_Hbb_ecm240":		{},
    "wzp6_ee_ssH_Hcc_ecm240":		{},
    "wzp6_ee_ssH_Hss_ecm240":		{},
    "wzp6_ee_ssH_Hgg_ecm240":		{},
    "wzp6_ee_ssH_HWW_ecm240":		{},
    "wzp6_ee_ssH_HZZ_ecm240":		{},

    "wzp6_ee_qqH_Htautau_ecm240":	{},
    "wzp6_ee_qqH_Hbb_ecm240":		{},
    "wzp6_ee_qqH_Hcc_ecm240":		{},
    "wzp6_ee_qqH_Hss_ecm240":		{},
    "wzp6_ee_qqH_Hgg_ecm240":		{},
    "wzp6_ee_qqH_HWW_ecm240":		{},
    "wzp6_ee_qqH_HZZ_ecm240":		{},
}

#Dictionary for prettier names of processes (optional)
# change them if you want but they don't do anything
processLabels = {
	"mgp8_ee_eeH_HAlpAlp":		"H $/rightarrow$ AlpAlp",
	"p8_ee_eeH_Hpsps_ecm240":	"H $\rightarrow$ psps",
	"p8_ee_WW_ecm240":			"ee $\rightarrow$ WW",
	"p8_ee_Zqq_ecm240":			"ee $\rightarrow$ Zqq",
	"p8_ee_ZZ_ecm240":			"ee $\rightarrow$ ZZ",
}

#Link to the dictonary that contains all the cross section information, etc
procDict = "FCCee_procDict_winter2023_IDEA.json"

#Add provate samples as it is not an offical process
procDictAdd = {
	"mgp8_ee_eeH_HAlpAlp":		{"numberOfEvents": 100000, "sumOfWeights": 100000, "crossSection": 0.00095, "kfactor": 1.0, "matchingEfficiency": 1.0},
	"p8_ee_eeH_Hpsps_ecm240":	{"numberOfEvents": 500000, "sumOfWeights": 500000, "crossSection": 0.00095, "kfactor": 1.0, "matchingEfficiency": 1.0},
}
	
#Dictionary of the list of cuts. The key is the name of the selection that will be added to the output file
cutList = {
	### no selection, just builds the histograms, it will not be shown in the latex table
	"NoCut":			"1>0",
	"KinematicCut":		"RecoHiggs_mass>120",
}

#Dictionary of the labels of cuts.
cutLabels = {
	"NoCut":			"No cut",
	"KinematicCut":		"Higgs mass > 120 GeV",
}

#Dictionary for the ouput variable/hitograms.
histoList = {
	
	# MC k+
	"n_GenKplus":		{"name":"n_GenKplus",		"title":"Number of MC K+",		"bin":50,	"xmin":0,	"xmax":10},
	"GenKplus_e":		{"name":"GenKplus_e",		"title":"Energy of MC K+",		"bin":50,	"xmin":0,	"xmax":100},
	"GenKplus_mass":	{"name":"GenKplus_mass",	"title":"Mass of MC K+",		"bin":50,	"xmin":0,	"xmax":1},
	"GenKplus_pt":		{"name":"GenKplus_pt",		"title":"$\p_{t}$ of MC K+",	"bin":50,	"xmin":0,	"xmax":110},
	"GenKplus_p":		{"name":"GenKplus_p",		"title":"Momentum of MC K+", 	"bin":50,	"xmin":0,	"xmax":100},
	"GenKplus_px":		{"name":"GenKplus_px", 		"title":"$\p_{x}$ of MC K+", 	"bin":50,	"xmin":0,	"xmax":100},
	"GenKplus_py":		{"name":"GenKplus_py", 		"title":"$\p_{y}$ of MC K+",	"bin":50,	"xmin":0,	"xmax":100},
	"GenKplus_pz":		{"name":"GenKplus_pz", 		"title":"$\p_{z}$ of MC K+",	"bin":50,	"xmin":0,	"xmax":100},
	"GenKplus_eta":		{"name":"GenKplus_eta",		"title":"Eta of MC K+",			"bin":50,	"xmin":-4,	"xmax":3},
	"GenKplus_theta":	{"name":"GenKplus_theta",	"title":"Theta of MC K+",		"bin":50,	"xmin":0,	"xmax":4},
	"GenKplus_phi":		{"name":"GenKplus_phi",		"title":"Phi of MC K+",			"bin":50,	"xmin":-4,	"xmax":4},
	"GenKplus_charge":	{"name":"GenKplus_charge",	"title":"Charge of MC K+",		"bin":50,	"xmin":0,	"xmax":2},
	
	# MC gamma
	"n_FSGenPhoton":		{"name":"n_FSGenPhoton",		"title":"Number of MC Photons",		"bin":50,	"xmin":0,	"xmax":20},
	"FSGenPhoton_e":		{"name":"FSGenPhoton_e",		"title":"Energy of MC Photons",		"bin":50,	"xmin":0,	"xmax":80},
	"FSGenPhoton_pt":		{"name":"FSGenPhoton_pt",		"title":"$\p_{t}$ of MC Photons",	"bin":50,	"xmin":0,	"xmax":90},
	"FSGenPhoton_p":		{"name":"FSGenPhoton_p",		"title":"Momentum of MC Photons",	"bin":50,	"xmin":0,	"xmax":90},
	"FSGenPhoton_px":		{"name":"FSGenPhoton_px",		"title":"$\p_{x}$ of MC Photons",	"bin":50,	"xmin":0,	"xmax":80},
	"FSGenPhoton_py":		{"name":"FSGenPhoton_py",		"title":"$\p_{y}$ of MC Photons",	"bin":50,	"xmin":0,	"xmax":80},
	"FSGenPhoton_pz":		{"name":"FSGenPhoton_pz",		"title":"$\p_{z}$ of MC Photons", 	"bin":50,	"xmin":0,	"xmax":80},
	"FSGenPhoton_eta":		{"name":"FSGenPhoton_eta",		"title":"Eta of MC Photons",		"bin":50,	"xmin":-4,	"xmax":4},
	"FSGenPhoton_theta":	{"name":"FSGenPhoton_theta",	"title":"Theta of MC Photons", 		"bin":50,	"xmin":0,	"xmax":4},
	"FSGenPhoton_phi":		{"name":"FSGenPhoton_phi",		"title":"Phi of MC Photons", 		"bin":50,	"xmin":-4,	"xmax":4},
	
	# MC e-
	"n_FSGenElectron":	  	{"name":"n_FSGenElectron",		"title":"Number of MC Electrons",	"bin":50,	"xmin":0,	"xmax":10},
	"FSGenElectron_e":		{"name":"FSGenElectron_e",		"title":"Energy of MC Electrons",	"bin":50,	"xmin":0,	"xmax":90},
	"FSGenElectron_mass":	{"name":"FSGenElectron_mass",	"title":"Mass of MC Electrons",		"bin":50,	"xmin":0,	"xmax":1},
	"FSGenElectron_pt":  	{"name":"FSGenElectron_pt",		"title":"$\p_{t}$ of MC Electrons",	"bin":50,	"xmin":0,	"xmax":90},
	"FSGenElectron_p":	 	{"name":"FSGenElectron_p",		"title":"Momentum of MC Electrons",	"bin":50,	"xmin":0,	"xmax":90},
	"FSGenElectron_px":		{"name":"FSGenElectron_px",		"title":"$\p_{x}$ of MC Electrons",	"bin":50,	"xmin":0,	"xmax":90},
	"FSGenElectron_py":		{"name":"FSGenElectron_py",		"title":"$\p_{y}$ of MC Electrons",	"bin":50,	"xmin":0,	"xmax":90},
	"FSGenElectron_pz":		{"name":"FSGenElectron_pz",		"title":"$\p_{z}$ of MC Electrons",	"bin":50,	"xmin":0,	"xmax":90},
	"FSGenElectron_eta":	{"name":"FSGenElectron_eta",	"title":"Eta of MC Electrons",		"bin":50,	"xmin":-4,	"xmax":4},
	"FSGenElectron_theta":	{"name":"FSGenElectron_theta",	"title":"Theta of MC Electrons",	"bin":50,	"xmin":-1,	"xmax":3},
	"FSGenElectron_phi":	{"name":"FSGenElectron_phi",	"title":"Phi of MC Electrons",		"bin":50,	"xmin":-4,	"xmax":4},
	"FSGenElectron_charge":	{"name":"FSGenElectron_charge",	"title":"Charge of MC Electrons",   "bin":50,	"xmin":0,	"xmax":2},
	
	#MC mu
	"n_FSGenMuon":	  	{"name":"n_FSGenMuon",		"title":"Number of MC Muons",	"bin":50,	"xmin":0,	"xmax":1},
	"FSGenMuon_e":		{"name":"FSGenMuon_e",		"title":"Energy of MC Muons",	"bin":50,	"xmin":0,	"xmax":50},
	"FSGenMuon_mass":	{"name":"FSGenMuon_mass",	"title":"Mass of MC Muons",		"bin":50,	"xmin":0,	"xmax":1},
	"FSGenMuon_pt":  	{"name":"FSGenMuon_pt",		"title":"$\p_{t}$ of MC Muons",	"bin":50,	"xmin":0,	"xmax":40},
	"FSGenMuon_p":	 	{"name":"FSGenMuon_p",		"title":"Momentum of MC Muons",	"bin":50,	"xmin":0,	"xmax":50},
	"FSGenMuon_px":		{"name":"FSGenMuon_px",		"title":"$\p_{x}$ of MC Muons",	"bin":50,	"xmin":0,	"xmax":30},
	"FSGenMuon_py":		{"name":"FSGenMuon_py",		"title":"$\p_{y}$ of MC Muons",	"bin":50,	"xmin":0,	"xmax":30},
	"FSGenMuon_pz":		{"name":"FSGenMuon_pz",		"title":"$\p_{z}$ of MC Muons",	"bin":50,	"xmin":0,	"xmax":30},
	"FSGenMuon_eta":	{"name":"FSGenMuon_eta",	"title":"Eta of MC Muons",		"bin":50,	"xmin":-3,	"xmax":3},
	"FSGenMuon_theta":	{"name":"FSGenMuon_theta",	"title":"Theta of MC Muons",	"bin":50,	"xmin":0,	"xmax":3},
	"FSGenMuon_phi":	{"name":"FSGenMuon_phi",	"title":"Phi of MC Muons",		"bin":50,	"xmin":-3,	"xmax":3},
	"FSGenMuon_charge":	{"name":"FSGenMuon_charge",	"title":"Charge of MC Muons",   "bin":50,	"xmin":0,	"xmax":2},
	
	# RECO k+
	"n_RecoKplus":	  			{"name":"n_RecoKplus",	   	"title":"Number of Reco Kplus",		"bin":50,	"xmin":0,	"xmax":10},
	"RecoKplus_e":	  			{"name":"RecoKplus_e",	   	"title":"Energy of Reco Kplus",		"bin":50,	"xmin":0,	"xmax":100},
	"RecoKplus_mass":			{"name":"RecoKplus_mass",	"title":"Mass of Reco Kplus",		"bin":50,	"xmin":0,	"xmax":1},
	"RecoKplus_p":	  			{"name":"RecoKplus_p",	   	"title":"Momentum of Reco Kplus",	"bin":50,	"xmin":0,	"xmax":100},
	"RecoKplus_pt":	  			{"name":"RecoKplus_pt",	   	"title":"$\p_{t}$ of Reco Kplus",	"bin":50,	"xmin":0,	"xmax":100},
	"RecoKplus_px":	  			{"name":"RecoKplus_px",	   	"title":"$\p_{x}$ of Reco Kplus",	"bin":50,	"xmin":0,	"xmax":100},
	"RecoKplus_py":	  			{"name":"RecoKplus_py",	   	"title":"$\p_{y}$ of Reco Kplus",	"bin":50,	"xmin":0,	"xmax":100},
	"RecoKplus_pz":	  			{"name":"RecoKplus_pz",	   	"title":"$\p_{z}$ of Reco Kplus",	"bin":50,	"xmin":0,	"xmax":100},
	"RecoKplus_charge":			{"name":"RecoKplus_charge",	"title":"Charge of Reco Kplus",		"bin":50,	"xmin":0,	"xmax":2},
	
	# RECO gamma
	"n_RecoPhotons":	{"name":"n_RecoPhotons",	"title":"Number of Reco Photons",	  "bin":50,	"xmin":0,	"xmax":10},
	"RecoPhoton_e":		{"name":"RecoPhoton_e",		"title":"Energy of Reco Photons",	  "bin":50,	"xmin":0,	"xmax":180},
	"RecoPhoton_p":		{"name":"RecoPhoton_p",		"title":"Momentum of Reco Photons",	  "bin":50,	"xmin":0,	"xmax":180},
	"RecoPhoton_pt":	{"name":"RecoPhoton_pt",	"title":"$\p_{t}$ of Reco Photons",	  "bin":50,	"xmin":0,	"xmax":180},
	"RecoPhoton_px":	{"name":"RecoPhoton_px",	"title":"$\p_{x}$ of Reco Photons",	  "bin":50,	"xmin":0,	"xmax":180},
	"RecoPhoton_py":	{"name":"RecoPhoton_py",	"title":"$\p_{y}$ of Reco Photons",	  "bin":50,	"xmin":0,	"xmax":180},
	"RecoPhoton_pz":	{"name":"RecoPhoton_pz",	"title":"$\p_{z}$ of Reco Photons",	  "bin":50,	"xmin":0,	"xmax":180},
	
	# RECO e-
	"n_RecoElectrons":		{"name":"n_RecoElectrons",		"title":"Number of Reco Electrons",		"bin":50, 	"xmin":0,	"xmax":10},
	"RecoElectron_e":		{"name":"RecoElectron_e",		"title":"Energy of Reco Electrons",		"bin":50, 	"xmin":0,	"xmax":100},
	"RecoElectron_mass":	{"name":"RecoElectron_mass",	"title":"Mass of Reco Electrons ",		"bin":50, 	"xmin":0,	"xmax":1},
	"RecoElectron_p":		{"name":"RecoElectron_p",		"title":"Momentum of Reco Electrons",	"bin":50, 	"xmin":0,	"xmax":100},
	"RecoElectron_pt":		{"name":"RecoElectron_pt",		"title":"$\p_{t}$ of Reco Electrons",	"bin":50, 	"xmin":0,	"xmax":100},
	"RecoElectron_px":		{"name":"RecoElectron_px",		"title":"$\p_{x}$ of Reco Electrons",	"bin":50, 	"xmin":0,	"xmax":100},
	"RecoElectron_py":		{"name":"RecoElectron_py",		"title":"$\p_{y}$ of Reco Electrons",	"bin":50, 	"xmin":0,	"xmax":100},
	"RecoElectron_pz":		{"name":"RecoElectron_pz",		"title":"$\p_{z}$ of Reco Electrons",	"bin":50, 	"xmin":0,	"xmax":100},
	"RecoElectron_charge":	{"name":"RecoElectron_charge",	"title":"Charge of Reco Electron",		"bin":50, 	"xmin":0,	"xmax":2},
	
	# RECO mu
	"n_RecoMuons":		{"name":"n_RecoMuons",		"title":"Number of Reco Muons",		"bin":50,	"xmin":0,	"xmax":10},
	"RecoMuon_e":		{"name":"RecoMuon_e",		"title":"Energy of Reco Muons",		"bin":50,	"xmin":0,	"xmax":60},
	"RecoMuon_mass":	{"name":"RecoMuon_mass",	"title":"Mass of Reco Muons ",		"bin":50,	"xmin":0,	"xmax":1},
	"RecoMuon_p":		{"name":"RecoMuon_p",		"title":"Momentum of Reco Muons",	"bin":50,	"xmin":0,	"xmax":50},
	"RecoMuon_pt":		{"name":"RecoMuon_pt",		"title":"$\p_{t}$ of Reco Muons",	"bin":50,	"xmin":0,	"xmax":40},
	"RecoMuon_px":		{"name":"RecoMuon_px",		"title":"$\p_{x}$ of Reco Muons",	"bin":50,	"xmin":0,	"xmax":40},
	"RecoMuon_py":		{"name":"RecoMuon_py",		"title":"$\p_{y}$ of Reco Muons",	"bin":50,	"xmin":0,	"xmax":40},
	"RecoMuon_pz":		{"name":"RecoMuon_pz",		"title":"$\p_{z}$ of Reco Muons",	"bin":50,	"xmin":0,	"xmax":40},
	"RecoMuon_charge":	{"name":"RecoMuon_charge",	"title":"Charge of Reco Muon",		"bin":50,	"xmin":0,	"xmax":2},
	
	# JETS
# 	"Jets_kt2_e":						{"name":"Jets_kt2_e",						"title":"Energy of Jets",							"bin":50,	"xmin":0,	"xmax":120},
# 	"Jets_kt2_mass":					{"name":"Jets_kt2_mass",					"title":"Mass of Jets",								"bin":50,	"xmin":0,	"xmax":30},
# 	"Jets_kt2_p":						{"name":"Jets_kt2_p",						"title":"Momentum of Jets",							"bin":50,	"xmin":0,	"xmax":120},
# 	"Jets_kt2_pt":						{"name":"Jets_kt2_pt",						"title":"$\p_{t}$ of Jets",							"bin":50,	"xmin":0,	"xmax":120},
# 	"Jets_kt2_px":						{"name":"Jets_kt2_px",						"title":"$\p_{x}$ of Jets",							"bin":50,	"xmin":0,	"xmax":120},
# 	"Jets_kt2_py":						{"name":"Jets_kt2_py",						"title":"$\p_{y}$ of Jets",							"bin":50,	"xmin":0,	"xmax":120},
# 	"Jets_kt2_pz":						{"name":"Jets_kt2_pz",						"title":"$\p_{z}$ of Jets",							"bin":50,	"xmin":0,	"xmax":120},
# 	"Jets_kt2_eta":						{"name":"Jets_kt2_eta",						"title":"Eta of Jets",								"bin":50,	"xmin":-4,	"xmax":4},
# 	"Jets_kt2_theta":					{"name":"Jets_kt2_theta",					"title":"Theta of Jets",							"bin":50,	"xmin":0,	"xmax":4},
# 	"Jets_kt2_phi":						{"name":"Jets_kt2_phi",						"title":"Phi of Jets",								"bin":50,	"xmin":0,	"xmax":4},
# 	"n_Jets_kt2_constituents":			{"name":"n_Jets_kt2_constituents",			"title":"Number of Jet Constituents",				"bin":50,	"xmin":0,	"xmax":20},
# 	"n_Jets_kt2_charged_constituents":	{"name":"n_Jets_kt2_charged_constituents",	"title":"Number of Charged Constituents of Jets",	"bin":50,	"xmin":0,	"xmax":10},
# 	"n_Jets_kt2_neutral_constituents":	{"name":"n_Jets_kt2_neutral_constituents",	"title":"Number of Neutral Constituents of Jets",	"bin":50,	"xmin":0,	"xmax":20},
# 	"n_Jets_kt2":						{"name":"n_Jets_kt2",						"title":"Number of Jets",							"bin":50,	"xmin":0,	"xmax":10},
	
	# RECO H
	"RecoHiggs_e":		{"name":"RecoHiggs_e",		"title":"Energy of Reco Higgs",		"bin":50,	"xmin":0,	"xmax":180},
	"RecoHiggs_mass":	{"name":"RecoHiggs_mass",	"title":"Mass of Reco Higgs",		"bin":50,	"xmin":0,	"xmax":180},
	"RecoHiggs_p":		{"name":"RecoHiggs_p",		"title":"Momentum of Reco Higgs",	"bin":50,	"xmin":0,	"xmax":90},
	"RecoHiggs_pt":		{"name":"RecoHiggs_pt",		"title":"Pt of Reco Higgs",			"bin":50,	"xmin":0,	"xmax":90},
	"RecoHiggs_px":		{"name":"RecoHiggs_px",		"title":"Px of Reco Higgs",			"bin":50,	"xmin":0,	"xmax":90},
	"RecoHiggs_py":		{"name":"RecoHiggs_py",		"title":"Py of Reco Higgs",			"bin":50,	"xmin":0,	"xmax":90},
	"RecoHiggs_pz":		{"name":"RecoHiggs_pz",		"title":"Pz Reco Higgs",			"bin":50,	"xmin":0,	"xmax":90},
	"RecoHiggs_eta":	{"name":"RecoHiggs_eta",	"title":"Eta of Reco Higgs",		"bin":50,	"xmin":0,	"xmax":10},
	"RecoHiggs_phi":	{"name":"RecoHiggs_phi",	"title":"Phi of Reco Higgs",		"bin":50,	"xmin":0,	"xmax":4},
	
	# RECO IND k+
	"Kplus_0_m":	{"name":"Kplus_0_m",	"title":"Mass of 1st K+",		"bin":50,	"xmin":0,	"xmax":1},
	"Kplus_0_e":	{"name":"Kplus_0_e",	"title":"Energy of 1st K+",		"bin":50,	"xmin":0,	"xmax":100},
	"Kplus_0_p": 	{"name":"Kplus_0_p",	"title":"Momentum of 1st K+",	"bin":50,	"xmin":0,	"xmax":100},
	"Kplus_0_pt":	{"name":"Kplus_0_pt",	"title":"Pt of 1st K+",			"bin":50,	"xmin":0,	"xmax":100},
	"Kplus_0_px":	{"name":"Kplus_0_px",	"title":"Px of 1st K+",			"bin":50,	"xmin":0,	"xmax":100},
	"Kplus_0_py":	{"name":"Kplus_0_py",	"title":"Py of 1st K+",			"bin":50,	"xmin":0,	"xmax":100},
	"Kplus_0_pz":	{"name":"Kplus_0_pz",	"title":"Pz of 1st K+",			"bin":50,	"xmin":0,	"xmax":30},
	"Kplus_0_eta":	{"name":"Kplus_0_eta",	"title":"Eta of 1st K+",		"bin":50,	"xmin":0,	"xmax":4},
	"Kplus_0_phi":	{"name":"Kplus_0_phi",	"title":"Phi of 1st K+",		"bin":50,	"xmin":0,	"xmax":4},
	
	"Kplus_1_m":	{"name":"Kplus_1_m",	"title":"Mass of 2nd K+",		"bin":50,	"xmin":0,	"xmax":1},
	"Kplus_1_e":	{"name":"Kplus_1_e",	"title":"Energy of 2nd K+",		"bin":50,	"xmin":0,	"xmax":100},
	"Kplus_1_p": 	{"name":"Kplus_1_p",	"title":"Momentum of 2nd K+",	"bin":50,	"xmin":0,	"xmax":100},
	"Kplus_1_pt":	{"name":"Kplus_1_pt",	"title":"Pt of 2nd K+",			"bin":50,	"xmin":0,	"xmax":100},
	"Kplus_1_px":	{"name":"Kplus_1_px",	"title":"Px of 2nd K+",			"bin":50,	"xmin":0,	"xmax":100},
	"Kplus_1_py":	{"name":"Kplus_1_py",	"title":"Py of 2nd K+",			"bin":50,	"xmin":0,	"xmax":100},
	"Kplus_1_pz":	{"name":"Kplus_1_pz",	"title":"Pz of 2nd K+",			"bin":50,	"xmin":0,	"xmax":50},
	"Kplus_1_eta":	{"name":"Kplus_1_eta",	"title":"Eta of 2nd K+",		"bin":50,	"xmin":0,	"xmax":4},
	"Kplus_1_phi":	{"name":"Kplus_1_phi",	"title":"Phi of 2nd K+",		"bin":50,	"xmin":0,	"xmax":4},
	
	"Kplus_2_m":	{"name":"Kplus_2_m",	"title":"Mass of 3rd K+",		"bin":50,	"xmin":0,	"xmax":1},
	"Kplus_2_e":	{"name":"Kplus_2_e",	"title":"Energy of 3rd K+",		"bin":50,	"xmin":0,	"xmax":100},
	"Kplus_2_p": 	{"name":"Kplus_2_p",	"title":"Momentum of 3rd K+",	"bin":50,	"xmin":0,	"xmax":100},
	"Kplus_2_pt":	{"name":"Kplus_2_pt",	"title":"Pt of 3rd K+",			"bin":50,	"xmin":0,	"xmax":100},
	"Kplus_2_px":	{"name":"Kplus_2_px",	"title":"Px of 3rd K+",			"bin":50,	"xmin":0,	"xmax":100},
	"Kplus_2_py":	{"name":"Kplus_2_py",	"title":"Py of 3rd K+",			"bin":50,	"xmin":0,	"xmax":100},
	"Kplus_2_pz":	{"name":"Kplus_2_pz",	"title":"Pz of 3rd K+",			"bin":50,	"xmin":0,	"xmax":100},
	"Kplus_2_eta":	{"name":"Kplus_2_eta",	"title":"Eta of 3rd K+",		"bin":50,	"xmin":0,	"xmax":4},
	"Kplus_2_phi":	{"name":"Kplus_2_phi",	"title":"Phi of 3rd K+",		"bin":50,	"xmin":0,	"xmax":4},
	
	"Kplus_3_m":	{"name":"Kplus_3_m",	"title":"Mass of 4th K+",		"bin":50,	"xmin":0,	"xmax":1},
	"Kplus_3_e":	{"name":"Kplus_3_e",	"title":"Energy of 4th K+",		"bin":50,	"xmin":0,	"xmax":100},
	"Kplus_3_p": 	{"name":"Kplus_3_p",	"title":"Momentum of 4th K+",	"bin":50,	"xmin":0,	"xmax":100},
	"Kplus_3_pt":	{"name":"Kplus_3_pt",	"title":"Pt of 4th K+",			"bin":50,	"xmin":0,	"xmax":100},
	"Kplus_3_px":	{"name":"Kplus_3_px",	"title":"Px of 4th K+",			"bin":50,	"xmin":0,	"xmax":100},
	"Kplus_3_py":	{"name":"Kplus_3_py",	"title":"Py of 4th K+",			"bin":50,	"xmin":0,	"xmax":100},
	"Kplus_3_pz":	{"name":"Kplus_3_pz",	"title":"Pz of 4th K+",			"bin":50,	"xmin":0,	"xmax":100},
	"Kplus_3_eta":	{"name":"Kplus_3_eta",	"title":"Eta of 4th K+",		"bin":50,	"xmin":0,	"xmax":4},
	"Kplus_3_phi":	{"name":"Kplus_3_phi",	"title":"Phi of 4th K+",		"bin":50,	"xmin":0,	"xmax":4},
	
	# RECO Z
	"RecoZ_e":		{"name":"RecoZ_e",		"title":"Energy of Reco Z",		"bin":50,	"xmin":0,	"xmax":120},
	"RecoZ_mass":	{"name":"RecoZ_mass",	"title":"Mass of Reco Z",		"bin":50,	"xmin":0,	"xmax":120},
	"RecoZ_p":		{"name":"RecoZ_p",		"title":"Momentum of Reco Z",	"bin":50,	"xmin":0,	"xmax":100},
	"RecoZ_pt":		{"name":"RecoZ_pt",		"title":"Pt of Reco Z",			"bin":50,	"xmin":0,	"xmax":90},
	"RecoZ_px":		{"name":"RecoZ_px",		"title":"Px of Reco Z",			"bin":50,	"xmin":0,	"xmax":90},
	"RecoZ_py":		{"name":"RecoZ_py",		"title":"Py of Reco Z",			"bin":50,	"xmin":0,	"xmax":90},
	"RecoZ_pz":		{"name":"RecoZ_pz",		"title":"Pz Reco Z",			"bin":50,	"xmin":0,	"xmax":90},
	"RecoZ_eta":	{"name":"RecoZ_eta",	"title":"Eta of Reco Z",		"bin":50,	"xmin":0,	"xmax":10},
	"RecoZ_phi":	{"name":"RecoZ_phi",	"title":"Phi of Reco Z",		"bin":50,	"xmin":0,	"xmax":10},
	
	# RECO IND e-
	"Electron_0_m":		{"name":"Electron_0_m",		"title":"Mass of 1st Electron",		"bin":50,	"xmin":0,	"xmax":1},
	"Electron_0_e":		{"name":"Electron_0_e",		"title":"Energy of 1st Electron",	"bin":50,	"xmin":0,	"xmax":100},
	"Electron_0_p": 	{"name":"Electron_0_p",		"title":"Momentum of 1st Electron",	"bin":50,	"xmin":0,	"xmax":90},
	"Electron_0_pt":	{"name":"Electron_0_pt",	"title":"Pt of 1st Electron",		"bin":50,	"xmin":0,	"xmax":90},
	"Electron_0_px":	{"name":"Electron_0_px",	"title":"Px of 1st Electron",		"bin":50,	"xmin":0,	"xmax":90},
	"Electron_0_py":	{"name":"Electron_0_py",	"title":"Py of 1st Electron",		"bin":50,	"xmin":0,	"xmax":90},
	"Electron_0_pz":	{"name":"Electron_0_pz",	"title":"Pz of 1st Electron",		"bin":50,	"xmin":0,	"xmax":90},
	"Electron_0_eta":	{"name":"Electron_0_eta",	"title":"Eta of 1st Electron",		"bin":50,	"xmin":0,	"xmax":3},
	"Electron_0_phi":	{"name":"Electron_0_phi",	"title":"Phi of 1st Electron",		"bin":50,	"xmin":0,	"xmax":4},
	
	"Electron_1_m":		{"name":"Electron_1_m",		"title":"Mass of 2nd Electron",		"bin":50,	"xmin":0,	"xmax":1},
	"Electron_1_e":		{"name":"Electron_1_e",		"title":"Energy of 2nd Electron",	"bin":50,	"xmin":0,	"xmax":100},
	"Electron_1_p": 	{"name":"Electron_1_p",		"title":"Momentum of 2nd Electron",	"bin":50,	"xmin":0,	"xmax":90},
	"Electron_1_pt":	{"name":"Electron_1_pt",	"title":"Pt of 2nd Electron",		"bin":50,	"xmin":0,	"xmax":80},
	"Electron_1_px":	{"name":"Electron_1_px",	"title":"Px of 2nd Electron",		"bin":50,	"xmin":0,	"xmax":80},
	"Electron_1_py":	{"name":"Electron_1_py",	"title":"Py of 2nd Electron",		"bin":50,	"xmin":0,	"xmax":80},
	"Electron_1_pz":	{"name":"Electron_1_pz",	"title":"Pz of 2nd Electron",		"bin":50,	"xmin":0,	"xmax":80},
	"Electron_1_eta":	{"name":"Electron_1_eta",	"title":"Eta of 2nd Electron",		"bin":50,	"xmin":0,	"xmax":3},
	"Electron_1_phi":	{"name":"Electron_1_phi",	"title":"Phi of 2nd Electron",		"bin":50,	"xmin":0,	"xmax":4},
	
	"RecoEmiss_e":		{"name":"RecoEmiss_e",		"title":"Energy of Emiss",		"bin":50,	"xmin":0,	"xmax":100},
	"RecoEmiss_mass":	{"name":"RecoEmiss_mass",	"title":"Mass of Emiss",		"bin":50,	"xmin":0,	"xmax":20},
	"RecoEmiss_p":		{"name":"RecoEmiss_p",		"title":"Momentum of Emiss",	"bin":50,	"xmin":0,	"xmax":80},
	"RecoEmiss_pt":		{"name":"RecoEmiss_pt",		"title":"Pt of Emiss",			"bin":50,	"xmin":0,	"xmax":80},
	"RecoEmiss_px":		{"name":"RecoEmiss_px",		"title":"Px of Emiss",			"bin":50,	"xmin":0,	"xmax":80},
	"RecoEmiss_py":		{"name":"RecoEmiss_py",		"title":"Py of Emiss",			"bin":50,	"xmin":0,	"xmax":80},
	"RecoEmiss_pz":		{"name":"RecoEmiss_pz",		"title":"Pz of Emiss",			"bin":50,	"xmin":0,	"xmax":80},
	
	"RecoIP_Lxyz":		{"name":"RecoIP_Lxyz",		"title":"Reco Displacement",	"bin":50,	"xmin":0,	"xmax":20},
}