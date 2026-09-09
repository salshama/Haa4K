import os
import copy
import re
import ROOT

ROOT.gROOT.SetBatch(True)

DIRECTORY			= "/ceph/salshamaily/haa4K_FCCee/analysis/final_output/all_samples_mgp8sig_norwt_082026"
OUTPUT_DIRECTORY	= "/ceph/salshamaily/haa4K_FCCee/merged_samples"
TAG       			= ["AlpAlp"]
CUTS      			= {"AlpAlp": ["RecoKaonElecSel", "RecoHiggsMassCut"]}

VARIABLES = [
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

			"RecoIP_Lxyz",]

ALL_BKG_PROCESSES = [
			"p8_ee_WW_ecm240",
			"p8_ee_Zqq_ecm240",
			"p8_ee_ZZ_ecm240",

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
			"wzp6_ee_qqH_HZZ_ecm240",]

# mgp8_ee_{ee|mumu}H_HAlpAlp_{mass}_ecm240_{ctau}
SIGNAL_PATTERN	= re.compile(r"^mgp8_ee_(ee|mumu)H_HAlpAlp_(m[0-9p]+)_ecm240_(ctau[0-9]+m+)$")

def file_exists(path):
    return os.path.isfile(path)

def sum_histograms(directory, process_list, var, cut):
    hh = None
    found_any = False
    for proc in process_list:
        fpath = f"{directory}/{proc}_{cut}_histo.root"
        if not file_exists(fpath):
            continue
        tf = ROOT.TFile.Open(fpath, "READ")
        h = tf.Get(var)
        if not h:
            tf.Close()
            continue
        h_clone = copy.deepcopy(h)
        h_clone.SetDirectory(0)
        if hh is None:
            hh = h_clone
        else:
            hh.Add(h_clone)
        found_any = True
        tf.Close()
    return hh if found_any else None

def write_merged_sample(directory, out_name, process_list, variables, cut, out_directory):
    os.makedirs(out_directory, exist_ok=True)
    output = f"{out_directory}/{out_name}_{cut}_histo.root"
    outFile = ROOT.TFile.Open(output, "RECREATE")
    wrote_anything = False
    for var in variables:
        hh = sum_histograms(directory, process_list, var, cut)
        if hh is not None:
            outFile.cd()
            hh.Write()
            wrote_anything = True
        print(f"[{out_name}] {cut}: {var} {'OK' if hh is not None else 'missing'}")
    outFile.Close()
    if not wrote_anything:
        os.remove(output)

def discover_signal_processes(directory, cut):
    procs = []
    if not os.path.isdir(directory):
        return procs
    suffix = f"_{cut}_histo.root"
    for fname in os.listdir(directory):
        if not fname.endswith(suffix):
            continue
        proc = fname[: -len(suffix)]
        if SIGNAL_PATTERN.match(proc):
            procs.append(proc)
    return sorted(procs)

for tag in TAG:
    directory = DIRECTORY
    variables = VARIABLES

    for cut in CUTS[tag]:
        # one bkg_sum for all bkg processes
        write_merged_sample(directory, "bkg_sum", ALL_BKG_PROCESSES, variables, cut, OUTPUT_DIRECTORY)

        # keep signals separate
        for proc in discover_signal_processes(directory, cut):
            write_merged_sample(directory, proc, [proc], variables, cut, OUTPUT_DIRECTORY)

        print(f"Done: {tag}, {cut}")