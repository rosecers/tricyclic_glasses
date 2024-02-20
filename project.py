import flow
import flow.environments
from flow import FlowProject

class Project(FlowProject):
    pass

@Project.pre.isfile('configuration.xyz')
@Project.post(lambda job: 'energy' in job.document)
@Project.operation
def run(job):
    from operations import run_calculation
    run_calculation(job)

if __name__=="__main__":
    fp = Project()
    fp.main()
