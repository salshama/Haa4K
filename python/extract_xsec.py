import os
import re
import glob
 
mg_dir  	= "/ceph/salshamaily/haa4K_FCCee/madgraph_3.7.1/"
script_dir	= os.path.dirname(os.path.abspath(__file__))
BANNER  	= "Events/run_01/run_01_tag_1_banner.txt"
XSEC_RE 	= re.compile(r"#\s+Integrated weight \(pb\)\s*:\s*([\d.eE+\-]+)")
RWG_RE  	= re.compile(r"#\s+rwgt_(\d+)\s*:\s*([\d.eE+\-]+)")
NEVENTS		= 500000
 
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
        if xsec is None:
            missing.append(tag)
        else:
            ok[tag] = (xsec, rwgt)
 
    col = 62
    print(f"\n{'Sample':<{col}} {'Nominal xsec (pb)':>18}  {'Reweights':>10}")
    print("\u2500" * (col + 33))
 
    for tag, (xsec, rwgt) in ok.items():
        rw_str = f"{len(rwgt)} columns" if rwgt else "none"
        print(f"{tag:<{col}} {xsec:>18.6e}  {rw_str:>10}")
 
    if missing:
        print()
        for tag in missing:
            print(f"{tag:<{col}} {'MISSING / NOT RUN':>18}")
 
    print("\n" + "\u2500" * (col + 33))
 
    if missing:
        print("\nMissing tags:")
        for tag in missing:
            print(f"    {tag}")
            
    # save use_xsec.py file imported by analysis_final.py directly
    alp_path	= os.path.join(script_dir, "use_xsec.py")
    
    with open(alp_path, "w") as fh:
    	### processList dict in analysis_final.py ###
    	fh.write("processList = {\n")
    	for tag in ok:
    		fh.write(f'	"{tag}": {{}},\n')
    	fh.write("}\n\n")
    	
    	### procDictAdd dict in analysis_final.py ###
    	fh.write("procDictAdd = {\n")
    	
    	for tag, (xsec, _) in ok.items():
    		fh.write(
    			f'	"{tag}": {{'
    			f'"numberOfEvents": {NEVENTS}, "sumOfWeights": {NEVENTS}, '
    			f'"crossSection": {xsec:.10e}, "kfactor": 1.0, "matchingEfficiency": 1.0}},\n'
    			)
    	fh.write("}\n")
    
    print(f"\nSaved: {alp_path}")
    print(f"\n{len(ok)} samples written, {len(missing)} missing (skipped)\n")
 
if __name__ == "__main__":
    main()