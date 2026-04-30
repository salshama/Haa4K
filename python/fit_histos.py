"""
Prepares signal and background processes for CMS combine:
    - Signal histograms: 120-130 GeV, 100 bins (0.1 GeV bin widths)
        - Signal Region (SR): narrow window around Higgs recoil mass peak
        - Fine binning: needed to resolve the signal shape
    - Background histograms: 0-180 GeV, 180 bins (1 GeV bin widths)
        - Coarse binning: needed for full mass range in backgrounds and then used
        to get a smooth shape estimation in the SR
    - Sums up all background processes in one histograms
    - Extracts smooth function in 120-130 GeV range to match signal binning
    - Merges signal + rebinned backgrounds in one output file for combine
"""

import numpy as np
import glob
import ROOT
import os

ROOT.gROOT.SetBatch(True) # suppress GUI

signal_files    = glob.glob("/ceph/salshamaily/haa4K_FCCee/analysis/final_output/only_signal_mgp8sig_norwt_042026/*.root")
bkg_files        = glob.glob("/ceph/salshamaily/haa4K_FCCee/analysis/final_output/only_bkg_mgp8sig_norwt_042026/*.root")

output_dir        = "/ceph/salshamaily/haa4K_FCCee/samples"
output_file        = os.path.join(output_dir, "RecoHiggs_mass_RecoKaonElecSel_rebinned.root")

plot_dir        = "/ceph/salshamaily/haa4K_FCCee/analysis/plots_output/replot_all_samples_mgp8sig_norwt_042026"
diag_dir		= "/ceph/salshamaily/haa4K_FCCee/analysis/plots_output/statistics"

sig_xmin	= 120.0
sig_xmax	= 130.0
sig_nbins	= 100

bkg_xmin	= 0.0
bkg_xmax	= 160.0
bkg_nbins	= 32

channel		= "RecoHiggs_mass"

fit_func	= "pol5" # could be expo or pol^n depending on bkg shape
fit_xmin	= 50.0
fit_xmax	= 160.0

mass_map	= {"m1": 1.5, "m10": 10, "m30": 30, "m60": 60}

def process_name(filepath):
    """
    - Extracts process name from the given ROOT filename; assumes filename pattern:
    <process_name>_<RecoXxx>_histo.root
    - Returns:
    process name
    - Args:
    filepath: path of the file
    """
    basename     = os.path.basename(filepath)
    basename    = basename.replace("_histo.root", "")
    parts        = basename.split("_Reco")
    return parts[0]
    
def get_histogram(filepath, hist_name):
    """
    - Opens ROOT file and gets specific histogram
    - Returns:
    TH1 (detached from file) or none if not found
    - Args:
    filepath: str, path of the file
    hist_name: str, name of the histogram to get
    """
    f    = ROOT.TFile.Open(filepath)
    
    if not f or f.IsZombie():
        raise RuntimeError(f"Cannot open file: {filepath}")
        
    h    = f.FindObjectAny(hist_name)
    
    if not h:
        print(f"WARNING: {hist_name} not found in {filepath}")
        print(f"Available keys:")
        for key in f.GetListOfKeys():
            print(f"    {key.GetName()}")
        f.Close()
        return None
    
    if not isinstance(h, ROOT.TH1):
    	print(f"WARNING: '{hist_name}' in '{filepath}' is not a TH1 histogram")
    	f.Close()
    	return h
    	
    h_clone	= h.Clone(hist_name)
    h_clone.SetDirectory(0)
    f.Close()
    return h_clone
    
def do_fit(h_coarse, nbins_fine, xmin, xmax, name, fit_func=fit_func, fit_xmin=fit_xmin, fit_xmax=fit_xmax):
	"""
	- Fits a smooth TF1 to the summed coarse background histogram then samples the fit function into
	a fine-binned histogram covering [xmin, xmax]
	- Returns:
	TH1F with fine binning in [xmin, xmax]
	- Args:
	h_coarse: TH1, summed background in full range with coarse binning
	nbins_fine: int, number of output bins
	xmin, xmax: float, output range in SR
	name: str, name of output histogram
	fit_func: str, TF1 formula (expo, pol3, pol5, etc)
	fit_xmin, fit_xmax: float, lower/upper range of fit range
	"""
	print(f"\n Fitting '{fit_func} over [{fit_xmin},{fit_xmax}] GeV...")
	
	# using events/GeV before fitting so that function is bin-width independent
	h_density	= h_coarse.Clone("h_density_temp")
	h_density.SetDirectory(0)
	
	for i in range(1, h_density.GetNbinsX()+1):
		w	= h_density.GetBinWidth(i)
		c	= h_density.GetBinContent(i)
		e	= h_density.GetBinError(i)
		h_density.SetBinContent(i, c/w if w > 0 else 0.0)
		h_density.SetBinError(i, e/w if w > 0 else 0.0)
	
	# Q: quiet, no printout. R: full fit range in TF1. S: return fit result. O: do not draw
	f1			= ROOT.TF1("bkg_fit", fit_func, fit_xmin, fit_xmax)
	fit_result	= h_density.Fit(f1, "QRSO")
	fit_status	= int(fit_result.Status())
	
	if fit_status != 0:
		print(f" WARNING: fit status - {fit_status} (non-zero may indicate poor convergence)")
	else:
		print(f" Fit converged (status = 0)")
	
	# sampling fitted function onto fine histogram in SR where each bin gets
	h_fine	= ROOT.TH1F(name, name, nbins_fine, xmin, xmax)
	h_fine.SetDirectory(0)
	
	bin_width_fine	= h_fine.GetBinWidth(1)
	
	for i in range(1, nbins_fine+1):
		x	= h_fine.GetBinCenter(i)
		val	= f1.Eval(x) * bin_width_fine # f1(bin_center) * bin_width to get events/bin
		val	= max(val, 0.0)
		h_fine.SetBinContent(i, val)
		h_fine.SetBinError(i, ROOT.TMath.Sqrt(val) if val > 0 else 0.0)
		
	# rescale so integral in SR matches actual summed bkg
	integral_coarse	= h_coarse.Integral(h_coarse.FindBin(xmin),h_coarse.FindBin(xmax-1e-6))
	integral_fine	= h_fine.Integral()
	
	if integral_fine > 0 and integral_coarse > 0:
		h_fine.Scale(integral_coarse/integral_fine)
		print(f"Rescaling...")
		print(f"Coarse integral in SR = {integral_coarse:.2f} \n Fine integral in SR = {integral_fine:.2f}")
	elif integral_coarse == 0:
		print(f"WARNING: zero background yield in SR")
	
	# print fit quality and metrics
	print_fit(fit_result, f1, h_density, fit_xmin, fit_xmax)
	
	return h_fine
	
def print_fit(fit_result, f1, h_density, fit_xmin, fit_xmax):
	"""
	- Prints fit quality metrics and parameters and plots fit on the full-range of
	summed background histogram
	- Returns:
	Diagnostics plot of the fit and prints fit metrics
	- Args:
	fit_result:
	f1:
	h_density:
	fit_xmin, fit_xmax: float, lower/upper range of fit range
	"""
	# printing fit results and parameters
	print(f"Fit results...")
	
	status	= int(fit_result.Status())
	print(f"Fit status: {status} ({'Ok - converged' if status==0 else 'WARNING: - check convergence'})")
	
	chi2	= fit_result.Chi2()
	ndf		= fit_result.Ndf()
	prob	= fit_result.Prob()
	
	if ndf > 0:
		print(f"Chi2:		{chi2:.4f}")
		print(f"ndf:		{ndf}")
		print(f"chi2 / ndf:	{chi2/ndf:.4f} (ideal ~ 1.0)")
		print(f"p-value:	{prob:.4f} ({'good >0.05' if prob>0.05 else 'poor - consider changing fit_func'})")
	else:
		print(f"chi2/ndf: NA (ndf=0, too few bins for this function)")
	
	print(f"\n Parameters:")
	for i in range(f1.GetNpar()):
		pname	= f1.GetParName(i)
		val		= f1.GetParameter(i)
		err		= f1.GetParError(i)
		print(f"[{i}] {pname:<12} = {val:+.6e} ± {err:.6e}")
		
	# creating diagnostic plot
	cdag	= ROOT.TCanvas("cdag","cdag", 900, 600)
	cdag.SetLogy()
	h_density.SetStats(0)
	h_density.SetTitle("Background fit diagnotics")
	h_density.SetLineWidth(2)
	h_density.GetXaxis().SetTitle("RecoMass_{Higgs} [GeV]")
	h_density.GetYaxis().SetTitle("Events / GeV")
	h_density.Draw("E") # error bars
	
	f1.SetLineColor(ROOT.kRed)
	f1.SetLineWidth(2)
	f1.Draw("SAME")
	
# 	ylo		= h_density.GetMinimum(1e-12)
# 	yhi		= h_density.GetMaximum() * 3.0
# 	line_lo	= ROOT.TLine(120, ylo, 120, yhi)
# 	line_hi	= ROOT.TLine(130, ylo, 130, yhi)
# 	for line in [line_lo, line_hi]:
# 		line.SetLineColor(ROOT.kBlue)
# 		line.SetLineStyle(2)
# 		line.SetLineWidth(2)
# 		line.Draw()
		
	legdag	= ROOT.TLegend(0.55, 0.75, 0.92, 0.92)
	legdag.AddEntry(h_density, "Summed bkg", "lep")
	legdag.AddEntry(f1, f"Fit: {fit_func}")
	legdag.AddEntry(f1, f"#chi^{{2}}/ndf = {chi2/ndf:.2f}","1")
	legdag.SetTextSize(0.025)
	legdag.SetFillColor(ROOT.kWhite)
	legdag.Draw()
	
	os.makedirs(diag_dir, exist_ok=True)
	cdag.SaveAs(os.path.join(diag_dir, f"bkg_fit_{fit_func}.pdf"))
		    
def make_plots(signal_hists, bkg_hist, plot_dir):
    """
    - Creates lin and log plots of signal and background histograms
    - Returns:
    PDF and PNG formats of the rebinned histograms in one plot
    - Args:
    signal_hists: dict {proc_name -> TH1}
    bkg_hist: TH1, background sum histogram
    plot_dir: str, directory to save plots
    """
    os.makedirs(plot_dir, exist_ok=True)
    
    # assign colors to each signal histogram
    colors        = [ROOT.TColor.GetColor('#c51b7d'), ROOT.TColor.GetColor('#2b8cbe'), ROOT.TColor.GetColor('#fdae6b'), ROOT.TColor.GetColor('#762a83')]
    proc_names    = sorted(signal_hists.keys())
    
    for scale in ["lin","log"]:
    	c	= ROOT.TCanvas(f"c_{scale}",f"c_{scale}",800, 600)
    	c.SetTicks(1, 1)
    	c.SetLeftMargin(0.14)
    	c.SetRightMargin(0.08)
    	if scale == 'log':
    		c.SetLogy()
    		bkg_hist.SetMinimum(1e-6 if scale=="log" else 0.0)
    	bkg_hist.SetLineColor(ROOT.kBlack)
    	bkg_hist.SetLineWidth(2)
    	bkg_hist.SetFillColor(ROOT.kGray)
    	bkg_hist.SetFillStyle(3004) # hatched
    	bkg_hist.SetStats(0)
    	bkg_hist.SetTitle("")
    	bkg_hist.GetXaxis().SetTitle("RecoMass_{Higgs} [GeV]")
    	bkg_hist.GetYaxis().SetTitle("Events / 0.1 GeV")
    	bkg_hist.GetXaxis().SetTitleOffset(1.2)
    	bkg_hist.SetMaximum(bkg_hist.GetMaximum() * 300)
    	bkg_hist.Draw("HIST")
    
    for i, proc_name in enumerate(proc_names):
        sig_hist    = signal_hists[proc_name]
        sig_hist.SetLineColor(colors[i%len(colors)])
        sig_hist.SetLineWidth(3)
        sig_hist.SetFillStyle(0) # no fill
        sig_hist.SetStats(0)
        sig_hist.SetTitle("")
        sig_hist.Draw("HIST SAME")
    
    leg	= c.BuildLegend(0.65, 0.70, 0.92, 0.90)
    leg.SetBorderSize(0)
    leg.SetFillStyle(0)
    
    c.SaveAs(os.path.join(plot_dir, f"RecoHiggs_mass_RecoKaonElecSel_rebinned_{scale}.png"))
    c.SaveAs(os.path.join(plot_dir, f"RecoHiggs_mass_RecoKaonElecSel_rebinned_{scale}.pdf"))
    print(f"    Saved {scale} PDF and PNG formats")
    
def main():
    if not signal_files:
        raise RuntimeError("No signal files found")
    if not bkg_files:
        raise RuntimeError("No background files found")
        
    print(f"Found {len(signal_files)} signal files(s)")
    print(f"Found {len(bkg_files)} background file(s)")
    
    os.makedirs(output_dir, exist_ok=True)
    out_file = ROOT.TFile.Open(output_file, "RECREATE")
    
    # storing plots
    signal_hists_plots    = {}
    
    ### SIGNAL HISTOGRAMS ###
    # for each signal mass point, extract histogram in [xmin,xmax] with fine binning
    # we scale bin contents if raw bin width is different from 0.1 to preserve yields
    print(f"Signal histograms ({sig_nbins} bins, {sig_xmin}-{sig_xmax} GeV)")
    
    for signal_file in sorted(signal_files):
        proc    = process_name(signal_file)
        print(f"\n Processing: {proc}")
        print(f"File: {os.path.basename(signal_file)}")
        
        h_raw	= get_histogram(signal_file, channel)
        
        if h_raw is None:
            print(f"SKIPPING {proc} - histogram not found!")
            continue
            
        print(f"Raw: {h_raw.GetNbinsX()} bins, "
              f"[{h_raw.GetXaxis().GetXmin():.1f}, {h_raw.GetXaxis().GetXmax():.1f}] GeV")
        print(f"  Integral (full range): {h_raw.Integral():.2f}")
        print(f"  Integral in SR: "
              f"{h_raw.Integral(h_raw.FindBin(sig_xmin), h_raw.FindBin(sig_xmax-1e-6)):.2f}")
              
        out_name = proc
        h_sig	 = ROOT.TH1F(out_name, out_name, sig_nbins, sig_xmin, sig_xmax)
        h_sig.SetDirectory(0)
        
        raw_bin_width    = h_raw.GetBinWidth(1)
        fine_bin_width    = h_sig.GetBinWidth(1)
        
        # copying content from raw hist to fine hist
        for i in range(1, sig_nbins+1):
            x		= h_sig.GetBinCenter(i)
            iraw	= h_raw.FindBin(x)
            c		= h_raw.GetBinContent(iraw)
            e		= h_raw.GetBinError(iraw)
            scale	= fine_bin_width/raw_bin_width if raw_bin_width > 0 else 1.0
            h_sig.SetBinContent(i, max(c*scale, 0.0))
            h_sig.SetBinError(i, e*scale)
            
        print(f"Output integral in SR: {h_sig.Integral():.2f}")
        out_file.cd()
        h_sig.Write(out_name, ROOT.TObject.kOverwrite) # no backup cycles
        
        signal_hists_plots[proc] = h_sig
    
    ### BACKGROUND HISTOGRAMS ###
    bkg_coarse_list	= []
    
    for bkg_file in sorted(bkg_files):
        proc	= process_name(bkg_file)
        print(f"\n Processing: {proc}")
        print(f" File: {os.path.basename(bkg_file)}")
        
        h	= get_histogram(bkg_file, channel)
        if h is None:
            print(f" SKIPPING {proc} - histogram not found")
            continue
        
        print(f" Histogram: {channel} | {h.GetNbinsX()} bins | Integral: {h.Integral():.2f}")
        bkg_coarse_list.append(h)
        
    ### MERGING BACKGROUNDS ###
    print(f"Merging all backgrounds...")
    
    bkg_sum_hist	= None
    
    if not bkg_coarse_list:
    	print(f"WARNING: no background histograms found!")
    else:
    	h_sum_coarse	= bkg_coarse_list[0].Clone("bkg_sum_coarse")
    	h_sum_coarse.SetDirectory(0)
    	h_sum_coarse.Reset()
    	
    	for h in bkg_coarse_list:
    		h_sum_coarse.Add(h)
    	
    	print(f"Summed background integral (full range): {h_sum_coarse.Integral():.2f}")
    	print(f"Summed background integral (SR): {h_sum_coarse.Integral(h_sum_coarse.FindBin(sig_xmin), h_sum_coarse.FindBin(sig_xmax)):.2f}")
    
    ### FITTING FUNC ###
    print(f"\n Fitting '{fit_func} to summed background...")
    
    bkg_sum_hist	= do_fit(h_sum_coarse, sig_nbins, sig_xmin, sig_xmax, "bkg_sum")
    out_file.cd()
    bkg_sum_hist.Write("bkg_sum", ROOT.TObject.kOverwrite)
         
    ### SUMMARY ###
    print(f" Output file contents")
    out_file.ls()
    out_file.Close()

    print(f"\n Successful: output written to {output_file}")
    
    ### OPTIONAL: PLOTTING ###
    if signal_hists_plots and bkg_sum_hist:
        print(f"\n Creating plots...")
        make_plots(signal_hists_plots, bkg_sum_hist, plot_dir)
        print(f"\n Successful: plot saved to {plot_dir}")
    else:
        print(f"\n WARNING: skipping plots - missing signal or background histograms")
        
if __name__ == "__main__":
    main()