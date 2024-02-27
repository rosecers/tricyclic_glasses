import flow
import flow.environments
from flow import FlowProject
import signac
import sys

project = signac.init_project()

class Project(FlowProject):
    pass

#@Project.pre.isfile('configuration.xyz')
@Project.post(lambda job: 'energy' in job.document)
@Project.operation
def run(job):
	print('hello!')
	job = project.open_job(id=job)
	from operations import run_calculation
	run_calculation(job)

if __name__=="__main__":
	globals()[sys.argv[1]](sys.argv[2])
	fp = Project()
	fp.main()
