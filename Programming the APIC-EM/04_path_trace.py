#!/usr/bin/env python3

import requests
import json
from tabulate import tabulate
import my_apic_em_functions as apic

apicem_host = "sandboxapicem.cisco.com"
user = "devnetuser"
password = "Cisco123!"

ticket = apic.get_ticket(apicem_host, user, password)

requests.packages.urllib3.disable_warnings()
url = "https://" + apicem_host + "/api/v1/flow-analysis"

headers = {
    "Content-Type": "application/json",
    "X-Auth-Token": ticket
}

print("Retrieving the list of hosts")
apic.print_hosts(apicem_host, user, password)

print("Retrieving the list of devices")
apic.print_devices(apicem_host, user, password)

while True:
    # s_ip = input("Insert source IP:")
    # d_ip = input("Insert destination IP:")

    s_ip = "10.1.7.1"
    d_ip = "10.1.11.1"
    if s_ip != "" and d_ip != "":
        break
    else:
        print("Error: Both source and destination IPs must be introduced")

path_data = {
    "sourceIP": s_ip,
    "destIP": d_ip
}

print(s_ip, "-->", d_ip)
req_body = json.dumps(path_data)
resp = requests.post(url, data=req_body, headers=headers, verify=False)
if resp.status_code != 200 and resp.status_code != 202:
    raise Exception(
        "Status code does not equal 200 or 202. Status: " + str(resp.status_code) + ".Response text: " + resp.text)

response_json = resp.json()
flowAnalysisId = response_json["response"]["flowAnalysisId"]
print("Flow Analysis Id:", flowAnalysisId)

data = ""
while True:
    check_url = "https://" + apicem_host + "/api/v1/flow-analysis/" + flowAnalysisId
    resp = requests.get(check_url, headers=headers, verify=False)
    if resp.status_code != 200:
        raise Exception(
            "Status code does not equal 200. Status: " + str(resp.status_code) + ".Response text: " + resp.text)

    data = resp.json()
    status = data["response"]["request"]["status"]
    if status == "COMPLETED":
        break
    elif status == "FAILED":
        raise Exception("Flow Analysis failed. Reason:", data["response"]["request"]["failureReason"])

        # resp = requests.post(url, headers=headers, verify=False)
        #
        # print("Status of /host request: ", resp.status_code)
        # if resp.status_code != 200:
        #     raise Exception("Status code does not equal 200. Response text: " + resp.text)
        # response_json = resp.json()
        #
        # dev_list = []
        # i = 0
        # for item in response_json["response"]:
        #     i += 1
        #     dev = [
        #         i,
        #         item["type"],
        #         item["managementIpAddress"]
        #     ]
        #     dev_list.append(dev)
        # table_header = ["Number", "Type", "IP"]
        # print(tabulate(dev_list, table_header))
        #
        # # # Test created function
        # print("Using now created function...")
        # apic.print_devices(apicem_host, user, password)

print("Source:", data["response"]["request"]["sourceIP"],
      "Destination", data["response"]["request"]["destIP"])

net_elems = []
i = 0
for item in data["response"]["networkElementsInfo"]:
    i += 1
    net_elem = [
        i,
        item["name"],
        item["ip"],
        item["ingressInterface"]["physicalInterface"]["name"]
        if ("ingressInterface" in item and "physicalInterface" in item["ingressInterface"]) else "-",
        item["egressInterface"]["physicalInterface"]["name"]
        if ("egressInterface" in item and "physicalInterface" in item["egressInterface"]) else "-"
    ]
    net_elems.append(net_elem)
table_header = ["Name", "IP", "Input ifaz", "Output ifaz"]
print(tabulate(net_elems, table_header))
