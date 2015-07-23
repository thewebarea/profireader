#!/bin/bash

#how to create point to point host<->guest connection. both interfaces (dummy and tap joined by bridge, no routing nor forwarding performed)

#creating dummy etherned device, bridge, adding dummy to bridge (tap device will be added by create_tun script)
modprobe dummy
lsmod | grep dummy
ip link set name eth10 dummy0
ifconfig eth10 hw ether 00:AA:AA:ff:ff:ff
ip link show eth10
ifup br10
apt-get install bridge-utils
brctl addbr br10
apt-get install uml-utilities

### /etc/network/interfaces

auto br10
 iface br10 inet static
  address 10.10.10.1
  network 10.10.10.0
  netmask 255.255.255.0
#  gateway 192.168.1.1
  bridge_ports eth10
  brodge_stp off
  bridge_fd 0
  bridge_maxwait 0



#### this is /root/create_tun.sh script
if [ -n "$1" ]; then
  tunctl -u root -t $1
  ip link set $1 up
  sleep 1
  brctl addif br10 $1
  exit 0
else
  echo "no device"
  exit 1
fi

# starting vm
kvm --daemonize -m 512 -device e1000,netdev=net10,mac=00:bb:aa:ff:ff:ff -netdev tap,id=net10,script=/root/create_tun.sh  ./vm-189-disk-1.raw
