# template.sub
# starter submit file for CHTC jobs

universe = vanilla
log = 7623db09eccee41830e4fab767e79c26.job.log
error = 7623db09eccee41830e4fab767e79c26.job.err
output = 7623db09eccee41830e4fab767e79c26.job.out

executable = submission_scripts/submit-7623db09eccee41830e4fab767e79c26.sh
arguments = "7623db09eccee41830e4fab767e79c26"


should_transfer_files = YES
when_to_transfer_output = ON_EXIT_OR_EVICT
transfer_input_files = Miniconda3-latest-Linux-x86_64.sh,  project.py, .signac, signac_project_document.json, workspace/7623db09eccee41830e4fab767e79c26, qe.yml, submission_scripts/submit-7623db09eccee41830e4fab767e79c26.sh, espresso, operations.py, file.in
transfer_output_files = workspace/7623db09eccee41830e4fab767e79c26

request_cpus = 8 
request_memory = 20GB
request_disk = 20GB

queue 1
