#!/bin/sh

SYSTEM=`uname`;

if [ "$SYSTEM" = "Linux" ]; then
    if ! grep "ogstun" /proc/net/dev > /dev/null; then
        ip tuntap add name ogstun mode tun
    fi
    if test "x`sysctl -n net.ipv6.conf.ogstun.disable_ipv6`" = x1; then
        echo "net.ipv6.conf.ogstun.disable_ipv6=0" > /etc/sysctl.d/30-open5gs.conf
        sysctl -p /etc/sysctl.d/30-open5gs.conf
    fi
    ip addr del 10.45.0.1/16 dev ogstun 2> /dev/null
    ip addr add 10.45.0.1/16 dev ogstun
    ip addr del 2001:db8:cafe::1/48 dev ogstun 2> /dev/null
    ip addr add 2001:db8:cafe::1/48 dev ogstun
    ip link set ogstun up
    iptables -D INPUT -i ogstun
    iptables -I INPUT -i ogstun -j ACCEPT
    sysctl -w net.ipv4.ip_forward=1
    sysctl -w net.ipv6.conf.all.forwarding=1
    iptables -t nat -D POSTROUTING -s 10.45.0.0/16 ! -o ogstun -j MASQUERADE
    iptables -t nat -A POSTROUTING -s 10.45.0.0/16 ! -o ogstun -j MASQUERADE
    ip6tables -t nat -D POSTROUTING -s 2001:db8:cafe::/48 ! -o ogstun -j MASQUERADE
    ip6tables -t nat -A POSTROUTING -s 2001:db8:cafe::/48 ! -o ogstun -j MASQUERADE

else
    sysctl -w net.inet.ip.forwarding=1
    sysctl -w net.inet6.ip6.forwarding=1
    ifconfig lo0 alias 127.0.0.2 netmask 255.255.255.255
    ifconfig lo0 alias 127.0.0.3 netmask 255.255.255.255
    ifconfig lo0 alias 127.0.0.4 netmask 255.255.255.255
    ifconfig lo0 alias 127.0.0.5 netmask 255.255.255.255
    ifconfig lo0 alias 127.0.0.6 netmask 255.255.255.255
    ifconfig lo0 alias 127.0.0.7 netmask 255.255.255.255
    ifconfig lo0 alias 127.0.0.8 netmask 255.255.255.255
    ifconfig lo0 alias 127.0.0.9 netmask 255.255.255.255
    ifconfig lo0 alias 127.0.0.10 netmask 255.255.255.255
    ifconfig lo0 alias 127.0.0.11 netmask 255.255.255.255
    ifconfig lo0 alias 127.0.0.12 netmask 255.255.255.255
    ifconfig lo0 alias 127.0.0.13 netmask 255.255.255.255
    ifconfig lo0 alias 127.0.0.14 netmask 255.255.255.255
    ifconfig lo0 alias 127.0.0.15 netmask 255.255.255.255
    ifconfig lo0 alias 127.0.0.16 netmask 255.255.255.255
    ifconfig lo0 alias 127.0.0.17 netmask 255.255.255.255
    ifconfig lo0 alias 127.0.0.18 netmask 255.255.255.255
    ifconfig lo0 alias 127.0.0.19 netmask 255.255.255.255
    ifconfig lo0 alias 127.0.0.20 netmask 255.255.255.255
    ifconfig lo0 alias 127.0.1.10 netmask 255.255.255.255
    ifconfig lo0 alias 127.0.1.11 netmask 255.255.255.255
    ifconfig lo0 alias 127.0.1.12 netmask 255.255.255.255
    if [ "$SYSTEM" = "Darwin" ]; then
        if ! test -f /etc/pf.anchors/org.open5gs; then
            sudo sh -c "echo 'nat on {en0} from 10.45.0.0/16 to any -> {en0}' > /etc/pf.anchors/org.open5gs"
            sudo sh -c "echo 'nat on {en0} from 2001:db8:cafe::1/48 to any -> {en0}' > /etc/pf.anchors/org.open5gs"
        fi
        pfctl -e -f /etc/pf.anchors/org.open5gs
    fi
fi

