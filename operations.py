import ase.io
import numpy as np
from scipy.spatial.transform import Rotation as R
from ase.calculators.espresso import Espresso
import csv
import signac
import os
import shutil
import sys

#espresso_profile = EspressoProfile(["mpirun", "-np", "16", "pw.x"])
pseudopotentials = {'C': 'C.pbe-tm-new-gipaw-dc.UPF',
                    'H': 'H.pbe-tm-new-gipaw-dc.UPF'}

input_data = {
	'control': {
		'calculation': 'scf',
    		'verbosity': 'high',
    		'restart_mode': 'from_scratch',
    		'nstep': 1,
    		'outdir': './', 
    		'prefix': 'sample'}, 
	'system': {
		'ibrav': 0,
		'nat': 66,
		'ntyp': 2, 
 		'ecutwfc': 60.0e0,
		'ecutrho': 240.0e0,
		'vdw_corr': 'dft-d',
		'nbnd': 111,
		'nosym': True,
		'assume_isolated': 'mt'},
	'electrons': {
		'conv_thr': 1.e-10, 
  		'mixing_beta': 0.5e0,
		'electron_maxstep': 1000,
		'diagonalization': 'cg'},
	}
calc = Espresso(pseudopotentials=pseudopotentials,
	#pseudo_dir='pseudo',
	input_data = input_data)

# read file.in
atoms = ase.io.read('file.in')
#atoms.write('atoms.xyz')

# separate into constituent pieces
benzyl = np.array([1,4,5,6,7,10,40,41,42])
filter = np.ones(66,dtype=bool)
for i in benzyl:
	filter[i] = False
benzene = atoms[np.invert(filter)]
paddles = atoms[filter]

#benzene.write('benzyl.xyz')
#paddles.write('paddles.xyz')
paddles_pos = paddles.get_positions()

paddle_A = paddles[paddles_pos[:,0]>12]

#paddle_A.write('paddle_A.xyz')

paddles_a = paddles[paddles_pos[:,0]<12]
paddles_a_pos = paddles_a.get_positions()
paddle_a1 = paddles_a[paddles_a_pos[:,1]>12]
paddle_a2 = paddles_a[paddles_a_pos[:,1]<12]

#paddle_a1.write('paddle_a1.xyz')
#paddle_a2.write('paddle_a2.xyz')

pos = atoms.get_positions()
n_A = pos[1] - pos[0]
n_a1 = pos[4] - pos[11]
n_a2 = pos[5] - pos[12]

center_A = pos[0]
center_a1 = pos[11]
center_a2 = pos[12]

a = 1
b = a
c = a
# rot_A = rotate_paddle(paddle_A.get_positions(),n_A,0,center_A)
# rot_a1 = rotate_paddle(paddle_a1.get_positions(),n_a1,0,center_a1)
# rot_a2 = rotate_paddle(paddle_a2.get_positions(),n_a2,0,center_a2)
energies = np.zeros([a,b,c]) + 9999

# cool function to rotate paddles
def rotate_paddle(paddle,n,theta,center):
	# center = pos.mean(axis=0)
	paddle = paddle.copy()
	pos = paddle.get_positions()
	pos = pos - center
	r = R.from_quat([n[0]*np.sin(theta/2),n[1]*np.sin(theta/2),n[2]*np.sin(theta/2),np.cos(theta/2)])
	rot_pos = r.apply(pos)
	rot_pos = rot_pos + center
	paddle.set_positions(rot_pos)
	return paddle

def output_energies():
	with open('energies.csv','w',newline='') as csvfile:
		spamwriter = csv.writer(csvfile, delimiter=',')
		spamwriter.writerow(['A','a1','a2','Energy'])
		for i in range(a):
			for j in range(b):
				for k in range(c):
					spamwriter.writerow([(180/np.pi)*i*np.pi/a,(180/np.pi)*j*2*np.pi/b,(180/np.pi)*k*2*np.pi/c,energies[i,j,k]])

def init():
	for i in range(a):
		rot_A = rotate_paddle(paddle_A,n_A,i* np.pi/a,center_A)

		for j in range(b):
			rot_a1 = rotate_paddle(paddle_a1,n_a1,j*2*np.pi/b,center_a1)

			for k in range(c):
				rot_a2 = rotate_paddle(paddle_a2,n_a2,k*2*np.pi/c,center_a2)

				sp = {"A": i, "a1": j, "a2": k}
				job = signac.get_project().open_job(sp).init()
				whole = benzene + rot_A + rot_a1 + rot_a2
				#ase.io.write(job.fn('A_'+str(i)+'_a1_'+str(j)+'_a2_'+str(k)+'.xyz'), whole)
				ase.io.write(job.fn('configuration.xyz'),whole)


def run_calculation(job):
	print('run_calculation')
	whole = ase.io.read(job.fn('configuration.xyz'))
	#whole = ase.io.read(job.fn('A_'+str(job.sp.A)+'_a1_'+str(job.sp.a1)+'_a2_'+str(job.sp.a2)+'.xyz'))
	#whole = ase.io.read(job.fn('A_0_a1_0_a2_0.xyz'))
	whole.calc = calc
	# whole.write('configurations/A_'+str(i)+',a1_'+str(j)+',a2_'+str(k)+'.xyz')
	job.document['energy'] = whole.get_potential_energy()

def submit_calculations():
	for i in range(a):
		for j in range(b):
			for k in range(c):
				sp = {"A": i, "a1": j, "a2": k}
				job = signac.get_project().open_job(sp).init()
				submit(False,job)

def submit(interact,job):
	if interact:
		interactive = " --interactive"
		#argv = [a for a in argv if a != "-i"]

	else:
		interactive = ""

	if os.path.exists(f"{job}.job.log"):
		print(f"Skipping. Job log for {job} exists")
	else:
		if not os.path.exists(f"templates/condor-{job}.sh"):
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

if __name__ == "__main__":
    init()
#     with open('energies.csv','w',newline='') as csvfile:
 #           spamwriter = csv.writer(csvfile, delimiter=',')
 #           spamwriter.writerow(['A','a1','a2','Energy'])
 #           for i in range(a):
 #                   for j in range(b):
 #                           for k in range(c):
 #                                   spamwriter.writerow([(180/np.pi)*i*np.pi/a,(180/np.pi)*j*2*np.pi/b,(180/np.pi)*k*2*np.pi/c,energies[i,j,k]])
