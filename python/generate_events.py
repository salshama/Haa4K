"""
Scans over alp mass and higgs-alp couplings (cah) for the signal process and
generates MG and Pythia8 cards and from templates and submits HTCondor jobs
per (mass, coupling) point defined
m_a 	= 0.1, 0.5, 1.0, 1.5, 5.0, 10.0, 30.0, 60.0 (GeV)
cah		= 1e-6, 1e-5, 1e-4, 1e-3, 1e-2, 1e-1, 1.0 (/GeV) -> Higgs-alp coupling
"""

import os
import itertools

### CONFIGURATION ###
alp_scan	= {
			0.1:	[1.0, 1e-1, 1e-2, 1e-3, 1e-4, 1e-5, 1e-6],
			0.5:	[1.0, 1e-1, 1e-2, 1e-3, 1e-4, 1e-5, 1e-6],
			1.0:	[1.0, 1e-1, 1e-2, 1e-3, 1e-4, 1e-5, 1e-6],
			1.5:	[1.0, 1e-1, 1e-2, 1e-3, 1e-4, 1e-5, 1e-6],
			5.0:	[1.0, 1e-1, 1e-2, 1e-3, 1e-4, 1e-5, 1e-6],
			10.0:	[1.0, 1e-1, 1e-2, 1e-3, 1e-4, 1e-5, 1e-6],
			30.0:	[1.0, 1e-1, 1e-2, 1e-3, 1e-4, 1e-5, 1e-6],
			60.0:	[1.0, 1e-1, 1e-2, 1e-3, 1e-4, 1e-5, 1e-6],
}

z_channels	= {
			"ee":	"e+ e-",
			"mumu": "mu+ mu-",
}

ebeam		= 120.0
memory		= 10000
ncpus		= 1
job_flavour	= "workday"
nevents		= 500000

### PATHS ###
source_dir	= "/ceph/sgiappic/FCCAnalyses/"
base_dir	= "/ceph/salshamaily/haa4K_FCCee/"
delphes_tcl	= "/ceph/sgiappic/card_IDEA.tcl"
delphes_dir	= base_dir + "delphes/" # delphes .root output
condor_dir	= base_dir + "HTCondor/" # HTCondor submission files & logs
mg_dir		= base_dir + "madgraph_3.6.6/" # path for lhe files

### FUNCTIONS ###
def make_dir(path: dir):
	"""
	- Creates directory if it does not exist then chmod +x
	"""
	os.makedirs(path, exist_ok=True)
	os.system(f"chmod -R +x {path}")
	
def point_tag(channel: str, ma: float, cah: float) -> str:
	"""
	- Filesystem-safe job label following FCC-ee naming conventions
	- Returns:
	specific naming convention like the process:
	mgp8_ee_{z_channel}H_HAlpAlp_m1p5_cah0p001_ecm240 -> ma = 1.5, cah = 0.001
	- Args:
	ma: float, alp mass
	cah: float, higgs-alp coupling
	"""
	m	= f"m{ma}".replace(".", "p")
	c	= f"cah{cah}".replace(".", "p")
	return f"mgp8_ee_{channel}H_HAlpAlp_m{m}_cah{c}_ecm240"
	
def write_mg_card(channel: str, ma: float, cah: float, job_dir: str, mg_out_dir: str) -> str:
	"""
	- Writes and modifies MadGraph card according to (channel, mass, coupling) point
	- Returns:
	path of modified MG card
	- Args:
	channel: Z channel (leptonic -> e or mu)
	ma, cah: floats, mass and coupling points of alp
	job_dir: directory where the card should be
	mg_out_dir: directory where madgraph is
	"""
	fs		= z_channels[channel]
	
	content	= '# import ALP model and define multi-particles\n'
    content	+= 'import model ALP\n\n'
    content += 'define p = g u c d s u~ c~ d~ s~\n'
    content += 'define j = g u c d s u~ c~ d~ s~\n'
    content += 'define l+ = e+ mu+\n'
    content += 'define l- = e- mu-\n'
    content += 'define vl = ve vm vt\n'
    content += 'define vl~ = ve~ vm~ vt~\n\n'
    content += f'generate e+ e- > z h, z > {fs}, h > ALP ALP\n\n'
    content += f'output {mg_out_dir}\n'
    content += f'launch {mg_out_dir}\n\n'
    content += '# Collision parameters\n'
    content += f'set ebeam1 {ebeam}   # beam 1 energy [GeV]\n'
    content += f'set ebeam2 {ebeam}   # beam 2 energy [GeV]\n'
    content += 'set no_parton_cuts\n\n'
    content += '# ALP model parameters\n'
    content += f'set malp {ma}         # ALP mass [GeV]\n'
    content += f'set cah  {cah}        # Higgs-ALP coupling [GeV^-1]\n\n'
    content += f'set nevents {nevents}\n'
    content += 'done\n'
    
	path	= job_dir + f"mg_param_m{ma}.txt"
	
	with open(path, "w") as f:
		f.write(content)
	
	return path
	
def write_pythia_card(ma: float, job_dir: str, lhe_path: str) -> str:
	"""
	- Writes and modifies the pythia card according to the mass point used
	- Returns:
	path of modified pythia8 card
	- Args:
	ma: float, alp mass
	job_dir: str, directory of where the card should be
	lhe_path: str, path of LHE file for pythia to read
	"""
	content  = 'Random:setSeed = on\n'
    content += 'Main:timesAllowErrors = 10\n'
    content += f'Main:numberOfEvents = {nevents}\n'
    content += '\n'
    content += 'Next:numberCount = 10000\n'
    content += '\n'
    content += 'Beams:frameType = 4\n'
    content += f'Beams:LHEF = {lhe_path}\n'
    content += '\n'
    content += 'Beams:allowMomentumSpread  = off\n'
    content += '\n'
    content += '! These settings sometimes make the covariant matrix of signals\n'
    content += '! negative and the simulation stops — irrelevant for signals anyway\n'
    content += '\n'
    content += 'Beams:allowVertexSpread = on\n'
    content += 'Beams:sigmaVertexX = 5.96E-3\n'
    content += 'Beams:sigmaVertexY = 23.8E-6\n'
    content += 'Beams:sigmaVertexZ = 0.397\n'
    content += 'Beams:sigmaTime = 10.89    !  36.3 ps\n'
    content += '\n'
    content += 'PartonLevel:ISR = on\n'
    content += 'PartonLevel:FSR = on\n'
    content += '\n'
    content += '! decay of ALP\n'
    content += '! mWidth = 0 is a placeholder: LesHouches:setLifetime = 2 (below)\n'
    content += '! overrides the lifetime with the value MadGraph wrote to the LHE\n'
    content += f'9000005:all = ALP ALP 0 0 0 {ma} 0 1.0 75.0 0\n'
    content += '9000005:oneChannel = 1 1.000 101 321 -321\n'
    content += '9000005:mayDecay = on\n'
    content += '9000005:isResonance = on\n'
    content += '9000005:onMode = off      ! turn off all channels first\n'
    content += '9000005:onIfAny = 321     ! then re-enable channels with K+\n'
    content += '\n'
    content += 'LesHouches:setLifetime = 2'
    
	path	= job_dir + "pythia_mg_m{ma}.cmd"
	
	with open(path, "w") as fh:
		fh.write(content)
		
	return path
	
def write_job(job_dir: str, mg_card: str, mg_out_dir: str, pythia_card: str, delphes_out_dir: str) -> str:
	"""
	- Writes bash script for HTCondor execution and follows: MG->P8->Delphes->compress LHE
	- Returns:
	path of bash script
	- Args:
	job_dir: str, directory of job submitted
	mg_card, mg_out_dir: str, MG card and directory paths
	pythia_card, pythia_dir: str, pythia card and directory paths
	output_root: 
	"""
	lhe_path	= mg_out_dir + "Events/run_01/unweighted_events.lhe"
	script_path	= job_dir + "run_production.sh"
	
	scr	= '#!/bin/bash\n\n'
    scr	+= f'source {SOURCE_DIR}setup.sh\n\n'
    scr += f'cd {BASE_DIR}\n\n'
    scr += '# Step 1: MadGraph event generation\n'
    scr += f'mg5_aMC {mg_card}\n\n'
    scr += '# Step 2: Pythia8 showering + Delphes fast simulation\n'
    scr += f'DelphesPythia8 {delphes_tcl} {pythia_card} {delphes_out_dir}\n\n'
    scr += '# Step 3: Compress LHE file to save disk space\n'
    scr += f'gzip {lhe_path} 2>/dev/null || true\n\n'
    scr += 'echo "Production complete."\n'
    
    with open(script_path, "w") as fh:
    	fh.write(scr)
    os.system(f"chmod +x {script_path}")
    
    return script_path
    
def write_condor_config(job_dir: str, script_path: str) -> str:
	"""
	- Writes the condor .sub file matching existing submission format with one job
	per (channel, mass, cah) point
	- Returns:
	cfg_path: path of configuration
	- Args:
	job_dir: str, directory of job submitted
	script_path: str, directory of bash script
	"""
	cfg  = 'Universe               = docker\n'
    cfg += 'docker_image           = cverstege/alma9-gridjob\n'
    cfg += 'accounting_group       = cms.higgs\n'
    cfg += f'executable             = {script_path}\n'
    cfg += f'log                    = {job_dir}condor.log\n'
    cfg += f'output                 = {job_dir}condor.out\n'
    cfg += f'error                  = {job_dir}condor.err\n'
    cfg += 'max_retries            = 3\n'
    cfg += f'+JobFlavour            = "{job_flavour}"\n'
    cfg += f'request_memory        = {memory} MB\n'
    cfg += f'request_cpus          = {ncpus}\n'
    cfg += 'requirements           = (TARGET.ProvidesCPU && TARGET.ProvidesEKPResources)\n'
    cfg += 'should_transfer_files  = IF_NEEDED\n'
    cfg += 'when_to_transfer_output = ON_EXIT\n'
    cfg += 'queue filename matching files\n'
    
    cfg_path = job_dir + "job_submit.cfg"
    
    with open(cfg_path, "w") as fh:
    	fh.write(cfg)
    
    return cfg_path
    
def run(dry_run: bool=True, skip_existing: bool=True):
	"""
	- Loops over all (channel, mass, cah) combinations, writes cards and scripts
	and optionally submits to HTCondor
	- Returns:
	submitted jobs (optional)
	- Args:
	dry_run: bool, if True then generate all files but do not call condor_submit
	skip_existing: bool, if True then skip points whose job_submit.cfg already exists (useful for resubmitting only failed jobs)
	"""
	make_dir(condor_dir)
	make_dir(mg_dir)
	make_dir(delphes_dir)
	
	combos	= list(itertools.product(z_channels.keys(), alp_scan.items()))
	ntotal	= sum(len(cahs) for _, (_, cahs) in combos) * 1
	
	print('\n' + '='*65)
    print('  ALP production scan — FCC-ee @ sqrt(s) = 240 GeV')
    print('='*65)
    print(f'  Z channels  : {list(z_channels.keys())}')
    print(f'  Masses [GeV]: {list(alp_scan.keys())}')
    print(f'  Events/job  : {nevents:,}')
    print(f'  Dry run     : {dry_run}')
    print('='*65 + '\n')
    
    nsubmit		= 0
    nskipped	= 0
    
    for channel, (ma, cahs) in combos:
    	for cah in cahs:
    		tag			= point_tag(channel, ma, cah)
    		job_dir		= condor_dir + tag + "/"
    		cfg_path	= job_dir + "job_submit.cfg"
    		
    		print(f"[{tag}]")
    		
    		# skip if already set up to avoid overwriting running jobs
    		if skip_existing and os.path.isfile(cfg_path):
    			print(f" Already configured - skipping")
    			nskipped += 1
    			if not dry_run:
    				os.system(f"condor_submit {cfg_path}")
    				nsubmit += 1
    			continue
    		
    		make_dir(job_dir)
    		
    		# paths for this point
    		mg_out_dir		= mg_dir + tag + "/"
    		lhe_path		= mg_out_dir + "Events/run_01/unweighted_events.lhe"
    		delphes_out_dir	= delphes_dir + tag + "/events.root"
    		make_dir(delphes_dir + tag + "/")
    		
    		# write all cards and the bash script
    		mg_card		= write_mg_card(channel, ma, cah, job_dir, mg_out_dir)
    		pythia_card	= write_pythia_card(ma, job_dir, lhe_path)
    		script		= write_job_script(job_dir, mg_card, mg_out_dir, pythia_card, delphes_out_dir)
    		cfg_path	= write_condor_config(job_dir, script)
    		print(f" Successful: cards + script written")
    		
    		if dry_run:
    			print(f" [DRY RUN]: would submit {cfg_path}")
    		else:
    			ret	= os.system(f"condor_submit {cfg_path}")
    			if ret==0:
    				print(f" Submission ok!")
    			else:
    				print(f" [ERROR] condor_submit returned {ret}")
    			nsubmit += 1
    print(f"\n Done. Submitted: {nsubmit} | Skipped: {nskipped}")
    
if __name__ == "__main__":
	run(dry_run=True, skip_existing=True)