import os
import itertools
 
### CONFIGURATION ###
cah_ref     = 1.0
cah_val     = 0.1
alp_scan    = {
    0.05:   [1e-1, 1e-2, 1e-3, 1e-4, 1e-5, 1e-6],
    0.1:    [1e-1, 1e-2, 1e-3, 1e-4, 1e-5, 1e-6],
    0.5:    [1e-1, 1e-2, 1e-3, 1e-4, 1e-5, 1e-6],
    1.0:    [1e-1, 1e-2, 1e-3, 1e-4, 1e-5, 1e-6],
    1.5:    [1e-1, 1e-2, 1e-3, 1e-4, 1e-5, 1e-6],
    5.0:    [1e-1, 1e-2, 1e-3, 1e-4, 1e-5, 1e-6],
    10.0:   [1e-1, 1e-2, 1e-3, 1e-4, 1e-5, 1e-6],
    20.0:   [1e-1, 1e-2, 1e-3, 1e-4, 1e-5, 1e-6],
    30.0:   [1e-1, 1e-2, 1e-3, 1e-4, 1e-5, 1e-6],
    40.0:   [1e-1, 1e-2, 1e-3, 1e-4, 1e-5, 1e-6],
    50.0:   [1e-1, 1e-2, 1e-3, 1e-4, 1e-5, 1e-6],
    60.0:   [1e-1, 1e-2, 1e-3, 1e-4, 1e-5, 1e-6],
}
 
z_channels  = {
    "ee":   "e+ e-",
    "mumu": "mu+ mu-",
    "qq":   "q q~",
}
 
ebeam       = 120.0
memory      = 20000
ncpus       = 1
request_sec = 3600
nevents     = 500000
use_condor  = False
 
### PATHS ###
base_dir        = "/ceph/salshamaily/haa4K_FCCee/"
delphes_tcl     = "/ceph/sgiappic/card_IDEA.tcl"
edm4hep_cfg     = base_dir + "edm4hep_output_config.tcl"
condor_dir      = base_dir + "HTCondor/"                   
lhe_dir         = base_dir + "madgraph_3.7.1/"             
delphes_dir     = base_dir + "delphes/"                    
local_setup     = base_dir + "setup_local.sh"
generation_dir  = base_dir + "generation/"                 
 
### FUNCTIONS ###
def make_dir(path: str):
    os.makedirs(path, exist_ok=True)
    os.system(f"chmod -R +x {path}")
 
def point_tag(channel: str, ma: float) -> str:
    m = f"{ma}".replace(".", "p")
    return f"mgp8_ee_{channel}H_HAlpAlp_m{m}_ecm240"
 
def validation_tag(channel: str, ma: float, cah: float) -> str:
    m = f"{ma}".replace(".", "p")
    c = f"{cah}".replace(".", "p")
    return f"mgp8_ee_{channel}H_HAlpAlp_m{m}_cah{c}_ecm240"
 
def write_metadata(gen_dir: str, channel: str, ma: float, cah_list: list):
    lines  = "# ALP production metadata\n"
    lines += f"# channel          : {channel}\n"
    lines += f"# mass [GeV]       : {ma}\n"
    lines += f"# cah_ref          : {cah_ref}  <- events generated at this coupling\n"
    lines += f"# nevents          : {nevents:,}\n"
    lines += f"# sqrt(s) [GeV]    : {2 * ebeam:.0f}\n"
    lines += "#\n"
    lines += "# Weight column index -> cah value\n"
    lines += "# Use this when calling do_weighted(index) in FCCAnalysis\n"
    lines += "# Index 0 = nominal weight at cah_ref\n"
    lines += "# Indices 1..N = reweighted to the cah values listed below\n"
    lines += "#\n"
    lines += f"#   index 0  :  {cah_ref}  (nominal / cah_ref)\n"
    for i, cah_value in enumerate(cah_list):
        lines += f"#   index {i+1}  :  {cah_value}\n"
 
    with open(gen_dir + "metadata.txt", "w") as fh:
        fh.write(lines)
 
def write_pythia_card(ma: float, gen_dir: str, lhe_path: str, tag: str = "") -> str:
    content  = "Random:setSeed = on\n"
    content += "Main:timesAllowErrors = 10\n"
    content += f"Main:numberOfEvents = {nevents}\n"
    content += "\n"
    content += "Next:numberCount = 10000\n"
    content += "\n"
    content += "Beams:frameType = 4\n"
    content += f"Beams:LHEF = {lhe_path}\n"
    content += "\n"
    content += "Beams:allowMomentumSpread  = off\n"
    content += "\n"
    content += "Beams:allowVertexSpread = on\n"
    content += "Beams:sigmaVertexX = 5.96E-3\n"
    content += "Beams:sigmaVertexY = 23.8E-6\n"
    content += "Beams:sigmaVertexZ = 0.397\n"
    content += "Beams:sigmaTime = 10.89    !  36.3 ps\n"
    content += "\n"
    content += "PartonLevel:ISR = on\n"
    content += "PartonLevel:FSR = on\n"
    content += "\n"
    content += "! decay of ALP\n"
    content += f"9000005:all = ALP ALP 0 0 0 {ma} __ALP_WIDTH__ 0.05 75.0 0\n"
    content += "9000005:oneChannel = 1 1.000 101 321 -321\n"
    content += "9000005:mayDecay = on\n"
    content += "9000005:isResonance = on\n"
    content += "9000005:onMode = off      ! turn off all channels first\n"
    content += "9000005:onIfAny = 321     ! then re-enable channels with K+\n"
    content += "\n"
    content += "LesHouches:setLifetime = 2"
 
    m      = f"{ma}".replace(".", "p")
    suffix = f"_{tag}" if tag else ""
    path   = gen_dir + f"pythia_mg_m{m}{suffix}.cmd"
 
    with open(path, "w") as fh:
        fh.write(content)
 
    return path
 
def write_job(condor_job_dir: str, lhe_base_dir: str, pythia_card: str, delphes_out: str) -> str:
    lhe_path        = lhe_base_dir + "Events/run_01/unweighted_events.lhe"
    lhe_gz_path     = lhe_path + ".gz"
    param_card_path = lhe_base_dir + "Cards/param_card.dat"
    script_path     = condor_job_dir + "run_production.sh"
 
    scr  = "#!/bin/bash\n\n"
    scr += "set -e\nset -o pipefail\n\n"
    scr += f"source {local_setup}\n\n"
    scr += f"cd {base_dir}\n\n"
    scr += f'PARAM_CARD="{param_card_path}"\n'
    scr += f'PYTHIA_CARD="{pythia_card}"\n'
    scr += 'ALP_WIDTH=$(grep -i "^DECAY[[:space:]]*9000005" "$PARAM_CARD" | awk \'{print $3}\')\n'
    scr += 'if [ -z "$ALP_WIDTH" ]; then\n'
    scr += '    echo "[ERROR] Could not find ALP width in $PARAM_CARD" >&2\n'
    scr += '    exit 1\n'
    scr += 'fi\n'
    scr += 'echo "  ALP width from param_card: $ALP_WIDTH GeV"\n'
    scr += 'sed -i "s/__ALP_WIDTH__/${ALP_WIDTH}/" "$PYTHIA_CARD"\n\n'
    scr += f'LHE="{lhe_path}"\n'
    scr += f'LHE_GZ="{lhe_gz_path}"\n'
    scr += 'if [ -f "$LHE_GZ" ] && [ ! -f "$LHE" ]; then\n'
    scr += '    echo "  Decompressing LHE file..."\n'
    scr += '    gunzip "$LHE_GZ"\n'
    scr += 'fi\n'
    scr += 'if [ ! -f "$LHE" ]; then\n'
    scr += '    echo "[ERROR] LHE file not found: $LHE" >&2\n'
    scr += '    exit 1\n'
    scr += 'fi\n\n'
    scr += f'DelphesPythia8_EDM4HEP {delphes_tcl} {edm4hep_cfg} "$PYTHIA_CARD" {delphes_out}\n\n'
    scr += 'echo "Production complete"\n'
 
    with open(script_path, "w") as fh:
        fh.write(scr)
    os.system(f"chmod +x {script_path}")
 
    return script_path
 
def write_job_validation(condor_job_dir: str, lhe_base_dir: str, pythia_card: str, delphes_out: str) -> str:
    lhe_path        = lhe_base_dir + "Events/run_01/unweighted_events.lhe"
    lhe_gz_path     = lhe_path + ".gz"
    param_card_path = lhe_base_dir + "Cards/param_card.dat"
    script_path     = condor_job_dir + "run_validation.sh"
 
    scr  = "#!/bin/bash\n"
    scr += "set -e\nset -o pipefail\n\n"
    scr += f"source {local_setup}\n\n"
    scr += f"cd {base_dir}\n\n"
    scr += f'PARAM_CARD="{param_card_path}"\n'
    scr += f'PYTHIA_CARD="{pythia_card}"\n'
    scr += 'ALP_WIDTH=$(grep -i "^DECAY[[:space:]]*9000005" "$PARAM_CARD" | awk \'{print $3}\')\n'
    scr += 'if [ -z "$ALP_WIDTH" ]; then\n'
    scr += '    echo "[ERROR] Could not find ALP width in $PARAM_CARD" >&2\n'
    scr += '    exit 1\n'
    scr += 'fi\n'
    scr += 'echo "  ALP width: $ALP_WIDTH GeV"\n'
    scr += 'sed -i "s/__ALP_WIDTH__/${ALP_WIDTH}/" "$PYTHIA_CARD"\n\n'
    scr += f'LHE="{lhe_path}"\n'
    scr += f'LHE_GZ="{lhe_gz_path}"\n'
    scr += 'if [ -f "$LHE_GZ" ] && [ ! -f "$LHE" ]; then\n'
    scr += '    gunzip "$LHE_GZ"\n'
    scr += 'fi\n'
    scr += 'if [ ! -f "$LHE" ]; then\n'
    scr += '    echo "[ERROR] LHE file not found: $LHE" >&2\n'
    scr += '    exit 1\n'
    scr += 'fi\n\n'
    scr += f'DelphesPythia8_EDM4HEP {delphes_tcl} {edm4hep_cfg} "$PYTHIA_CARD" {delphes_out}'
 
    with open(script_path, "w") as fh:
        fh.write(scr)
    os.system(f"chmod +x {script_path}")
 
    return script_path
 
 
def write_condor_config(condor_job_dir: str, script_path: str) -> str:
    cfg  = "Universe        			= vanilla\n"
    cfg += "accounting_group			= cms.higgs\n"
    cfg += f"executable					= {script_path}\n"
    cfg += f"log       					= {condor_job_dir}condor.log\n"
    cfg += f"output    					= {condor_job_dir}condor.out\n"
    cfg += f"error     					= {condor_job_dir}condor.err\n"
    cfg += "max_retries					= 3\n"
    cfg += f'+RequestWalltime			= "{request_sec}"\n'
    cfg += f"request_memory  			= {memory} MB\n"
    cfg += f"request_cpus    			= {ncpus}\n"
    cfg += "requirements                = (TARGET.ProvidesCPU && TARGET.ProvidesEKPResources)\n"
    cfg += "should_transfer_files       = IF_NEEDED\n"
    cfg += "when_to_transfer_output     = ON_EXIT\n"
    cfg += "queue 1\n"
 
    cfg_path = condor_job_dir + "job_submit.cfg"
    with open(cfg_path, "w") as fh:
        fh.write(cfg)
 
    return cfg_path
 
 
def run(dry_run: bool = True, skip_existing: bool = True, use_condor: bool = True):
    make_dir(generation_dir)
    make_dir(condor_dir)
    make_dir(delphes_dir)
 
    print("  ALP Pythia8+Delphes scan — FCC-ee @ sqrt(s) = 240 GeV\n")
    print(f"  Z channels  : {list(z_channels.keys())}")
    print(f"  Masses [GeV]: {list(alp_scan.keys())}")
    print(f"  Reference CAH: {cah_ref}")
    print(f"  Events/job  : {nevents:,}")
    print(f"  Dry run     : {dry_run}\n")
 
    nsubmit  = 0
    nskipped = 0
 
    for channel, (ma, cah_list) in itertools.product(z_channels.keys(), alp_scan.items()):
        tag            = point_tag(channel, ma)
        gen_job_dir    = generation_dir + tag + "/"
        condor_job_dir = condor_dir + tag + "/"
        cfg_path       = condor_job_dir + "job_submit.cfg"
 
        print(f"[{tag}]  ({len(cah_list)} reweight targets)")
 
        if skip_existing and os.path.isfile(cfg_path):
            print("  Already configured — skipping")
            nskipped += 1
            if not dry_run:
                os.system(f"condor_submit {cfg_path}")
                nsubmit += 1
            continue
 
        make_dir(gen_job_dir)
        make_dir(condor_job_dir)
 
        lhe_base_dir = lhe_dir + tag + "/"
        lhe_path     = lhe_base_dir + "Events/run_01/unweighted_events.lhe"
        delphes_out  = delphes_dir + tag + "/events.root"
 
        make_dir(delphes_dir + tag + "/")
 
        write_metadata(gen_job_dir, channel, ma, cah_list)
        pythia_card = write_pythia_card(ma, gen_job_dir, lhe_path)
        script      = write_job(condor_job_dir, lhe_base_dir, pythia_card, delphes_out)
        cfg_path    = write_condor_config(condor_job_dir, script)
 
        print(f"  Written: cards -> {gen_job_dir}")
        print(f"  Written: jobs  -> {condor_job_dir}")
 
        if dry_run:
            mode = "condor_submit" if use_condor else "local"
            print(f"  [DRY RUN] Would run via {mode}: {cfg_path if use_condor else script}")
        elif use_condor:
            ret = os.system(f"condor_submit {cfg_path}")
            print(f"  Submitted OK!" if ret == 0 else f"  [ERROR] condor_submit returned {ret}")
            nsubmit += 1
        else:
            print(f"  Running locally: {script}")
            ret = os.system(f"bash {script}")
            print(f"  Local run complete!" if ret == 0 else f"  [ERROR] local run returned {ret}")
            nsubmit += 1
 
    print(f"\nSubmitted: {nsubmit} | Skipped: {nskipped}")
 
 
def run_validation(channel: str, ma: float, cah: float, dry_run: bool = True, use_condor: bool = True):
    tag            = validation_tag(channel, ma, cah)
    gen_job_dir    = generation_dir + tag + "/"
    condor_job_dir = condor_dir + tag + "/"
 
    print("  Validation job:")
    print(f"  Channel : {channel} (Z -> {z_channels[channel]})")
    print(f"  Mass    : {ma} GeV")
    print(f"  CAH     : {cah}")
    print(f"  Tag     : {tag}")
    print(f"  Dry run : {dry_run}\n")
 
    make_dir(gen_job_dir)
    make_dir(condor_job_dir)
    make_dir(delphes_dir + tag + "/")
 
    lhe_base_dir = lhe_dir + tag + "/"
    lhe_path     = lhe_base_dir + "Events/run_01/unweighted_events.lhe"
    delphes_out  = delphes_dir + tag + "/events.root"
 
    pythia_card = write_pythia_card(ma, gen_job_dir, lhe_path, tag="val")
    script      = write_job_validation(condor_job_dir, lhe_base_dir, pythia_card, delphes_out)
    cfg_path    = write_condor_config(condor_job_dir, script)
 
    print(f"[{tag}]")
    print(f"  Cards written to: {gen_job_dir}")
 
    if ma in alp_scan and cah in alp_scan[ma]:
        prod_tag = point_tag(channel, ma)
        idx      = alp_scan[ma].index(cah) + 1   # +1 because index 0 = cah_ref
        print(f"  Production sample : {condor_dir}{prod_tag}/")
        print(f"  Reweight index    : {idx}  (do_weighted({idx}) in FCCAnalysis)")
    else:
        print(f"  [NOTE] cah={cah} not in alp_scan for ma={ma} — check scan values")
 
    if dry_run:
        mode = "condor_submit" if use_condor else "local"
        print(f"\n  [DRY RUN] Would run via {mode}: {cfg_path if use_condor else script}")
    elif use_condor:
        ret = os.system(f"condor_submit {cfg_path}")
        print(f"  Validation job submitted OK!" if ret == 0 else f"  [ERROR] condor_submit returned {ret}")
    else:
        print(f"  Running locally: {script}")
        ret = os.system(f"bash {script}")
        print(f"  Validation complete!" if ret == 0 else f"  [ERROR] local execution returned {ret}")
 
 
if __name__ == "__main__":
    run(dry_run=False, skip_existing=False, use_condor=use_condor)
 
    for channel, (ma, cah_list) in itertools.product(z_channels.keys(), alp_scan.items()):
        if cah_val not in cah_list:
            continue
        run_validation(channel, ma, cah_val, dry_run=False, use_condor=use_condor)