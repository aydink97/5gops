#!/bin/bash

echo "Stop runnning instances, if any"
killall -r '^free5gc'

echo "Change into correct directory"
cd /home/user5g/free5gc/
echo "Start all Free5GC components"
echo "Start NRF"
./bin/nrf &
echo "Start UDR"
./bin/udr &
echo "Start UDM"
./bin/udm &
echo "Start AUSF"
./bin/ausf &
echo "Start NSSF"
./bin/nssf &
echo "Start AMF"
./bin/amf &
echo "Start PCF"
./bin/pcf &
echo "Start UPF"
./bin/upf &
echo "Start SMF"
./bin/smf &
echo "Start N3IWF"
./bin/n3iwf &