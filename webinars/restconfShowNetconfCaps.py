#!/usr/bin/env python3

import requests
import urllib3
import json

requests.packages.urllib3.disable_warnings()

url = "https://192.168.56.101/restconf/data/netconf-state/capabilities"

headers = {
    "Accept": "application/yang-data+json",
    "Content-Type": "application/yang-data+json"
}

basic_auth = ("cisco", "cisco123!")

resp = requests.get(url, headers=headers, auth=basic_auth, verify=False)

resp_body = resp.json()
print(json.dumps(resp_body, indent=4))
