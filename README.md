# 5GOps



## Getting started

This is a tool to produce ansible playbook files for automatic setup purposes. 
At the current time the only supported test situations are.
- Open5GS + UERANSIM (Control Plane and User Plane running on the same VM)
- Open5GS + UERANSIM + UPF (Control Plane and User Plane running on seperate VMs)
- Free5GC + UERANSIM
- Free5GC + UERANSIM + UPF

This is all tested in KVM (Virtual Machines), before procedure it is highly recommended to screenshot the system or virtual machine to revert any changes.

## How to use

To use this software, it has to be started in the PythonProgram folder. Otherwise it cannot access the Template Folder.

0. !!! Important !!! Again, run the program in the directory where it's located
1. Open the GUI
2. Select the Core Solution
3. Check if the UPF is running on a seperate VM / Hardware
4. Fill in the fields correspondingly (When the AMF is running on the UPF, please put in the same IP address in there)
5. Click on the Button Generate


## Requirements

This software depends on two modules, that have to be installed.

ruamel.yaml
Link: https://pypi.org/project/ruamel.yaml/
Install with:
```
pip install ruamel.yaml
```

tkinter-tooltip
Link: https://pypi.org/project/tkinter-tooltip/
Install with:
```
pip install tkinter-tooltip
```

## Usage of Output files

To run the ansible configurations. Use a command similar to this.

- To deploy 5G Core with UPF and UERANSIM: (2 Endpoints)
```
ansible-playbook -i inventory.yaml playbook-{coresolution}.yaml playboook-{correct-ue}.yaml -K
```
- To deploy 5G Core without UPF and UERANSIM and UPF Only (3 Endpoints)
```
ansible-playbook -i inventory.yaml playbook-{coresolution}.yaml playbook-{UPF-Only}.yaml playboook-{correct-ue}.yaml -K
```

Note: It seems Free5GC prefers to have the UPF running before the SMF, in that case. Run the playbook-{UPF-Only}.yaml before the playbook-{coresolution}.yaml

For example:
```
ansible-playbook -i inventory.yaml playbook-Free5GC-UPF-Only.yaml playbook-Free5GC-Without-UPF.yaml playbook-Free5GC-UE.yaml -K
```

-K paramter is used to ask for the "sudo" password
additional -v or -vv/-vvv/-vvvv gives a more verbose output in the command line

For further options please refer to the Ansible documentation


## Project status
This is only a prototype and should be considered as such. It is by no means a polished software.


## Troubleshoot

If a errormessage like this appears:

```
fatal: [upf]: FAILED! => {
    "changed": false,
    "cmd": "/usr/bin/gmake install",
    "invocation": {
        "module_args": {
            "chdir": "/home/user5g/gtp5g",
            "file": null,
            "jobs": null,
            "make": null,
            "params": null,
            "target": "install"
        }
    },
    "msg": "modprobe: ERROR: could not insert 'gtp5g': Exec format error\ngmake: *** [Makefile:58: install] Error 1",
    "rc": 2,
    "stderr": "modprobe: ERROR: could not insert 'gtp5g': Exec format error\ngmake: *** [Makefile:58: install] Error 1\n",
    "stderr_lines": [
        "modprobe: ERROR: could not insert 'gtp5g': Exec format error",
        "gmake: *** [Makefile:58: install] Error 1"
    ],
    "stdout": "cp gtp5g.ko /lib/modules/5.15.0-69-generic/kernel/drivers/net\nmodprobe udp_tunnel\n/sbin/depmod -a\nmodprobe gtp5g\n",
    "stdout_lines": [
        "cp gtp5g.ko /lib/modules/5.15.0-69-generic/kernel/drivers/net",
        "modprobe udp_tunnel",
        "/sbin/depmod -a",
        "modprobe gtp5g"
    ]
}
```
It is most certainly because of the linux kernel or headers.
As this was all done in Virtual Machines with snapshots it is recommended to do a full revert to a snapshot as of the time of writing I did not find a solution to this.


If there is no connection to the Data Network on Free5GC. It could be a firewall issue

Enable a forward to the correct interface on the machine which runs the UPF.

```
sudo iptables -t nat -D POSTROUTING -o enp1s0 -j MASQUERADE
```
Replace enp1s0 with the interface that is connected with the Data Network.