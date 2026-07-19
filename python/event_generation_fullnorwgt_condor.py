"""
Scans over alp mass and higgs-alp couplings (cah) for the signal process

Directory structure
--------------------
base_dir/
1. generation/{tag} -> all cards (MG, Pythia, metadata)
2. HTCondor/{tag} -> only HTCondor files (run, job config, logs)
3. madgraph/{tag} -> MG output (LHE files, param_card, etc)
4. delphes/{tag} -> Delphes .root output
"""

import hashlib
import os
import itertools

### CONFIGURATION ###
alp_scan: dict[float, list[float]] = {
            0.05:	[1e-1, 1e-2, 1e-3, 1e-4, 1e-5, 1e-6],
            0.1:    [1e-1, 1e-2, 1e-3, 1e-4, 1e-5, 1e-6],
            0.5:    [1e-1, 1e-2, 1e-3, 1e-4, 1e-5, 1e-6],
            1.0:    [1e-1, 1e-2, 1e-3, 1e-4, 1e-5, 1e-6],
            1.5:    [1e-1, 1e-2, 1e-3, 1e-4, 1e-5, 1e-6],
            5.0:    [1e-1, 1e-2, 1e-3, 1e-4, 1e-5, 1e-6],
            10.0:	[1e-1, 1e-2, 1e-3, 1e-4, 1e-5, 1e-6],
            20.0:	[1e-1, 1e-2, 1e-3, 1e-4, 1e-5, 1e-6],
            30.0:	[1e-1, 1e-2, 1e-3, 1e-4, 1e-5, 1e-6],
            40.0:	[1e-1, 1e-2, 1e-3, 1e-4, 1e-5, 1e-6],
            50.0:	[1e-1, 1e-2, 1e-3, 1e-4, 1e-5, 1e-6],
            60.0:	[1e-1, 1e-2, 1e-3, 1e-4, 1e-5, 1e-6],
}

z_channels: dict[str, str]	= {
            "ee":	"e+ e-",
            "mumu": "mu+ mu-",
            "qq":	"q q~",
}

ebeam			= 120.0
memory			= 50000
ncpus			= 1
request_sec		= 28800
nevents    		= 500000
use_condor		= True
skip_mg			= True
skip_existing	= False
dry_run			= False

### PATHS ###
base_dir        = "/ceph/salshamaily/haa4K_FCCee/"
delphes_tcl		= "/ceph/sgiappic/card_IDEA.tcl"
edm4hep_cfg		= base_dir + "edm4hep_output_config.tcl" # steers EDM4HEP output
condor_dir		= base_dir + "HTCondor/" # HTCondor submission files & logs
mg_dir    		= base_dir + "madgraph_3.7.1/" # path for lhe files
delphes_dir		= base_dir + "delphes/" # delphes .root output
local_setup		= base_dir + "setup_local.sh" # local path for stack
generation_dir	= base_dir + "generation/" # cards for all samples

### FUNCTIONS ###
def make_dir(path: dir):
    """
    - Creates directory if it does not exist then chmod +x
    """
    os.makedirs(path, exist_ok=True)
    os.system(f"chmod -R +x {path}")
    
def format_cah(cah: float) -> str:
	"""
	- Converts a coupling value to string and uses scientific notation
	"""
	s	= f"{cah:.0e}"
	s	= s.replace("e-0", "em")
	s	= s.replace("e-", "em")
	
	return s
    
def point_tag(channel: str, ma: float, cah: float) -> str:
    """
    - Job label following for one (channel, mass) point
    - Returns:
    specific naming convention like the process:
    mgp8_ee_{z_channel}H_HAlpAlp_m1p5_ecm240 -> ma = 1.5
    - Args:
    channel: str, z channel
    ma: float, alp mass
    cah: float, cah value
    """
    m	= f"{ma}".replace(".", "p")
    c	= format_cah(cah)
    return f"mgp8_ee_{channel}H_HAlpAlp_m{m}_cah{c}_ecm240"

def write_mg_card(channel: str, ma: float, cah: float, gen_dir: str, mg_out_dir: str) -> str:
    """
    - Writes and modifies MadGraph card according to (channel, mass) point
    - Returns:
    path of modified MG card
    - Args:
    channel: Z channel (e, mu, or jets)
    ma, cah: floats, mass and coupling points of alp
    gen_dir: directory where the card should be
    mg_out_dir: directory where madgraph is
    """
    fs		= z_channels[channel]
    
    content	=	'# import ALP model and define particles\n'
    content +=	f'import model ALP\n\n'
    content +=	'define p = g u c d s u~ c~ d~ s~\n'
    content +=	'define j = g u c d s u~ c~ d~ s~\n'
    content +=	'define l+ = e+ mu+\n'
    content +=	'define l- = e- mu-\n'
    content +=	'define q = u d s c b\n'
    content +=	'define q~ = u~ d~ s~ c~ b~\n'
    content +=	'define vl = ve vm vt\n'
    content +=	'define vl~ = ve~ vm~ vt~\n\n'
    content +=	f'generate e+ e- > z h, z > {fs}, h > ALP ALP\n\n'
    content +=	f'output {mg_out_dir}\n'
    content +=	f'launch {mg_out_dir}\n\n'
    content	+=	'# Collision parameters\n'
    content	+=	f'set ebeam1 {ebeam}   # beam 1 energy [GeV]\n'
    content	+=	f'set ebeam2 {ebeam}   # beam 2 energy [GeV]\n'
    content +=	'set no_parton_cut\n\n'
    content +=	'# ALP model parameters\n'
    content +=	f'set malp {ma}		# ALP mass [GeV]\n'
    content +=	f'set CAH  {cah}	# Higgs-ALP coupling [GeV^-1]\n'
    content +=	f'set czh5 0\n'
    content	+=	f'set param_card DECAY 9000005 Auto\n\n'
    content +=	f'set nevents {nevents}\n'
    content +=	'done\n\n'
    
    m		= f"{ma}".replace(".", "p")
    c		= format_cah(cah)
    path	= gen_dir + f"mg_param_m{m}_cah{c}.txt"
    
    with open(path, "w") as f:
        f.write(content)
    
    return path
    
def write_pythia_card(ma: float, cah: float, gen_dir: str, lhe_path: str) -> str:
    """
    - Writes and modifies the pythia card according to the mass point used
    - Returns:
    path of modified pythia8 card
    - Args:
    ma: float, alp mass
    cah: float, alp-higgs coupling
    gen_dir: str, directory of where the card should be
    lhe_path: str, path of LHE file for pythia to read
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
    content	+=	f'9000005:all = ALP ALP 0 0 0 {ma} __ALP_WIDTH__ 0.05 75.0 0\n'
    content	+=	'9000005:oneChannel = 1 1.000 101 321 -321\n'
    content	+=	'9000005:mayDecay = on\n'
    content	+=	'9000005:isResonance = on\n'
    content	+=	'9000005:onMode = off      ! turn off all channels first\n'
    content	+=	'9000005:onIfAny = 321     ! then re-enable channels with K+\n'
    content	+=	'\n'
    content	+=	'LesHouches:setLifetime = 2'
    
    m		= f"{ma}".replace(".", "p")
    c		= format_cah(cah)
    path    = gen_dir + f"pythia_mg_m{m}_cah{c}.cmd"
    
    with open(path, "w") as fh:
        fh.write(content)
        
    return path
        
def write_job(condor_job_dir: str, mg_card: str, mg_out_dir: str, pythia_card: str, delphes_out: str, skip_mg: bool=False) -> str:
    """
    - Writes bash script for HTCondor execution and follows: MG->P8->Delphes
    - Returns:
    path of bash script
    - Args:
    condor_job_dir: str, directory of job submitted
    mg_card, mg_out_dir: str, MG card and directory paths
    pythia_card, pythia_dir: str, pythia card and directory paths
    delphes_out_dir: str, path of the output from delphes 
    """
    lhe_path		= mg_out_dir        + "Events/run_01/unweighted_events.lhe"
    lhe_gz_path		= lhe_path			+ ".gz"
    param_card_path	= mg_out_dir        + "Cards/param_card.dat"
    script_path		= condor_job_dir    + "run_production.sh"
    
    scr	=	'#!/bin/bash\n\n'
    scr	+=	'set -e\nset -o pipefail\n\n'
    scr	+=	f'source {local_setup}\n\n'
    scr +=  f'cd {base_dir}\n\n'
    
    if not skip_mg:
    	scr += 'export MAKEFLAGS="-j1"\n\n'        # forces serial Fortran compilation
    	scr +=  f'{mg_dir}bin/mg5_aMC {mg_card}\n\n'
    	scr +=  f'mv {base_dir}MG5_debug {mg_out_dir} 2>/dev/null || true\n\n'
    	
    scr +=  f'PARAM_CARD="{param_card_path}"\n'
    scr +=  f'PYTHIA_CARD="{pythia_card}"\n'
    scr +=  'ALP_WIDTH=$(grep -i "^DECAY[[:space:]]*9000005" "$PARAM_CARD" | awk \'{print $3}\')\n'
    scr +=  'if [ -z "$ALP_WIDTH" ]; then\n'
    scr +=  '    echo "[ERROR] Could not find ALP width in $PARAM_CARD" >&2\n'
    scr +=  '    exit 1\n'
    scr +=  'fi\n'
    scr +=  'echo "  ALP width from MadGraph: $ALP_WIDTH GeV"\n'
    scr +=  'sed -i "s/__ALP_WIDTH__/${ALP_WIDTH}/" "$PYTHIA_CARD"\n\n'
    scr +=  f'LHE="{lhe_path}"\n'
    scr +=  f'LHE_GZ="{lhe_gz_path}"\n'
    scr +=  'if [ -f "$LHE_GZ" ] && [ ! -f "$LHE" ]; then\n'
    scr +=  '    echo "  Decompressing LHE file..."\n'
    scr +=  '    gunzip "$LHE_GZ"\n'
    scr +=	'fi\n'
    scr +=  'if [ ! -f "$LHE" ]; then\n'
    scr +=  '    echo "[ERROR] LHE file not found after MadGraph — did MG compilation fail?" >&2\n'
    scr +=  '    exit 1\n'
    scr +=  'fi\n\n'
    scr +=  f'DelphesPythia8_EDM4HEP {delphes_tcl} {edm4hep_cfg} "$PYTHIA_CARD" {delphes_out}\n\n'
    scr	+=	'echo "Production complete"\n'
    
    with open(script_path, "w") as fh:
        fh.write(scr)
    os.system(f"chmod +x {script_path}")
    
    return script_path
    
def write_condor_config(condor_job_dir: str, script_path: str) -> str:
    """
    - Writes the condor .sub file matching existing submission format with one job
    per (channel, mass, cah) point
    - Returns:
    cfg_path: path of configuration
    - Args:
    condor_job_dir: str, directory of job submitted
    script_path: str, directory of bash script
    """
    cfg    =	'Universe        			= vanilla\n'
    cfg    +=	'accounting_group			= cms.higgs\n'
    cfg    +=	f'executable     			= {script_path}\n'
    cfg    +=	f'log						= {condor_job_dir}condor.log\n'
    cfg    +=	f'output					= {condor_job_dir}condor.out\n'
    cfg    +=	f'error						= {condor_job_dir}condor.err\n'
    cfg    +=	'max_retries      			= 3\n'
    cfg    +=	f'+RequestWalltime			= "{request_sec}"\n'
    cfg    +=	f'request_memory  			= {memory} MB\n'
    cfg    +=	f'request_cpus				= {ncpus}\n'
    cfg    +=	'requirements				= (TARGET.ProvidesCPU && TARGET.ProvidesEKPResources)\n'
    cfg    +=	'should_transfer_files		= IF_NEEDED\n'
    cfg    +=	'when_to_transfer_output	= ON_EXIT\n'
    cfg    +=	'queue 1\n'
    
    cfg_path = condor_job_dir + "job_submit.cfg"
    
    with open(cfg_path, "w") as fh:
        fh.write(cfg)
    
    return cfg_path
    
def is_job_active(script_path: str) -> bool:
	"""
	- Checks HTCondor queue for a job whose executable matches script_path
	- Returns:
	boolean value if True/False
	- Args:
	script_path: str, path of the script
	"""
	result = os.popen(
		f'condor_q -constraint \'Cmd == "{script_path}"\' -format "%d\\n" ClusterId'
	).read()
	
	return bool(result.strip())

### RUN ###
def run(dry_run: bool=True, skip_existing: bool=True, use_condor: bool=True, skip_mg=False) -> None:
    """
    - Loops over all (channel, mass) combinations, writes cards and scripts
    and optionally submits to HTCondor
    - Returns:
    submitted jobs (optional)
    - Args:
    dry_run: bool, if True then generate all files but do not call condor_submit
    skip_existing: bool, if True then skip points whose job_submit.cfg already exists (useful for resubmitting only failed jobs)
    use_condor: bool, if True then submits jobs to HTCondor
    """
    make_dir(generation_dir)
    make_dir(condor_dir)
    make_dir(mg_dir)
    make_dir(delphes_dir)
    
    scan_points	= [(ma, cah) for ma, cah_list in alp_scan.items()
    			for cah in cah_list]
    
    ntotal		= len(z_channels) * len(scan_points)

    print('ALP production scan — FCC-ee @ sqrt(s) = 240 GeV\n')
    print(f'Z channels:		{list(z_channels.keys())}')
    print(f'Masses [GeV]:	{list(alp_scan.keys())}')
    print(f'CAH values:		{list(list(alp_scan.values())[0])}')
    print(f'Events/job:		{nevents:,}')
    print(f'Total jobs:		{ntotal:,}')
    print(f'Dry run:		{dry_run}\n')
    
    nsubmit		= 0
    nskipped    = 0
    
    for channel, (ma, cah) in itertools.product(z_channels.keys(), scan_points):
        tag        		= point_tag(channel, ma, cah)
        gen_job_dir		= generation_dir + tag + "/"
        condor_job_dir  = condor_dir + tag + "/"
        cfg_path		= condor_job_dir + "job_submit.cfg"
 
        print(f"[{tag}]")
        
        if skip_existing and os.path.isfile(cfg_path):
            script_path = condor_job_dir + "run_production.sh"
            delphes_out = delphes_dir + tag + "/events.root"

            if os.path.isfile(delphes_out):
                print(f"  Already completed — skipping")
                nskipped += 1
                continue

            if is_job_active(script_path):
                print(f"  Already running/queued — skipping")
                nskipped += 1
                continue

            print(f"  Configured but not active — resubmitting")
            
            if not dry_run and use_condor:
                os.system(f"condor_submit {cfg_path}")
                nsubmit += 1
            continue
 
        make_dir(gen_job_dir)
        make_dir(condor_job_dir)
 
        # paths derived from the tag for this (channel, mass) point
        mg_out_dir  = mg_dir      + tag + "/"
        lhe_path    = mg_out_dir  + "Events/run_01/unweighted_events.lhe"
        delphes_out = delphes_dir + tag + "/events.root"
        
        make_dir(delphes_dir + tag + "/")
 
        # write all cards and the bash script
        mg_card     = write_mg_card(channel, ma, cah, gen_job_dir, mg_out_dir)
        pythia_card = write_pythia_card(ma, cah, gen_job_dir, lhe_path)
        script      = write_job(condor_job_dir, mg_card, mg_out_dir, pythia_card, delphes_out, skip_mg=skip_mg)
        cfg_path    = write_condor_config(condor_job_dir, script)
        
        print(f"	Written: cards -> {gen_job_dir}")
        print(f"	Written: jobs -> {condor_job_dir}")
        
        if dry_run:
        	mode   = "condor_submit" if use_condor else "local"
        	target = cfg_path if use_condor else script
        	print(f"  [DRY RUN] Would run via {mode}: {target}")
        elif use_condor:
        	ret    = os.system(f"condor_submit {cfg_path}")
        	status = "ok" if ret == 0 else f"[ERROR] returned {ret}"
        	print(f"  Submitted: {status}")
        	nsubmit += 1
        else:
        	print(f"  Running locally: {script}")
        	ret    = os.system(f"bash {script}")
        	status = "complete" if ret == 0 else f"[ERROR] returned {ret}"
        	print(f"  Local run: {status}")
        	nsubmit += 1
        	
        print(f"\nSubmitted: {nsubmit} | Skipped: {nskipped} | Total configured: {ntotal:,}")
    
if __name__ == "__main__":
	run(dry_run=dry_run, skip_existing=skip_existing, use_condor=use_condor, skip_mg=skip_mg)