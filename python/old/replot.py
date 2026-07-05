#code adapted from FCCAnalyses/do_plots.py

import sys
import os
import os.path
import ntpath
import importlib
import copy
import re
import logging
import ROOT

# Set ROOT to batch mode so it doesn't open all the plots
ROOT.gROOT.SetBatch(True)

def sorted_dict_values(dic: dict) -> list:
    ''''
    Sort values in the dictionary.
    '''
    keys = sorted(dic)
    return [dic[key] for key in keys]

def make_dir_if_not_exists(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)
        os.system("cp /web/salshamaily/public_html/haa4K_FCCee/index.php {}".format(directory)) #copy index to show plots in web page automatically
        print(f"Directory created successfully.")
    #else:
        print(f"Directory already exists.")

def file_exists(file_path):
    return os.path.isfile(file_path)

# directory with final stage files
DIRECTORY = "/ceph/salshamaily/haa4K_FCCee/samples/"

TAG = ["HAlpHAlp"]

SUBDIR = ["RecoKaonElecSel"]

#category to plot
CAT = [""]

CUTS = {"RecoKaonElecSel":"RecoKaonElecSel"}

#now you can list all the histograms that you want to plot
VARIABLES = [
	"RecoHiggs_mass"
]

LIST_VAR = {"Variables": VARIABLES}

#directory where you want your plots to go
DIR_PLOTS = '/ceph/salshamaily/haa4K_FCCee/analysis/plots_output/replot_all_samples_mgp8sig_norwt_042026/'

#labels for the cuts in the plots
LABELS = {"RecoKaonElecSel": "n_{kaons}=4 and n_{electrons}=2, charge_{kaons}=1, 0.2 < E_{kaons} < 0.7 GeV"}

ana_tex_cat = {""}

ana_tex_sub = {'HAlpAlp':"e^{+}e^{-} #rightarrow Z H, H #rightarrow aa #rightarrow K^{+}K^{-}K^{+}K^{-}"}

energy		= 240
collider	= 'FCC-ee'
intLumi		= 10.8 #ab^-1
LOGY 		= True

#list of backgrounds, then legend and colors to be assigned to them
backgrounds_all = [
    "p8_ee_WW_ecm240",
    "p8_ee_Zqq_ecm240",
    "p8_ee_ZZ_ecm240",
]

legend = {
	"mgp8_ee_eeH_HAlpAlp_m1_ecm240":"m_{a} = 1.5 GeV",
	"mgp8_ee_eeH_HAlpAlp_m10_ecm240":"m_{a} = 10 GeV",
	"mgp8_ee_eeH_HAlpAlp_m30_ecm240":"m_{a} = 30 GeV",
	"mgp8_ee_eeH_HAlpAlp_m60_ecm240":"m_{a} = 60 GeV",
    
    "p8_ee_WW_ecm240":"ee #rightarrow WW",
    "p8_ee_Zqq_ecm240":"ee #rightarrow Z #rightarrow qq",
    "p8_ee_ZZ_ecm240":"ee #rightarrow ZZ",
}

legcolors = {
	'mgp8_ee_eeH_HAlpAlp_m1_ecm240':ROOT.TColor.GetColor('#c51b7d'),
	'mgp8_ee_eeH_HAlpAlp_m10_ecm240':ROOT.TColor.GetColor('#2b8cbe'),
	'mgp8_ee_eeH_HAlpAlp_m30_ecm240':ROOT.TColor.GetColor('#fdae6b'),
	'mgp8_ee_eeH_HAlpAlp_m60_ecm240':ROOT.TColor.GetColor('#762a83'),
    
    'p8_ee_WW_ecm240':ROOT.TColor.GetColor('#d9f0d3'),
    'p8_ee_Zqq_ecm240':ROOT.TColor.GetColor('#1b7837'),
    'p8_ee_ZZ_ecm240':ROOT.TColor.GetColor('#7fbf7b'),
}

#list of signals, then legend and colors to be assigned to them
signals = [
	'mgp8_ee_eeH_HAlpAlp_m1_ecm240',
	'mgp8_ee_eeH_HAlpAlp_m10_ecm240',
	'mgp8_ee_eeH_HAlpAlp_m30_ecm240',
	'mgp8_ee_eeH_HAlpAlp_m60_ecm240',
]
    
# for tag in TAG:
# #     for cat in CAT:
# #         if "tag" in tag:
# #                 variables = VARIABLES + VARIABLES_TAG + LIST_VAR[cat]
# #         else: 
# #             variables = VARIABLES + LIST_VAR[cat]
# #         variables = ["RecoHiggs_mass"]
# 
# 	for sub in SUBDIR:
# 		directory = DIRECTORY + tag + "/" + sub + "/"
# 
# 		CUT = ["RecoKaonElecSel"]

# 		for cut in CUT:
for variable in VARIABLES:

	directory = DIRECTORY
	print(variable, directory)

	canvas = ROOT.TCanvas("", "", 800, 800)

	nsig = len(signals)
	nbkg = len(backgrounds_all) #put to zero if you only want to look at signals

	#legend coordinates and style
	legsize = 0.04*nsig
	legsize2 = 0.04*nbkg
	leg = ROOT.TLegend(0.16, 0.70 - legsize, 0.45, 0.70)
	leg.SetFillColor(0)
	leg.SetFillStyle(0)
	leg.SetLineColor(0)
	leg.SetShadowColor(0)
	leg.SetTextSize(0.025)
	leg.SetTextFont(42)
	leg.SetBorderSize(0) 

	leg2 = ROOT.TLegend(0.45, 0.70 - legsize2, 0.90, 0.70)
	leg2.SetNColumns(2)
	leg2.SetFillColor(0)
	leg2.SetFillStyle(0)
	leg2.SetLineColor(0)
	leg2.SetShadowColor(0)
	leg2.SetTextSize(0.025)
	leg2.SetTextFont(42)
	leg2.SetBorderSize(0) 

	#global arrays for histos and colors
	histos = []
	colors = []
	leg_bkg = []

	#loop over files for signals and backgrounds and assign corresponding colors and titles
	#loop to merge different sources into one histograms for easier plotting

	for s in signals:
		fin = directory+"RecoHiggs_mass_RecoKaonElecSel_rebinned.root"
		if file_exists(fin): #might be an empty file after stage2 
			tf = ROOT.TFile.Open(fin, 'READ')
			h = tf.Get(s+"_"+variable)
			hh = copy.deepcopy(h)
			hh.SetDirectory(0)
			histos.append(hh)
			colors.append(legcolors[s])
			leg.AddEntry(histos[-1], legend[s], "l")
			leg_bkg.append(0)
	nsig=len(histos)

	if nbkg!=0:
		#for the common backgrounds i want to keep them separate into different histograms
		#no need to have the ones that are empty
		for b in backgrounds_all:
			fin = directory+"RecoHiggs_mass_RecoKaonElecSel_rebinned.root"
			if file_exists(fin):
				tf = ROOT.TFile.Open(fin, 'READ')
				h = tf.Get(b+"_"+variable)
				hh = copy.deepcopy(h)
				hh.SetDirectory(0)
				histos.append(hh)
				colors.append(legcolors[b])
				leg_bkg.append(b)

		#merge backgrounds in plotting
# 		i = 0
# 		hh = None
# 		for b in LIST_B[cat]:
# 			j = 0
# 			for sub in SUBDIR:
# 				fin = f"{directory}{sub}{b}_{cut}_histo.root"
# 				if (i==0 and j==0):
# 					with ROOT.TFile(fin) as tf:
# 						h = tf.Get(variable)
# 						hh = copy.deepcopy(h)
# 						hh.SetDirectory(0)
# 				else:
# 					with ROOT.TFile(fin) as tf:
# 						h = tf.Get(variable)
# 						hh1 = copy.deepcopy(h)
# 						hh1.SetDirectory(0)
# 					hh.Add(hh1)
# 				j += 1
# 			i += 1
# 		histos.append(hh)
# 		colors.append(bcolors[cat])
# 		leg2.AddEntry(histos[-1], blegend[cat], "f")
		
		#drawing stack for backgrounds
		hStackBkg = ROOT.THStack("hStackBkg", "")

		BgMCHistYieldsDic = {}
		for i in range(nsig, len(histos)):
			h = histos[i]
			h.SetLineWidth(1)
			h.SetLineColor(ROOT.kBlack)
			h.SetFillColor(colors[i])
			#making sure only histograms with integral positive get added to the stack and legend
			if h.Integral() > 0:
				BgMCHistYieldsDic[h.Integral()] = h
				leg2.AddEntry(h, legend[leg_bkg[i]], "f")
			else:
				BgMCHistYieldsDic[-1*nbkg] = h

		# sort stack by yields (smallest to largest)
		BgMCHistYieldsDic = sorted_dict_values(BgMCHistYieldsDic)
		for h in BgMCHistYieldsDic:
			hStackBkg.Add(h)

		if LOGY==True :
			hStackBkg.SetMinimum(1e-1) #change the range to be plotted
			hStackBkg.SetMaximum(1e10) #leave some space on top for the legend
		else:
			h = hStackBkg.GetHists() #list of histograms 
			last = 0
			for i in range(len(histos)):
				if (last<histos[i].GetMaximum()):
					last = histos[i].GetMaximum() 
				# Set the y-axis range with additional white space
			hStackBkg.SetMinimum(0)
			hStackBkg.SetMaximum(last*3)

		#draw the histograms
		hStackBkg.Draw("HIST")

		# add the signal histograms
		for i in range(nsig):
			h = histos[i]
			h.SetLineWidth(3)
			h.SetLineColor(colors[i])
			h.Draw("HIST SAME")

		hStackBkg.GetYaxis().SetTitle("Events")
		hStackBkg.GetXaxis().SetTitle(histos[0].GetXaxis().GetTitle()) #get x axis label from final stage
		hStackBkg.GetXaxis().SetTitleOffset(1.2)
		
# 		hStackBkg.GetXaxis().SetLimits(100, 180)

	else: 
		# add the signal histograms
		for i in range(nsig):
			h = histos[i]
			h.SetLineWidth(3)
			h.SetLineColor(colors[i])
			if i == 0:
				h.Draw("HIST")
				h.GetYaxis().SetTitle("Events")
				h.GetXaxis().SetTitle(histos[i].GetXaxis().GetTitle())
				#h.GetYaxis().SetTitleOffset(1.5)
				h.GetXaxis().SetTitleOffset(1.2)
				#h.GetXaxis().SetLimits(1, 1000)
				if LOGY==True :
					h.GetYaxis().SetRangeUser(1e-6,1e8) #range to set if only working with signals
				else:
					max_y = h.GetMaximum() 
					h.GetYaxis().SetRangeUser(0, max_y*1.5 )
			else: 
				h.Draw("HIST SAME")
	
# 	extralab = LABELS[cut]
	
	if 'ee' in collider:
		leftText = 'FCCAnalyses: FCC-ee Simulation (Delphes)'
	rightText = f'#sqrt{{s}} = {energy} GeV, L={intLumi} ab^{{-1}}'

	latex = ROOT.TLatex()
	latex.SetNDC()

	text = '#bf{#it{'+rightText+'}}'
	latex.SetTextSize(0.03)
	latex.DrawLatex(0.18, 0.84, text)

# 	text = '#bf{#it{' + ana_tex_cat[cat] + ana_tex_sub[sub] + '}}'
# 	latex.SetTextSize(0.03)
# 	latex.DrawLatex(0.18, 0.80, text)

# 	text = '#bf{#it{' + extralab + '}}'
# 	latex.SetTextSize(0.025)
# 	latex.DrawLatex(0.18, 0.74, text)

	latex.SetTextAlign(31)
	text = '#it{' + leftText + '}'
	latex.SetTextSize(0.03)
	latex.DrawLatex(0.92, 0.92, text)

	#fix legend height after having the correct number of processes

	legsize = 0.04*nsig
	legsize2 = 0.03*(len(histos)-nsig)/2
	leg.SetY1(0.70 - legsize)
	leg2.SetY1(0.70 - legsize2)

	leg.Draw()
	leg2.Draw()

	# Set Logarithmic scales for both x and y axes
	if LOGY == True:
		canvas.SetLogy()
		canvas.SetTicks(1, 1)
		canvas.SetLeftMargin(0.14)
		canvas.SetRightMargin(0.08)
		canvas.GetFrame().SetBorderSize(12)

		canvas.RedrawAxis()
		canvas.Modified()
		canvas.Update()

		dir = DIR_PLOTS
		make_dir_if_not_exists(DIR_PLOTS)

		canvas.SaveAs(dir + variable + "_RecoKaonElecSel" + "_logy_rebinned.pdf")
	else:
		canvas.SetTicks(1, 1)
		canvas.SetLeftMargin(0.14)
		canvas.SetRightMargin(0.08)
		canvas.GetFrame().SetBorderSize(12)

		canvas.RedrawAxis()
		canvas.Modified()
		canvas.Update()

		dir = DIR_PLOTS

		canvas.SaveAs(dir + variable + "_RecoKaonElecSel" + "_lin_rebinned.pdf")