import flow
import flow.environments
from flow import FlowProject
import signac
import sys
import shutil
import os

project = signac.init_project()

class Project(FlowProject):
	pass

#@Project.pre.isfile('configuration.xyz')
@Project.post(lambda job: 'energy' in job.document)
@Project.operation
def run(job):
	print(f"run job {job}")
	job = project.open_job(id=job)
	from operations import run_calculation
	run_calculation(job)

@Project.pre(lambda job: job.isfile(f"../../{job}/signac_statepoint.json"))
@Project.operation
def transfer(job):
	print(f"transfer job {job} into signac pile")
	job = job.id
	if os.path.exists(job):
		if os.path.exists(f"workspace/{job}"):
			shutil.rmtree(f"workspace/{job}")
		shutil.move(job,"workspace")
		if os.path.exists(f"{job}.job.log"):
			shutil.move(f"{job}.job.log","workspace/{job}")
		if os.path.exists(f"{job}.job.err"):
			shutil.move(f"{job}.job.err","workspace/{job}")
		if os.path.exists(f"{job}.job.out"):
			shutil.move(f"{job}.job.out","workspace/{job}")

if __name__=="__main__":
	globals()[sys.argv[1]](sys.argv[2])	# when this file is called, set arguments
	fp = Project()
	fp.main()
