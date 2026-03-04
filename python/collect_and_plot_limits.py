#!/usr/bin/env python3
"""
Script to collect and plot limit results from multiple mass hypotheses.
"""

import os
import ROOT
import argparse
import glob
from pathlib import Path
import json
import numpy as np
import matplotlib.pyplot as plt
import uproot
import mplhep as hep   

combined_dirs 	= glob.glob("/ceph/salshamaily/haa4K_FCCee/datacards/mass*")
ma_values 		= []
expected_limits = []
one_sigma_minus = []
one_sigma_plus 	= []
two_sigma_minus = []
two_sigma_plus 	= []

# xsec for different alp mass points
xsec_alp_dict = {1.5:0.0009558, 30:0.001129, 60:0.01174}

for dir in combined_dirs:
    ma 			= float(dir.split("mass")[-1])
    
    xsec_alp 	= xsec_alp_dict[ma]

    uproot_file = uproot.open(os.path.join(dir, "higgsCombineTest.AsymptoticLimits.mH120.root"))
    tree 		= uproot_file["limit"]
    limits 		= tree.arrays(library="np")["limit"]
    quantiles 	= tree.arrays(library="np")["quantileExpected"]

    exp_limit 			= limits[quantiles == 0.5][0]*xsec_alp
    exp_limit_1s_minus 	= limits[quantiles == 0.16][0]*xsec_alp
    exp_limit_1s_plus 	= limits[quantiles == 0.84][0]*xsec_alp
    exp_limit_2s_minus 	= limits[quantiles == 0.025][0]*xsec_alp
    exp_limit_2s_plus 	= limits[quantiles == 0.975][0]*xsec_alp

    ma_values.append(ma)
    expected_limits.append(exp_limit)
    one_sigma_minus.append(exp_limit_1s_minus)
    one_sigma_plus.append(exp_limit_1s_plus)
    two_sigma_minus.append(exp_limit_2s_minus)
    two_sigma_plus.append(exp_limit_2s_plus)

# Sort by ma values
sorted_indices 	= np.argsort(ma_values)
ma_values 		= np.array(ma_values)[sorted_indices]
expected_limits = np.array(expected_limits)[sorted_indices]
one_sigma_minus = np.array(one_sigma_minus)[sorted_indices]
one_sigma_plus 	= np.array(one_sigma_plus)[sorted_indices]
two_sigma_minus = np.array(two_sigma_minus)[sorted_indices]
two_sigma_plus 	= np.array(two_sigma_plus)[sorted_indices]

# Plotting
plt.style.use(hep.style.CMS)
plt.rcParams.update({'font.size': 20})
fig, ax = plt.subplots()

line_exp	= ax.plot(ma_values, expected_limits, label="Expected Limit", color="black", linestyle="--")
fill_2s 	= ax.fill_between(ma_values, two_sigma_minus, two_sigma_plus, color="gold", alpha=1, label="95% expected")
fill_1s 	= ax.fill_between(ma_values, one_sigma_minus, one_sigma_plus, color="limegreen", alpha=1, label="68% expected")

ax.set_xlabel(r"$m_a$ [GeV]")
ax.set_xlim(ma_values.min(), ma_values.max())

ax.set_ylabel(r"$\mathrm{BR}(H\rightarrow aa\rightarrow K^+K^-K^+K^-)$")
ax.set_ylim(top= max(two_sigma_plus)*1.25)

ax.set_title(r"$\it{" + "FCCAnalyses \: " + "}$" +" "+ r"$\bf{" + "FCC-ee Simulation (Delphes)" + "}$",loc="left", fontsize=18)
ax.set_title(f"10.8 pb$^{{-1}}$ (240 $\mathrm{{{{GeV}}}}$)",loc="right", fontsize=20)

# Custom legend order: Expected, 68%, 95%
handles = [line_exp[0], fill_1s, fill_2s]
labels 	= ["Expected Limit", "68% expected", "95% expected"]
plt.legend(handles=handles, labels=labels)

plt.savefig("combined_limits.png")
plt.savefig("combined_limits.pdf")

print("Lowest expected limit at m$_a$ =", ma_values[np.argmin(expected_limits)], "GeV with limit =", np.min(expected_limits), " plus ", one_sigma_plus[np.argmin(expected_limits)] - np.min(expected_limits), "minus ", np.abs(one_sigma_minus[np.argmin(expected_limits)] - np.min(expected_limits)))
print("Highest expected limit at m$_a$ =", ma_values[np.argmax(expected_limits)], "GeV with limit =", np.max(expected_limits), " plus ", one_sigma_plus[np.argmax(expected_limits)] - np.max(expected_limits), "minus ", np.abs(one_sigma_minus[np.argmax(expected_limits)] - np.max(expected_limits)))