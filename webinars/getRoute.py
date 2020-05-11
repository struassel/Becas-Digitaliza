#!/usr/bin/env python3

import requests
import urllib3
import json
from pprint import pprint
from tabulate import *

requests.packages.urllib3.disable_warnings()
url = "https://devnetsbx-netacad-apicem-3.cisco.com/api/v1/host"

headers = {
    "Content-Type": "application/json",
    "X-Auth-Token": "ST-3106-I5Sm2dY0dR9dL47dQtxB-cas"
}

resp = requests.get(url, headers=headers, verify=False)

resp_body = resp.json()
pprint(resp_body)

hostList = []
if resp.status_code == 200:
    i = 1
    for item in resp_body["response"]:
        # print("Host:", i)
        # pprint(item)
        host = [
            i,
            item['hostType'],
            item['hostIp'],
            item['hostMac'],
            item['lastUpdated']
        ]
        hostList.append(host)
        i += 1

    tableHeader = ["Index", "Type", "IP", "MAC", "Updated"]
    print(tabulate(hostList, tableHeader))
else:
    print("Error: " + str(resp.status_code) + ". Content: " + str(resp_body))
