#!/usr/bin/env python3

import re
import warnings
from pathlib import Path

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm

malp = [0.05, 0.1, 0.5, 1.0, 1.5, 5.0, 10, 20, 30, 40, 50, 60]

# ctau values as sampled on disk, with their numeric value in mm
CTAU_LABELS = ["1mm", "10mm", "1m", "2m"]
CTAU_MM = {"1mm": 1.0, "10mm": 10.0, "1m": 1000.0, "2m": 2000.0}

sqrt_s   = 240.0
mh       = 125.0
mz       = 91.2
ldet     = 2.0          # effective detector radius [m]
int_lumi = 10.8e6       # pb^-1
n_events_thresh = 1
channels = ["ee", "mumu"]

base_dir      = Path("/ceph/salshamaily/haa4K_FCCee/madgraph_3.7.1")
out_plot_path = Path("/ceph/salshamaily/haa4K_FCCee/analysis/plots_output/param_space/")

# hbar*c in GeV*mm
HBAR_C_GEV_MM = 1.973269804e-13

def alp_width_from_ctau(ctau_mm: float) -> float:
	"""Gamma = 1 / ctau -> converted from mm to natural units"""
	ctau_natural = ctau_mm / HBAR_C_GEV_MM   # GeV^-1
	return 1.0 / ctau_natural                # GeV

def format_mass_tag(malp_val):
	s = f"{malp_val:g}"
	if "." not in s:
		s += ".0"
	return "m" + s.replace(".", "p")

def run_dir(channel, malp_val, ctau_label):
	mass_tag = format_mass_tag(malp_val)
	dirname = f"mgp8_ee_{channel}H_HAlpAlp_{mass_tag}_ecm240"
	return base_dir / dirname

def events_dir(channel, malp_val, ctau_label):
	return run_dir(channel, malp_val, ctau_label) / "Events" / "run_01"

def read_xsec(banner_path):
	banner_path = Path(banner_path)
	if not banner_path.exists():
		return np.nan

	text = banner_path.read_text()
	m = re.search(r"Integrated weight \(pb\)\s*:\s*([0-9.eE+\-]+)", text)
	if not m:
		warnings.warn(f"Could not find integrated weight in {banner_path}")
		return np.nan
	return float(m.group(1))

def higgs_lab_kin(sqrt_s, mh, mz):
	Eh     = (sqrt_s ** 2 + mh ** 2 - mz ** 2) / (2.0 * sqrt_s)
	ph     = np.sqrt(max(Eh ** 2 - mh ** 2, 0.0))
	betah  = ph / Eh
	gammah = Eh / mh
	return Eh, ph, betah, gammah

def alp_rest_kin(mh, ma):
	Estar  = mh / 2.0
	pstar2 = Estar ** 2 - ma ** 2
	if pstar2 <= 0:
		return Estar, 0.0
	return Estar, np.sqrt(pstar2)

def alp_lab_components(betah, gammah, Estar, pstar, costheta):
	"""
	Boost alp from the Higgs rest frame
	"""
	pz = gammah * (pstar * costheta + betah * Estar)
	pt = pstar * np.sqrt(np.clip(1.0 - costheta ** 2, 0.0, None))
	return pz, pt

def f_dec(ma, ctau_m, sqrt_s, mh, mz, ldet, n_costheta=4000):
	"""
	Probability that both alps from h -> aa decay inside the detector
	"""
	if not np.isfinite(ctau_m) or ctau_m <= 0:
		return np.nan
	_, _, betah, gammah = higgs_lab_kin(sqrt_s, mh, mz)
	Estar, pstar = alp_rest_kin(mh, ma)
	if pstar == 0.0:
		return np.nan

	costheta = np.linspace(-1.0, 1.0, n_costheta)

	# alps are back-to-back in the Higgs rest frame
	pz1, pt1 = alp_lab_components(betah, gammah, Estar, pstar, costheta)
	pz2, pt2 = alp_lab_components(betah, gammah, Estar, pstar, -costheta)

	p1 = np.sqrt(pz1 ** 2 + pt1 ** 2)
	p2 = np.sqrt(pz2 ** 2 + pt2 ** 2)

	# lab-frame polar angle w.r.t. the beam axis for each ALP
	theta_lab1 = np.arctan2(pt1, pz1)
	theta_lab2 = np.arctan2(pt2, pz2)

	# L_perp = (p/ma) * ctau * sin(theta_lab)
	L1_perp = (p1 / ma) * ctau_m * np.sin(theta_lab1)
	L2_perp = (p2 / ma) * ctau_m * np.sin(theta_lab2)

	with np.errstate(divide="ignore", invalid="ignore"):
		P1 = np.where(L1_perp > 0, 1.0 - np.exp(-ldet / np.where(L1_perp > 0, L1_perp, 1.0)), 0.0)
		P2 = np.where(L2_perp > 0, 1.0 - np.exp(-ldet / np.where(L2_perp > 0, L2_perp, 1.0)), 0.0)

	integrand = P1 * P2
	trapz_fn = getattr(np, "trapezoid", None) or np.trapz
	return 0.5 * trapz_fn(integrand, costheta)

def build_grid():
	n_malp = len(malp)
	n_ctau = len(CTAU_LABELS)

	xsec_pb    = np.zeros((n_ctau, n_malp))
	xsec_found = np.zeros((n_ctau, n_malp), dtype=bool)

	for i_c, ctau_label in enumerate(CTAU_LABELS):
		for i_m, malp_val in enumerate(malp):
			for channel in channels:
				edir   = events_dir(channel, malp_val, ctau_label)
				banner = edir / "run_01_tag_1_banner.txt"
				if not banner.exists():
					print(f"MISSING BANNER: {banner}")
				xsec = read_xsec(banner)
				if np.isfinite(xsec):
					xsec_pb[i_c, i_m]    += xsec
					xsec_found[i_c, i_m]  = True
	xsec_pb[~xsec_found] = np.nan

	ctau_mm_arr = np.array([CTAU_MM[c] for c in CTAU_LABELS])
	ctau_m_arr  = ctau_mm_arr / 1000.0
	width_arr   = np.array([alp_width_from_ctau(c) for c in ctau_mm_arr])  # GeV, one per ctau

	fdec = np.full((n_ctau, n_malp), np.nan)
	for i_c, ctau_m_val in enumerate(ctau_m_arr):
		for i_m, ma in enumerate(malp):
			fdec[i_c, i_m] = f_dec(ma, ctau_m_val, sqrt_s, mh, mz, ldet)

	n_events = int_lumi * xsec_pb * fdec
	return n_events, xsec_pb, fdec, ctau_mm_arr, width_arr

def _draw_heatmap(vals, x_ticklabels, y_ticklabels, x_axis_label, y_axis_label, out_dir, out_name, x_rotation=45):
	out_dir = Path(out_dir)
	out_dir.mkdir(parents=True, exist_ok=True)

	n_rows, n_cols = vals.shape

	fig, ax = plt.subplots(figsize=(10, 5.5))

	plot_vals = np.where(np.isfinite(vals) & (vals > 0), vals, np.nan)
	if np.all(np.isnan(plot_vals)):
		warnings.warn("No valid n_events values to plot.")
		plt.close(fig)
		return

	im = ax.imshow(
		plot_vals,
		aspect="auto",
		origin="lower",
		norm=LogNorm(vmin=np.nanmin(plot_vals), vmax=np.nanmax(plot_vals)),
		cmap="viridis",
		extent=[-0.5, n_cols - 0.5, -0.5, n_rows - 0.5],
	)

	vmax = np.nanmax(plot_vals)
	for i in range(n_rows):
		for j in range(n_cols):
			val = vals[i, j]
			if np.isfinite(val) and val > 0:
				txt_color = "white" if val < vmax ** 0.5 else "black"
				ax.text(j, i, f"{val:.1e}", ha="center", va="center",
				         fontsize=7, color=txt_color)

	ax.set_xticks(range(n_cols))
	ax.set_xticklabels(x_ticklabels, rotation=x_rotation, ha="right")
	ax.set_yticks(range(n_rows))
	ax.set_yticklabels(y_ticklabels)

	ax.set_xlabel(x_axis_label, fontsize=12)
	ax.set_ylabel(y_axis_label, fontsize=12)

	title = (
		r"$e^+e^-\to ZH,\ H\to aa\to K^{+}K^{-}K^{+}K^{-},\ Z\to\ell\ell$"
		f"\n$\\sqrt{{s}}={sqrt_s:.0f}$ GeV, "
		rf"$\mathcal{{L}}={int_lumi/1e6:.1f}\times 10^{{6}}\,\mathrm{{pb}}^{{-1}}$"
	)
	ax.set_title(title, fontsize=13)

	cbar = fig.colorbar(im, ax=ax, pad=0.02)
	cbar.set_label(r"$N_{\rm events}$", fontsize=12)

	fig.tight_layout()
	fig.savefig(out_dir / f"{out_name}.png", dpi=300)
	fig.savefig(out_dir / f"{out_name}.pdf")
	print(f"Saved plot to {out_dir / out_name}.[pdf|png]")
	plt.close(fig)

def make_plot_2d_ctau(n_events, ctau_mm_arr, malp, out_dir=out_plot_path, out_name="alp_parameter_space_2d_ctau"):
	x_ticklabels = [f"{m:g}" for m in malp]
	_draw_heatmap(n_events, x_ticklabels, CTAU_LABELS,
	              r"$m_a$ [GeV]", r"$c\tau_a$",
	              out_dir, out_name)

def make_plot_2d_gamma(n_events, width_arr, malp, out_dir=out_plot_path, out_name="alp_parameter_space_2d_gamma"):
	n_events_T = n_events.T  # rows: malp, columns: ctau/gamma
	y_ticklabels = [f"{m:g}" for m in malp]
	x_ticklabels = [f"{w:.2e}" for w in width_arr]
	_draw_heatmap(n_events_T, x_ticklabels, y_ticklabels,
	              r"$\Gamma_a$ [GeV]", r"$m_a$ [GeV]",
	              out_dir, out_name)

if __name__ == "__main__":
	n_events, xsec_pb, fdec, ctau_mm_arr, width_arr = build_grid()

	print("\nctau     :  Gamma [GeV]")
	for c_label, c_mm, w in zip(CTAU_LABELS, ctau_mm_arr, width_arr):
		print(f"{c_label:>8} :  {w:.3e}")

	print("\nm_a [GeV]  |  ctau  |  fdec  |  xsec [pb]  |  n_events")
	for i_c, c_label in enumerate(CTAU_LABELS):
		for i_m, ma in enumerate(malp):
			fd  = fdec[i_c, i_m]
			xs  = xsec_pb[i_c, i_m]
			nev = n_events[i_c, i_m]
			fd_str  = f"{fd:.3e}"  if np.isfinite(fd)  else "nan"
			xs_str  = f"{xs:.3e}"  if np.isfinite(xs)  else "nan"
			nev_str = f"{nev:.3e}" if np.isfinite(nev) else "nan"
			print(f"{ma:>9.2f}  |  {c_label:>5}  |  {fd_str:>10}  |  {xs_str:>10}  |  {nev_str}")

	make_plot_2d_ctau(n_events, ctau_mm_arr, malp)
	make_plot_2d_gamma(n_events, width_arr, malp)