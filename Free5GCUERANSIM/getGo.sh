#!/bin/bash

# First lets check if the correct go version is already installed
FILE=/usr/local/go/VERSION
if grep -q 1.17.8 "$FILE"; then
    echo "Correct Go version is already installed"
    exit
else
    wget https://dl.google.com/go/go1.17.8.linux-amd64.tar.gz
    mkdir -p ~/go/{bin,pkg,src}
fi