#!/usr/bin/env python3
"""
Cleans the MadGraph output directory and reruns MG5 -> Pythia -> Delphes
for a set of failed samples, each in its own detached tmux session.
"""

import os
import glob
import subprocess
from typing import Optional, Dict

### CONFIGURATION ###
base_dir        = "/ceph/salshamaily/haa4K_FCCee/"
mg_dir          = base_dir + "madgraph_3.7.1/"
generation_dir  = base_dir + "generation/"
delphes_dir     = base_dir + "delphes/"
local_setup     = base_dir + "setup_local.sh"
delphes_tcl     = "/ceph/sgiappic/card_IDEA.tcl"
edm4hep_cfg     = base_dir + "edm4hep_output_config.tcl"

samples: Dict[str, str] = {
    "mgp8_ee_qqH_HAlpAlp_m30p0_cah1em2_ecm240":	"qq_m30p0_cah1em2",
}


def find_card(gen_dir: str, pattern: str) -> Optional[str]:
    """
    - Finds a single card file matching a glob pattern in gen_dir
    - Returns:
    path of the matched file, or None if not found
    """
    matches = glob.glob(os.path.join(gen_dir, pattern))
    return matches[0] if matches else None


def build_command(tag: str, mg_card: str, pythia_card: str) -> str:
    """
    - Builds the bash command string run inside each tmux session:
    clean mg_out_dir -> recompile via mg5_aMC -> substitute ALP width ->
    decompress LHE if needed -> run Delphes
    - Returns:
    the bash -c command string
    """
    mg_out_dir      = mg_dir + tag + "/"
    lhe_path        = mg_out_dir + "Events/run_01/unweighted_events.lhe"
    param_card_path = mg_out_dir + "Cards/param_card.dat"
    delphes_out     = delphes_dir + tag + "/events.root"

    cmd  = f'source {local_setup}\n'
    cmd += f'cd {mg_dir}\n'
    cmd += 'export MAKEFLAGS="-j1"\n'
    cmd += f'bin/mg5_aMC "{mg_card}"\n'
    cmd += f'ALP_WIDTH=$(grep -i "^DECAY[[:space:]]*9000005" "{param_card_path}" | awk \'{{print $3}}\')\n'
    cmd += 'if [ -z "$ALP_WIDTH" ]; then\n'
    cmd += f'    echo "[ERROR] Could not find ALP width in {param_card_path}" >&2\n'
    cmd += '    exec bash\n'
    cmd += 'fi\n'
    cmd += 'echo "  ALP width from MadGraph: $ALP_WIDTH GeV"\n'
    cmd += f'sed -i "s/__ALP_WIDTH__/${{ALP_WIDTH}}/" "{pythia_card}"\n'
    cmd += f'if [ -f "{lhe_path}.gz" ] && [ ! -f "{lhe_path}" ]; then\n'
    cmd += f'    gunzip "{lhe_path}.gz"\n'
    cmd += 'fi\n'
    cmd += f'if [ ! -f "{lhe_path}" ]; then\n'
    cmd += '    echo "[ERROR] LHE file not found after MadGraph" >&2\n'
    cmd += '    exec bash\n'
    cmd += 'fi\n'
    cmd += f'DelphesPythia8_EDM4HEP {delphes_tcl} {edm4hep_cfg} "{pythia_card}" {delphes_out}\n'
    cmd += f'echo "=== Done: {tag} (exit code $?) ==="\n'
    cmd += 'exec bash\n'

    return cmd


def main() -> None:
    for tag, session in samples.items():
        gen_dir = generation_dir + tag + "/"

        mg_card     = find_card(gen_dir, "mg_param_*.txt")
        pythia_card = find_card(gen_dir, "pythia_mg_*.cmd")

        if mg_card is None or pythia_card is None:
            print(f"[WARN] Missing card(s) for {tag} in {gen_dir} — skipping")
            continue

        delphes_out_dir = delphes_dir + tag + "/"
        os.makedirs(delphes_out_dir, exist_ok=True)

        bash_cmd = build_command(tag, mg_card, pythia_card)

        subprocess.run(
            ["tmux", "new-session", "-d", "-s", session, "bash", "-c", bash_cmd]
        )
        print(f"Launched {session} for {tag}")


if __name__ == "__main__":
    main()