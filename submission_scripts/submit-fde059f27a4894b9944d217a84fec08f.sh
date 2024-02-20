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
export ESPRESSO_PSEUDO=$PWD/espresso/pseudo
mv fde059f27a4894b9944d217a84fec08f workspace/.
python3 project.py run -n 1 -j fde059f27a4894b9944d217a84fec08f
