#!/bin/bash

echo "Stop runnning instances, if any"
killall -r '^node-'

echo "Change into the WebUI directory"
cd /home/user5g/open5gs/webui/
echo "Run the WebUI"
npm run dev &