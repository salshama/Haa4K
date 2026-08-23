#!/usr/bin/env python3

import os
import subprocess
from typing import List, Tuple

### CONFIGURATION ###
base_dir        = "/ceph/salshamaily/haa4K_FCCee/"
mg_dir          = base_dir		+ "madgraph_3.7.1/"		# where the already-generated LHE files live
generation_dir  = base_dir		+ "generation/"			# where cards (incl. the new pythia card) get written
delphes_dir     = base_dir		+ "delphes/"
local_setup     = base_dir		+ "setup_local.sh"
delphes_tcl     = delphes_dir	+ "card_IDEA.tcl"
edm4hep_cfg     = delphes_dir	+ "edm4hep_output_config.tcl"

nevents = 500000

# hbar*c in GeV*mm (CODATA: 1.973269804e-16 GeV*m), used purely as the
# conversion factor mm -> GeV^-1 so everything is computed in natural
# units (hbar = c = 1).
HBAR_C_GEV_MM = 1.973269804e-13

z_channels = {
    "ee":   "e+ e-",
    "mumu": "mu+ mu-",
}

# List of (channel, ma, cah, ctau_mm) points for already-generated MG
# samples you want to rerun Pythia -> Delphes on. You choose ctau_mm
# yourself -- the width is derived from it. tmux session names are
# generated automatically from the point tag, no manual naming needed.
samples: List[Tuple[str, float, float, float]] = [
    ("ee",	0.05,	1,	1.0),
    ("ee",	0.05,	1,	10.0),
    ("ee",	0.05,	1,	1000.0),
    ("ee",	0.05,	1,	2000.0),
    ("ee",	0.1,	1,	1.0),
    ("ee",	0.1,	1,	10.0),
    ("ee",	0.1,	1,	1000.0),
    ("ee",	0.1,	1,	2000.0),
    ("ee",	0.5,	1,	1.0),
    ("ee",	0.5,	1,	10.0),
    ("ee",	0.5,	1,	1000.0),
    ("ee",	0.5,	1,	2000.0),
    ("ee",	1.0,	1,	1.0),
    ("ee",	1.0,	1,	10.0),
    ("ee",	1.0,	1,	1000.0),
    ("ee",	1.0,	1,	2000.0),
    ("ee",	1.5,	1,	1.0),
    ("ee",	1.5,	1,	10.0),
    ("ee",	1.5,	1,	1000.0),
    ("ee",	1.5,	1,	2000.0),
    ("ee",	5.0,	1,	1.0),
    ("ee",	5.0,	1,	10.0),
    ("ee",	5.0,	1,	1000.0),
    ("ee",	5.0,	1,	2000.0),
    ("ee",	10.0,	1,	1.0),
    ("ee",	10.0,	1,	10.0),
    ("ee",	10.0,	1,	1000.0),
    ("ee",	10.0,	1,	2000.0),
    ("ee",	20.0,	1,	1.0),
    ("ee",	20.0,	1,	10.0),
    ("ee",	20.0,	1,	1000.0),
    ("ee",	20.0,	1,	2000.0),
    ("ee",	30.0,	1,	1.0),
    ("ee",	30.0,	1,	10.0),
    ("ee",	30.0,	1,	1000.0),
    ("ee",	30.0,	1,	2000.0),
    ("ee",	40.0,	1,	1.0),
    ("ee",	40.0,	1,	10.0),
    ("ee",	40.0,	1,	1000.0),
    ("ee",	40.0,	1,	2000.0),
    ("ee",	50.0,	1,	1.0),
    ("ee",	50.0,	1,	10.0),
    ("ee",	50.0,	1,	1000.0),
    ("ee",	50.0,	1,	2000.0),
    ("ee",	60.0,	1,	1.0),
    ("ee",	60.0,	1,	10.0),
    ("ee",	60.0,	1,	1000.0),
    ("ee",	60.0,	1,	2000.0),
    
	("mumu",	0.05,	1,	1.0),
    ("mumu",	0.05,	1,	10.0),
    ("mumu",	0.05,	1,	1000.0),
    ("mumu",	0.05,	1,	2000.0),
    ("mumu",	0.1,	1,	1.0),
    ("mumu",	0.1,	1,	10.0),
    ("mumu",	0.1,	1,	1000.0),
    ("mumu",	0.1,	1,	2000.0),
    ("mumu",	0.5,	1,	1.0),
    ("mumu",	0.5,	1,	10.0),
    ("mumu",	0.5,	1,	1000.0),
    ("mumu",	0.5,	1,	2000.0),
    ("mumu",	1.0,	1,	1.0),
    ("mumu",	1.0,	1,	10.0),
    ("mumu",	1.0,	1,	1000.0),
    ("mumu",	1.0,	1,	2000.0),
    ("mumu",	1.5,	1,	1.0),
    ("mumu",	1.5,	1,	10.0),
    ("mumu",	1.5,	1,	1000.0),
    ("mumu",	1.5,	1,	2000.0),
    ("mumu",	5.0,	1,	1.0),
    ("mumu",	5.0,	1,	10.0),
    ("mumu",	5.0,	1,	1000.0),
    ("mumu",	5.0,	1,	2000.0),
    ("mumu",	10.0,	1,	1.0),
    ("mumu",	10.0,	1,	10.0),
    ("mumu",	10.0,	1,	1000.0),
    ("mumu",	10.0,	1,	2000.0),
    ("mumu",	20.0,	1,	1.0),
    ("mumu",	20.0,	1,	10.0),
    ("mumu",	20.0,	1,	1000.0),
    ("mumu",	20.0,	1,	2000.0),
    ("mumu",	30.0,	1,	1.0),
    ("mumu",	30.0,	1,	10.0),
    ("mumu",	30.0,	1,	1000.0),
    ("mumu",	30.0,	1,	2000.0),
    ("mumu",	40.0,	1,	1.0),
    ("mumu",	40.0,	1,	10.0),
    ("mumu",	40.0,	1,	1000.0),
    ("mumu",	40.0,	1,	2000.0),
    ("mumu",	50.0,	1,	1.0),
    ("mumu",	50.0,	1,	10.0),
    ("mumu",	50.0,	1,	1000.0),
    ("mumu",	50.0,	1,	2000.0),
    ("mumu",	60.0,	1,	1.0),
    ("mumu",	60.0,	1,	10.0),
    ("mumu",	60.0,	1,	1000.0),
    ("mumu",	60.0,	1,	2000.0),
]

def format_ctau(ctau_mm: float) -> str:
    if ctau_mm >= 1000.0 and (ctau_mm % 1000.0 == 0):
        return f"{int(ctau_mm // 1000)}m"
    if ctau_mm == int(ctau_mm):
        return f"{int(ctau_mm)}mm"
    return f"{ctau_mm}".replace(".", "p") + "mm"

def alp_width_from_ctau(ctau_mm: float) -> float:
    """Gamma = 1 / ctau, with ctau converted from mm to natural units (GeV^-1)."""
    ctau_natural = ctau_mm / HBAR_C_GEV_MM   # GeV^-1
    return 1.0 / ctau_natural

def format_cah(cah: float) -> str:
    s = f"{cah:.0e}"
    s = s.replace("e-0", "em")
    s = s.replace("e-", "em")
    s = s.replace("e+0", "e")
    s = s.replace("e+", "e")
    return s

def mg_tag(channel: str, ma: float, cah: float) -> str:
    m = f"{ma}".replace(".", "p")
    if cah == 1.0:
        return f"mgp8_ee_{channel}H_HAlpAlp_m{m}_ecm240"
    c = format_cah(cah)
    return f"mgp8_ee_{channel}H_HAlpAlp_m{m}_cah{c}_ecm240"

def point_tag(channel: str, ma: float, cah: float, ctau_mm: float) -> str:
    return f"{mg_tag(channel, ma, cah)}_ctau{format_ctau(ctau_mm)}"

def write_pythia_card(ma: float, ctau_mm: float, gen_dir: str, lhe_path: str) -> str:
    width = alp_width_from_ctau(ctau_mm)

    content  =  'Random:setSeed = on\n'
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
    content += f'9000005:all = ALP void 0 0 0 {ma} {width:.6e} 0.1 60.0 0\n'
    content += '9000005:oneChannel = 1 1.000 0 321 -321\n'
    content += '9000005:mayDecay = on\n'
    content += '9000005:isResonance = off\n'
    content += '9000005:onMode = off      ! turn off all channels first\n'
    content += '9000005:onIfAny = 321     ! then re-enable channels with K+\n'
    content += '\n'
    content += 'LesHouches:setLifetime = 2'

    m     = f"{ma}".replace(".", "p")
    c_lab = format_ctau(ctau_mm)
    path  = gen_dir + f"pythia_mg_m{m}_ctau{c_lab}.cmd"

    with open(path, "w") as fh:
        fh.write(content)

    return path

def build_command(pythia_card: str, lhe_path: str, delphes_out: str) -> str:
    cmd  = f'source {local_setup}\n'
    cmd += f'cd {base_dir}\n'
    cmd += f'if [ -f "{lhe_path}.gz" ] && [ ! -f "{lhe_path}" ]; then\n'
    cmd += '    echo "  Decompressing LHE file..."\n'
    cmd += f'    gunzip -k "{lhe_path}.gz"\n'
    cmd += 'fi\n'
    cmd += f'if [ ! -f "{lhe_path}" ]; then\n'
    cmd += f'    echo "[ERROR] LHE file not found: {lhe_path}" >&2\n'
    cmd += '    exec bash\n'
    cmd += 'fi\n'
    cmd += f'DelphesPythia8_EDM4HEP {delphes_tcl} {edm4hep_cfg} "{pythia_card}" {delphes_out}\n'
    cmd += 'echo "=== Done (exit code $?) ==="\n'
    cmd += 'exec bash\n'
    return cmd

def main() -> None:
    for channel, ma, cah, ctau_mm in samples:
        mgtag   = mg_tag(channel, ma, cah)
        tag     = point_tag(channel, ma, cah, ctau_mm)
        session = tag   # tmux session name auto-derived from the point tag

        gen_dir         = generation_dir + mgtag + "/"
        mg_out_dir      = mg_dir + mgtag + "/"
        lhe_path        = mg_out_dir + "Events/run_01/unweighted_events.lhe"
        delphes_out_dir = delphes_dir + tag + "/"
        delphes_out     = delphes_out_dir + "events.root"

        os.makedirs(gen_dir, exist_ok=True)
        os.makedirs(delphes_out_dir, exist_ok=True)

        if not (os.path.isfile(lhe_path) or os.path.isfile(lhe_path + ".gz")):
            print(f"[WARN] No LHE file found for {mgtag} at {lhe_path}(.gz) — skipping")
            continue

        pythia_card = write_pythia_card(ma, ctau_mm, gen_dir, lhe_path)
        width       = alp_width_from_ctau(ctau_mm)

        bash_cmd = build_command(pythia_card, lhe_path, delphes_out)

        subprocess.run(
            ["tmux", "new-session", "-d", "-s", session, "bash", "-c", bash_cmd])
       
        print(f"Launched {session} for {tag}  "
              f"(Pythia-only, ctau={ctau_mm} mm -> width={width:.3e} GeV)")

if __name__ == "__main__":
    main()