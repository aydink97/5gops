from tkinter import *
from tkinter import ttk
from tkinter import filedialog
# install ruamel with pip before this
from ruamel.yaml import YAML
# install tktooltip with pip before this
from tktooltip import ToolTip
import json


# Here is where the magic happens.
#  Ask for script path or make it relative.
#  Selection Free5GC or Open5GS
#  Checkbox UPF Seperate?
#  Configure AMF IP address
#  -> When UPF Seperate, Ask UPF IP address
#
#  # Free5GC UPF Same Machine #
#  GOPATH: e.g. /home/user5g/go
#  Set HOMEPATH environment Variable to use for make command e.g /home/user5g/gtp5g
#  AMF IP Address
#  SMF endpoints IP Address (UERANSIM)
#  UPF IP Address
#
#  # Open5GS UPF Same Machine #
#  Set HOMEPATH environment variable e.g /home/user5g/
#  AMF IP Address with Jinja Variable
#  Set UPF GTP IP Address with Jinja Variable
#  Save / Output File

# Use default files like template and edit them or replace Variables in Template with values


def import_file(*args):
    try:
        filetypes = (
            ('JSON Files', '*.json'),
            ('All files', '*.*')
        )

        filename = filedialog.askopenfilename(
            title='Select Import File',
            initialdir='./',
            filetypes=filetypes
        )
    except:
        FileNotFoundError

    try:
        with open(filename, "r") as j_r:
            data = json.load(j_r)

        coreSolution.set(data['solution'])
        seperate_upf.set(data['seperateUPF'])
        scriptPath.set(data['scriptpath'])
        amf.set(data['amf'])
        ueransim.set(data['ue'])
        homepath.set(data['homepath'])
        upf.set(data['upf'])
        hostname.set(data['web'])
        username.set(data['user'])

    except:
        FileNotFoundError


def select_solution():
    if (coreSolution.get() == "open5gs"):
        if (seperate_upf.get() == True):
            playbook_name = "Open5GS-Without-UPF.yaml"
            filename.set(playbook_name)
        else:
            playbook_name = "Open5GS-With-UPF.yaml"
            filename.set(playbook_name)
    if (coreSolution.get() == "free5gc"):
        if (seperate_upf.get() == True):
            playbook_name = "Free5GC-Without-UPF.yaml"
            filename.set(playbook_name)
        else:
            playbook_name = "Free5GC-With-UPF.yaml"
            filename.set(playbook_name)
    return playbook_name


def select_inventory():
    if (seperate_upf.get() == True):
        inventory_name = "inventory-seperateUPF-template.yaml"
        filename.set(inventory_name)
    else:
        inventory_name = "inventory-AiO-Template.yaml"
        filename.set(inventory_name)
    return inventory_name


def select_correct_UE():
    if (coreSolution.get() == "open5gs"):
        ue_playbook = "Open5GS-UE.yaml"
        filename.set(ue_playbook)
    if (coreSolution.get() == "free5gc"):
        ue_playbook = "Free5GC-UE.yaml"
        filename.set(ue_playbook)
    return ue_playbook


def select_UPF_solution():
    if (coreSolution.get() == "open5gs"):
        upf_playbook = "Open5GS-UPF-Only.yaml"
        filename.set(upf_playbook)
    if (coreSolution.get() == "free5gc"):
        upf_playbook = "Free5GC-UPF-Only.yaml"
        filename.set(upf_playbook)
    return upf_playbook


def save_files_and_values(*args):
    yaml = YAML()
    yaml.preserve_quotes = True
    yaml.default_flow_style = False
    yaml.indent(sequence=4, mapping=2, offset=2)

    # Edit Inventory YAML
    try:
        with open("./Ansible-Templates/Inventories/" + select_inventory(), "r") as i_r:
            data_inventory = yaml.load(i_r)

            try:
                data_inventory['all']['hosts']['upf']['ansible_host'] = upf_entry.get(
                )
            except:
                KeyError
            pass

        data_inventory['all']['hosts']['core']['ansible_host'] = amf_entry.get()
        data_inventory['all']['hosts']['ue']['ansible_host'] = ueransim_entry.get()
        data_inventory['all']['vars']['ansible_user'] = username_entry.get()

        with open("./Output/inventory.yaml", "w") as i_d:
            yaml.dump(data_inventory, i_d)

    except:
        FileNotFoundError

    # Edit Solution Playbook
    try:
        with open("./Ansible-Templates/Playbooks/" + select_solution(), "r") as f_r:
            data_playbook = yaml.load(f_r)

        if (hostname_entry.get() == ""):
            data_playbook[0]['vars']['hostname'] = "127.0.0.1"
        else:
            data_playbook[0]['vars']['hostname'] = hostname_entry.get()
            
        if (homepath_entry.get() == ""):
            data_playbook[0]['vars']['homepath'] = "/home/user5g"
        else:
            data_playbook[0]['vars']['homepath'] = homepath_entry.get()
            
        if (scriptPath_entry.get() == ""):
            data_playbook[0]['vars']['scriptpath'] = "~/Documents/Path/to/Scripts"
        else:
            data_playbook[0]['vars']['scriptpath'] = scriptPath.get()
            
        if (amf_entry.get() == "" and coreSolution.get() == "open5gs"):
            data_playbook[0]['vars']['amf'] = "127.0.0.5"
        if (amf_entry.get() == "" and coreSolution.get() == "free5gc"):
            data_playbook[0]['vars']['amf'] = "127.0.0.18"
        else:
            data_playbook[0]['vars']['amf'] = amf_entry.get()
            
        if (upf_entry.get() == "" and coreSolution.get() == "open5gs"):
            data_playbook[0]['vars']['upf'] = "127.0.0.7"
        if (upf_entry.get() == "" and coreSolution.get() == "free5gc"):
            data_playbook[0]['vars']['upf'] = "127.0.0.8"
        else:
            data_playbook[0]['vars']['upf'] = upf_entry.get()

        with open("./Output/playbook-" + select_solution(), "w") as f_d:
            yaml.dump(data_playbook, f_d)
            print("5G core playbook written!")
    except:
        FileNotFoundError

    # Edit UERANSIM Playbook
    try:
        with open("./Ansible-Templates/Playbooks/" + select_correct_UE(), "r") as f_r:
            data_playbook1 = yaml.load(f_r)

        data_playbook1[0]['vars']['homepath'] = homepath_entry.get()
        data_playbook1[0]['vars']['scriptpath'] = scriptPath_entry.get()
        data_playbook1[0]['vars']['amfip'] = amf_entry.get()
        data_playbook1[0]['vars']['ueip'] = ueransim_entry.get()

        with open("./Output/playbook-" + select_correct_UE(), "w") as f_d:
            yaml.dump(data_playbook1, f_d)
            print("UE playbook written!")
    except:
        FileNotFoundError

    # Edit UPF only playbooks
    if (seperate_upf.get() == True):
        try:
            with open("./Ansible-Templates/Playbooks/" + select_UPF_solution(), "r") as f_r:
                data_playbook = yaml.load(f_r)

            data_playbook[0]['vars']['hostname'] = hostname_entry.get()
            data_playbook[0]['vars']['homepath'] = homepath_entry.get()
            data_playbook[0]['vars']['scriptpath'] = scriptPath_entry.get()
            data_playbook[0]['vars']['amf'] = amf_entry.get()
            data_playbook[0]['vars']['upf'] = upf_entry.get()

            with open("./Output/playbook-" + select_UPF_solution(), "w") as f_d:
                yaml.dump(data_playbook, f_d)
            print("5G UPF playbook written!")
        except:
            FileNotFoundError

    # Edit the Scripts (yea all of them, even if you do not use them)
    try:
        with open("./Scripts/runWebUI-template.sh", "r") as file:
            filedata = file.read()

        filedata = filedata.replace('/home/user5g', homepath_entry.get())

        with open("./Scripts/runWebUI.sh", "w") as file:
            file.write(filedata)
    except:
        FileNotFoundError

    # Edit the Scripts (yea all of them, even if you do not use them)
    try:
        with open("./Scripts/runFree5GCCore-template.sh", "r") as file:
            filedata = file.read()

        filedata = filedata.replace('/home/user5g', homepath_entry.get())

        with open("./Scripts/runFree5GCCore.sh", "w") as file:
            file.write(filedata)
    except:
        FileNotFoundError

       # Edit the Scripts (yea all of them, even if you do not use them)
    try:
        with open("./Scripts/runFree5GCUPF-template.sh", "r") as file:
            filedata = file.read()

        filedata = filedata.replace('/home/user5g', homepath_entry.get())

        with open("./Scripts/runFree5GCUPF.sh", "w") as file:
            file.write(filedata)
    except:
        FileNotFoundError

    # Edit the Scripts (yea all of them, even if you do not use them)
    try:
        with open("./Scripts/runWebConsole-template.sh", "r") as file:
            filedata = file.read()

        filedata = filedata.replace('/home/user5g', homepath_entry.get())

        with open("./Scripts/runWebConsole.sh", "w") as file:
            file.write(filedata)
    except:
        FileNotFoundError

    # Edit the Scripts (yea all of them, even if you do not use them)
    try:
        with open("./Scripts/runUERANSIM-F5GC-template.sh", "r") as file:
            filedata = file.read()

        filedata = filedata.replace('/home/user5g', homepath_entry.get())

        with open("./Scripts/runUERANSIM-F5GC.sh", "w") as file:
            file.write(filedata)
    except:
        FileNotFoundError

       # Edit the Scripts (yea all of them, even if you do not use them)
    try:
        with open("./Scripts/runUERANSIM-O5GS-template.sh", "r") as file:
            filedata = file.read()

        filedata = filedata.replace('/home/user5g', homepath_entry.get())

        with open("./Scripts/runUERANSIM-O5GS.sh", "w") as file:
            file.write(filedata)
    except:
        FileNotFoundError
    if (coreSolution.get() == ""):
        finishLabel.set("Please select 5G solution")
    else:
        finishLabel.set("Playbooks generated in Output Folder")
# GUI Begin


root = Tk()
root.title("5GOps")

# Add a menu
menubar = Menu(root)
menu_file = Menu(menubar)
menu_import = Menu(menu_file)
menu_help = Menu(menubar)
menubar.add_cascade(menu=menu_file, label='File')
menu_file.add_command(label="Import JSON (Crtl + O)", command=import_file)
# menubar.add_cascade(menu=menu_help, label='?')
root.config(menu=menubar)

mainframe = ttk.Frame(root, padding="3 3 12 12")
mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)


# Select 5G solution
coreSolution = StringVar()
ttk.Radiobutton(mainframe, text="Free5GC", variable=coreSolution,
                value="free5gc").grid(column=1, row=1, sticky=W)
ttk.Radiobutton(mainframe, text="Open5GS", variable=coreSolution,
                value="open5gs").grid(column=2, row=1, sticky=W)


# Is the UPF running on another instance?
seperate_upf = BooleanVar()
check = ttk.Checkbutton(mainframe, text="Seperate UPF?", variable=seperate_upf, onvalue=True, offvalue=False).grid(
    column=1, row=2, sticky=W
)


# Type in ScriptPath or Select it with the "..." Button
ttk.Label(mainframe, text="Path to Scripts: ").grid(column=1, row=3, sticky=W)
scriptPath = StringVar()
scriptPath_entry = ttk.Entry(mainframe, width=30, textvariable=scriptPath)
scriptPath_entry.grid(column=2, row=3, sticky=(W, E))
ToolTip(scriptPath_entry, msg="Please type in full path to the folder containing the Scripts.\nNote: May not contain trailing slash ('/')")


# AMF IP Address
ttk.Label(mainframe, text="AMF IP:").grid(column=1, row=5, sticky=W)
amf = StringVar()
amf_entry = ttk.Entry(mainframe, width=30, textvariable=amf)
amf_entry.grid(column=2, row=5, sticky=W)


# Type UERANSIM IP Address
ttk.Label(mainframe, text="UERANSIM IP:").grid(column=1, row=6, sticky=W)
ueransim = StringVar()
ueransim_entry = ttk.Entry(mainframe, width=30, textvariable=ueransim)
ueransim_entry.grid(column=2, row=6, sticky=W)

# Set Homepath for VMs
ttk.Label(mainframe, text="Homepath of target machine:").grid(
    column=1, row=7, sticky=W)
homepath = StringVar()
homepath_entry = ttk.Entry(mainframe, width=30, textvariable=homepath)
homepath_entry.grid(column=2, row=7, sticky=W)
ToolTip(homepath_entry, msg="Please type in the homepath for the user on the target machines.\nNote: They have to be identical on all machines \nNote 2: May not contain trailing slash ('/')")

# Set UPF Address if seperate UPF is selected
ttk.Label(mainframe, text="UPF IP:").grid(column=1, row=8, sticky=W)
upf = StringVar()
upf_entry = ttk.Entry(mainframe, width=30, textvariable=upf)
upf_entry.grid(column=2, row=8, sticky=W)

# Type in HOST IP Address for HOSTNAME (WebUI Open5GS Only)
ttk.Label(mainframe, text="WebUI / WebConsole IP:").grid(column=1, row=9, sticky=W)
hostname = StringVar()
hostname_entry = ttk.Entry(mainframe, width=30, textvariable=hostname)
hostname_entry.grid(column=2, row=9, sticky=W)
ToolTip(hostname_entry, msg="This is for setting the environment variable on Open5GS. Generally it is the same IP Address as the AMF so it has to be typed in.")

# Type in the authorized SSH user (must be able to sudo, and passwordless logon must be possible [use ssh-copy-id or equivalent])
ttk.Label(mainframe, text="SSH User: ").grid(column=1, row=10, sticky=W)
username = StringVar()
username_entry = ttk.Entry(mainframe, width=30, textvariable=username)
username_entry.grid(column=2, row=10, sticky=W)
ToolTip(username_entry,
        msg="This is needed to login in as the user account from Ansible")

# Select Import JSON
filename = StringVar()
ttk.Button(mainframe, text='Import File...',
           command=import_file).grid(column=1, row=11, sticky=W)

# Save File as Ansible-Playbook
finishLabel = StringVar()
ttk.Label(mainframe, text="", textvariable=finishLabel).grid(
    column=2, row=11, sticky=W)
ttk.Button(mainframe, text="Generate", command=save_files_and_values).grid(
    column=3, row=11, sticky=W)


for child in mainframe.winfo_children():
    child.grid_configure(padx=5, pady=5)


root.bind("<Return>", save_files_and_values)
root.bind("<Escape>", exit)
root.bind("<Control-o>", import_file)


root.mainloop()
