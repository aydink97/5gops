#!/bin/bash

echo "Stop runnning instances, if any"
killall -r '^node-'

echo "Change into the WebConsole directory"
cd /home/user5g/free5gc/webconsole/
echo "Run WebConsole"
./bin/webconsole &