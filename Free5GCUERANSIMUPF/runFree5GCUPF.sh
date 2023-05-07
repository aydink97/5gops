#!/bin/bash

killall -r '^upf'

echo "Change into correct directory"
cd /home/user5g/free5gc/
echo "Start UPF"
./bin/upf &