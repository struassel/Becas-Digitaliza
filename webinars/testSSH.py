#!/usr/bin/env python3

from netmiko import ConnectHandler
from webinars.device_info import ios_xe1

sshcli = ConnectHandler(ip=ios_xe1["address"], port=ios_xe1["ssh_port"],
                        username=ios_xe1["username"], password=ios_xe1["password"],
                        device_type=ios_xe1["device"])

resp = sshcli.send_command("show ip interface brief")
print("Result:", resp)
