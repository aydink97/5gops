#!/bin/bash

# Enable IPv4 forwarding
sudo sysctl -w net.ipv4.ip_forward=1

# Remove NAT if there is any
sudo iptables -t nat -D POSTROUTING -o enp1s0 -j MASQUERADE
# Add NAT
sudo iptables -t nat -A POSTROUTING -o enp1s0 -j MASQUERADE

# Remove Forward Rule if there is any
sudo iptables -D FORWARD 1
# Add Forward Rule
sudo iptables -I FORWARD 1 -j ACCEPT

sudo systemctl stop ufw