import os
import re
import glob

mg_dir            = "/ceph/salshamaily/haa4K_FCCee/madgraph_3.7.1/"
analysis_dir      = "/ceph/salshamaily/haa4K_FCCee/analysis/"
ANALYSIS_STAGE1   = os.path.join(analysis_dir, "analysis_stage1.py")
script_dir    	  = os.path.dirname(os.path.abspath(__file__))
BANNER            = "Events/run_01/run_01_tag_1_banner.txt"
XSEC_RE           = re.compile(r"#\s+Integrated weight \(pb\)\s*:\s*([\d.eE+\-]+)")
TAG_CTAU_RE       = re.compile(r"^(.*)_ctau([^_/]+)$")
WIDTH_RE          = re.compile(r"^9000005:all\s*=\s*ALP ALP 0 0 0\s+([\d.eE+\-]+)\s+([\d.eE+\-]+)")
PROCESSLIST_BLOCK_RE = re.compile(r"processList\s*=\s*\{(.*?)\n\}", re.DOTALL)
PROCESSLIST_KEY_RE   = re.compile(r'"([^"]+)"\s*:')

NEVENTS               = 500000

def get_sample_tags(analysis_stage1_path):
    with open(analysis_stage1_path) as fh:
        text = fh.read()

    block_match = PROCESSLIST_BLOCK_RE.search(text)
    if not block_match:
        return []

    return PROCESSLIST_KEY_RE.findall(block_match.group(1))

def split_tag(tag: str):
    m = TAG_CTAU_RE.match(tag)
    if not m:
        return tag, None
    return m.group(1), m.group(2)

def extract_xsec(sample_dir):

    banner_path = os.path.join(sample_dir, BANNER)

    if not os.path.isfile(banner_path):
        return None

    nominal = None

    with open(banner_path) as fh:
        for line in fh:
            m = XSEC_RE.search(line)
            if m:
                nominal = float(m.group(1))
                break
    return nominal

def extract_width_for_ctau(sample_dir, ctau):
    if ctau is None:
        return None

    candidates = glob.glob(os.path.join(sample_dir, f"pythia_mg_*_ctau{ctau}.cmd"))
    if not candidates:
        return None

    with open(candidates[0]) as fh:
        for line in fh:
            m = WIDTH_RE.match(line.strip())
            if m:
                return float(m.group(2))
    return None

def main():
    tags = get_sample_tags(ANALYSIS_STAGE1)

    if not tags:
        print(f"No sample tags found in: {ANALYSIS_STAGE1}")
        return

    ok      = {}
    missing = []

    for tag in tags:
        mass_dir, ctau = split_tag(tag)
        sample_dir = os.path.join(mg_dir, mass_dir)
        xsec       = extract_xsec(sample_dir)
        width      = extract_width_for_ctau(sample_dir, ctau)

        if xsec is None:
            missing.append(tag)
        else:
            ok[tag] = (xsec, ctau, width)

    col = 62
    print(f"\n{'Sample':<{col}} {'Nominal xsec (pb)':>18}  {'c_tau':>10}  {'ALP width (GeV)':>16}")
    print("\u2500" * (col + 50))

    for tag, (xsec, ctau, width) in ok.items():
        ctau_str  = ctau if ctau else "MISSING"
        width_str = f"{width:.6e}" if width is not None else "MISSING"
        print(f"{tag:<{col}} {xsec:>18.6e}  {ctau_str:>10}  {width_str:>16}")

    if missing:
        print()
        for tag in missing:
            print(f"{tag:<{col}} {'MISSING / NOT RUN':>18}")

    print("\n" + "\u2500" * (col + 50))

    if missing:
        print("\nMissing tags (no xsec found under madgraph dir):")
        for tag in missing:
            print(f"    {tag}")

    no_width = [tag for tag, (_, _, w) in ok.items() if w is None]
    if no_width:
        print("\nSamples with unresolved/missing ALP width in pythia card:")
        for tag in no_width:
            print(f"    {tag}")

    # save use_xsec.py file
    alp_path    = os.path.join(script_dir, "use_xsec.py")

    with open(alp_path, "w") as fh:
        ### processList dict in analysis_final.py ###
        fh.write("processList = {\n")
        for tag in ok:
            fh.write(f'    "{tag}": {{}},\n')
        fh.write("}\n\n")

        ### procDictAdd dict in analysis_final.py ###
        fh.write("procDictAdd = {\n")

        for tag, (xsec, _, _) in ok.items():
            fh.write(
                f'    "{tag}": {{'
                f'"numberOfEvents": {NEVENTS}, "sumOfWeights": {NEVENTS}, '
                f'"crossSection": {xsec:.10e}, "kfactor": 1.0, "matchingEfficiency": 1.0}},\n'
                )
        fh.write("}\n")

    print(f"\nSaved: {alp_path}")
    print(f"\n{len(ok)} samples written, {len(missing)} missing (skipped)\n")

if __name__ == "__main__":
    main()