#!/bin/bash

echo "Stop runnning instances, if any"
killall -r '^nr-'

echo "Change into UERANSIM directory"
cd /home/user5g/UERANSIM/
echo "Start GNB Station"
./build/nr-gnb -c /home/user5g/UERANSIM/config/open5gs-gnb.yaml &
echo "Start UE"
./build/nr-ue -c  /home/user5g/UERANSIM/config/open5gs-ue.yaml &