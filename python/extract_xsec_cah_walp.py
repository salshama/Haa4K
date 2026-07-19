import os
import re
import glob

mg_dir          = "/ceph/salshamaily/haa4K_FCCee/madgraph_3.7.1/"
generation_dir    = "/ceph/salshamaily/haa4K_FCCee/generation/"
script_dir        = os.path.dirname(os.path.abspath(__file__))
BANNER          = "Events/run_01/run_01_tag_1_banner.txt"
XSEC_RE         = re.compile(r"#\s+Integrated weight \(pb\)\s*:\s*([\d.eE+\-]+)")
RWG_RE          = re.compile(r"#\s+rwgt_(\d+)\s*:\s*([\d.eE+\-]+)")
CAH_RE            = re.compile(r"_cah([\d]+em[\d]+)_")
# picks up mass (group 1) and width (group 2) from the ALP decay line
WIDTH_RE        = re.compile(
    r"^9000005:all\s*=\s*ALP ALP 0 0 0\s+([\d.eE+\-]+)\s+([\d.eE+\-]+)"
)
NEVENTS            = 500000


def extract_xsec(sample_dir):

    banner_path = os.path.join(sample_dir, BANNER)

    if not os.path.isfile(banner_path):
        return None, {}

    nominal  = None
    reweight = {}

    with open(banner_path) as fh:
        for line in fh:
            if nominal is None:
                m = XSEC_RE.search(line)
                if m:
                    nominal = float(m.group(1))
            m = RWG_RE.search(line)
            if m:
                reweight[int(m.group(1))] = float(m.group(2))

    return nominal, reweight


def extract_cah_from_tag(tag: str):
    """
    - Pulls the CAH label straight out of the sample tag
      (e.g. "..._cah1em3_..." -> "1em3")
    - Returns:
    str or None if not found
    """
    m = CAH_RE.search(tag)
    return m.group(1) if m else None


def extract_alp_width(tag: str):
    """
    - Locates the pythia card written for this (mass, cah) point under
      generation_dir/{tag}/ and parses out the ALP width that was
      substituted in at runtime (via sed, from the MadGraph param_card)
    - Returns:
    float or None if the card / line can't be found
    - Args:
    tag: str, sample tag (same naming as madgraph output dir)
    """
    gen_sample_dir = os.path.join(generation_dir, tag)
    candidates = glob.glob(os.path.join(gen_sample_dir, "pythia_mg_m*_cah*.cmd"))

    if not candidates:
        return None

    with open(candidates[0]) as fh:
        for line in fh:
            m = WIDTH_RE.match(line.strip())
            if m:
                return float(m.group(2))

    return None


def main():
    sample_dirs = sorted(glob.glob(os.path.join(mg_dir, "mgp8*_cah*em*/")))

    if not sample_dirs:
        print(f"No sample directories found under: {mg_dir}")
        return

    ok      = {}
    missing = []

    for path in sample_dirs:
        tag = os.path.basename(path.rstrip("/"))
        xsec, rwgt = extract_xsec(path)
        cah   = extract_cah_from_tag(tag)
        width = extract_alp_width(tag)

        if xsec is None:
            missing.append(tag)
        else:
            ok[tag] = (xsec, rwgt, cah, width)

    col = 62
    print(f"\n{'Sample':<{col}} {'Nominal xsec (pb)':>18}  {'CAH':>10}  {'ALP width (GeV)':>16}  {'Reweights':>10}")
    print("\u2500" * (col + 62))

    for tag, (xsec, rwgt, cah, width) in ok.items():
        rw_str    = f"{len(rwgt)} columns" if rwgt else "none"
        cah_str   = cah if cah else "MISSING"
        width_str = f"{width:.6e}" if width is not None else "MISSING"
        print(f"{tag:<{col}} {xsec:>18.6e}  {cah_str:>10}  {width_str:>16}  {rw_str:>10}")

    if missing:
        print()
        for tag in missing:
            print(f"{tag:<{col}} {'MISSING / NOT RUN':>18}")

    print("\n" + "\u2500" * (col + 62))

    if missing:
        print("\nMissing tags:")
        for tag in missing:
            print(f"    {tag}")

    # flag any points where the pythia card couldn't be found or parsed —
    # this would indicate the width substitution didn't happen correctly
    no_width = [tag for tag, (_, _, _, w) in ok.items() if w is None]
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

        for tag, (xsec, _, _, _) in ok.items():
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