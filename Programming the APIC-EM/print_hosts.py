#!/usr/bin/env python3

import requests
from tabulate import tabulate
import my_apic_em_functions as apic

apicem_host = "devnetsbx-netacad-apicem-3.cisco.com"
user = "devnetuser"
password = "Xj3BDqbU"

ticket = apic.get_ticket(apicem_host, user, password)

requests.packages.urllib3.disable_warnings()
url = "https://"+apicem_host+"/api/v1/host"

headers = {
    "Content-Type": "application/json",
    "X-Auth-Token": ticket
}

resp = requests.get(url, headers=headers, verify=False)

print("Status of /host request: ", resp.status_code)
if resp.status_code != 200:
    raise Exception("Status code does not equal 200. Response text: " + resp.text)
response_json = resp.json()

host_list = []
i = 0
for item in response_json["response"]:
    i += 1
    host = [
        i,
        item["hostType"],
        item["hostIp"]
    ]
    host_list.append(host)
table_header = ["Number", "Type", "IP"]
print(tabulate(host_list, table_header))

# Test created function
print("Using now created function...")
apic.print_hosts(apicem_host, user, password)
