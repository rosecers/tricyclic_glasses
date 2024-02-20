import signac
import os
import shutil
import sys

argv = sys.argv[1:]
if "-i" in argv:
    interactive = " --interactive"
    argv = [a for a in argv if a != "-i"]

else:
    interactive = ""

if "-l" in argv:
    is_long = True
    argv = [a for a in argv if a != "-l"]

for s in argv:
    job = signac.get_project().open_job(id=s)

    if os.path.exists(f"{job}.job.log"):
        print(f"Skipping. Job log for {job} exists")
    else:
        if not os.path.exists(f"templates/condor-{job}.sh"):
            if job.document.NAtoms > 30 or is_long:
                template = "templates/condor-long.sh"
            else:
                template = "templates/condor.sh"

            shutil.copy(template, f"templates/condor-{job}.sh")
            os.system(
                f'sed -i "s/7623db09eccee41830e4fab767e79c26/{job}/g" templates/condor-{job}.sh'
            )
        if not os.path.exists(f"submission_scripts/submit-{job}.sh"):
            shutil.copy(
                "submission_scripts/submit.sh",
                f"submission_scripts/submit-{job}.sh",
            )
            os.system(
                f'sed -i "s/7623db09eccee41830e4fab767e79c26/{job}/g" submission_scripts/submit-{job}.sh'
            )

        os.system(f"condor_submit templates/condor-{job}.sh {interactive}")
