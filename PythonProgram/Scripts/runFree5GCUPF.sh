#!/bin/bash

killall -r '^upf'
sleep 5
echo "Change into correct directory"
cd /home/user5g/free5gc/
echo "Start UPF"
./bin/upf &