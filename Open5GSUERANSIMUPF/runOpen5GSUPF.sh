#!/bin/bash

echo "Stop runnning instances, if any"
killall -r '^open5gs'

echo "Start UPF"
open5gs-upfd -D