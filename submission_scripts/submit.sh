#!/bin/bash

set -e

# installation steps for Miniconda
export HOME=$PWD
export PATH
sh Miniconda3-latest-Linux-x86_64.sh -b -p $PWD/miniconda3
export PATH=$PWD/miniconda3/bin:$PATH

# install packages
rm -rf $PWD/miniconda3/envs/*
source $PWD/miniconda3/etc/profile.d/conda.sh
conda env create -f qe.yml --force
conda activate qe
pip install signac signac-flow ase

# modify this line to run your desired Python script
mkdir workspace

# passed from submit argument
job=$1

export ESPRESSO_PSEUDO=$PWD/espresso/pseudo
#mv 7623db09eccee41830e4fab767e79c26 workspace/.
#python3 project.py run -n 1 -j 7623db09eccee41830e4fab767e79c26

mv ${job} workspace/.
python3 project.py run $job

echo
echo
echo GOODBYE
echo $job
echo
#echo scrungus >> workspace/${job}/scrungus.txt
