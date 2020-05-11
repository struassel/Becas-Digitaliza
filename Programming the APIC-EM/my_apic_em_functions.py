#!/usr/bin/env python3macAddress

import requests
import json
from tabulate import tabulate


def get_ticket(host, user, password):
    requests.packages.urllib3.disable_warnings()
    url = "https://" + host + "/api/v1/ticket"

    headers = {
        "Content-Type": "application/json"
    }

    req_body = {
        "password": password,
        "username": user
    }

    resp = requests.post(url, json.dumps(req_body), headers=headers, verify=False)

    if resp.status_code == 200:
        print("Ticket request status:", resp.status_code)

        response_json = resp.json()
        serviceticket = response_json["response"]["serviceTicket"]
        print("The service ticket number is:", serviceticket)
        return serviceticket
    else:
        raise Exception("Cannot obtain ticket Response text: " + resp.text)


def print_hosts(host, user, password):
    ticket = get_ticket(host, user, password)

    requests.packages.urllib3.disable_warnings()
    url = "https://" + host + "/api/v1/host"

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


def print_devices(host, user, password):
    ticket = get_ticket(host, user, password)

    requests.packages.urllib3.disable_warnings()
    url = "https://" + host + "/api/v1/network-device"

    headers = {
        "Content-Type": "application/json",
        "X-Auth-Token": ticket
    }

    resp = requests.get(url, headers=headers, verify=False)

    print("Status of /host request: ", resp.status_code)
    if resp.status_code != 200:
        raise Exception("Status code does not equal 200. Response text: " + resp.text)
    response_json = resp.json()

    dev_list = []
    i = 0
    for item in response_json["response"]:
        i += 1
        dev = [
            i,
            item["type"],
            item["managementIpAddress"]
        ]
        dev_list.append(dev)
    table_header = ["Number", "Type", "IP"]
    print(tabulate(dev_list, table_header))
