#!/usr/bin/env python3

import requests
import urllib3
import json

requests.packages.urllib3.disable_warnings()

url = "https://192.168.56.101/restconf/data/ietf-interfaces:interfaces/interface=Loopback77"

headers = {
    "Accept": "application/yang-data+json",
    "Content-Type": "application/yang-data+json"
}

basic_auth = ("cisco", "cisco123!")

yang_config = {
    "ietf-interfaces:interface": {
        "name": "Loopback77",
        "description": "MIAY",
        "type":"iana-if-type:softwareLoopback",
        "enabled": True,
        "ietf-ip:ipv4": {
            "address": [
                {
                    "ip": "77.77.77.77",
                    "netmask": "255.255.255.0"
                }
            ]
        },
        "ietf-ip:ipv6": {}
    }
}

resp = requests.put(url, data=json.dumps(yang_config), headers=headers, auth=basic_auth, verify=False)

if resp.status_code >= 200 and resp.status_code < 300:
    print("Everything goes OK: {}".format(resp.status_code))
    if(resp.text!=""):
        resp_body = resp.json()
        print(json.dumps(resp_body, indent=4))
else:
    print("Error code: {}, reply: {}".format(resp.status_code, resp.json()))