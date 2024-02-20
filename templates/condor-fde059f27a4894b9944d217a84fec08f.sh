# template.sub
# starter submit file for CHTC jobs

universe = vanilla
log = fde059f27a4894b9944d217a84fec08f.job.log
error = fde059f27a4894b9944d217a84fec08f.job.err
output = fde059f27a4894b9944d217a84fec08f.job.out

executable = submission_scripts/submit-fde059f27a4894b9944d217a84fec08f.sh
arguments = fde059f27a4894b9944d217a84fec08f


should_transfer_files = YES
when_to_transfer_output = ON_EXIT_OR_EVICT
transfer_input_files = Miniconda3-latest-Linux-x86_64.sh,  project.py, .signac, signac_project_document.json, workspace/fde059f27a4894b9944d217a84fec08f, qe.yml, submission_scripts/submit-fde059f27a4894b9944d217a84fec08f.sh, espresso, operations.py, file.in
transfer_output_files = workspace/fde059f27a4894b9944d217a84fec08f

request_cpus = 16 
request_memory = 100GB
request_disk = 100GB

queue 1
