#!/usr/bin/env python3

from __future__ import annotations
import argparse
import os
import re
import shutil
import subprocess
import sys

# fit_histos output (only file Combine should read)
SHAPES = ("/ceph/salshamaily/haa4K_FCCee/combine/ready_samples/RecoHiggs_mass_RecoKaonElecSel_rebinned.root")
DATA_FILE = SHAPES
DATA_HIST = "bkg_sum"
MERGED_DIR = "/ceph/salshamaily/haa4K_FCCee/merged_samples"
MERGED_CUT = "RecoKaonElecSel"
MERGED_VAR = "RecoHiggs_mass"
OUTDIR    = "/ceph/salshamaily/haa4K_FCCee/combine/datacards"
BIN_NAME  = "RecoHiggs_mass"
BKG       = "bkg_sum"
SIGNAL_RE = re.compile(r"^mgp8_ee_(ee|mumu)H_HAlpAlp_(m[0-9p]+)_ecm240_(ctau[0-9]+m+)$")

def axis(h):
    ax = h.GetXaxis()
    return h.GetNbinsX(), ax.GetXmin(), ax.GetXmax()

def print_axis(label, h):
    n, xmin, xmax = axis(h)
    print(f"  {label}: {n} bins, [{xmin:.1f}, {xmax:.1f}] GeV, "
          f"integral={h.Integral():.4g}")

def list_signals(path):
    import ROOT
    ROOT.gROOT.SetBatch(True)

    tf = ROOT.TFile.Open(path)
    if not tf or tf.IsZombie():
        raise SystemExit(f"Cannot open fit_histos file: {path}")
    h_bkg = tf.Get(BKG)
    if not h_bkg:
        raise SystemExit(f"Missing '{BKG}' in {path}")
    print("fit_histos (Combine templates):")
    print_axis(BKG, h_bkg)
    fitted_axis = axis(h_bkg)

    h_data = tf.Get(DATA_HIST)
    if not h_data:
        raise SystemExit(f"Missing data_obs hist '{DATA_HIST}' in {path}")
    print_axis(f"data_obs={DATA_HIST}", h_data)
    if axis(h_data) != fitted_axis:
        raise SystemExit("data_obs and bkg_sum binning differ in the fitted file.")

    merged_bkg = os.path.join(MERGED_DIR, f"bkg_sum_{MERGED_CUT}_histo.root")
    if os.path.isfile(merged_bkg):
        mf = ROOT.TFile.Open(merged_bkg)
        h_m = mf.Get(MERGED_VAR) if mf and not mf.IsZombie() else None
        print("merge_histos (upstream of fit; not used in the card):")
        if h_m:
            print_axis(f"bkg_sum/{MERGED_VAR}", h_m)
            if axis(h_m) != fitted_axis:
                print("  (different axis is expected: fit_histos rebins to the SR)")
        mf.Close()
    else:
        print(f"merge_histos file not found (ok): {merged_bkg}")

    names, skipped = [], []
    for k in tf.GetListOfKeys():
        name = k.GetName()
        if not SIGNAL_RE.match(name):
            continue
        h = tf.Get(name)
        integral = h.Integral() if h else 0.0
        if integral > 0.0:
            names.append(name)
        else:
            skipped.append(name)
    tf.Close()

    names = sorted(set(names))
    if skipped:
        print(f"Skipping {len(skipped)} empty signal histogram(s):")
        for name in skipped:
            print(f"  {name}")
    if not names:
        raise SystemExit(f"No non-empty signal histograms in {path}")
    return names

def write_datacard(card_path, signal):
    card = f"""\
# text2workspace.py  datacard.txt  -o ws.root
# combine -M AsymptoticLimits ws.root -t -1 --expectSignal=1 > result.txt

imax	1 number of bins
jmax	* number of processes minus 1
kmax	* number of nuisance parameters
--------------------------------------------------------------------------------
shapes	data_obs	*	{DATA_FILE}	{DATA_HIST}
shapes	*		*	{SHAPES}	$PROCESS
--------------------------------------------------------------------------------
bin			{BIN_NAME}
observation		-1
--------------------------------------------------------------------------------
bin			{BIN_NAME}		{BIN_NAME}
process		{signal}	{BKG}
process		0		1
rate		-1		-1
--------------------------------------------------------------------------------
scale rateParam * {BKG} 1.0 [0,20]

* autoMCStats 1 1
"""
    with open(card_path, "w") as f:
        f.write(card)

def existing_sample_dirs():
    if not os.path.isdir(OUTDIR):
        return []
    dirs = []
    for name in sorted(os.listdir(OUTDIR)):
        if not SIGNAL_RE.match(name):
            continue
        sample_dir = os.path.join(OUTDIR, name)
        if os.path.isfile(os.path.join(sample_dir, "datacard.txt")):
            dirs.append(sample_dir)
    return dirs

def run_combine(sample_dir):
    tw = shutil.which("text2workspace.py")
    comb = shutil.which("combine")
    if tw is None or comb is None:
        raise SystemExit(
            "text2workspace.py / combine not in PATH.\n"
            "srcroot removes the Combine environment. In a new shell run:\n"
            "  srccms\n"
            "  python make_datacards.py --run"
        )

    commands = [
        [tw, "datacard.txt", "-o", "ws.root"],
        [comb, "-M", "AsymptoticLimits", "ws.root",
         "-t", "-1", "--expectSignal=1", "-m", "120"],
    ]
    result_path = os.path.join(sample_dir, "result.txt")
    with open(result_path, "w") as result:
        for cmd in commands:
            proc = subprocess.run(
                cmd,
                cwd=sample_dir,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
            )
            result.write(f"$ {' '.join(cmd)}\n")
            result.write(proc.stdout)
            result.write("\n")
            sys.stdout.write(proc.stdout)
            if proc.returncode != 0:
                raise SystemExit(
                    f"{os.path.basename(cmd[0])} failed in {sample_dir} "
                    f"(exit {proc.returncode})"
                )

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--run",
        action="store_true",
        help="Run Combine in each sample dir (needs srccms, not srcroot)",
    )
    args = parser.parse_args()

    if not args.run:
        if not os.path.isfile(SHAPES):
            raise SystemExit(f"Missing fit_histos file: {SHAPES}")
        signals = list_signals(SHAPES)
        os.makedirs(OUTDIR, exist_ok=True)
        print(f"data_obs : {DATA_FILE}  ({DATA_HIST})")
        print(f"shapes   : {SHAPES}")
        print(f"outdir   : {OUTDIR}")
        print(f"cards    : {len(signals)}")
        for signal in signals:
            sample_dir = os.path.join(OUTDIR, signal)
            os.makedirs(sample_dir, exist_ok=True)
            write_datacard(os.path.join(sample_dir, "datacard.txt"), signal)
            print(f"  {sample_dir}/datacard.txt")
        print("\nNow in a new shell:")
        print("  srccms")
        print(f"  python {os.path.basename(sys.argv[0])} --run")
        return

    sample_dirs = existing_sample_dirs()
    if not sample_dirs:
        raise SystemExit(
            f"No datacard.txt under {OUTDIR}.\n"
            "First run:  srcroot && python make_datacards.py"
        )
    print(f"Running Combine in {len(sample_dirs)} directories")
    for sample_dir in sample_dirs:
        print(f"=== {os.path.basename(sample_dir)} ===")
        run_combine(sample_dir)

if __name__ == "__main__":
    main()