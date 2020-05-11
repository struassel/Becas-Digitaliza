#!/usr/bin/env python3

import requests
import json

requests.packages.urllib3.disable_warnings()
url = "https://devnetsbx-netacad-apicem-3.cisco.com/api/v1/ticket"

headers = {
    "Content-Type": "application/json"
}

req_body = {
    "password": "Xj3BDqbU",
    "username": "devnetuser"
}

resp = requests.post(url, json.dumps(req_body), headers=headers, verify=False)

print("Ticket request status:", resp.status_code)

response_json = resp.json()
serviceTicket = response_json["response"]["serviceTicket"]
print("The service ticket number is:", serviceTicket)
