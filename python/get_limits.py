#!/usr/bin/env python3
"""limit plots vs m_a: one figure per flavour, linear sigma x BR [pb]"""

from __future__ import annotations
import os
import re
from collections import defaultdict
import numpy as np
import matplotlib.pyplot as plt
import ROOT

try:
    import mplhep as hep
    plt.style.use(hep.style.CMS)
except Exception:
    pass

plt.rcParams.update({"font.size": 20})
ROOT.gROOT.SetBatch(True)

DATACARD_DIR = "/ceph/salshamaily/haa4K_FCCee/combine/datacards"
OUT_DIR = "/ceph/salshamaily/haa4K_FCCee/analysis/plots_output/statistics"
COMBINE_FILE = "higgsCombineTest.AsymptoticLimits.mH120.root"
# None = most sensitive ctau at each mass. Or e.g. "1mm".
CTAU = None
SIGNAL_RE = re.compile(r"^mgp8_ee_(ee|mumu)H_HAlpAlp_(m[0-9p]+)_ecm240_(ctau[0-9]+m+)$")
CTAU_ORDER = ["1mm", "10mm", "1m", "2m"]
CHANNEL_LABEL = {
    "ee": r"$Z\to e^+e^-$",
    "mumu": r"$Z\to\mu^+\mu^-$",}
Q_EXP, Q_M1, Q_P1 = 0.50, 0.16, 0.84
Q_M2, Q_P2 = 0.025, 0.975
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
    ("ee", 60.0): 1.17362e-02, ("mumu", 60.0): 1.17360e-02,}

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
        m2 = match_quantile(qmap, Q_M2)
        p2 = match_quantile(qmap, Q_P2)
        if exp is None or m1 is None or p1 is None:
            print(f"skip {name}: missing median or +/-1sigma")
            continue
        if m2 is None:
            m2 = m1
            print(f"note {name}: missing 0.025, using 0.16 for -2sigma")
        if p2 is None:
            p2 = p1
            print(f"note {name}: missing 0.975, using 0.84 for +2sigma")

        flavour, mass_tag, ctau_tag = match.groups()
        mass = mass_from_tag(mass_tag)
        ctau = ctau_from_tag(ctau_tag)
        xsec = XSEC_PB.get((flavour, mass))
        if xsec is None:
            print(f"skip {name}: no xsec for {(flavour, mass)}")
            continue

        rows.append(
            dict(
                channel=flavour,
                ctau=ctau,
                mass=mass,
                exp=exp,
                m1=m1,
                p1=p1,
                m2=m2,
                p2=p2,
                xsec=xsec,
            )
        )
    return rows

def pick_points(rows, channel):
    by_mass = defaultdict(list)
    for r in rows:
        if r["channel"] != channel:
            continue
        if CTAU is not None and r["ctau"] != CTAU:
            continue
        by_mass[r["mass"]].append(r)

    picked = []
    for mass in sorted(by_mass):
        cands = by_mass[mass]
        best = min(cands, key=lambda r: r["exp"] * r["xsec"])
        picked.append(best)
        if CTAU is None and len(cands) > 1:
            print(
                f"{channel}  m_a={mass:g} GeV  using ctau={best['ctau']}  "
                f"sigmaBR={best['exp'] * best['xsec']:.3e} pb"
            )
    return picked

def draw_channel(rows, channel):
    pts = pick_points(rows, channel)
    if not pts:
        print(f"no points for {channel}")
        return

    ma = np.array([p["mass"] for p in pts], dtype=float)
    exp = np.array([p["exp"] * p["xsec"] for p in pts], dtype=float)
    m1 = np.array([p["m1"] * p["xsec"] for p in pts], dtype=float)
    p1 = np.array([p["p1"] * p["xsec"] for p in pts], dtype=float)
    m2 = np.array([p["m2"] * p["xsec"] for p in pts], dtype=float)
    p2 = np.array([p["p2"] * p["xsec"] for p in pts], dtype=float)

    theo_m, theo_s = [], []
    for (flav, mass), xsec in sorted(XSEC_PB.items()):
        if flav == channel:
            theo_m.append(mass)
            theo_s.append(xsec)
    theo_m = np.array(theo_m)
    theo_s = np.array(theo_s)

    fig, ax = plt.subplots()
    fill_2s = ax.fill_between(ma, m2, p2, color="gold", alpha=1.0, zorder=1)
    fill_1s = ax.fill_between(ma, m1, p1, color="limegreen", alpha=1.0, zorder=2)
    line_theo = ax.plot(
        theo_m, theo_s, color="red", linewidth=2, linestyle="-", zorder=3
    )
    line_exp = ax.plot(
        ma,
        exp,
        color="black",
        linestyle="--",
        marker="o",
        markersize=7,
        linewidth=2,
        zorder=4,
    )

    ax.set_xlabel(r"$m_a$ [GeV]")
    ax.set_ylabel(
        r"$\sigma \times \mathrm{BR}(H\rightarrow aa\rightarrow K^+K^-K^+K^-)$ [pb]"
    )
    ax.set_xlim(ma.min(), ma.max())
    ax.set_ylim(0.0, float(np.max(p2)) * 1.25)
    ax.ticklabel_format(axis="y", style="sci", scilimits=(0, 0))
    ax.yaxis.get_offset_text().set_fontsize(20)
    ax.set_title(
        r"$\mathbf{FCCAnalyses:\ FCC\!-\!ee\ Simulation\ (Delphes)}$",
        loc="center",
        fontsize=18,
        pad=14,
    )

    LEPTON_TEX = {"ee": r"e^+e^-", "mumu": r"\mu^+\mu^-"}
    info_lines = "\n".join([
        r"$\sqrt{s} = 240.0$ GeV",
        r"$\mathcal{L} = 10.8$ ab$^{-1}$",
        rf"$e^+e^- \rightarrow ZH,\ Z\rightarrow {LEPTON_TEX[channel]},\ H\rightarrow aa$",
    ])
    ax.text(
        0.03,
        0.95,
        info_lines,
        transform=ax.transAxes,
        fontsize=14,
        va="top",
        ha="left",
        linespacing=1.6,
    )

    ax.legend(
        handles=[line_exp[0], line_theo[0], fill_1s, fill_2s],
        labels=["Expected Limit", "Theoretical Limit", "68% expected", "95% expected"],
        loc="upper right",
        frameon=False,
        fontsize=13,
    )
    fig.subplots_adjust(left=0.18, right=0.97, bottom=0.15, top=0.88)
    os.makedirs(OUT_DIR, exist_ok=True)
    out = os.path.join(OUT_DIR, f"limit_{channel}")
    fig.savefig(out + ".pdf")
    fig.savefig(out + ".png", dpi=200)
    print(f"Wrote {out}.pdf")
    plt.close(fig)

def print_table(rows):
    print("\nchannel  ctau    m_a [GeV]   mu_exp    sigmaBR_exp [pb]")
    print("-" * 62)
    for r in sorted(
        rows, key=lambda x: (x["channel"], CTAU_ORDER.index(x["ctau"]), x["mass"])
    ):
        print(
            f"{r['channel']:6s}  {r['ctau']:6s}  {r['mass']:9.2f}  "
            f"{r['exp']:8.3g}  {r['exp'] * r['xsec']:8.3g}"
        )

if __name__ == "__main__":
    rows = load_rows()
    print(f"Loaded {len(rows)} limit points")
    if not rows:
        raise SystemExit("No usable Combine outputs")
    print_table(rows)
    draw_channel(rows, "ee")
    draw_channel(rows, "mumu")