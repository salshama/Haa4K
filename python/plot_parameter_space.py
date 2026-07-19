#!/usr/bin/env pyyhon3
"""
ctau: proper decay length from ALP total width
fdec: probability that both back-to-back ALPs from h>aa decay before traveling a distance ldet
xsec: theoretical cross-section from MG sample cards
n_events: xsec * int_lumi * fdec
"""
import re
import warnings
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from scipy.interpolate import griddata

malp	= [0.05, 0.1, 0.5, 1.0, 1.5, 5.0, 10, 20, 30]
cah_exp = [1, 2, 3, 4, 5, 6]
cah_val = [10.0**(-exp) for exp in cah_exp]

sqrt_s			= 240.0
mh				= 125.0
mz				= 91.2
ldet			= 2.0 # effective detector length used for decays inside/outside detector
int_lumi		= 10.8e6 # pb^-1
n_events_thresh	= 3
hbarc			= 1.973269804e-16 # gev * m
channels		= ["ee", "mumu"]
base_dir 		= Path("/ceph/salshamaily/haa4K_FCCee/madgraph_3.7.1")
out_plot_path	= "/ceph/salshamaily/haa4K_FCCee/analysis/plots_output/param_space/"

def format_mass_tag(malp):
	s = f"{malp:g}"
	if "." not in s:
		s += ".0"
	return "m" + s.replace(".", "p")
	
def format_cah_tag(cah_exp):
	return f"cah1em{cah_exp}"
	
def run_dir(channel, malp, cah_exp):
	mass_tag	= format_mass_tag(malp)
	cah_tag		= format_cah_tag(cah_exp)
	dirname		= f"mgp8_ee_{channel}H_HAlpAlp_{mass_tag}_{cah_tag}_ecm240"
	return base_dir / dirname
	
def events_dir(channel, malp, cah_exp):
	return run_dir(channel, malp, cah_exp)/ "Events" / "run_01"
	
def cards_dir(channel, malp, cah_exp):
	return run_dir(channel, malp, cah_exp) / "Cards"
	
def read_xsec(banner_path):
	banner_path	= Path(banner_path)
	if not banner_path.exists():
		return np.nan
		
	text	= banner_path.read_text()
	m		= re.search(r"Integrated weight \(pb\)\s*:\s*([0-9.eE+\-]+)", text)
	if not m:
		warnings.warn(f"Could not find integrated weight in {banner_path}")
		return np.nan
	return float(m.group(1))
	
def read_walp(param_card_path, alp_pdg=9000005):
	param_card_path	= Path(param_card_path)
	if not param_card_path.exists():
		return np.nan
	text	= param_card_path.read_text()
	pattern	= rf"DECAY\s+{alp_pdg}\s+([0-9.eE+\-]+)"
	m		= re.search(pattern, text)
	if not m:
		warnings.warn(f"Could not find ALP width in {param_card_path}")
		return np.nan
	return float(m.group(1))
	
def higgs_lab_kin(sqrt_s, mh, mz):
	Eh			= (sqrt_s ** 2 + mh ** 2 - mz ** 2) / (2.0 * sqrt_s)
	ph			= np.sqrt(max(Eh ** 2 - mh ** 2, 0.0))
	betah		= ph/ Eh
	gammah		= Eh/mh
	return Eh, ph, betah, gammah
	
def alp_rest_kin(mh, ma):
	Estar	= mh / 2.0
	pstar2	= Estar**2 - ma**2
	if pstar2 <= 0:
		return Estar, 0.0
	return Estar, np.sqrt(pstar2)
	
def alp_lab_kin(betah, gammah, Estar, pstar, costheta):
	pz = gammah * (pstar * costheta + betah * Estar)
	pt = pstar * np.sqrt(np.clip(1.0 - costheta ** 2, 0.0, None))
	return np.sqrt(pz**2 + pt**2)
	
def threshold_cah(xsec_pb_col, cah_vals, fdec_val, n_thresh, int_lumi):
	valid = np.isfinite(xsec_pb_col) & (xsec_pb_col > 0)
	if not np.any(valid) or not np.isfinite(fdec_val) or fdec_val <= 0:
		return np.nan
	cah_ref  = np.asarray(cah_vals)[valid][0]
	xsec_ref = xsec_pb_col[valid][0]
	denom = int_lumi * xsec_ref * fdec_val
	if denom <= 0:
		return np.nan
	return cah_ref * np.sqrt(n_thresh / denom)
	
def f_dec(ma, ctau_m, sqrt_s, mh, mz, ldet, n_costheta=4000):
	if not np.isfinite(ctau_m) or ctau_m <= 0:
		return np.nan
	_, _, betah, gammah = higgs_lab_kin(sqrt_s, mh, mz)
	Estar, pstar		= alp_rest_kin(mh, ma)
	if pstar == 0.0:
		return np.nan
	costheta 	= np.linspace(-1.0, 1.0, n_costheta)
	p1			= alp_lab_kin(betah,gammah, Estar, pstar, costheta)
	p2			= alp_lab_kin(betah, gammah, Estar, pstar, -costheta)
	L1			= (p1/ma) * ctau_m
	L2			= (p2/ma) * ctau_m
	P1			= 1.0 - np.exp(-ldet/L1)
	P2			= 1.0 - np.exp(-ldet/L2)
	
	integrand	= P1*P2
	trapz_fn	= getattr(np, "trapezoid", None) or np.trapz
	return 0.5 * trapz_fn(integrand, costheta)
	
def build_grid():
	n_malp		= len(malp)
	n_cah		= len(cah_val)
	xsec_pb		= np.zeros((n_cah, n_malp))
	xsec_found	= np.zeros((n_cah, n_malp), dtype=bool)
	walp		= np.full((n_cah, n_malp), np.nan)
	
	for i_c, cah_exp_val in enumerate(cah_exp):
		for i_m, malp_val in enumerate(malp):
			for channel in channels:
				edir		= events_dir(channel, malp_val, cah_exp_val)
				cdir		= cards_dir(channel, malp_val, cah_exp_val)
				banner		= edir / "run_01_tag_1_banner.txt"
				param_card	= cdir / "param_card.dat"
				if not banner.exists():
					print(f"MISSING BANNER: {banner}")
				xsec		= read_xsec(banner)
				if np.isfinite(xsec):
					xsec_pb[i_c, i_m]		+= xsec
					xsec_found[i_c, i_m]	= True
				if not np.isfinite(walp[i_c, i_m]):
					walp[i_c, i_m]			= read_walp(param_card)
	xsec_pb[~xsec_found]	= np.nan
	ctau_m					= np.full(n_malp, np.nan)
	for i_m in range(n_malp):
		col			= walp[:, i_m]
		valid		= col[np.isfinite(col) & (col>0)]
		if len(valid)==0:
			continue
		gamma_tot	= valid[0]
		ctau_m[i_m]	= hbarc / gamma_tot
	fdec_m			= np.array([f_dec(ma, ctau_m[i_m], sqrt_s, mh, mz, ldet) for i_m, ma in enumerate(malp)])
	n_events		= int_lumi * xsec_pb * fdec_m[np.newaxis, :]
	return n_events, ctau_m, fdec_m, xsec_pb

def make_plot(n_events, xsec_pb, fdec_m, out_dir="/ceph/salshamaily/haa4K_FCCee/analysis/plots_output/param_space/", out_name="alp_parameter_space"):
	out_dir			= Path(out_dir)
	out_dir.mkdir(parents=True,exist_ok=True)	
	mass_flat		= np.tile(malp, len(cah_val))
	log_cah_flat	= np.repeat(np.log10(cah_val), len(malp))
	cah_thresh		= np.array([
	threshold_cah(xsec_pb[:, i_m], cah_val, fdec_m[i_m], n_events_thresh, int_lumi)
	
	for i_m in range(len(malp))])
	valid_thresh	= np.isfinite(cah_thresh) & (cah_thresh > 0)
		
	fig, ax			= plt.subplots(figsize=(8,8))
	
	ax.fill_between(
	np.array(malp)[valid_thresh],
	np.log10(cah_thresh[valid_thresh]),
	np.log10(min(cah_val)) if False else max(np.log10(cah_val)),
	color="#4e7b37", alpha=0.25,)
	
	ax.plot(
	np.array(malp)[valid_thresh],
	np.log10(cah_thresh[valid_thresh]),
	color="#89c262", linewidth=3, linestyle="-",)
	
	ax.scatter(mass_flat, log_cah_flat, marker='x', c='k', s=25, zorder=5)
	
	ax.set_xlabel(r"$m_a$ [GeV]", fontsize=13)
	ax.set_ylabel(r"$\log_{10} C_{ah}$", fontsize=13)
	title=(
	r"$e^+e^-\to ZH,\ H\to aa\to K^{+}K^{-}K^{+}K^{-},\ Z\to\ell\ell$"
	f"\n$\\sqrt{{s}}={sqrt_s:.0f}$ GeV, "
	rf"$\mathcal{{L}}={int_lumi/1e6:.1f}\times 10^{{6}}\,\mathrm{{pb}}^{{-1}}$")
	ax.set_title(title, fontsize=16)
	ax.tick_params(direction='out', labelsize=13)
	legend_line=Line2D([0],[0],color="#89c262", lw=3)
	ax.legend(
	[legend_line],
	[rf"$N_{{\rm events}} = {n_events_thresh}$"],
	loc='lower right', fontsize=13,)
	
	fig.tight_layout()
	fig.savefig(out_dir/f"{out_name}.png", dpi=300)
	fig.savefig(out_dir/f"{out_name}.pdf")
	print(f"Saved plot to {out_dir / out_name}.[pdf|png]")
	
if __name__ == "__main__":
	n_events, ctau_m, fdec_m, xsec_pb = build_grid()
	print("\nm_a [GeV]  :  c*tau_a [m]  :  f_dec")
	for ma, ct, fd in zip(malp, ctau_m, fdec_m):
		ct_str = f"{ct:.3e}" if np.isfinite(ct) else "nan"
		fd_str = f"{fd:.3e}" if np.isfinite(fd) else "nan"
		print(f"{ma:>9.2f}  :  {ct_str:>11}  :  {fd_str}")
	make_plot(n_events, xsec_pb, fdec_m)