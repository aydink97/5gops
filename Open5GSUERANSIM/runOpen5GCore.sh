#!/bin/bash

echo "Stop runnning instances, if any"
killall -r '^open5gs'

echo "Start all Open5GS components"
echo "Start NRF"
open5gs-nrfd -D
echo "Start SCP"
open5gs-scpd -D
echo "Start AMF"
open5gs-amfd -D
echo "Start SMF"
open5gs-smfd -D
echo "Start UPF"
open5gs-upfd -D
echo "Start AUSF"
open5gs-ausfd -D
echo "Start UDM"
open5gs-udmd -D
echo "Start PCF"
open5gs-pcfd -D
echo "Start NSSF"
open5gs-nssfd -D
echo "Start BSF"
open5gs-bsfd -D
echo "Start UDR"
open5gs-udrd -D