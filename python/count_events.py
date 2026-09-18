#!/usr/bin/env python3
"""
count_events.py

Counts surviving events for any number of named stage1(+final) output
directories -- e.g. "filter1", "filter1_filter2", "filter1_lepton",
"filter1_filter2_lepton" -- and compares each against a fixed, known
generated-sample size (you don't need a "no filters" run since you already
know each signal sample was generated with 500,000 events).

For every process x every stage it reports:
  n_events        events in that stage's output ntuple
  efficiency      n_events / n_generated

Only run this AFTER you have the ROOT output files on disk for every stage
you list in STAGE_DIRS below (i.e. after running stage1 [+ final] with the
corresponding filter combination active, to its own output directory).

Usage:
    python count_events.py
Edit the CONFIG block below before running.
"""

import os
import glob
import csv
import ROOT
from analysis_stage1 import processList

N_GENERATED = 500000

# use after stage1 and not  final to avoid final stage selection
STAGE_DIRS = {
    "selk":	"/ceph/salshamaily/haa4K_FCCee/analysis/filter1",
    "pt":	"/ceph/salshamaily/haa4K_FCCee/analysis/filter12",
    "all":	"/ceph/salshamaily/haa4K_FCCee/sig_samples",
}

TREE_NAME = "events"

PROCESS_LIST = list(processList.keys())
# PROCESS_LIST = [
    # "mgp8_ee_eeH_HAlpAlp_m0p05_ecm240_ctau1mm",
    # ... add every process key here, or import as shown above
# ]

OUTPUT_CSV = "cutflow_counts.csv"

def find_files(base_dir, proc):
    """Handle both 'proc.root' (single file) and 'proc/*.root' (chunked) layouts."""
    single = os.path.join(base_dir, f"{proc}.root")
    if os.path.isfile(single):
        return [single]
    chunked = sorted(glob.glob(os.path.join(base_dir, proc, "*.root")))
    return chunked

def count_tree_entries(files):
    """Sum TTree entries across all files for a process."""
    if not files:
        return None
    n = 0
    for f in files:
        tf = ROOT.TFile.Open(f)
        if not tf or tf.IsZombie():
            print(f"[WARN] could not open {f}")
            continue
        tree = tf.Get(TREE_NAME)
        if tree:
            n += tree.GetEntries()
        else:
            print(f"[WARN] no tree '{TREE_NAME}' found in {f}")
        tf.Close()
    return n

def get_n_generated(proc):
    if isinstance(N_GENERATED, dict):
        return N_GENERATED.get(proc)
    return N_GENERATED

def main():
    if not STAGE_DIRS:
        print("STAGE_DIRS is empty -- add at least one stage name -> directory.")
        return

    rows = []
    for proc in PROCESS_LIST:
        n_gen = get_n_generated(proc)
        row = {"process": proc, "n_generated": n_gen}
        summary_bits = []

        for stage_name, stage_dir in STAGE_DIRS.items():
            files = find_files(stage_dir, proc)
            if not files:
                print(f"[WARN] no files found for '{proc}' in {stage_dir}")
            n_events = count_tree_entries(files)

            row[f"{stage_name}_n_events"] = n_events
            if n_events is not None and n_gen:
                eff = n_events / n_gen
                row[f"{stage_name}_efficiency"] = eff
                summary_bits.append(f"{stage_name}={n_events} (eff={eff:.4f})")
            else:
                row[f"{stage_name}_efficiency"] = None
                summary_bits.append(f"{stage_name}=MISSING")

        rows.append(row)
        print(f"{proc}: n_generated={n_gen}  " + "  ".join(summary_bits))

    if rows:
        with open(OUTPUT_CSV, "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=rows[0].keys())
            writer.writeheader()
            writer.writerows(rows)
        print(f"\nWrote {len(rows)} rows to {OUTPUT_CSV}")
    else:
        print("No rows collected -- check STAGE_DIRS / PROCESS_LIST")

if __name__ == "__main__":
    main()