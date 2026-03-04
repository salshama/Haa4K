import ROOT

# Mandatory: list of processes

# signal processes
processList = {
		'mgp8_ee_eeH_HAlpAlp_m1_ecm240':{},
		'mgp8_ee_eeH_HAlpAlp_m3_ecm240':{},
		'mgp8_ee_eeH_HAlpAlp_m6_ecm240':{},
}

# Production tag. This points to the yaml files for getting sample statistics
# Mandatory when running over EDM4Hep centrally produced events
#Comment out when running over privately produced events
# prodTag	 = "FCCee/Delphes/IDEA"

#Input directory
#Comment out when running over centrally produced events
#Mandatory when running over privately produced events
# For now, signal and background processes have different directories
inputDir = "/ceph/salshamaily/haa4K_FCCee/delphes"

# Output directory, default is local dir
outputDir = "/ceph/salshamaily/haa4K_FCCee/samples"

#Additional/custom C++ functions
includePaths = ["functions.h"]

#Optional
nCPUS	    = 8
# runBatch	= True
batchQueue  = "workday"
compGroup   = "group_u_FCC.local_gen"

#Mandatory: RDFanalysis class where the use defines the operations on the TTree
class RDFanalysis():

	#__________________________________________________________
	#Mandatory: analysers funtion to define the analysers to process, please make sure you return the last dataframe, in this example it is df2
	def analysers(df):
		df2 = (df
	   
	   .Alias("Particle0",				"Particle#0.index")
	   .Alias("Particle1",				"Particle#1.index")
	   .Alias("MCRecoAssociations0",	"MCRecoAssociations#0.index")
	   .Alias("MCRecoAssociations1",	"MCRecoAssociations#1.index")
	   
	   ### PHOTONS ###
	   .Alias("Photon0", "Photon#0.index")
	   
	   #all final state gen photons
	   .Define("GenPhoton_PID",			"FCCAnalyses::MCParticle::sel_pdgID(22, false)(Particle)")
	   .Define("FSGenPhoton",			"FCCAnalyses::MCParticle::sel_genStatus(1)(GenPhoton_PID)") #gen status==1 means final state particle (FS)
	   .Define("n_FSGenPhoton", 		"FCCAnalyses::MCParticle::get_n(FSGenPhoton)")
	   .Define("FSGenPhoton_e", 		"FCCAnalyses::MCParticle::get_e(FSGenPhoton)")
	   .Define("FSGenPhoton_p", 		"FCCAnalyses::MCParticle::get_p(FSGenPhoton)")
	   .Define("FSGenPhoton_pt",		"FCCAnalyses::MCParticle::get_pt(FSGenPhoton)")
	   .Define("FSGenPhoton_px", 		"FCCAnalyses::MCParticle::get_px(FSGenPhoton)")
	   .Define("FSGenPhoton_py",		"FCCAnalyses::MCParticle::get_py(FSGenPhoton)")
	   .Define("FSGenPhoton_pz",		"FCCAnalyses::MCParticle::get_pz(FSGenPhoton)")
	   .Define("FSGenPhoton_eta",		"FCCAnalyses::MCParticle::get_eta(FSGenPhoton)")
	   .Define("FSGenPhoton_theta", 	"FCCAnalyses::MCParticle::get_theta(FSGenPhoton)")
	   .Define("FSGenPhoton_phi",		"FCCAnalyses::MCParticle::get_phi(FSGenPhoton)")
	   .Define("FSGenPhoton_charge",	"FCCAnalyses::MCParticle::get_charge(FSGenPhoton)")
	   
	   .Define("RecoPhotons",   	"ReconstructedParticle::get(Photon0, ReconstructedParticles)")
	   .Define("n_RecoPhotons", 	"ReconstructedParticle::get_n(RecoPhotons)") #count how many photons are in the event in total
	   .Define("RecoPhoton_e",		"ReconstructedParticle::get_e(RecoPhotons)")
	   .Define("RecoPhoton_p",		"ReconstructedParticle::get_p(RecoPhotons)")
	   .Define("RecoPhoton_pt",		"ReconstructedParticle::get_pt(RecoPhotons)")
	   .Define("RecoPhoton_px",		"ReconstructedParticle::get_px(RecoPhotons)")
	   .Define("RecoPhoton_py",		"ReconstructedParticle::get_py(RecoPhotons)")
	   .Define("RecoPhoton_pz",		"ReconstructedParticle::get_pz(RecoPhotons)")
	   .Define("RecoPhoton_eta",	"ReconstructedParticle::get_eta(RecoPhotons)") #pseudorapidity eta
	   .Define("RecoPhoton_theta",  "ReconstructedParticle::get_theta(RecoPhotons)")
	   .Define("RecoPhoton_phi",	"ReconstructedParticle::get_phi(RecoPhotons)") #polar angle in the transverse plane phi
	   .Define("RecoPhoton_charge", "ReconstructedParticle::get_charge(RecoPhotons)")
	   
	   ### ELECTRONS ###
	   .Alias("Electron0", "Electron#0.index")
	   
	   #all final state gen electrons and positrons
	   .Define("GenElectron_PID",	"FCCAnalyses::MCParticle::sel_pdgID(11, true)(Particle)")
	   .Define("FSGenElectron",		"FCCAnalyses::MCParticle::sel_genStatus(1)(GenElectron_PID)") #genstatus==1 means final state particle (FS)
	   .Define("n_FSGenElectron",	"FCCAnalyses::MCParticle::get_n(FSGenElectron)")
	   #put in dummy values below if there aren't any FSGenElectrons, to avoid seg fault
	   .Define("FSGenElectron_e",			"if (n_FSGenElectron>0) return FCCAnalyses::MCParticle::get_e(FSGenElectron); else return FCCAnalyses::MCParticle::get_genStatus(GenElectron_PID);")
	   .Define("FSGenElectron_mass",		"if (n_FSGenElectron>0) return FCCAnalyses::MCParticle::get_mass(FSGenElectron); else return FCCAnalyses::MCParticle::get_genStatus(GenElectron_PID);")
	   .Define("FSGenElectron_p",			"if (n_FSGenElectron>0) return FCCAnalyses::MCParticle::get_p(FSGenElectron); else return FCCAnalyses::MCParticle::get_genStatus(GenElectron_PID);")
	   .Define("FSGenElectron_pt",			"if (n_FSGenElectron>0) return FCCAnalyses::MCParticle::get_pt(FSGenElectron); else return FCCAnalyses::MCParticle::get_genStatus(GenElectron_PID);")
	   .Define("FSGenElectron_px",			"if (n_FSGenElectron>0) return FCCAnalyses::MCParticle::get_px(FSGenElectron); else return FCCAnalyses::MCParticle::get_genStatus(GenElectron_PID);")
	   .Define("FSGenElectron_py",			"if (n_FSGenElectron>0) return FCCAnalyses::MCParticle::get_py(FSGenElectron); else return FCCAnalyses::MCParticle::get_genStatus(GenElectron_PID);")
	   .Define("FSGenElectron_pz",			"if (n_FSGenElectron>0) return FCCAnalyses::MCParticle::get_pz(FSGenElectron); else return FCCAnalyses::MCParticle::get_genStatus(GenElectron_PID);")
	   .Define("FSGenElectron_eta",			"if (n_FSGenElectron>0) return FCCAnalyses::MCParticle::get_eta(FSGenElectron); else return FCCAnalyses::MCParticle::get_genStatus(GenElectron_PID);")
	   .Define("FSGenElectron_theta",		"if (n_FSGenElectron>0) return FCCAnalyses::MCParticle::get_theta(FSGenElectron); else return FCCAnalyses::MCParticle::get_genStatus(GenElectron_PID);")
	   .Define("FSGenElectron_phi",			"if (n_FSGenElectron>0) return FCCAnalyses::MCParticle::get_phi(FSGenElectron); else return FCCAnalyses::MCParticle::get_genStatus(GenElectron_PID);")
	   .Define("FSGenElectron_charge",		"if (n_FSGenElectron>0) return FCCAnalyses::MCParticle::get_charge(FSGenElectron); else return FCCAnalyses::MCParticle::get_genStatus(GenElectron_PID);")
	   .Define("FSGenElectron_vertex_x",	"if (n_FSGenElectron>0) return FCCAnalyses::MCParticle::get_vertex_x( FSGenElectron ); else return FCCAnalyses::MCParticle::get_genStatus(GenElectron_PID);")
	   .Define("FSGenElectron_vertex_y",	"if (n_FSGenElectron>0) return FCCAnalyses::MCParticle::get_vertex_y( FSGenElectron ); else return FCCAnalyses::MCParticle::get_genStatus(GenElectron_PID);")
	   .Define("FSGenElectron_vertex_z",	"if (n_FSGenElectron>0) return FCCAnalyses::MCParticle::get_vertex_z( FSGenElectron ); else return FCCAnalyses::MCParticle::get_genStatus(GenElectron_PID);")
	   
	   .Define("RecoElectrons",		  	"ReconstructedParticle::get(Electron0, ReconstructedParticles)")
	   .Define("n_RecoElectrons",	  	"ReconstructedParticle::get_n(RecoElectrons)") #count how many electrons are in the event in total
	   .Define("RecoElectron_e",	  	"ReconstructedParticle::get_e(RecoElectrons)")
	   .Define("RecoElectron_mass",		"ReconstructedParticle::get_mass(RecoElectrons)")
	   .Define("RecoElectron_p",	  	"ReconstructedParticle::get_p(RecoElectrons)")
	   .Define("RecoElectron_pt",	  	"ReconstructedParticle::get_pt(RecoElectrons)")
	   .Define("RecoElectron_px",	  	"ReconstructedParticle::get_px(RecoElectrons)")
	   .Define("RecoElectron_py",	  	"ReconstructedParticle::get_py(RecoElectrons)")
	   .Define("RecoElectron_pz",	  	"ReconstructedParticle::get_pz(RecoElectrons)")
	   .Define("RecoElectron_eta",	  	"ReconstructedParticle::get_eta(RecoElectrons)") #pseudorapidity eta
	   .Define("RecoElectron_theta",  	"ReconstructedParticle::get_theta(RecoElectrons)")
	   .Define("RecoElectron_phi",	  	"ReconstructedParticle::get_phi(RecoElectrons)") #polar angle in the transverse plane phi
	   .Define("RecoElectron_charge", 	"ReconstructedParticle::get_charge(RecoElectrons)")
	   .Define("RecoElectronTrack_absD0",		"return abs(ReconstructedParticle2Track::getRP2TRK_D0(RecoElectrons,EFlowTrack_1))")
	   .Define("RecoElectronTrack_absZ0", 		"return abs(ReconstructedParticle2Track::getRP2TRK_Z0(RecoElectrons,EFlowTrack_1))")
	   .Define("RecoElectronTrack_absD0sig",	"return abs(ReconstructedParticle2Track::getRP2TRK_D0_sig(RecoElectrons,EFlowTrack_1))") #significance
	   .Define("RecoElectronTrack_absZ0sig",	"return abs(ReconstructedParticle2Track::getRP2TRK_Z0_sig(RecoElectrons,EFlowTrack_1))")
	   .Define("RecoElectronTrack_D0cov",		"ReconstructedParticle2Track::getRP2TRK_D0_cov(RecoElectrons,EFlowTrack_1)") #variance (not sigma)
	   .Define("RecoElectronTrack_Z0cov",		"ReconstructedParticle2Track::getRP2TRK_Z0_cov(RecoElectrons,EFlowTrack_1)")
		
		### MUONS ###
		.Alias("Muon0", "Muon#0.index")
		
		.Define("GenMuon_PID", "FCCAnalyses::MCParticle::sel_pdgID(13, true)(Particle)")
		.Define("FSGenMuon",   "FCCAnalyses::MCParticle::sel_genStatus(1)(GenMuon_PID)") #gen status==1 means final state particle (FS)
		.Define("n_FSGenMuon", "FCCAnalyses::MCParticle::get_n(FSGenMuon)")
		#put in dummy values below if there aren't any FSGenMuons to avoid seg fault
		.Define("FSGenMuon_e",			"if (n_FSGenMuon>0) return FCCAnalyses::MCParticle::get_e(FSGenMuon); else return FCCAnalyses::MCParticle::get_genStatus(GenMuon_PID);")
		.Define("FSGenMuon_p",			"if (n_FSGenMuon>0) return FCCAnalyses::MCParticle::get_p(FSGenMuon); else return FCCAnalyses::MCParticle::get_genStatus(GenMuon_PID);")
		.Define("FSGenMuon_mass",		"if (n_FSGenMuon>0) return FCCAnalyses::MCParticle::get_mass(FSGenMuon); else return FCCAnalyses::MCParticle::get_genStatus(GenMuon_PID);")
		.Define("FSGenMuon_pt",			"if (n_FSGenMuon>0) return FCCAnalyses::MCParticle::get_pt(FSGenMuon); else return FCCAnalyses::MCParticle::get_genStatus(GenMuon_PID);")
		.Define("FSGenMuon_px",			"if (n_FSGenMuon>0) return FCCAnalyses::MCParticle::get_px(FSGenMuon); else return FCCAnalyses::MCParticle::get_genStatus(GenMuon_PID);")
		.Define("FSGenMuon_py",			"if (n_FSGenMuon>0) return FCCAnalyses::MCParticle::get_py(FSGenMuon); else return FCCAnalyses::MCParticle::get_genStatus(GenMuon_PID);")
		.Define("FSGenMuon_pz",			"if (n_FSGenMuon>0) return FCCAnalyses::MCParticle::get_pz(FSGenMuon); else return FCCAnalyses::MCParticle::get_genStatus(GenMuon_PID);")
		.Define("FSGenMuon_eta",		"if (n_FSGenMuon>0) return FCCAnalyses::MCParticle::get_eta(FSGenMuon); else return FCCAnalyses::MCParticle::get_genStatus(GenMuon_PID);")
		.Define("FSGenMuon_theta",		"if (n_FSGenMuon>0) return FCCAnalyses::MCParticle::get_theta(FSGenMuon); else return FCCAnalyses::MCParticle::get_genStatus(GenMuon_PID);")
		.Define("FSGenMuon_phi",		"if (n_FSGenMuon>0) return FCCAnalyses::MCParticle::get_phi(FSGenMuon); else return FCCAnalyses::MCParticle::get_genStatus(GenMuon_PID);")
		.Define("FSGenMuon_charge",		"if (n_FSGenMuon>0) return FCCAnalyses::MCParticle::get_charge(FSGenMuon); else return FCCAnalyses::MCParticle::get_genStatus(GenMuon_PID);")
		.Define("FSGenMuon_vertex_x",	"if (n_FSGenMuon>0) return FCCAnalyses::MCParticle::get_vertex_x( FSGenMuon ); else return FCCAnalyses::MCParticle::get_genStatus(GenMuon_PID);")
		.Define("FSGenMuon_vertex_y",	"if (n_FSGenMuon>0) return FCCAnalyses::MCParticle::get_vertex_y( FSGenMuon ); else return FCCAnalyses::MCParticle::get_genStatus(GenMuon_PID);")
		.Define("FSGenMuon_vertex_z",	"if (n_FSGenMuon>0) return FCCAnalyses::MCParticle::get_vertex_z( FSGenMuon ); else return FCCAnalyses::MCParticle::get_genStatus(GenMuon_PID);")
		
		.Define("RecoMuons",	 	"ReconstructedParticle::get(Muon0, ReconstructedParticles)")
		.Define("n_RecoMuons",	 	"ReconstructedParticle::get_n(RecoMuons)") #count how many muons are in the event in total
		.Define("RecoMuon_e",	 	"ReconstructedParticle::get_e(RecoMuons)")
		.Define("RecoMuon_mass",	"ReconstructedParticle::get_mass(RecoMuons)")
		.Define("RecoMuon_p",	 	"ReconstructedParticle::get_p(RecoMuons)")
		.Define("RecoMuon_pt",	 	"ReconstructedParticle::get_pt(RecoMuons)")
		.Define("RecoMuon_px",	 	"ReconstructedParticle::get_px(RecoMuons)")
		.Define("RecoMuon_py",	 	"ReconstructedParticle::get_py(RecoMuons)")
		.Define("RecoMuon_pz",	 	"ReconstructedParticle::get_pz(RecoMuons)")
		.Define("RecoMuon_eta",	 	"ReconstructedParticle::get_eta(RecoMuons)") #pseudorapidity eta
		.Define("RecoMuon_theta",	"ReconstructedParticle::get_theta(RecoMuons)")
		.Define("RecoMuon_phi",	 	"ReconstructedParticle::get_phi(RecoMuons)") #polar angle in the transverse plane phi
		.Define("RecoMuon_charge",	"ReconstructedParticle::get_charge(RecoMuons)")
		.Define("RecoMuonTrack_absD0",	  "return abs(ReconstructedParticle2Track::getRP2TRK_D0(RecoMuons,EFlowTrack_1))")
		.Define("RecoMuonTrack_absZ0",	  "return abs(ReconstructedParticle2Track::getRP2TRK_Z0(RecoMuons,EFlowTrack_1))")
		.Define("RecoMuonTrack_absD0sig", "return abs(ReconstructedParticle2Track::getRP2TRK_D0_sig(RecoMuons,EFlowTrack_1))") #significance
		.Define("RecoMuonTrack_absZ0sig", "return abs(ReconstructedParticle2Track::getRP2TRK_Z0_sig(RecoMuons,EFlowTrack_1))")
		.Define("RecoMuonTrack_D0cov",	  "ReconstructedParticle2Track::getRP2TRK_D0_cov(RecoMuons,EFlowTrack_1)") #variance (not sigma)
		.Define("RecoMuonTrack_Z0cov",	  "ReconstructedParticle2Track::getRP2TRK_Z0_cov(RecoMuons,EFlowTrack_1)")
		
		### LEPTONS ###
		.Define("RecoLeptons",			"ReconstructedParticle::merge(RecoElectrons, RecoMuons)")
        .Define("n_RecoLeptons",  		"ReconstructedParticle::get_n(RecoLeptons)") 
        .Define("RecoLepton_e",      	"ReconstructedParticle::get_e(RecoLeptons)")
        .Define("RecoLepton_p",      	"ReconstructedParticle::get_p(RecoLeptons)")
        .Define("RecoLepton_pt",      	"ReconstructedParticle::get_pt(RecoLeptons)")
        .Define("RecoLepton_px",      	"ReconstructedParticle::get_px(RecoLeptons)")
        .Define("RecoLepton_py",      	"ReconstructedParticle::get_py(RecoLeptons)")
        .Define("RecoLepton_pz",      	"ReconstructedParticle::get_pz(RecoLeptons)")
        .Define("RecoLepton_eta",     	"ReconstructedParticle::get_eta(RecoLeptons)") #pseudorapidity eta
        .Define("RecoLepton_theta",   	"ReconstructedParticle::get_theta(RecoLeptons)")
        .Define("RecoLepton_phi",     	"ReconstructedParticle::get_phi(RecoLeptons)") #polar angle in the transverse plane phi
        .Define("RecoLepton_charge",  	"ReconstructedParticle::get_charge(RecoLeptons)")
        .Define("RecoLeptonTrack",		"ReconstructedParticle2Track::getRP2TRK(RecoLeptons, EFlowTrack_1)")
        .Define("RecoLeptonTrack_absD0", 	"return abs(ReconstructedParticle2Track::getRP2TRK_D0(RecoLeptons,EFlowTrack_1))")
        .Define("RecoLeptonTrack_absZ0", 	"return abs(ReconstructedParticle2Track::getRP2TRK_Z0(RecoLeptons,EFlowTrack_1))")
        .Define("RecoLeptonTrack_absD0sig",	"return abs(ReconstructedParticle2Track::getRP2TRK_D0_sig(RecoLeptons,EFlowTrack_1))") #significance
        .Define("RecoLeptonTrack_absZ0sig", "return abs(ReconstructedParticle2Track::getRP2TRK_Z0_sig(RecoLeptons,EFlowTrack_1))")
        .Define("RecoLeptonTrack_D0cov", 	"ReconstructedParticle2Track::getRP2TRK_D0_cov(RecoLeptons,EFlowTrack_1)") #variance (not sigma)
        .Define("RecoLeptonTrack_Z0cov", 	"ReconstructedParticle2Track::getRP2TRK_Z0_cov(RecoLeptons,EFlowTrack_1)")
		
		### K PLUS ###
	   .Define("GenKplus",			"FCCAnalyses::MCParticle::sel_pdgID(321, true)(Particle)")
	   .Define("n_GenKplus",		"FCCAnalyses::MCParticle::get_n(GenKplus)")
	   .Define("GenKplus_e",		"if (n_GenKplus>0) return FCCAnalyses::MCParticle::get_e(GenKplus); else return FCCAnalyses::MCParticle::get_genStatus(GenKplus);")
	   .Define("GenKplus_mass",		"if (n_GenKplus>0) return FCCAnalyses::MCParticle::get_mass(GenKplus); else return FCCAnalyses::MCParticle::get_genStatus(GenKplus);")
	   .Define("GenKplus_pt",		"if (n_GenKplus>0) return FCCAnalyses::MCParticle::get_pt(GenKplus); else return FCCAnalyses::MCParticle::get_genStatus(GenKplus);")
	   .Define("GenKplus_p",		"if (n_GenKplus>0) return FCCAnalyses::MCParticle::get_p(GenKplus); else return FCCAnalyses::MCParticle::get_genStatus(GenKplus);")
	   .Define("GenKplus_px",		"if (n_GenKplus>0) return FCCAnalyses::MCParticle::get_px(GenKplus); else return FCCAnalyses::MCParticle::get_genStatus(GenKplus);")
	   .Define("GenKplus_py",		"if (n_GenKplus>0) return FCCAnalyses::MCParticle::get_py(GenKplus); else return FCCAnalyses::MCParticle::get_genStatus(GenKplus);")
	   .Define("GenKplus_pz",		"if (n_GenKplus>0) return FCCAnalyses::MCParticle::get_pz(GenKplus); else return FCCAnalyses::MCParticle::get_genStatus(GenKplus);")
	   .Define("GenKplus_eta",		"FCCAnalyses::MCParticle::get_eta(GenKplus)")
	   .Define("GenKplus_theta",	"FCCAnalyses::MCParticle::get_theta(GenKplus)")
	   .Define("GenKplus_phi",		"FCCAnalyses::MCParticle::get_phi(GenKplus)")
	   .Define("GenKplus_charge",	"FCCAnalyses::MCParticle::get_charge(GenKplus)")
	   
	   # removing electrons and muons from reco particles and setting charge==1 to get K candidates
	   .Define("Cands",        	"ReconstructedParticle::remove(ReconstructedParticles, RecoElectrons)")
	   .Define("Candidates",   	"ReconstructedParticle::remove(Cands, RecoMuons)")
	   .Define("RecoKplus",		"ReconstructedParticle::sel_charge(1, true)(Candidates)")
	   
	   ### KAONS ###
		
	   .Define("n_RecoKplus",	  	"ReconstructedParticle::get_n(RecoKplus)") #count how many K+ are in the event in total
	   .Define("RecoKplus_e",	  	"ReconstructedParticle::get_e(RecoKplus)")
	   .Define("RecoKplus_mass",	"ReconstructedParticle::get_mass(RecoKplus)")
	   .Define("RecoKplus_p",	  	"ReconstructedParticle::get_p(RecoKplus)")
	   .Define("RecoKplus_pt",	  	"ReconstructedParticle::get_pt(RecoKplus)")
	   .Define("RecoKplus_px",	  	"ReconstructedParticle::get_px(RecoKplus)")
	   .Define("RecoKplus_py",	  	"ReconstructedParticle::get_py(RecoKplus)")
	   .Define("RecoKplus_pz",	  	"ReconstructedParticle::get_pz(RecoKplus)")
	   .Define("RecoKplus_eta",	  	"ReconstructedParticle::get_eta(RecoKplus)") #pseudorapidity eta
	   .Define("RecoKplus_theta",  	"ReconstructedParticle::get_theta(RecoKplus)")
	   .Define("RecoKplus_phi",	  	"ReconstructedParticle::get_phi(RecoKplus)") #polar angle in the transverse plane phi
	   .Define("RecoKplus_charge", 	"ReconstructedParticle::get_charge(RecoKplus)")
	   # constructing a TLV to apply kaon mass cut
	   .Define("RecoKplus_tlv",			"FCCAnalyses::ZHfunctions::build_p4(RecoKplus_px, RecoKplus_py, RecoKplus_pz, RecoKplus_e)")
	   .Define("RecoKplus_tlv_mass",	"FCCAnalyses::ZHfunctions::get_mass_tlv(RecoKplus_tlv)")
	   .Define("RecoKplus_MassCut",		"RecoKplus_tlv[RecoKplus_tlv_mass>0.2 && RecoKplus_tlv_mass<0.7]")
	   # tracks
	   .Define("RecoKplus_TrackSel",		"RecoKplus[RecoKplus_tlv_mass>0.2 && RecoKplus_tlv_mass<0.7]")
	   .Define("RecoKplusTrack",			"ReconstructedParticle2Track::getRP2TRK(RecoKplus_TrackSel, EFlowTrack_1)")
	   .Define("RecoKplusTrack_absD0",		"return abs(ReconstructedParticle2Track::getRP2TRK_D0(RecoKplus_TrackSel,EFlowTrack_1))")
	   .Define("RecoKplusTrack_absZ0", 		"return abs(ReconstructedParticle2Track::getRP2TRK_Z0(RecoKplus_TrackSel,EFlowTrack_1))")
	   .Define("RecoKplusTrack_absD0sig",	"return abs(ReconstructedParticle2Track::getRP2TRK_D0_sig(RecoKplus_TrackSel,EFlowTrack_1))") #significance
	   .Define("RecoKplusTrack_absZ0sig",	"return abs(ReconstructedParticle2Track::getRP2TRK_Z0_sig(RecoKplus_TrackSel,EFlowTrack_1))")
	   .Define("RecoKplusTrack_D0cov",		"ReconstructedParticle2Track::getRP2TRK_D0_cov(RecoKplus_TrackSel,EFlowTrack_1)") #variance (not sigma)
	   .Define("RecoKplusTrack_Z0cov",		"ReconstructedParticle2Track::getRP2TRK_Z0_cov(RecoKplus_TrackSel,EFlowTrack_1)")
	   
	   ### KAON SELECTION ###
	   .Filter("RecoKplus_MassCut.size()==4 && (RecoKplus_charge.at(0)+RecoKplus_charge.at(1)+RecoKplus_charge.at(2)+RecoKplus_charge.at(3))==0")
	   
		### JETS ###

		# Jet clustering with different algorithm, only on non leptons #
# 		.Define("RP_px",	"ReconstructedParticle::get_px(RecoKplus) ")
# 		.Define("RP_py",	"ReconstructedParticle::get_py(RecoKplus) ")
# 		.Define("RP_pz",	"ReconstructedParticle::get_pz(RecoKplus) ")
# 		.Define("RP_e",		"ReconstructedParticle::get_e(RecoKplus) ")
# 		
# 		# build pseudo jets with the RP, using the interface that takes px,py,pz,E
# 		.Define("pseudo_jets",	"JetClusteringUtils::set_pseudoJets(RP_px, RP_py, RP_pz, RP_e)")
# 		
# 		# Durham algo, exclusive clustering (first number 2) N_jets=4 (second number), E-scheme=0 (third and forth numbers) #
# 		.Define("FCCAnalysesJets_ee_kt",	"JetClustering::clustering_ee_kt(2, 4, 1, 0)(pseudo_jets)")
# 		.Define("Jets_kt2",					"JetClusteringUtils::get_pseudoJets( FCCAnalysesJets_ee_kt )")
# 		.Define("Jet_GetConstituents_kt2",	"JetClusteringUtils::get_constituents(FCCAnalysesJets_ee_kt)") # constituents indices
# 		.Define("Jets_Constituents_kt2",	"JetConstituentsUtils::build_constituents_cluster(RecoKplus, Jet_GetConstituents_kt2)") #build jet constituents lists for reconstruction
# 		.Define("Jets_kt2_e",				"JetClusteringUtils::get_e(Jets_kt2)")
# 		.Define("Jets_kt2_mass",			"JetClusteringUtils::get_m(Jets_kt2)")
# 		.Define("Jets_kt2_p",				"JetClusteringUtils::get_p(Jets_kt2)")  #momentum p
# 		.Define("Jets_kt2_pt",				"JetClusteringUtils::get_pt(Jets_kt2)") #transverse momentum pt
# 		.Define("Jets_kt2_px",				"JetClusteringUtils::get_px(Jets_kt2)")
# 		.Define("Jets_kt2_py",				"JetClusteringUtils::get_py(Jets_kt2)")
# 		.Define("Jets_kt2_pz",				"JetClusteringUtils::get_pz(Jets_kt2)")
# 		.Define("Jets_kt2_eta",				"JetClusteringUtils::get_eta(Jets_kt2)") #pseudorapidity eta
# 		.Define("Jets_kt2_theta",   		"JetClusteringUtils::get_theta(Jets_kt2)")
# 		.Define("Jets_kt2_phi",				"JetClusteringUtils::get_phi(Jets_kt2)") #polar angle in the transverse plane phi
# 		.Define("n_Jets_kt2_constituents",	"JetConstituentsUtils::get_n_constituents(Jets_Constituents_kt2)")
# 		.Define("n_Jets_kt2_charged_constituents", "JetConstituentsUtils::get_ncharged_constituents(Jets_Constituents_kt2)")
# 		.Define("n_Jets_kt2_neutral_constituents", "JetConstituentsUtils::get_nneutral_constituents(Jets_Constituents_kt2)")
# 		.Define("n_Jets_kt2",						"Jets_kt2_e.size()")
		
		### VERTEX RECONSTRUCTION ###
		
		# Primary IP (Primary IP) -> for leptons
		.Define("RecoDecayVertexObjectLepton",	"VertexFitterSimple::VertexFitter_Tk(0, RecoLeptonTrack)")
		.Define("RecoDecayVertexLepton",		"VertexingUtils::get_VertexData(RecoDecayVertexObjectLepton)")
		.Define("RecoLeptonIP_p4",				"TLorentzVector(RecoDecayVertexLepton.position.x, RecoDecayVertexLepton.position.y, RecoDecayVertexLepton.position.z, 0.)")
		.Define("RecoLeptonIP_px",				"RecoLeptonIP_p4.Px()")
		.Define("RecoLeptonIP_py",				"RecoLeptonIP_p4.Py()")
		.Define("RecoLeptonIP_pz",				"RecoLeptonIP_p4.Pz()")
		
		# Secondary IP or Displaced Vertex (Secondary IP or DV) -> for kaons
		.Define("RecoDecayVertexObjectKplus",	"VertexFitterSimple::VertexFitter_Tk(0, RecoKplusTrack)")
		.Define("RecoDecayVertexKplus",			"VertexingUtils::get_VertexData(RecoDecayVertexObjectKplus)")
		.Define("RecoKplusIP_p4",				"TLorentzVector(RecoDecayVertexKplus.position.x, RecoDecayVertexKplus.position.y, RecoDecayVertexKplus.position.z, 0.)")
		.Define("RecoKplusIP_px",				"RecoKplusIP_p4.Px()")
		.Define("RecoKplusIP_py",				"RecoKplusIP_p4.Py()")
		.Define("RecoKplusIP_pz",				"RecoKplusIP_p4.Pz()")
		
		# Displacement between the two vertices
		.Define("RecoIP_Lxyz",	"(RecoKplusIP_p4.Vect() - RecoLeptonIP_p4.Vect()).Mag()")
		
		### HIGGS RECONSTRUCTION ###
		
		# starting with the first four kaons
		.Define("Kplus_0",	"RecoKplus_MassCut.at(0)")
		.Define("Kplus_1",	"RecoKplus_MassCut.at(1)")
		.Define("Kplus_2",	"RecoKplus_MassCut.at(2)")
		.Define("Kplus_3",	"RecoKplus_MassCut.at(3)")
		
		# accessing the individual 4 kaon masses
		.Define("Kplus_0_m",	"Kplus_0.M()")
		.Define("Kplus_0_e",	"Kplus_0.E()")
		.Define("Kplus_0_p",	"Kplus_0.P()")
		.Define("Kplus_0_pt",	"Kplus_0.Pt()")
		.Define("Kplus_0_px",	"Kplus_0.Px()")
		.Define("Kplus_0_py",	"Kplus_0.Py()")
		.Define("Kplus_0_pz",	"Kplus_0.Pz()")
		.Define("Kplus_0_eta",	"Kplus_0.Eta()")
		.Define("Kplus_0_phi",	"Kplus_0.Phi()")
		
		.Define("Kplus_1_m",	"Kplus_1.M()")
		.Define("Kplus_1_e",	"Kplus_1.E()")
		.Define("Kplus_1_p",	"Kplus_1.P()")
		.Define("Kplus_1_pt",	"Kplus_1.Pt()")
		.Define("Kplus_1_px",	"Kplus_1.Px()")
		.Define("Kplus_1_py", 	"Kplus_1.Py()")
		.Define("Kplus_1_pz",	"Kplus_1.Pz()")
		.Define("Kplus_1_eta",	"Kplus_1.Eta()")
		.Define("Kplus_1_phi",	"Kplus_1.Phi()")
		
		.Define("Kplus_2_m",	"Kplus_2.M()")
		.Define("Kplus_2_e",	"Kplus_2.E()")
		.Define("Kplus_2_p",	"Kplus_2.P()")
		.Define("Kplus_2_pt",	"Kplus_2.Pt()")
		.Define("Kplus_2_px",	"Kplus_2.Px()")
		.Define("Kplus_2_py",	"Kplus_2.Py()")
		.Define("Kplus_2_pz",	"Kplus_2.Pz()")
		.Define("Kplus_2_eta",	"Kplus_2.Eta()")
		.Define("Kplus_2_phi",	"Kplus_2.Phi()")
		
		.Define("Kplus_3_m",	"Kplus_3.M()")
		.Define("Kplus_3_e",	"Kplus_3.E()")
		.Define("Kplus_3_p",	"Kplus_3.P()")
		.Define("Kplus_3_pt",	"Kplus_3.Pt()")
		.Define("Kplus_3_px",	"Kplus_3.Px()")
		.Define("Kplus_3_py",	"Kplus_3.Py()")
		.Define("Kplus_3_pz",	"Kplus_3.Pz()")
		.Define("Kplus_3_eta",	"Kplus_3.Eta()")
		.Define("Kplus_3_phi",	"Kplus_3.Phi()")
		
		# summing these kaons together to get reconstructed Higgs
		.Define("RecoHiggs",	"Kplus_0 + Kplus_1 + Kplus_2 + Kplus_3")
		
		# getting Higgs properties
		.Define("RecoHiggs_mass",	"RecoHiggs.M()")
		.Define("RecoHiggs_e",		"RecoHiggs.E()")
		.Define("RecoHiggs_p",		"RecoHiggs.P()")
		.Define("RecoHiggs_pt",		"RecoHiggs.Pt()")
		.Define("RecoHiggs_px",		"RecoHiggs.Px()")
		.Define("RecoHiggs_py",		"RecoHiggs.Py()")
		.Define("RecoHiggs_pz",		"RecoHiggs.Pz()")
		.Define("RecoHiggs_eta",	"RecoHiggs.Eta()")
		.Define("RecoHiggs_phi",	"RecoHiggs.Phi()")
		
		### ELECTRON SELECTION ###
		.Filter("n_RecoElectrons==2 && (RecoElectron_charge.at(0)+RecoElectron_charge.at(1))==0")
		
		### Z RECONSTRUCTION ###
		
		# starting with the first two electrons
		.Define("Electron_0",	"TLorentzVector(RecoElectron_px.at(0), RecoElectron_py.at(0), RecoElectron_pz.at(0), RecoElectron_e.at(0))")
		.Define("Electron_1",	"TLorentzVector(RecoElectron_px.at(1), RecoElectron_py.at(1), RecoElectron_pz.at(1), RecoElectron_e.at(1))")
		
		# accessing individual 2 electron masses
		.Define("Electron_0_m",		"Electron_0.M()")
		.Define("Electron_0_e",		"Electron_0.E()")
		.Define("Electron_0_p",		"Electron_0.P()")
		.Define("Electron_0_pt",	"Electron_0.Pt()")
		.Define("Electron_0_px",	"Electron_0.Px()")
		.Define("Electron_0_py",	"Electron_0.Py()")
		.Define("Electron_0_pz",	"Electron_0.Pz()")
		.Define("Electron_0_eta",	"Electron_0.Eta()")
		.Define("Electron_0_phi",	"Electron_0.Phi()")
		
		.Define("Electron_1_m",		"Electron_1.M()")
		.Define("Electron_1_e",		"Electron_1.E()")
		.Define("Electron_1_p",		"Electron_1.P()")
		.Define("Electron_1_pt",	"Electron_1.Pt()")
		.Define("Electron_1_px",	"Electron_1.Px()")
		.Define("Electron_1_py",	"Electron_1.Py()")
		.Define("Electron_1_pz",	"Electron_1.Pz()")
		.Define("Electron_1_eta",	"Electron_1.Eta()")
		.Define("Electron_1_phi",	"Electron_1.Phi()")
		
		# summing these electrons together to get reconstructed Z
		.Define("RecoZ",	"Electron_0 + Electron_1")
		
		# getting Z properties
		.Define("RecoZ_mass",	"RecoZ.M()")
		.Define("RecoZ_e",		"RecoZ.E()")
		.Define("RecoZ_p",		"RecoZ.P()")
		.Define("RecoZ_pt",		"RecoZ.Pt()")
		.Define("RecoZ_px",		"RecoZ.Px()")
		.Define("RecoZ_py",		"RecoZ.Py()")
		.Define("RecoZ_pz",		"RecoZ.Pz()")
		.Define("RecoZ_eta",	"RecoZ.Eta()")
		.Define("RecoZ_phi",	"RecoZ.Phi()")
		
		 ### MISSING ENERGY ###
		.Define("RecoEmiss",		"FCCAnalyses::ZHfunctions::missingEnergy(240., ReconstructedParticles)") #ecm=240
        .Define("RecoEmiss_px",		"RecoEmiss[0].momentum.x")
        .Define("RecoEmiss_py",		"RecoEmiss[0].momentum.y")
        .Define("RecoEmiss_pz",		"RecoEmiss[0].momentum.z")
        .Define("RecoEmiss_pt",		"return sqrt(RecoEmiss_px*RecoEmiss_px + RecoEmiss_py*RecoEmiss_py)")
        .Define("RecoEmiss_p",		"return sqrt(RecoEmiss_px*RecoEmiss_px + RecoEmiss_py*RecoEmiss_py + RecoEmiss_pz*RecoEmiss_pz)")
        .Define("RecoEmiss_e",		"RecoEmiss[0].energy")
        .Define("RecoEmiss_mass",	"RecoEmiss[0].mass")
		)
		
		return df2

	#__________________________________________________________
	#Mandatory: output function, please make sure you return the branchlist as a python list
	def output():
		branchList = [
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
				"GenPhoton_PID",
				"FSGenPhoton",
				"n_FSGenPhoton",
				"FSGenPhoton_e",
				"FSGenPhoton_p",
				"FSGenPhoton_pt",
				"FSGenPhoton_px",
				"FSGenPhoton_py",
				"FSGenPhoton_pz",
				"FSGenPhoton_eta",
				"FSGenPhoton_phi",
				"FSGenPhoton_theta",
				
				# MC e-
				"GenElectron_PID",
				"FSGenElectron",
				"n_FSGenElectron",
				"FSGenElectron_e",
				"FSGenElectron_mass",
				"FSGenElectron_p",
				"FSGenElectron_pt",
				"FSGenElectron_px",
				"FSGenElectron_py",
				"FSGenElectron_pz",
				"FSGenElectron_eta",
				"FSGenElectron_phi",
				"FSGenElectron_theta",
				"FSGenElectron_charge",
				
				# MC mu
				"GenMuon_PID",
				"FSGenMuon",
				"n_FSGenMuon",
				"FSGenMuon_e",
				"FSGenMuon_mass",
				"FSGenMuon_p",
				"FSGenMuon_pt",
				"FSGenMuon_px",
				"FSGenMuon_py",
				"FSGenMuon_pz",
				"FSGenMuon_eta",
				"FSGenMuon_phi",
				"FSGenMuon_theta",
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
				"RecoKplusTrack",
				"RecoKplusTrack_absD0",
				"RecoKplusTrack_absZ0",
				"RecoKplusTrack_absD0sig",
				"RecoKplusTrack_absZ0sig",
				"RecoKplusTrack_D0cov",
				"RecoKplusTrack_Z0cov",
				
				# RECO gamma
				"n_RecoPhotons",
				"RecoPhoton_e",
				"RecoPhoton_p",
				"RecoPhoton_pt",
				"RecoPhoton_px",
				"RecoPhoton_py",
				"RecoPhoton_pz",
				"RecoPhoton_eta",
				"RecoPhoton_theta",
				"RecoPhoton_phi",
				"RecoPhoton_charge",
				
				# RECO e-
				"n_RecoElectrons",
				"RecoElectron_e",
				"RecoElectron_mass",
				"RecoElectron_p",
				"RecoElectron_pt",
				"RecoElectron_px",
				"RecoElectron_py",
				"RecoElectron_pz",
				"RecoElectron_eta",
				"RecoElectron_theta",
				"RecoElectron_phi",
				"RecoElectron_charge",
				"RecoElectronTrack_absD0",
				"RecoElectronTrack_absZ0",
				"RecoElectronTrack_absD0sig",
				"RecoElectronTrack_absZ0sig",
				"RecoElectronTrack_D0cov",
				"RecoElectronTrack_Z0cov",
				
				# RECO mu
				"n_RecoMuons",
				"RecoMuon_e",
				"RecoMuon_mass",
				"RecoMuon_p",
				"RecoMuon_pt",
				"RecoMuon_px",
				"RecoMuon_py",
				"RecoMuon_pz",
				"RecoMuon_eta",
				"RecoMuon_theta",
				"RecoMuon_phi",
				"RecoMuon_charge",
				"RecoMuonTrack_absD0",
				"RecoMuonTrack_absZ0",
				"RecoMuonTrack_absD0sig",
				"RecoMuonTrack_absZ0sig",
				"RecoMuonTrack_D0cov",
				"RecoMuonTrack_Z0cov",
				
				# JETS
# 				"Jets_kt2_e",
# 				"Jets_kt2_mass",
# 				"Jets_kt2_p",
# 				"Jets_kt2_pt",
# 				"Jets_kt2_px",
# 				"Jets_kt2_py",
# 				"Jets_kt2_pz",
# 				"Jets_kt2_eta",
# 				"Jets_kt2_theta",
# 				"Jets_kt2_phi",
# 				"Jets_Constituents_kt2",
# 				"n_Jets_kt2_constituents",
# 				"n_Jets_kt2_charged_constituents",
# 				"n_Jets_kt2_neutral_constituents",
# 				"n_Jets_kt2",
				
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
				
				# RECO VERTEX
				"RecoLeptonIP_p4",
				"RecoLeptonIP_px",
				"RecoLeptonIP_py",
				"RecoLeptonIP_pz",
				
				"RecoKplusIP_p4",
				"RecoKplusIP_px",
				"RecoKplusIP_py",
				"RecoKplusIP_pz",
				
				"RecoIP_Lxyz",

				# RECO EMISS
				"RecoEmiss_e",
				"RecoEmiss_mass",
				"RecoEmiss_p",
				"RecoEmiss_pt",
				"RecoEmiss_px",
				"RecoEmiss_py",
				"RecoEmiss_pz",
				]

		return branchList