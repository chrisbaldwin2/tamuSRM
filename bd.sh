#!/bin/bash


"""
## Instruction list for Infiniband 
## M1 is compute node, M2 is memory node

# 1. Setup Infiniband NIC on both machines
cd setup
# M1:192.168.0.11, M2:192.168.0.12
sudo ./ib_setup.sh 192.168.0.<11, 12>

# 2. Compile infiniswap daemon on M2:
# In setup
./install.sh daemon

# 3. Install infiniswap block device on M1:
# In setup
./install.sh bd
"""

REPO_DIR = $(dirname -- $(readlink -f "${BASH_SOURCE}"))

cd $REPO_DIR/setup

if [ $# -eq 0 ]
  then
    echo "No arguments supplied; default 192.168.1.11"
    sudo ./ib_setup.sh 192.168.1.11
  else
    echo "Setup with $1"
    sudo ./ib_setup.sh $1

fi

./install.sh bd