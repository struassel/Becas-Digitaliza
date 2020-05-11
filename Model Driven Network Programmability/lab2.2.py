#!/usr/bin/env python3

from netmiko import ConnectHandler
from device_info import ios_xe1

def show_interaces(connection):
    resp = connection.send_command("show ip interface brief")
    print("Show ip int brief:", "{}".format(resp), sep="\n")

    # Part 3: question d
    print("Data type:", type(resp))
    interfaces = resp.split("\n")[1:]
    index = 0
    for i in interfaces:
        interface = i.split()
        name = interface[0]
        ip = interface[1]
        print("Interface [" + str(index) + "]:\n\tName ->", name, "\n\tIP ->", ip)
        index += 1


sshcli = ConnectHandler(ip=ios_xe1["address"], port=ios_xe1["ssh_port"],
                        username=ios_xe1["username"], password=ios_xe1["password"],
                        device_type=ios_xe1["device"])

show_interaces(sshcli)

config_commands=[
    'int loopback 1',
    'ip address 2.2.2.2 255.255.255.0',
    'description WHATEVER']

output=sshcli.send_config_set(config_commands)
print("Config output from the device:\n{}\n".format(output))

show_interaces(sshcli)


config_commands=[
    'int loopback 2',
    'ip address 2.2.2.2 255.255.255.0',
    'description WHATEVER2']

output=sshcli.send_config_set(config_commands)
print("Config output from the device:\n{}\n".format(output))

show_interaces(sshcli)