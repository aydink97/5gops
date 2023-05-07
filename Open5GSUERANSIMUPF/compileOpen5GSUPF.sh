#!/bin/bash

# First lets check if open5gs is already installed
FILE=~/open5gs/install
if [ -d "$FILE"]; then
    echo "Open5GS UPF already compiled with meson"
    exit
else
    echo "Changing into the Git folder"
    cd ~/open5gs/
    echo "Compiling Open5GS with meson"
    meson build --prefix=`pwd`/install
    echo "Compile with Ninja"
    ninja -C build
fi