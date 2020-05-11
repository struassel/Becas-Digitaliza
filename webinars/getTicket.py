#!/usr/bin/env python3

import requests
import json
import urllib3
from pprint import pprint

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

print("Status code: " + str(resp.status_code) + " Objeto es " + str(resp.text))
print("Status code: {}. Objeto es {}".format(resp.status_code, resp.text))

resp_body=resp.json()
pprint(resp_body)

try:
    print("Ticket es: "+str(resp_body["response"]["serviceTicket"]))
except:
    print("Error: " + str(resp_body["response"]["errorCode"]))
