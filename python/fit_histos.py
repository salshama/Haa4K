"""
bkg_sum_{cut}_histo.root       (one file, summed over all bkg processes)
mgp8_ee_*HAlpAlp*_{cut}_histo.root   (one file per signal mass point)

For the chosen VARIABLE:
    1. Loads the summed background histogram.
    2. Optionally rebins it coarser (BKG_REBIN) before fitting, since a fit
       to a very finely-binned, low-stats background is noisy.
    3. Fits several candidate smooth functions (expo, pol2, pol3, pol5) over
       a wide range, prints a goodness-of-fit comparison table for all of
       them, and picks the best one (or uses FORCE_FIT_FUNC if you set it).
    4. Samples the chosen fit onto a fine signal-region (SR) binning.
    5. Rebins each signal process onto the same fine SR binning.
    6. Writes one combined output ROOT file per variable/cut.
       Also makes per-signal and combined plots, restricted to a
       user-selected subset of signal points (mass x ctau).
"""

import re
import glob
import os
import colorsys
import itertools
import ROOT

ROOT.gROOT.SetBatch(True)

##########
# CONFIG #
##########
CUT        = "RecoKaonElecSel"   # or "RecoHiggsMassCut"
MERGED_DIR = "/ceph/salshamaily/haa4K_FCCee/merged_samples"
OUTPUT_DIR = "/ceph/salshamaily/haa4K_FCCee/combine/ready_samples"
PLOT_DIR   = "/ceph/salshamaily/haa4K_FCCee/analysis/plots_output/rebinned"
DIAG_DIR   = "/ceph/salshamaily/haa4K_FCCee/analysis/plots_output/statistics"

energy    = 240
collider  = "FCC-ee"
intLumi   = 10.8  # ab^-1

VARIABLE = "RecoHiggs_mass"

# Per-variable config:
#   sr_xmin/xmax/sr_nbins : fine signal-region binning (output binning)
#   fit_xmin/fit_xmax     : range over which the background fit is performed
#   bkg_rebin             : rebin factor applied to the *input* bkg histogram
#                           before fitting (coarser -> smoother/more stable fit)
#   axis_title            : x-axis label for plots

VARIABLE_CONFIG = {
    "RecoHiggs_mass": dict(
        sr_xmin=120.0, sr_xmax=130.0, sr_nbins=100,
        fit_xmin=50.0, fit_xmax=160.0, bkg_rebin=4,
        axis_title="RecoMass_{Higgs} [GeV]",
    ),
    "RecoZ_mass": dict(
        sr_xmin=80.0, sr_xmax=100.0, sr_nbins=100,
        fit_xmin=50.0, fit_xmax=160.0, bkg_rebin=4,
        axis_title="RecoMass_{Z} [GeV]",
    ),
    "alp_0_m": dict(
        sr_xmin=0.0, sr_xmax=70.0, sr_nbins=140,
        fit_xmin=0.0, fit_xmax=160.0, bkg_rebin=4,
        axis_title="m_{a,0} [GeV]",
    ),
    "alp_1_m": dict(
        sr_xmin=0.0, sr_xmax=70.0, sr_nbins=140,
        fit_xmin=0.0, fit_xmax=160.0, bkg_rebin=4,
        axis_title="m_{a,1} [GeV]",
    ),
}

cfg        = VARIABLE_CONFIG[VARIABLE]
sig_xmin   = cfg["sr_xmin"]
sig_xmax   = cfg["sr_xmax"]
sig_nbins  = cfg["sr_nbins"]
fit_xmin   = cfg["fit_xmin"]
fit_xmax   = cfg["fit_xmax"]
BKG_REBIN  = cfg["bkg_rebin"]
axis_title = cfg["axis_title"]

channel = VARIABLE

# background fit functions
FIT_CANDIDATES = ["expo", "pol2", "pol3", "pol5"]

# Set to one of FIT_CANDIDATES to force that choice; leave as None for the best
FORCE_FIT_FUNC = None

signal_files = glob.glob(f"{MERGED_DIR}/mgp8_ee_*HAlpAlp*_{CUT}_histo.root")
bkg_sum_file = f"{MERGED_DIR}/bkg_sum_{CUT}_histo.root"

# one combined output file per variable/cut: bkg_sum + every signal process
output_file = os.path.join(OUTPUT_DIR, f"{VARIABLE}_{CUT}_rebinned.root")

# Captures channel (ee/mumu), mass (e.g. "10p0"), and the FULL ctau string
# including its unit (e.g. "1mm" or "1m") as separate groups, so ctau values
# that share a leading digit but differ in unit (1mm vs 1m) are distinguished.
SIGNAL_PATTERN = re.compile(r"^mgp8_ee_(ee|mumu)H_HAlpAlp_m([0-9p]+)_ecm240_ctau([0-9]+m+)$")

SIGNAL_MASSES = ["10p0", "30p0", "60p0"]
SIGNAL_CTAUS  = ["1mm", "1m"]

# Full cross-product of the two lists above, in a fixed, reproducible order.
# If you need a specific subset instead of the full cross-product (e.g. you
# don't have every mass/ctau combination), just replace this line with an
# explicit list of (mass, ctau) tuples, e.g.:
#   SIGNAL_POINTS = [("10p0", "1mm"), ("30p0", "1m"), ("60p0", "1m")]
SIGNAL_POINTS = list(itertools.product(SIGNAL_MASSES, SIGNAL_CTAUS))

def _hex_from_hls(h_deg, l, s=0.65):
    h = (h_deg % 360) / 360.0
    r, g, b = colorsys.hls_to_rgb(h, l, s)
    return f"#{int(round(r*255)):02x}{int(round(g*255)):02x}{int(round(b*255)):02x}"

SIGNAL_COLOR_HEX = {
    "red":     "#e6194b",
    "blue":    "#4363d8",
    "magenta": "#f032e6",
    "orange":  "#f58231",
    "green":   "#3cb44b",
}
SIGNAL_COLOR_ORDER = ["red", "blue", "magenta", "orange", "green"]

def _color_hex_for_index(i):
    if i < len(SIGNAL_COLOR_ORDER):
        return SIGNAL_COLOR_HEX[SIGNAL_COLOR_ORDER[i]]
    return _hex_from_hls(h_deg=(i * 47) % 360, l=0.5)

# (mass, ctau) -> ROOT TColor index, assigned once, in SIGNAL_POINTS order
SIGNAL_POINT_COLOR = {
    point: ROOT.TColor.GetColor(_color_hex_for_index(i))
    for i, point in enumerate(SIGNAL_POINTS)
}

def pretty_label(proc):
    m = SIGNAL_PATTERN.match(proc)
    if not m:
        return proc
    mass = m.group(2).replace("p", ".")
    ctau = m.group(3)
    return f"m_{{a}} = {mass} GeV, c#tau = {ctau}"

def signal_point_of(proc_name):
    """
    Returns (mass, ctau) tuple for a signal proc name, or None
    """
    m = SIGNAL_PATTERN.match(proc_name)
    if not m:
        return None
    return (m.group(2), m.group(3))

def is_selected_signal(proc_name):
    """
    True if proc_name's (mass, ctau) is in SIGNAL_POINTS
    """
    point = signal_point_of(proc_name)
    return point is not None and point in SIGNAL_POINT_COLOR

def color_for_signal(proc_name):
    point = signal_point_of(proc_name)
    return SIGNAL_POINT_COLOR.get(point, ROOT.TColor.GetColor(_color_hex_for_index(0)))

def channel_of(proc_name):
    return "mumu" if "mumu" in proc_name.lower() else "ee"

def process_name(filepath, cut=CUT):
    basename = os.path.basename(filepath)
    suffix = f"_{cut}_histo.root"
    if basename.endswith(suffix):
        return basename[: -len(suffix)]
    return basename.replace("_histo.root", "")

def get_histogram(filepath, hist_name):
    f = ROOT.TFile.Open(filepath)
    if not f or f.IsZombie():
        raise RuntimeError(f"Cannot open file: {filepath}")

    h = f.FindObjectAny(hist_name)
    if not h:
        print(f"WARNING: {hist_name} not found in {filepath}")
        print("Available keys:")
        for key in f.GetListOfKeys():
            print(f"    {key.GetName()}")
        f.Close()
        return None

    if not isinstance(h, ROOT.TH1):
        print(f"WARNING: '{hist_name}' in '{filepath}' is not a TH1 histogram")
        f.Close()
        return h

    h_clone = h.Clone(hist_name)
    h_clone.SetDirectory(0)
    f.Close()
    return h_clone

def make_density_hist(h, name):
    """
    Clone h and divide bin content/error by bin width -> events/GeV
    """
    hd = h.Clone(name)
    hd.SetDirectory(0)
    for i in range(1, hd.GetNbinsX() + 1):
        w = hd.GetBinWidth(i)
        c = hd.GetBinContent(i)
        e = hd.GetBinError(i)
        hd.SetBinContent(i, c / w if w > 0 else 0.0)
        hd.SetBinError(i, e / w if w > 0 else 0.0)
    return hd

def fit_one_candidate(h_density, fit_func, fit_xmin, fit_xmax):
    """
    Fits a single TF1 candidate to h_density (events/GeV) over [fit_xmin,fit_xmax]
    """
    f1 = ROOT.TF1(f"bkg_fit_{fit_func}", fit_func, fit_xmin, fit_xmax)
    # Q: quiet, R: use TF1 range, S: return fit result, O: don't draw
    fit_result = h_density.Fit(f1, "QRSO")
    status = int(fit_result.Status())
    chi2 = fit_result.Chi2()
    ndf = fit_result.Ndf()
    prob = fit_result.Prob() if ndf > 0 else 0.0

    return dict(
        fit_func=fit_func,
        f1=f1,
        status=status,
        chi2=chi2,
        ndf=ndf,
        chi2_ndf=(chi2 / ndf if ndf > 0 else float("nan")),
        prob=prob,
    )

def print_comparison_table(results):
    print("\n" + "=" * 72)
    print(f"Background fit comparison for '{VARIABLE}' over [{fit_xmin}, {fit_xmax}] GeV")
    print("=" * 72)
    header = f"{'func':<8}{'status':>8}{'chi2':>12}{'ndf':>8}{'chi2/ndf':>12}{'p-value':>12}"
    print(header)
    print("-" * 72)
    for r in results:
        print(f"{r['fit_func']:<8}{r['status']:>8}{r['chi2']:>12.3f}{r['ndf']:>8}"
              f"{r['chi2_ndf']:>12.3f}{r['prob']:>12.4f}")
    print("-" * 72)

def choose_best_fit(results):
    if FORCE_FIT_FUNC is not None:
        for r in results:
            if r["fit_func"] == FORCE_FIT_FUNC:
                print(f"\nUsing FORCED fit function: {FORCE_FIT_FUNC}")
                return r
        raise RuntimeError(f"FORCE_FIT_FUNC='{FORCE_FIT_FUNC}' not in FIT_CANDIDATES={FIT_CANDIDATES}")

    # highest p-value among converged fits; fall back to best chi2/ndf
    converged = [r for r in results if r["status"] == 0 and r["ndf"] > 0]
    pool = converged if converged else results
    best = max(pool, key=lambda r: r["prob"])
    print(f"\nAuto-selected fit function: '{best['fit_func']}' "
          f"(p-value = {best['prob']:.4f}, chi2/ndf = {best['chi2_ndf']:.3f})")
    return best

def save_diagnostic_plot(h_density, results, best_func):
    os.makedirs(DIAG_DIR, exist_ok=True)

    c = ROOT.TCanvas("cdiag", "cdiag", 1100, 650)
    c.SetLogy()
    c.SetTicks(1, 1)

    c.SetLeftMargin(0.11)
    c.SetRightMargin(0.30)
    c.SetTopMargin(0.10)
    c.SetBottomMargin(0.12)

    h_density.SetStats(0)
    h_density.SetTitle(f"Background fit diagnostics")
    h_density.SetLineColor(ROOT.kBlack)
    h_density.SetMarkerColor(ROOT.kBlack)
    h_density.SetLineWidth(2)
    
    h_density.GetXaxis().SetTitle(axis_title)
    h_density.GetYaxis().SetTitle("Events / GeV")
    
    h_density.GetXaxis().SetTitleSize(0.045)
    h_density.GetYaxis().SetTitleSize(0.045)
    h_density.GetXaxis().SetLabelSize(0.040)
    h_density.GetYaxis().SetLabelSize(0.040)

    h_density.GetXaxis().SetTitleOffset(1.05)
    h_density.GetYaxis().SetTitleOffset(1.10)

    h_density.SetTitleSize(0.045, "T")
    h_density.SetTitleOffset(0.75, "T")

    h_density.Draw("E")

    leg = ROOT.TLegend(0.715,0.12,0.985,0.90)

    leg.SetTextSize(0.022)
    leg.SetTextFont(42)
    leg.SetFillColor(ROOT.kWhite)
    leg.SetBorderSize(1)
    leg.SetMargin(0.06)

    leg.AddEntry(h_density,"Summed bkg (rebinned)","lep")

    colors = [ROOT.kRed,ROOT.kBlue,ROOT.kGreen + 2,ROOT.kMagenta + 1]

    for i, r in enumerate(results):

        f1 = r["f1"]

        is_best = (r["fit_func"] == best_func)

        f1.SetLineColor(colors[i % len(colors)])
        f1.SetLineWidth(3 if is_best else 1)
        f1.SetLineStyle(1 if is_best else 2)

        f1.Draw("SAME")

        star = " (chosen)" if is_best else ""

        label = (
            f"{r['fit_func']}: "
            f"#chi^{{2}}/ndf={r['chi2_ndf']:.2f}, "
            f"p={r['prob']:.3f}{star}"
        )

        leg.AddEntry(f1, label, "l")

    leg.Draw()

    c.RedrawAxis()

    c.Update()

    out_base = os.path.join(
        DIAG_DIR,
        f"bkg_fit_comparison_{VARIABLE}_{CUT}"
    )

    c.SaveAs(out_base + ".pdf")
    c.SaveAs(out_base + ".png")

    print(
        f"Saved fit-comparison diagnostic plot: "
        f"{out_base}.png/.pdf"
    )

def build_bkg_sum():
    """
    Loads merged bkg_sum histogram, optionally rebins it coarser, fits
    every fit function, prints the comparison table, saves a
    diagnostic overlay, and returns the fine-binned bkg histogram sampled
    from the chosen best fit
    """
    print(f"Loading merged background sum: {bkg_sum_file}")
    h_sum_coarse_raw = get_histogram(bkg_sum_file, channel)
    if h_sum_coarse_raw is None:
        raise RuntimeError(f"Histogram '{channel}' not found in {bkg_sum_file}")

    print(f"Summed background integral (full range): {h_sum_coarse_raw.Integral():.2f}")
    print(f"Summed background integral (SR): "
          f"{h_sum_coarse_raw.Integral(h_sum_coarse_raw.FindBin(sig_xmin), h_sum_coarse_raw.FindBin(sig_xmax - 1e-6)):.2f}")

    # coarser rebin before fitting for smoother fit
    h_sum_coarse = h_sum_coarse_raw.Clone("h_sum_coarse_rebinned")
    h_sum_coarse.SetDirectory(0)
    if BKG_REBIN and BKG_REBIN > 1:
        h_sum_coarse.Rebin(BKG_REBIN)
        print(f"Rebinned bkg input by factor {BKG_REBIN} before fitting "
              f"({h_sum_coarse.GetNbinsX()} bins now)")

    h_density = make_density_hist(h_sum_coarse, "h_density_tmp")

    print(f"\nFitting {FIT_CANDIDATES} over [{fit_xmin},{fit_xmax}] GeV...")
    results = [fit_one_candidate(h_density, fn, fit_xmin, fit_xmax) for fn in FIT_CANDIDATES]
    print_comparison_table(results)

    best = choose_best_fit(results)
    save_diagnostic_plot(h_density, results, best["fit_func"])

    f1 = best["f1"]

    # sample chosen fit onto fine SR histogram
    h_fine = ROOT.TH1F("bkg_sum", "bkg_sum", sig_nbins, sig_xmin, sig_xmax)
    h_fine.SetDirectory(0)
    bin_width_fine = h_fine.GetBinWidth(1)

    for i in range(1, sig_nbins + 1):
        x = h_fine.GetBinCenter(i)
        val = max(f1.Eval(x) * bin_width_fine, 0.0)
        h_fine.SetBinContent(i, val)
        h_fine.SetBinError(i, ROOT.TMath.Sqrt(val) if val > 0 else 0.0)

    # rescale so integral in SR matches actual summed bkg
    integral_coarse = h_sum_coarse_raw.Integral(
        h_sum_coarse_raw.FindBin(sig_xmin), h_sum_coarse_raw.FindBin(sig_xmax - 1e-6))
    integral_fine = h_fine.Integral()

    if integral_fine > 0 and integral_coarse > 0:
        h_fine.Scale(integral_coarse / integral_fine)
        print(f"\nRescaled fine bkg histogram: coarse SR integral = {integral_coarse:.2f}, "
              f"fine SR integral (pre-scale) = {integral_fine:.2f}")
    elif integral_coarse == 0:
        print("WARNING: zero background yield in SR")

    return h_fine, best["fit_func"]

def build_signal_hist(signal_file):
    proc = process_name(signal_file)
    print(f"\nProcessing: {proc}")
    print(f"File: {os.path.basename(signal_file)}")

    h_raw = get_histogram(signal_file, channel)
    if h_raw is None:
        print(f"SKIPPING {proc} - histogram '{channel}' not found!")
        return proc, None

    print(f"Raw: {h_raw.GetNbinsX()} bins, "
          f"[{h_raw.GetXaxis().GetXmin():.1f}, {h_raw.GetXaxis().GetXmax():.1f}] GeV")
    print(f"Integral (full range): {h_raw.Integral():.2f}")
    print(f"Integral in SR: "
          f"{h_raw.Integral(h_raw.FindBin(sig_xmin), h_raw.FindBin(sig_xmax - 1e-6)):.2f}")

    h_sig = ROOT.TH1F(proc, proc, sig_nbins, sig_xmin, sig_xmax)
    h_sig.SetDirectory(0)

    raw_bin_width = h_raw.GetBinWidth(1)
    fine_bin_width = h_sig.GetBinWidth(1)
    scale = fine_bin_width / raw_bin_width if raw_bin_width > 0 else 1.0

    for i in range(1, sig_nbins + 1):
        x = h_sig.GetBinCenter(i)
        iraw = h_raw.FindBin(x)
        c = h_raw.GetBinContent(iraw)
        e = h_raw.GetBinError(iraw)
        h_sig.SetBinContent(i, max(c * scale, 0.0))
        h_sig.SetBinError(i, e * scale)

    print(f"Output integral in SR: {h_sig.Integral():.2f}")
    return proc, h_sig

def make_plots(proc_name, h_sig, bkg_hist, plot_dir):
    os.makedirs(plot_dir, exist_ok=True)
    label = pretty_label(proc_name)
    sig_color = color_for_signal(proc_name)

    for scale in ["lin", "log"]:
        c = ROOT.TCanvas(f"c_{proc_name}_{scale}", f"c_{proc_name}_{scale}", 800, 600)
        c.SetTicks(1, 1)
        c.SetLeftMargin(0.14)
        c.SetRightMargin(0.08)

        leg = ROOT.TLegend(0.55, 0.75, 0.90, 0.88)
        leg.SetFillColor(0); leg.SetFillStyle(0); leg.SetLineColor(0)
        leg.SetShadowColor(0); leg.SetTextSize(0.03)
        leg.SetTextFont(42); leg.SetBorderSize(0)

        bkg_hist.SetLineColor(ROOT.kBlack)
        bkg_hist.SetLineWidth(2)
        bkg_hist.SetFillStyle(0)
        bkg_hist.SetStats(0)
        bkg_hist.SetTitle("")
        bkg_hist.GetXaxis().SetTitle(axis_title)
        bkg_hist.GetYaxis().SetTitle("Events")
        bkg_hist.GetXaxis().SetTitleOffset(1.2)

        if scale == "log":
            bkg_hist.SetMinimum(1e-6)
            bkg_hist.SetMaximum(1e10)
        else:
            bkg_hist.SetMinimum(0)
            bkg_hist.SetMaximum(max(bkg_hist.GetMaximum(), h_sig.GetMaximum()) * 3)

        bkg_hist.Draw("HIST")
        leg.AddEntry(bkg_hist, "Sum bkg", "l")

        h_sig.SetLineColor(sig_color)
        h_sig.SetLineWidth(2)
        h_sig.SetFillStyle(0)
        h_sig.SetStats(0)
        h_sig.SetTitle("")
        h_sig.Draw("HIST SAME")
        leg.AddEntry(h_sig, label, "l")

        leftText = "FCCAnalyses: FCC-ee Simulation (Delphes)"
        rightText = f"#sqrt{{s}} = {energy} GeV, L = {intLumi} ab^{{-1}}"

        latex = ROOT.TLatex()
        latex.SetNDC()
        latex.SetTextSize(0.03)
        latex.DrawLatex(0.18, 0.84, f"#bf{{#it{{{rightText}}}}}")
        latex.SetTextAlign(31)
        latex.DrawLatex(0.92, 0.92, f"#it{{{leftText}}}")

        leg.Draw()
        if scale == "log":
            c.SetLogy()

        c.GetFrame().SetBorderSize(12)
        c.RedrawAxis()
        c.Modified()
        c.Update()

        out_base = f"{VARIABLE}_{CUT}_{proc_name}_{scale}"
        c.SaveAs(os.path.join(plot_dir, f"{out_base}.png"))
        c.SaveAs(os.path.join(plot_dir, f"{out_base}.pdf"))
        print(f"    Saved {scale} PDF and PNG for {proc_name}")

def make_combined_plot(channel_label, signal_hists, bkg_hist, plot_dir):
    os.makedirs(plot_dir, exist_ok=True)
    proc_names = sorted(signal_hists.keys())
    nsig = len(proc_names)

    for scale in ["lin", "log"]:
        c = ROOT.TCanvas(f"c_{channel_label}_{scale}", f"c_{channel_label}_{scale}", 800, 600)
        c.SetTicks(1, 1)
        c.SetLeftMargin(0.14)
        c.SetRightMargin(0.08)

        siglegsize = 0.04 * nsig
        sigleg = ROOT.TLegend(0.16, 0.70 - siglegsize, 0.45, 0.70)
        sigleg.SetFillColor(0); sigleg.SetFillStyle(0); sigleg.SetLineColor(0)
        sigleg.SetShadowColor(0); sigleg.SetTextSize(0.025)
        sigleg.SetTextFont(42); sigleg.SetBorderSize(0)

        bkgleg = ROOT.TLegend(0.45, 0.66, 0.90, 0.70)
        bkgleg.SetFillColor(0); bkgleg.SetFillStyle(0); bkgleg.SetLineColor(0)
        bkgleg.SetShadowColor(0); bkgleg.SetTextSize(0.025)
        bkgleg.SetTextFont(42); bkgleg.SetBorderSize(0)

        bkg_hist.SetLineColor(ROOT.kBlack)
        bkg_hist.SetLineWidth(2)
        bkg_hist.SetFillStyle(0)
        bkg_hist.SetStats(0)
        bkg_hist.SetTitle("")
        bkg_hist.GetXaxis().SetTitle(axis_title)
        bkg_hist.GetYaxis().SetTitle("Events")
        bkg_hist.GetXaxis().SetTitleOffset(1.2)

        if scale == "log":
            bkg_hist.SetMinimum(1e-6)
            bkg_hist.SetMaximum(1e10)
        else:
            max_sig = max((signal_hists[p].GetMaximum() for p in proc_names), default=1)
            bkg_hist.SetMinimum(0)
            bkg_hist.SetMaximum(max(bkg_hist.GetMaximum(), max_sig) * 3)

        bkg_hist.Draw("HIST")
        bkgleg.AddEntry(bkg_hist, "Sum bkg", "l")

        for proc_name in proc_names:
            h = signal_hists[proc_name]
            h.SetLineColor(color_for_signal(proc_name))
            h.SetLineWidth(2)
            h.SetFillStyle(0)
            h.SetStats(0)
            h.SetTitle("")
            h.Draw("HIST SAME")
            label = pretty_label(proc_name)
            sigleg.AddEntry(h, label, "l")

        leftText = "FCCAnalyses: FCC-ee Simulation (Delphes)"
        rightText = f"#sqrt{{s}} = {energy} GeV, L = {intLumi} ab^{{-1}}"

        latex = ROOT.TLatex()
        latex.SetNDC()
        latex.SetTextSize(0.03)
        latex.DrawLatex(0.18, 0.84, f"#bf{{#it{{{rightText}}}}}")
        latex.SetTextAlign(31)
        latex.DrawLatex(0.92, 0.92, f"#it{{{leftText}}}")

        sigleg.Draw()
        bkgleg.Draw()
        if scale == "log":
            c.SetLogy()

        c.GetFrame().SetBorderSize(12)
        c.RedrawAxis()
        c.Modified()
        c.Update()

        out_base = f"{VARIABLE}_{CUT}_{channel_label}_allsignals_{scale}"
        c.SaveAs(os.path.join(plot_dir, f"{out_base}.png"))
        c.SaveAs(os.path.join(plot_dir, f"{out_base}.pdf"))
        print(f"    Saved {scale} PDF and PNG for combined {channel_label} plot")

def main():
    if not signal_files:
        raise RuntimeError(f"No signal files found matching {MERGED_DIR}/mgp8_ee_*HAlpAlp*_{CUT}_histo.root")
    if not os.path.isfile(bkg_sum_file):
        raise RuntimeError(f"Background sum file not found: {bkg_sum_file}")

    print(f"Variable: {VARIABLE}   Cut: {CUT}")
    print(f"Found {len(signal_files)} signal file(s)")
    print(f"Using background sum file: {bkg_sum_file}")
    print(f"Signal points selected for plotting ({len(SIGNAL_POINTS)}): {SIGNAL_POINTS}")

    os.makedirs(OUTPUT_DIR, exist_ok=True)

    bkg_sum_hist, chosen_fit = build_bkg_sum()

    print(f"\nSignal histograms ({sig_nbins} bins, {sig_xmin}-{sig_xmax} GeV)")

    signal_hists = {} # proc -> h_sig
    signal_hists_by_channel = {"ee": {}, "mumu": {}}

    for signal_file in sorted(signal_files):
        proc, h_sig = build_signal_hist(signal_file)
        if h_sig is None:
            continue
        signal_hists[proc] = h_sig
        signal_hists_by_channel[channel_of(proc)][proc] = h_sig

    if not signal_hists:
        raise RuntimeError("No signal histograms were built successfully - nothing to write")

    # write single combined output file (all sig)
    out_f = ROOT.TFile.Open(output_file, "RECREATE")
    out_f.cd()
    bkg_sum_hist.Write("bkg_sum", ROOT.TObject.kOverwrite)
    for proc, h_sig in signal_hists.items():
        h_sig.Write(proc, ROOT.TObject.kOverwrite)
    out_f.ls()
    out_f.Close()
    print(f"\nWritten combined file: {output_file}")
    print(f"  Contains: bkg_sum + {len(signal_hists)} signal process(es):")
    for proc in signal_hists:
        print(f"    {proc}")

    plotted_signal_hists = {p: h for p, h in signal_hists.items() if is_selected_signal(p)}

    if not plotted_signal_hists:
        print("\nWARNING: none of the found signal processes match the "
              "SIGNAL_MASSES/SIGNAL_CTAUS selection - no plots will be made.")

    skipped = sorted(set(signal_hists) - set(plotted_signal_hists))
    if skipped:
        print(f"\nSkipping plots for {len(skipped)} signal process(es) not in the selection:")
        for proc in skipped:
            print(f"    {proc}")

    # per-signal overlay plots
    for proc, h_sig in plotted_signal_hists.items():
        make_plots(proc, h_sig, bkg_sum_hist, PLOT_DIR)

    # combined sig + bkg per channel
    plotted_by_channel = {"ee": {}, "mumu": {}}
    for proc, h_sig in plotted_signal_hists.items():
        plotted_by_channel[channel_of(proc)][proc] = h_sig

    for ch_label, hists in plotted_by_channel.items():
        if hists:
            print(f"\nBuilding combined plot for channel: {ch_label} ({len(hists)} signal points)")
            make_combined_plot(ch_label, hists, bkg_sum_hist, PLOT_DIR)
        else:
            print(f"\nNo selected signal histograms found for channel: {ch_label} - skipping combined plot")

    print(f"\nDone. Background fit function used: {chosen_fit}")
    print(f"Combined output file: {output_file}")

if __name__ == "__main__":
    main()