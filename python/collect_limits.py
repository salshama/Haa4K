"""
Collects asymptotic limits from combine output across multiple mass hypotheses
and produces a Brazilian band limit plot with theoretical cross sections
"""

import os
import glob
import numpy as np
import matplotlib.pyplot as plt
import uproot
import mplhep as hep

mass_dirs		= "/ceph/salshamaily/haa4K_FCCee/datacards/mass*"
combine_file	= "higgsCombineTest.AsymptoticLimits.mH120.root"
output_pdf		= "r_limits.pdf"
output_png		= "r_limits.png"

# add mass points here and script picks them up automatically
xsec_map	= {
			1.5:	0.0009558,
			10:		0.0009775,
			30:		0.001129,
			60:		0.01174,
}

# quantile tolerance for float point matching
atol		= 0.01

# adding quantiles here
quantile_map	= {
			"exp":			0.5,
			"1sig_minus":	0.16,
			"1sig_plus":	0.84,
			"2sig_minus":	0.025,
			"2sig_plus":	0.975,
}

def extract_mass(directory: str) -> float:
	"""
	- Parses ALP masses from a directory name like .../mass1.5/...
	- Returns:
	float of ALP mass point
	- Args:
	directory: directory in the form of mass1.5, mass10, etc
	"""
	return float(os.path.basename(directory).replace("mass", ""))
	
def get_limit(limits: np.ndarray, quantiles: np.ndarray, target: float) -> float:
	"""
	- Extracts the limits from the given arrays
	- Returns:
	limit value for a given target quantile
	- Args:
	limits ndarray, array of limits
	quantiles: ndarray, array of quantiles
	target: float, the target quantile
	"""
	mask	= np.isclose(quantiles, target, atol=atol)
	matches	= limits[mask]
	
	if len(matches)==0:
		raise ValueError(f"No quantile  found near {target}" f"\n Available quantiles: {quantiles}")
	
	return float(matches[0])
	
def collect_limits(directories: list) -> dict:
	"""
	- Loops over directories and extracts all 5 quantile limits scaled by theoretical cross-section
	- Returns:
	dictionary with lists of mass and quantiles sorted by mass
	- Args:
	directories: list of all directories to look at
	"""
	results	= {key: [] for key in ["ma"] + list(quantile_map.keys())}
	
	for d in sorted(directories, key=extract_mass):
		ma	= extract_mass(d)
		
		if ma not in xsec_map:
			print(f"[SKIP] m_a = {ma} GeV - no xsec defined in xsec_map")
			continue
			
		root_path	= os.path.join(d, combine_file)
		
		if not os.path.isfile(root_path):
			print(f"[SKIP] m_a = {ma} GeV - ROOT file not found")
			continue
		
		try:
			f			= uproot.open(root_path)
			tree		= f["limit"]
			arrays		= tree.arrays(["limit", "quantileExpected"], library="np")
			limits		= arrays["limit"]
			quantiles	= arrays["quantileExpected"]
		except Exception as e:
			print(f"[ERROR] m_a = {ma} GeV - could not read ROOT file: {e}")
			continue
			
		xsec	= xsec_map[ma]
		print(f"ma = {ma} GeV | xsec = {xsec:.6f} pb | quantiles = {np.round(quantiles,4)}")
		
		try:
			row	= {key: get_limit(limits, quantiles, q) * xsec
				for key, q in quantile_map.items()}
		except ValueError as e:
			print(f" [ERROR] ma={ma} GeV - {e}")
			continue
		
		results["ma"].append(ma)
		
		for key in quantile_map:
			results[key].append(row[key])
	
	order	= np.argsort(results["ma"])
	return {k: np.array(v)[order] for k,v in results.items()}
	
def make_plot(r: dict) -> None:
	"""
	Produces Brazilian limit plot
	- Returns:
	saves plot as PDF file
	- Args:
	r, dictionary of results renamed to "r" locally within this function
	"""
	ma				= r["ma"]
	exp				= r["exp"]
	onesig_minus	= r["1sig_minus"]
	onesig_plus		= r["1sig_plus"]
	twosig_minus	= r["2sig_minus"]
	twosig_plus		= r["2sig_plus"]
	
	xsec_theo_x		= np.array(sorted(xsec_map.keys()))
	xsec_theo_y		= np.array([xsec_map[m] for m in xsec_theo_x])
	
	plt.style.use(hep.style.CMS)
	plt.rcParams.update({"font.size": 20})
	
	fig, ax	= plt.subplots()
	
	# 2σ and 1σ bands (drawn first so lines sit on top)
	fill_2s		= ax.fill_between(ma, twosig_minus, twosig_plus, color="gold", alpha=1, label="95% expected")
	fill_1s		= ax.fill_between(ma, onesig_minus, onesig_plus, color="limegreen", alpha=1, label="65% expected")
	
	# expected limit line
	line_exp,	= ax.plot(ma, exp, color="black", linestyle="--", marker="o", markersize=7, linewidth=2, label="Expected limit")
	
	# theoretical cross section
	line_theo,	= ax.plot(xsec_theo_x, xsec_theo_y, color="red", linewidth=2, linestyle="-", label=r"$\sigma_{\mathrm{theo}}$")
	
	# axes
	ax.set_xlabel(r"$m_a$ [GeV]")
	ax.set_ylabel(r"$\sigma \times \mathrm{BR}(H\rightarrow aa\rightarrow K^+K^-K^+K^-)$ [pb]")
	ax.set_xlim(ma.min(), ma.max())
	ax.set_ylim(top=max(twosig_plus)*1.25, bottom=0.000)
	
	# title
	ax.set_title(r"$\mathbf{FCC\!-\!ee\ Simulation\ (Delphes)}$", loc="left", fontsize=20)
	ax.set_title(f"10.8 ab$^{{-1}}$ (240 $\mathrm{{{{GeV}}}}$)", loc="right", fontsize=19)
	
	# legend in explicit order
	ax.legend(handles=[line_exp, line_theo, fill_1s, fill_2s], labels=["Expected Limit", "Theoretical Limit", "68% expected", "95% expected"], loc="upper right")
	
	fig.tight_layout()
	plt.savefig(os.path.join("/ceph/salshamaily/haa4K_FCCee/analysis/plots_output/statistics/",output_pdf))
	plt.savefig(os.path.join("/ceph/salshamaily/haa4K_FCCee/analysis/plots_output/statistics/",output_png))
	print(f"\n Successful: plot saved to {output_pdf} and {output_png}")
	
def main():
	directories	= glob.glob(mass_dirs)
	
	if not directories:
		raise RuntimeError(f"ERROR: no directories found matching!")
	
	print(f"Found {len(directories)} \n")
	
	results		= collect_limits(directories)
	
	if len(results["ma"])==0:
		raise RuntimeError(f"ERROR: no valid limits collected - check path and files")
		
	print(f"\n Collected limits for ma = {results['ma']} GeV")
	
	make_plot(results)
	
if __name__ == "__main__":
	main()