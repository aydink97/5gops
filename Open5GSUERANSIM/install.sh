#!/bin/bash

# First lets check if open5gs is already installed
FILE=/home/user5g/open5gs/install/bin
if [ -d "$FILE"]; then
    echo "Open5GS is already installed"
    exit
else
    echo "Changing into the Build folder"
    cd /home/user5g/open5gs/build
    echo "Installing Open5GS with Ninja"
    ninja install
fi
