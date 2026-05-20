"""
Scans over alp mass and higgs-alp couplings (cah) for the signal process and
generates MG and Pythia8 cards from templates and submits HTCondor jobs per (mass, coupling) point defined.
Instead of producing a separate sample for every cah value, one sample is produced per (mass, Z channel) at cah_ref
and MG reweights the events to all other cah values -> 12 mass x 3 channels = 36 jobs.
Each LHE job file contains one event set + N reweighted weight columns

Workflow per job
-----------------
1. MG generates events + reweighted LHE
2. MG computes ALP width automatically
3. Script extracts computed width from param_card
4. sed patches the __ALP_WIDTH__ in the pythia card
5. DelphesPythia8 runs pythia8 showering + delphes simulation

Notes on reweighting
---------------------
Before running at full scale, verify:
1. k4SimDelphes includes PR #148
2. FCCAnalysis do_weighted() is available
3. Run one job manually, confirm LHE has <rwgt> blocks
"""

import os
import itertools

### CONFIGURATION ###
cah_ref		= 1.0
cah_val		= 0.01
alp_scan	= {
			0.05:	[1e-1, 1e-2, 1e-3, 1e-4, 1e-5, 1e-6],
			0.1:	[1e-1, 1e-2, 1e-3, 1e-4, 1e-5, 1e-6],
			0.5:	[1e-1, 1e-2, 1e-3, 1e-4, 1e-5, 1e-6],
			1.0:	[1e-1, 1e-2, 1e-3, 1e-4, 1e-5, 1e-6],
			1.5:	[1e-1, 1e-2, 1e-3, 1e-4, 1e-5, 1e-6],
			5.0:	[1e-1, 1e-2, 1e-3, 1e-4, 1e-5, 1e-6],
			10.0:	[1e-1, 1e-2, 1e-3, 1e-4, 1e-5, 1e-6],
			20.0:	[1e-1, 1e-2, 1e-3, 1e-4, 1e-5, 1e-6],
			30.0:	[1e-1, 1e-2, 1e-3, 1e-4, 1e-5, 1e-6],
			40.0:	[1e-1, 1e-2, 1e-3, 1e-4, 1e-5, 1e-6],
			50.0:	[1e-1, 1e-2, 1e-3, 1e-4, 1e-5, 1e-6],
			60.0:	[1e-1, 1e-2, 1e-3, 1e-4, 1e-5, 1e-6],
}

z_channels	= {
			"ee":	"e+ e-",
			"mumu": "mu+ mu-",
			"qq":	"q q~",
}

ebeam		= 120.0
memory		= 10000
ncpus		= 1
job_flavour	= "workday"
nevents		= 500000

### PATHS ###
base_dir	= "/ceph/salshamaily/haa4K_FCCee/"
source_dir	= "/ceph/sgiappic/FCCAnalyses/"
delphes_tcl	= "/ceph/sgiappic/card_IDEA.tcl"
edm4hep_cfg	= base_dir + "edm4hep_output_config.tcl" # steers EDM4HEP output
condor_dir	= base_dir + "HTCondor/" # HTCondor submission files & logs
mg_dir		= base_dir + "madgraph_3.6.6/" # path for lhe files
delphes_dir	= base_dir + "delphes/" # delphes .root output
local_setup	= base_dir + "setup_local.sh" # local path for stack


### FUNCTIONS ###
def make_dir(path: dir):
	"""
	- Creates directory if it does not exist then chmod +x
	"""
	os.makedirs(path, exist_ok=True)
	os.system(f"chmod -R +x {path}")
	
def point_tag(channel: str, ma: float) -> str:
	"""
	- Filesystem-safe job label following FCC-ee naming conventions
	- Returns:
	specific naming convention like the process:
	mgp8_ee_{z_channel}H_HAlpAlp_m1p5_ecm240 -> ma = 1.5
	- Args:
	channel: str, z channel
	ma: float, alp mass
	"""
	m	= f"{ma}".replace(".", "p")
	return f"mgp8_ee_{channel}H_HAlpAlp_m{m}_ecm240"
	
def validation_tag(channel: str, ma: float, cah: float) -> str:
	"""
	- Creates tag for a generated sample at a fixed (channel, mass, cah)
	- Returns:
	string of tag
	- Args:
	channel: str, mode of Z boson decay
	ma: float, mass point of ALP
	cah: float, coupling of Higgs-Alp
	"""
	m	= f"{ma}".replace(".","p")
	c	= f"{cah}".replace(".","p")
	
	return f'mgp8_ee_{channel}H_HAlpAlp_m{m}_cah{c}_ecm240'
	
def write_metadata(job_dir: str, channel: str, ma: float, cah_list: list):
	"""
	- Writes a human-readable metadata file for this (channel, mass) job to record the
	generation and reweighting values. This is a table that you need to call when using
	do_weighted(index) in FCCAnalysis where indices show the reweighting "cah" values in the
	order they appear in alp_scan and MG reweighting block
	- Returns:
	txt file
	- Args:
	job_dir: directory where the job should be
	channel: str, z channel
	ma: float, alp mass
	cah_list: list of cah targeted values
	"""
	lines	= '# ALP production metadata\n'
    lines	+= f'# channel          : {channel}\n'
    lines	+= f'# mass [GeV]       : {ma}\n'
    lines	+= f'# cah_ref          : {cah_ref}  <- events generated at this coupling\n'
    lines	+= f'# nevents          : {nevents:,}\n'
    lines	+= f'# sqrt(s) [GeV]    : {2 * ebeam:.0f}\n'
    lines	+= '#\n'
    lines	+= '# Weight column index -> cah value\n'
    lines	+= '# Use this when calling do_weighted(index) in FCCAnalysis\n'
    lines	+= '# Index 0 = nominal weight at cah_ref\n'
    lines	+= '# Indices 1..N = reweighted to the cah values listed below\n'
    lines	+= '#\n'
    lines	+= f'#   index 0  :  {cah_ref}  (nominal / cah_ref)\n'
    
    for i, cah_value in enumerate(cah_list):
    	lines	+= f'#   index {i+1}  :  {cah_value}\n'
    
    with open(job_dir + "metadata.txt", "w") as fh:
    	fh.write(lines)
	
def write_mg_card(channel: str, ma: float, cah_list: list, job_dir: str, mg_out_dir: str) -> str:
	"""
	- Writes and modifies MadGraph card according to (channel, mass) point
	- Returns:
	path of modified MG card
	- Args:
	channel: Z channel (e, mu, or jets)
	ma, cah: floats, mass and coupling points of alp
	job_dir: directory where the card should be
	mg_out_dir: directory where madgraph is
	"""
	fs		= z_channels[channel]
	
	content	=	'# import ALP model and define multi-particles\n'
    content	+=	'import model ALP\n\n'
    content +=	'define p = g u c d s u~ c~ d~ s~\n'
    content +=	'define j = g u c d s u~ c~ d~ s~\n'
    content +=	'define l+ = e+ mu+\n'
    content +=	'define l- = e- mu-\n'
    content	+=	'define q = u d s c b\n\n'
    content	+=	'define q~ = u~ d~ s~ c~ b~\n\n'
    content +=	'define vl = ve vm vt\n'
    content +=	'define vl~ = ve~ vm~ vt~\n\n'
    content +=	f'generate e+ e- > z h, z > {fs}, h > ALP ALP\n\n'
    content +=	f'output {mg_out_dir}\n'
    content +=	f'launch {mg_out_dir}\n\n'
    content +=	'# Collision parameters\n'
    content +=	f'set ebeam1 {ebeam}   # beam 1 energy [GeV]\n'
    content +=	f'set ebeam2 {ebeam}   # beam 2 energy [GeV]\n'
    content +=	'set no_parton_cuts\n\n'
    content +=	'# ALP model parameters\n'
    content +=	f'set malp {ma}		# ALP mass [GeV]\n'
    content +=	f'set CAH  {cah_ref}	# Higgs-ALP coupling [GeV^-1]\n'
    content	+=	f'set param_card DECAY 9000005 Auto\n\n'
    content +=	f'set nevents {nevents}\n'
    content	+=	'reweight 1\n'
    
    for i, cah_value in enumerate(cah_list):
    	content	+= f' # index {i+1}: CAH = {cah_value}\n'
    	content	+= f' change param_card CAH {cah_value}\n'
    
    content += 'done\n\n'
    content += 'done\n'
    
	path	= job_dir + f"mg_param_m{ma}.txt"
	
	with open(path, "w") as f:
		f.write(content)
	
	return path
	
def write_mg_validation_card(channel: str, ma: float, cah:float, job_dir: str, mg_out_dir: str) -> str:
	"""
	- Writes and modifies the MG card according to the channels, masses, and selected cah value
	- Returns:
	path of the MG card for validation of re-weighting
	- Args:
	channel: str, modes of the Z boson decays
	ma: float, mass points of the ALP
	cah: float, given cah value to validate
	job_dir: str, path of the job submitted
	mg_out_dir: str, output of the MG job
	"""
	fs		= z_channels[channel]
	
	content	=	'# import ALP model and define multi-particles\n'
    content	+=	'import model ALP\n\n'
    content +=	'define p = g u c d s u~ c~ d~ s~\n'
    content +=	'define j = g u c d s u~ c~ d~ s~\n'
    content +=	'define l+ = e+ mu+\n'
    content +=	'define l- = e- mu-\n'
    content	+=	'define q = u d s c b\n\n'
    content	+=	'define q~ = u~ d~ s~ c~ b~\n\n'
    content +=	'define vl = ve vm vt\n'
    content +=	'define vl~ = ve~ vm~ vt~\n\n'
    content +=	f'generate e+ e- > z h, z > {fs}, h > ALP ALP\n\n'
    content +=	f'output {mg_out_dir}\n'
    content +=	f'launch {mg_out_dir}\n\n'
    content +=	'# Collision parameters\n'
    content +=	f'set ebeam1 {ebeam}   # beam 1 energy [GeV]\n'
    content +=	f'set ebeam2 {ebeam}   # beam 2 energy [GeV]\n'
    content +=	'set no_parton_cuts\n\n'
    content +=	'# ALP model parameters\n'
    content +=	f'set malp {ma}		# ALP mass [GeV]\n'
    content +=	f'set CAH  {cah}	# Higgs-ALP coupling [GeV^-1]\n'
    content	+=	f'set param_card DECAY 9000005 Auto\n\n'
    content += 	f'set nevents {nevents}\n'
    content	+= 	'done\n'
    
    path	= job_dir + f"mg_param_m{ma}_val.txt"
    
    with open(path, "w") as fh:
    	fh.write(content)
    return path
	
def write_pythia_card(ma: float, job_dir: str, lhe_path: str, tag: str = '') -> str:
	"""
	- Writes and modifies the pythia card according to the mass point used
	- Returns:
	path of modified pythia8 card
	- Args:
	ma: float, alp mass
	job_dir: str, directory of where the card should be
	lhe_path: str, path of LHE file for pythia to read
	tag: str, if tag is present then a validation tag will be attached to the path else empty
	"""
	content	=	'Random:setSeed = on\n'
    content	+=	'Main:timesAllowErrors = 10\n'
    content	+=	f'Main:numberOfEvents = {nevents}\n'
    content	+=	'\n'
    content	+=	'Next:numberCount = 10000\n'
    content	+=	'\n'
    content	+=	'Beams:frameType = 4\n'
    content	+=	f'Beams:LHEF = {lhe_path}\n'
    content	+=	'\n'
    content	+=	'Beams:allowMomentumSpread  = off\n'
    content	+=	'\n'
    content	+=	'Beams:allowVertexSpread = on\n'
    content	+=	'Beams:sigmaVertexX = 5.96E-3\n'
    content	+=	'Beams:sigmaVertexY = 23.8E-6\n'
    content	+=	'Beams:sigmaVertexZ = 0.397\n'
    content	+=	'Beams:sigmaTime = 10.89    !  36.3 ps\n'
    content	+=	'\n'
    content	+=	'PartonLevel:ISR = on\n'
    content	+=	'PartonLevel:FSR = on\n'
    content	+=	'\n'
    content	+=	'! decay of ALP\n'
    content	+=	f'9000005:all = ALP ALP 0 0 0 {ma} __ALP_WIDTH__ 1.0 75.0 0\n'
    content	+=	'9000005:oneChannel = 1 1.000 101 321 -321\n'
    content	+=	'9000005:mayDecay = on\n'
    content	+=	'9000005:isResonance = on\n'
    content	+=	'9000005:onMode = off      ! turn off all channels first\n'
    content	+=	'9000005:onIfAny = 321     ! then re-enable channels with K+\n'
    content	+=	'\n'
    content	+=	'LesHouches:setLifetime = 2'
    
    suffix	= f"_{tag}" if tag else ""
    
	path	= job_dir + f"pythia_mg_m{ma}{suffix}.cmd"
	
	with open(path, "w") as fh:
		fh.write(content)
		
	return path
	
def write_job(job_dir: str, mg_card: str, mg_out_dir: str, pythia_card: str, delphes_out: str) -> str:
	"""
	- Writes bash script for HTCondor execution and follows: MG->P8->Delphes
	- Returns:
	path of bash script
	- Args:
	job_dir: str, directory of job submitted
	mg_card, mg_out_dir: str, MG card and directory paths
	pythia_card, pythia_dir: str, pythia card and directory paths
	delphes_out_dir: str, path of the output from delphes 
	"""
	lhe_path		= mg_out_dir	+ "Events/run_01/unweighted_events.lhe"
	lhe_gz_path		= lhe_path		+ ".gz"
	param_card_path	= mg_out_dir	+ "Cards/param_card.dat"
	script_path		= job_dir		+ "run_production.sh"
	
	scr	=	'#!/bin/bash\n\n'
    scr +=	f'source {base_dir}setup_local.sh\n\n'
    scr	+=	f'cd {base_dir}\n\n'
    scr	+=	f'mg5_aMC {mg_card}\n\n'
    scr	+=	f'PARAM_CARD="{param_card_path}"\n'
    scr	+=	f'PYTHIA_CARD="{pythia_card}"\n'
    scr	+=	'ALP_WIDTH=$(grep -i "^DECAY[[:space:]]*9000005" "$PARAM_CARD" | awk \'{print $3}\')\n'
    scr	+=	'if [ -z "$ALP_WIDTH" ]; then\n'
    scr	+=	'    echo "[ERROR] Could not find ALP width in $PARAM_CARD" >&2\n'
    scr	+=	'    exit 1\n'
    scr	+=	'fi\n'
    scr	+=	'echo "  ALP width from MadGraph: $ALP_WIDTH GeV"\n'
    scr	+=	'sed -i "s/__ALP_WIDTH__/${ALP_WIDTH}/" "$PYTHIA_CARD"\n\n'
    scr +=	f'LHE="{lhe_path}"\n'
    scr +=	f'LHE_GZ="{lhe_gz_path}"\n'
    scr +=	'if [ -f "$LHE_GZ" ] && [ ! -f "$LHE" ]; then\n'
    scr +=	'    echo "  Decompressing LHE file..."\n'
    scr +=	'    gunzip "$LHE_GZ"\n'
    scr +=	'fi\n\n'
    scr +=	f'DelphesPythia8_EDM4HEP {delphes_tcl} {edm4hep_cfg} "$PYTHIA_CARD" {delphes_out}\n\n'
    scr	+=	'echo "Production complete"\n'
    
    with open(script_path, "w") as fh:
    	fh.write(scr)
    os.system(f"chmod +x {script_path}")
    
    return script_path
    
def write_job_validation(job_dir: str, mg_card: str, mg_out_dir: str, pythia_card: str, delphes_out: str) -> str:
	"""
	Identical to write_job except no re-weighting
	"""
	lhe_path		= mg_out_dir + "Events/run_01/unweighted_events.lhe"
	lhe_gz_path		= lhe_path + ".gz"
	param_card_path	= mg_out_dir + "Cards/param_card.dat"
	script_path		= job_dir + "run_validation.sh"
	
	scr  = '#!/bin/bash\n'
	scr += f'source {local_setup}\n\n'
    scr += f'cd {base_dir}\n\n'
    scr += 'echo "VALIDATION JOB"\n'
    scr += 'echo "Using: $(which DelphesPythia8_EDM4HEP)"\n\n'
    scr += f'mg5_aMC {mg_card}\n\n'
    scr += f'PARAM_CARD="{param_card_path}"\n'
    scr += f'PYTHIA_CARD="{pythia_card}"\n'
    scr += 'ALP_WIDTH=$(grep -i "^DECAY[[:space:]]*9000005" "$PARAM_CARD" | awk \'{print $3}\')\n'
    scr += 'if [ -z "$ALP_WIDTH" ]; then\n'
    scr += '    echo "[ERROR] Could not find ALP width in $PARAM_CARD" >&2\n'
    scr += '    exit 1\n'
    scr += 'fi\n'
    scr += 'echo "  ALP width: $ALP_WIDTH GeV"\n\n'
    scr += 'sed -i "s/__ALP_WIDTH__/${ALP_WIDTH}/" "$PYTHIA_CARD"\n\n'
    scr += f'LHE="{lhe_path}"\n'
    scr += f'LHE_GZ="{lhe_gz_path}"\n'
    scr += 'if [ -f "$LHE_GZ" ] && [ ! -f "$LHE" ]; then\n'
    scr += '    gunzip "$LHE_GZ"\n'
    scr += 'fi\n\n'
    scr += f'DelphesPythia8_EDM4HEP {delphes_tcl} {edm4hep_cfg} "$PYTHIA_CARD" {delphes_out}\n\n'
    scr += 'echo "Validation complete."\n'
    
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
	cfg	=	'Universe					= docker\n'
    cfg	+=	'docker_image				= cverstege/alma9-gridjob\n'
    cfg	+=	'accounting_group			= cms.higgs\n'
    cfg	+=	f'executable				= {script_path}\n'
    cfg	+=	f'log						= {job_dir}condor.log\n'
    cfg	+=	f'output					= {job_dir}condor.out\n'
    cfg	+=	f'error						= {job_dir}condor.err\n'
    cfg	+=	'max_retries				= 3\n'
    cfg	+=	f'+JobFlavour				= "{job_flavour}"\n'
    cfg	+=	f'request_memory			= {memory} MB\n'
    cfg	+=	f'request_cpus				= {ncpus}\n'
    cfg	+=	'requirements				= (TARGET.ProvidesCPU && TARGET.ProvidesEKPResources)\n'
    cfg	+=	'should_transfer_files		= IF_NEEDED\n'
    cfg	+=	'when_to_transfer_output	= ON_EXIT\n'
    cfg	+=	'queue 1\n'
    
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
	
	ntotal	= len(z_channels) * len(alp_scan)

    print('  ALP production scan — FCC-ee @ sqrt(s) = 240 GeV\n')
    print(f'  Z channels  : 	{list(z_channels.keys())}')
    print(f'  Masses [GeV]: 	{list(alp_scan.keys())}')
    print(f'  Reference CAH:	{cah_ref}')
    print(f'  Reweight CAH: 	{list(list(alp_scan.values())[0])}')
    print(f'  Events/job  :		{nevents:,}')
    print(f'  Dry run     :		{dry_run}\n')
    
    nsubmit		= 0
    nskipped	= 0
    
    for channel, (ma, cah_list) in itertools.product(z_channels.keys(), alp_scan.items()):
    	
    	tag      = point_tag(channel, ma)
        job_dir  = condor_dir + tag + "/"
        cfg_path = job_dir + "job_submit.cfg"
 
        print(f"[{tag}]  ({len(cah_list)} reweight targets)")
        
        if skip_existing and os.path.isfile(cfg_path):
            print(f"  Already configured — skipping")
            nskipped += 1
            if not dry_run:
                os.system(f"condor_submit {cfg_path}")
                nsubmit += 1
            continue
 
        make_dir(job_dir)
 
        # paths derived from the tag for this (channel, mass) point
        mg_out_dir  = mg_dir      + tag + "/"
        lhe_path    = mg_out_dir  + "Events/run_01/unweighted_events.lhe"
        delphes_out = delphes_dir + tag + "/events.root"
        
        make_dir(delphes_dir + tag + "/")
 
        # write metadata first so the index mapping is always present
        write_metadata(job_dir, channel, ma, cah_list)
 
        # write all cards and the bash script
        mg_card     = write_mg_card(channel, ma, cah_list, job_dir, mg_out_dir)
        pythia_card = write_pythia_card(ma, job_dir, lhe_path)
        script      = write_job(job_dir, mg_card, mg_out_dir, pythia_card, delphes_out)
        cfg_path    = write_condor_config(job_dir, script)
        
        print(f"  Cards + metadata written")
    		
		if dry_run:
			print(f" [DRY RUN]: would submit {cfg_path}")
		else:
			ret	= os.system(f"condor_submit {cfg_path}")
			if ret==0:
				print(f" Submission ok!")
			else:
				print(f" [ERROR] condor_submit returned {ret}")
			nsubmit += 1
    
    print(f"\nSubmitted: {nsubmit} | Skipped: {nskipped}")
    
def run_validation(channel: str, ma: float, cah: float, dry_run: bool = True):
    """
    - Generates one dedicated validation sample at a fixed (channel, mass, cah) without re-weighting
    - Returns:
    - Args:
    channel: str, decay mode of Z boson
    ma: float, mass of ALP
    cah: float, Higgs-Alp coupling (must be in cah_list)
    dry_run: if True, write files but do not submit
    """
    tag     = validation_tag(channel, ma, cah)
    job_dir = condor_dir + tag + "/"
    
    print(" Validation job:")
    print(f" Channel: {channel} (Z -> {z_channels[channel]})")
    print(f" Mass: {ma} GeV")
    print(f" CAH: {cah}")
    print(f" Tag: {tag}")
    print(f" Dry run: {dry_run}\n")
 
    make_dir(job_dir)
    make_dir(mg_dir)
    make_dir(delphes_dir + tag + '/')
 
    mg_out_dir  = mg_dir      + tag + "/"
    lhe_path    = mg_out_dir  + "Events/run_01/unweighted_events.lhe"
    delphes_out = delphes_dir + tag + "/events.root"
 
    mg_card     = write_mg_card_validation(channel, ma, cah, job_dir, mg_out_dir)
    pythia_card = write_pythia_card(ma, job_dir, lhe_path, tag="val")
    script      = write_job_validation(job_dir, mg_card, mg_out_dir, pythia_card, delphes_out)
    cfg_path    = write_condor_config(job_dir, script)
    
    print(f" Cards written to: {job_dir}")
 
    # print index to this cah
    prod_tag	= point_tag(channel, ma)
    
    if ma in alp_scan and cah in alp_scan[ma]:
        idx		= alp_scan[ma].index(cah) + 1   # +1 because index 0 = cah_ref
        print(f" Production sample: {condor_dir}{prod_tag}/")
        print(f" Reweight index: {idx} (do_weighted({idx}) in FCCAnalysis)")
    else:
        print(f"  [NOTE] cah={cah} not in alp_scan for ma={ma} — check scan values")
    if dry_run:
        print(f"\n  [DRY RUN] Would submit: {cfg_path}")
    else:
        ret		= os.system(f"condor_submit {cfg_path}")
        if ret == 0:
            print(f"  Validation job submitted OK")
        else:
            print(f"  [ERROR] condor_submit returned {ret}")
    
if __name__ == "__main__":
	run(dry_run=True, skip_existing=True)
	for channel, ma in itertools.product(z_channels, alp_scan):
		run_validation(channel, ma, cah_val, dry_run=True)