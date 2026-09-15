#!/usr/bin/env python3

from __future__ import annotations
import os
import re
from collections import defaultdict
import numpy as np
import matplotlib.pyplot as plt
import ROOT

ROOT.gROOT.SetBatch(True)

DATACARD_DIR = "/ceph/salshamaily/haa4K_FCCee/combine/datacards"
OUT_DIR = "/ceph/salshamaily/haa4K_FCCee/analysis/plots_output/limits"
COMBINE_FILE = "higgsCombineTest.AsymptoticLimits.mH120.root"
SIGNAL_RE = re.compile(r"^mgp8_ee_(ee|mumu)H_HAlpAlp_(m[0-9p]+)_ecm240_(ctau[0-9]+m+)$")
CTAU_ORDER = ["1mm", "10mm", "1m", "2m"]
CHANNEL_LABEL = {
    "ee": r"$Z\to e^+e^-$",
    "mumu": r"$Z\to\mu^+\mu^-$",
}

# quantileExpected -> name. Median and +/-1sigma are required.
Q_EXP, Q_M1, Q_P1 = 0.50, 0.16, 0.84
Q_M2, Q_P2, Q_OBS = 0.025, 0.975, -1.0

# Generated MadGraph cross sections [pb], same as finalSel.py
XSEC_PB = {
    ("ee", 0.05): 9.5532e-04, ("mumu", 0.05): 9.5531e-04,
    ("ee", 0.1): 9.5532e-04, ("mumu", 0.1): 9.5531e-04,
    ("ee", 0.5): 9.5537e-04, ("mumu", 0.5): 9.5536e-04,
    ("ee", 1.0): 9.5553e-04, ("mumu", 1.0): 9.5552e-04,
    ("ee", 1.5): 9.5581e-04, ("mumu", 1.5): 9.5580e-04,
    ("ee", 5.0): 9.6079e-04, ("mumu", 5.0): 9.6079e-04,
    ("ee", 10.0): 9.7750e-04, ("mumu", 10.0): 9.7749e-04,
    ("ee", 20.0): 1.0460e-03, ("mumu", 20.0): 1.0460e-03,
    ("ee", 30.0): 1.1290e-03, ("mumu", 30.0): 1.1290e-03,
    ("ee", 40.0): 6.9960e-02, ("mumu", 40.0): 6.9920e-02,
    ("ee", 50.0): 3.9978e-02, ("mumu", 50.0): 3.9972e-02,
    ("ee", 60.0): 1.17362e-02, ("mumu", 60.0): 1.17360e-02,
}

def mass_from_tag(tag):
    return float(tag[1:].replace("p", "."))

def ctau_from_tag(tag):
    return tag.replace("ctau", "")

def match_quantile(qmap, target, tol=2e-3):
    for q, val in qmap.items():
        if abs(q - target) < tol:
            return val
    return None

def read_quantiles(path):
    tf = ROOT.TFile.Open(path)
    if not tf or tf.IsZombie():
        return None
    tree = tf.Get("limit")
    if not tree:
        tf.Close()
        return None
    qmap = {}
    for i in range(tree.GetEntries()):
        tree.GetEntry(i)
        qmap[float(tree.quantileExpected)] = float(tree.limit)
    tf.Close()
    return qmap

def load_rows():
    rows = []
    if not os.path.isdir(DATACARD_DIR):
        raise SystemExit(f"Missing {DATACARD_DIR}")

    for name in sorted(os.listdir(DATACARD_DIR)):
        match = SIGNAL_RE.match(name)
        if not match:
            continue
        path = os.path.join(DATACARD_DIR, name, COMBINE_FILE)
        if not os.path.isfile(path):
            print(f"skip {name}: missing {COMBINE_FILE}")
            continue

        qmap = read_quantiles(path)
        if not qmap:
            print(f"skip {name}: empty or unreadable limit tree")
            continue

        exp = match_quantile(qmap, Q_EXP)
        m1 = match_quantile(qmap, Q_M1)
        p1 = match_quantile(qmap, Q_P1)
        if exp is None or m1 is None or p1 is None:
            print(f"skip {name}: {path}: missing median or +/-1sigma")
            continue

        m2 = match_quantile(qmap, Q_M2)
        p2 = match_quantile(qmap, Q_P2)
        if m2 is None:
            print(f"note {name}: missing quantile 0.025, using +/-1sigma")
            m2 = m1
        if p2 is None:
            print(f"note {name}: missing quantile 0.975, using +/-1sigma")
            p2 = p1

        channel = match.group(1)
        mass = mass_from_tag(match.group(2))
        ctau = ctau_from_tag(match.group(3))
        xsec = XSEC_PB.get((channel, mass), np.nan)

        rows.append(
            dict(
                name=name,
                channel=channel,
                mass=mass,
                ctau=ctau,
                exp=exp,
                m1=m1,
                p1=p1,
                m2=m2,
                p2=p2,
                obs=match_quantile(qmap, Q_OBS),
                xsec=xsec,
            )
        )
    return rows

def draw_brazil(ax, pts, ylabel):
    pts = sorted(pts, key=lambda r: r["mass"])
    m = np.array([r["mass"] for r in pts])
    exp = np.array([r["exp"] for r in pts])
    m1 = np.array([r["m1"] for r in pts])
    p1 = np.array([r["p1"] for r in pts])
    m2 = np.array([r["m2"] for r in pts])
    p2 = np.array([r["p2"] for r in pts])

    ax.fill_between(m, m2, p2, color="#F5BB54", lw=0, zorder=1, label=r"Expected $\pm 2\sigma$")
    ax.fill_between(m, m1, p1, color="#8CD48C", lw=0, zorder=2, label=r"Expected $\pm 1\sigma$")
    ax.plot(m, exp, color="black", ls="--", lw=1.4, zorder=3, label="Median expected")
    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.set_xlabel(r"$m_a$ [GeV]")
    ax.set_ylabel(ylabel)
    ax.set_xticks(m)
    ax.set_xticklabels([f"{x:g}" for x in m], rotation=45, ha="right")
    ax.minorticks_off()
    ax.grid(True, which="major", alpha=0.25)

def plot(rows):
    os.makedirs(OUT_DIR, exist_ok=True)

    by_key = defaultdict(list)
    for row in rows:
        by_key[(row["channel"], row["ctau"])].append(row)

    for channel in ("ee", "mumu"):
        fig, axes = plt.subplots(2, 2, figsize=(11.0, 8.5), sharex=False)
        axes = axes.ravel()
        handles, labels = None, None
        for i, ctau in enumerate(CTAU_ORDER):
            ax = axes[i]
            pts = by_key.get((channel, ctau), [])
            ax.set_title(rf"{CHANNEL_LABEL[channel]}, $c\tau_a={ctau}$")
            if not pts:
                ax.text(0.5, 0.5, "no points", ha="center", va="center", transform=ax.transAxes)
                continue
            draw_brazil(ax, pts, r"Expected 95% CL limit on $\mu$")
            handles, labels = ax.get_legend_handles_labels()

        fig.suptitle(
            r"$e^+e^-\to ZH,\ H\to aa\to K^+K^-K^+K^-$"
            "\n"
            r"FCC-ee IDEA, $\sqrt{s}=240$ GeV, $\mathcal{L}=10.8$ ab$^{-1}$",
            fontsize=13,
        )
        if handles:
            fig.legend(handles, labels, loc="center left", bbox_to_anchor=(0.82, 0.5), frameon=False)
        fig.subplots_adjust(left=0.10, right=0.80, bottom=0.10, top=0.86, wspace=0.32, hspace=0.38)
        out = os.path.join(OUT_DIR, f"limits_{channel}_mu")
        fig.savefig(out + ".pdf")
        fig.savefig(out + ".png", dpi=200)
        print(f"Wrote {out}.pdf")
        plt.close(fig)

        fig, axes = plt.subplots(2, 2, figsize=(11.0, 8.5))
        axes = axes.ravel()
        handles, labels = None, None
        for i, ctau in enumerate(CTAU_ORDER):
            ax = axes[i]
            pts = by_key.get((channel, ctau), [])
            ax.set_title(rf"{CHANNEL_LABEL[channel]}, $c\tau_a={ctau}$")
            xsec_pts = []
            for r in pts:
                if not np.isfinite(r["xsec"]):
                    continue
                xsec_pts.append(
                    dict(
                        mass=r["mass"],
                        exp=r["exp"] * r["xsec"],
                        m1=r["m1"] * r["xsec"],
                        p1=r["p1"] * r["xsec"],
                        m2=r["m2"] * r["xsec"],
                        p2=r["p2"] * r["xsec"],
                    )
                )
            if not xsec_pts:
                ax.text(0.5, 0.5, "no points", ha="center", va="center", transform=ax.transAxes)
                continue
            draw_brazil(ax, xsec_pts, r"Expected 95% CL limit on $\sigma\times\mathcal{B}$ [pb]")
            handles, labels = ax.get_legend_handles_labels()

        fig.suptitle(
            r"$e^+e^-\to ZH,\ H\to aa\to K^+K^-K^+K^-$"
            "\n"
            r"FCC-ee IDEA, $\sqrt{s}=240$ GeV, $\mathcal{L}=10.8$ ab$^{-1}$",
            fontsize=13,
        )
        if handles:
            fig.legend(handles, labels, loc="center left", bbox_to_anchor=(0.82, 0.5), frameon=False)
        fig.subplots_adjust(left=0.10, right=0.80, bottom=0.10, top=0.86, wspace=0.32, hspace=0.38)
        out = os.path.join(OUT_DIR, f"limits_{channel}_xsec")
        fig.savefig(out + ".pdf")
        fig.savefig(out + ".png", dpi=200)
        print(f"Wrote {out}.pdf")
        plt.close(fig)

def print_table(rows):
    print("\nchannel  ctau    m_a [GeV]   mu_exp    mu-1s     mu+1s     xsec[pb]")
    print("-" * 76)
    for r in sorted(rows, key=lambda x: (x["channel"], CTAU_ORDER.index(x["ctau"]), x["mass"])):
        print(
            f"{r['channel']:6s}  {r['ctau']:6s}  {r['mass']:9.2f}  "
            f"{r['exp']:8.3g}  {r['m1']:8.3g}  {r['p1']:8.3g}  {r['xsec']:8.3g}"
        )

if __name__ == "__main__":
    rows = load_rows()
    print(f"Loaded {len(rows)} limit points")
    if not rows:
        raise SystemExit("No usable Combine outputs")
    print_table(rows)
    plot(rows)