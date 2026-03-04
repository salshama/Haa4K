import os
import re

def make_dir_if_not_exists(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)
    os.system(f"chmod -R +x {directory}")
     
def create_condor_config(nCPUs: int,
                         memory: int,
                         output_dir: str):
    '''
    Creates contents of condor configuration file.
    '''
    cfg = 'Universe          = docker\n'

    cfg += 'docker_image     = cverstege/alma9-gridjob\n'

    cfg += 'accounting_group = cms.higgs \n'

    cfg += 'output_dir       = '+output_dir+'\n'

    cfg += 'executable       = $(filename)\n'

    cfg += 'log              = $(output_dir)log/condor_$(ClusterId).$(ProcId).log\n'

    cfg += 'output           = $(output_dir)out/condor_$(ClusterId).$(ProcId).out\n'

    cfg += 'error            = $(output_dir)err/condor_$(ClusterId).$(ProcId).err\n'

    cfg += 'max_retries      = 3\n'

    cfg += '+JobFlavour      = "workday"\n'

    cfg += 'request_memory   = '+str(memory)+' MB\n'

    cfg += 'request_cpus     = '+str(nCPUs)+'\n'

    cfg += 'requirements     = (TARGET.ProvidesCPU && TARGET.ProvidesEKPResources)\n'

    cfg += 'should_transfer_files   = IF_NEEDED\n'

    cfg += 'when_to_transfer_output  = ON_EXIT\n'

    cfg += 'queue filename matching files'
 
    for process in processList:
        with open(output_dir + process + '/job_submit.cfg', 'w') as sub:
            sub.write(cfg)
            for file in os.listdir(output_dir + process):
                filename = os.fsdecode(file)
                if filename.endswith('.sh'):
                    sub.write(f' ' + output_dir + process + '/' + filename)

def create_subjob_script(local_dir: str,
                         source_dir: str,
                         input_dir: str,
                         output_dir: str,
                         output_ana: str,
                         ananame: str):
    '''
    Creates sub-job script to be run.
    '''

    make_dir_if_not_exists(output_dir)
    make_dir_if_not_exists(output_dir+"out")
    make_dir_if_not_exists(output_dir+"log")
    make_dir_if_not_exists(output_dir+"err")

    for process in processList:
        j = 0
        
        for file in os.listdir(input_dir+process): 
            make_dir_if_not_exists(output_dir+process)   
            g = input_dir + process + '/' + file + ' '
            scr  = '#!/bin/bash\n\n'
            scr += 'source ' + source_dir + 'setup.sh\n\n'
            scr += 'cd ' + local_dir + '\n\n'
            scr += 'fccanalysis run ' + ananame + ' --batch '
            scr += f' --output  ' + output_ana + process + '/' + 'chunk_'+str(j)+'.root --files-list  ' + g
            scr += '\n\n'     
            with open(output_dir + process + '/submit_chunk_' + str(j) + '.sh', 'w') as sh:
                sh.write(scr)
            j+=1
            print(f"SUBMISSION FIlE CREATED: {process}, chunk {j-1}")

def submit_jobs(output_dir: str):
    for process in processList:
        dir = output_dir + process 
        num_files = len(os.listdir(dir))-1
        os.system(f"chmod -R +x {dir}")
        os.system(f"condor_submit {dir}/job_submit.cfg")
        print(f"GOOD SUBMISSION: {process} with {num_files} chunks")
             
# signal and background process lists will be different because there are
# different directories
processList = {
    'p8_ee_WW_ecm240':{},
    'p8_ee_Zqq_ecm240':{},
    'p8_ee_ZZ_ecm240':{},
    
    'wzp6_ee_tautau_ecm240':{},
    'wzp6_ee_mumu_ecm240':{},
    'wzp6_ee_ee_Mee_30_150_ecm240':{},

    'wzp6_ee_tautauH_Htautau_ecm240':{},
    'wzp6_ee_tautauH_Hbb_ecm240':{},
    'wzp6_ee_tautauH_Hcc_ecm240':{},
    'wzp6_ee_tautauH_Hss_ecm240':{},
    'wzp6_ee_tautauH_Hgg_ecm240':{},
    'wzp6_ee_tautauH_HWW_ecm240':{},
    'wzp6_ee_tautauH_HZZ_ecm240':{},

    'wzp6_egamma_eZ_Zmumu_ecm240':{},
    'wzp6_egamma_eZ_Zee_ecm240':{},
    'wzp6_gammae_eZ_Zmumu_ecm240':{},
    'wzp6_gammae_eZ_Zee_ecm240':{},

    'wzp6_gaga_tautau_60_ecm240':{},
    'wzp6_gaga_mumu_60_ecm240':{},
    'wzp6_gaga_ee_60_ecm240':{},

    'wzp6_ee_nuenueZ_ecm240':{},
    'wzp6_ee_nunuH_Htautau_ecm240':{},
    'wzp6_ee_nunuH_Hbb_ecm240':{},
    'wzp6_ee_nunuH_Hcc_ecm240':{},
    'wzp6_ee_nunuH_Hss_ecm240':{},
    'wzp6_ee_nunuH_Hgg_ecm240':{},
    'wzp6_ee_nunuH_HWW_ecm240':{},
    'wzp6_ee_nunuH_HZZ_ecm240':{},

    'wzp6_ee_eeH_Htautau_ecm240':{},
    'wzp6_ee_eeH_Hbb_ecm240':{},
    'wzp6_ee_eeH_Hcc_ecm240':{},
    'wzp6_ee_eeH_Hss_ecm240':{},
    'wzp6_ee_eeH_Hgg_ecm240':{},
    'wzp6_ee_eeH_HWW_ecm240':{},
    'wzp6_ee_eeH_HZZ_ecm240':{},

    'wzp6_ee_mumuH_Htautau_ecm240':{},
    'wzp6_ee_mumuH_Hbb_ecm240':{},
    'wzp6_ee_mumuH_Hcc_ecm240':{},
    'wzp6_ee_mumuH_Hss_ecm240':{},
    'wzp6_ee_mumuH_Hgg_ecm240':{},
    'wzp6_ee_mumuH_HWW_ecm240':{},
    'wzp6_ee_mumuH_HZZ_ecm240':{},

    'wzp6_ee_bbH_Htautau_ecm240':{},
    'wzp6_ee_bbH_Hbb_ecm240':{},
    'wzp6_ee_bbH_Hcc_ecm240':{},
    'wzp6_ee_bbH_Hss_ecm240':{},
    'wzp6_ee_bbH_Hgg_ecm240':{},
    'wzp6_ee_bbH_HWW_ecm240':{},
    'wzp6_ee_bbH_HZZ_ecm240':{},

    'wzp6_ee_ccH_Htautau_ecm240':{},
    'wzp6_ee_ccH_Hbb_ecm240':{},
    'wzp6_ee_ccH_Hcc_ecm240':{},
    'wzp6_ee_ccH_Hss_ecm240':{},
    'wzp6_ee_ccH_Hgg_ecm240':{},
    'wzp6_ee_ccH_HWW_ecm240':{},
    'wzp6_ee_ccH_HZZ_ecm240':{},

    'wzp6_ee_ssH_Htautau_ecm240':{},
    'wzp6_ee_ssH_Hbb_ecm240':{},
    'wzp6_ee_ssH_Hcc_ecm240':{},
    'wzp6_ee_ssH_Hss_ecm240':{},
    'wzp6_ee_ssH_Hgg_ecm240':{},
    'wzp6_ee_ssH_HWW_ecm240':{},
    'wzp6_ee_ssH_HZZ_ecm240':{},

    'wzp6_ee_qqH_Htautau_ecm240':{},
    'wzp6_ee_qqH_Hbb_ecm240':{},
    'wzp6_ee_qqH_Hcc_ecm240':{},
    'wzp6_ee_qqH_Hss_ecm240':{},
    'wzp6_ee_qqH_Hgg_ecm240':{},
    'wzp6_ee_qqH_HWW_ecm240':{},
    'wzp6_ee_qqH_HZZ_ecm240':{},
}

def save_failed_paths(output_dir: str, save_file: str):
    """
    Scans log files for each process.
    - If log contains "exit-code 0": skip.
    - Otherwise: find the matching .err file, read "output file path", and
      save it to one text file (one path per line).
    """

    failed_paths = []

    print("\n--- Scanning condor log files ---\n")

    for process in processList:

        log_dir = os.path.join(output_dir, process, "log")
        err_dir = os.path.join(output_dir, process, "err")

        if not os.path.isdir(log_dir):
            continue

        for filename in os.listdir(log_dir):
            if not filename.endswith(".log"):
                continue

            log_path = os.path.join(log_dir, filename)

            # extract job ID: condor_12345.0.log → 12345.0
            match = re.search(r"condor_(.+)\.log", filename)
            if not match:
                continue

            job_id = match.group(1)

            # read log file
            try:
                with open(log_path, "r") as f:
                    content = f.read()
            except:
                print(f"Could not read {log_path}")
                continue

            # successful job → skip
            if "exit-code 0" in content:
                continue

            # unsuccessful job → check error file
            err_file = f"condor_{job_id}.err"
            err_path = os.path.join(err_dir, err_file)

            if not os.path.isfile(err_path):
                print(f"No error file for {process}, job {job_id}")
                continue

            # search for "output file path"
            output_path = None
            try:
                with open(err_path, "r") as ef:
                    for line in ef:
                        if "output file path" in line.lower():
                            output_path = line.strip()
                            break
            except:
                print(f"Could not read {err_path}")
                continue

            if output_path:
                failed_paths.append(f"{process}  {job_id}  {output_path}")
            else:
                failed_paths.append(f"{process}  {job_id}  NO OUTPUT PATH FOUND")

    # save everything to a single file
    with open(save_file, "w") as f:
        for line in failed_paths:
            f.write(line + "\n")

    print(f"\nSaved {len(failed_paths)} failed path entries → {save_file}\n")

inputDir		= '/ceph/sgiappic/HiggsCP/winter23/'
output			= '/ceph/salshamaily/haa4K_FCCee/HTCondor/' ##output directory of submission files, needs to be different to have unique submission files
outputDir		= '/ceph/salshamaily/haa4K_FCCee/samples/' ##output directory of stage1 samples
localDir		= '/ceph/salshamaily/haa4K_FCCee/analysis/'
sourceDir		= '/ceph/sgiappic/FCCAnalyses/'
Filename		= 'analysis_stage1.py'

nCPUS = 1
Memory = 10000

create_subjob_script(localDir, sourceDir, inputDir, output, outputDir, Filename)

create_condor_config(nCPUS, Memory, output)

submit_jobs(output)