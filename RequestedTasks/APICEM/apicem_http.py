#!/usr/bin/env python3
import requests
import json
from RequestedTasks.exceptions import ConnectionError, AuthError, DataError, RequestError

requests.packages.urllib3.disable_warnings()


class TicketError(Exception):
    pass


def create_url(host, path):
    """Function to create APICEM API URLs"""
    return "https://{}/api/v1/{}".format(host, path)


# Simplify common HTTP functions and checks
def get(endpoint, path, headers=None, with_ticket=True):
    if headers is None:
        headers = {}

    try:
        url = create_url(endpoint["host"], path)
    except KeyError as e:
        raise ConnectionError("Invalid endpoint data, some fields are missing") from e

    headers["Content-Type"] = "application/json"
    if with_ticket:
        headers["X-Auth-Token"] = get_ticket(endpoint)

    try:
        resp = requests.get(url, headers=headers, verify=False)
        if resp.status_code == 401:
            if with_ticket:
                raise TicketError("Invalid ticket: {}".format(headers["X-Auth-Token"]))
            else:
                raise AuthError("Unauthorized request")

        resp.raise_for_status()

        response = [
            resp.status_code,
            resp.json()
        ]
    except requests.exceptions.HTTPError as e:
        raise RequestError("GET returned an error") from e
    except requests.exceptions.RequestException as e:
        raise ConnectionError("An error occurred while trying to GET from " + url) from e
    except json.decoder.JSONDecodeError as e:
        raise DataError("Malformed response") from e

    #print("Response code:", resp.status_code)
    #print("Response body:\n", resp.text)
    return response


def post(endpoint, path, headers=None, body=None, with_ticket=True):
    if headers is None:
        headers = {}
    if body is None:
        body = {}

    try:
        url = create_url(endpoint["host"], path)
    except KeyError as e:
        raise ConnectionError("Invalid endpoint data, some fields are missing") from e

    headers["Content-Type"] = "application/json"

    if with_ticket:
        headers["X-Auth-Token"] = get_ticket(endpoint)

    try:
        resp = requests.post(url, json.dumps(body), headers=headers, verify=False)
        if resp.status_code == 401:
            if with_ticket:
                raise TicketError("Invalid ticket: {}".format(headers["X-Auth-Token"]))
            else:
                raise AuthError("Invalid username or password")

        resp.raise_for_status()

        response = [
            resp.status_code,
            resp.json()
        ]
    except requests.exceptions.HTTPError as e:
        raise RequestError("POST returned an error") from e
    except requests.exceptions.RequestException as e:
        raise ConnectionError("An error occurred while trying to POST to " + url) from e
    except json.decoder.JSONDecodeError as e:
        raise DataError("Malformed response") from e
    
    print("Response code:", resp.status_code)
    print("Response body:\n", resp.text)
    return response


def get_ticket(endpoint):
    """Get access ticket"""

    try:
        req_body = {
            "password": endpoint["pass"],
            "username": endpoint["user"]
        }
    except KeyError as e:
        raise ConnectionError("Invalid endpoint data, some fields are missing") from e

    resp = post(endpoint, "ticket", body=req_body, with_ticket=False)

    try:
        service_ticket = resp[1]["response"]["serviceTicket"]
    except KeyError as e:
        raise AuthError("Cannot obtain authentication ticket") from e

    return service_ticket


if __name__ == '__main__':
    import sys

    try:
        device = {"host": "sandboxapicem.cisco.com",
                  "user": "devnetuser",
                  "pass": "Cisco123!"}
        print("Returned ticket:", get_ticket(device))
    except ConnectionError as e:
        pass

    try:
        device = {"host": "sandboxapicem.cis/co.com",
                  "user": "devnetuser",
                  "pass": "Cisco123!"}
        print("Returned ticket:", get_ticket(device))
        sys.exit(-1)
    except ConnectionError as e:
        pass

    try:
        device = {"host": "sandboxapicem.cisco.com",
                  "user": "devnetuser4",
                  "pass": "Cisco123!"}
        print("Returned ticket:", get_ticket(device))
        sys.exit(-1)
    except AuthError as e:
        pass

    try:
        device = {"host": "sandboxapicem.cisco.com",
                  "user": "",
                  "pass": ""}
        print("Returned ticket:", get_ticket(device))
        sys.exit(-1)
    except RequestError as e:
        pass

    try:
        device = {"host": "sandboxapicem.cisco.com/",
                  "user": "devnetuser",
                  "pass": "Cisco123!"}
        print("Returned ticket:", get_ticket(device))
        sys.exit(-1)
    except RequestError as e:
        pass

    try:
        device = {"host": "https://sandboxapicem.cisco.com",
                  "user": "devnetuser",
                  "pass": "Cisco123!"}
        print("Returned ticket:", get_ticket(device))
        sys.exit(-1)
    except ConnectionError as e:
        pass

    try:
        device = {"host": "",
                  "user": "devnetuser",
                  "pass": "Cisco123!"}
        print("Returned ticket:", get_ticket(device))
        sys.exit(-1)
    except ConnectionError as e:
        pass

    try:
        device = {"host": "google.es",
                  "user": "devnetuser",
                  "pass": "Cisco123!"}
        print("Returned ticket:", get_ticket(device))
        sys.exit(-1)
    except RequestError as e:
        pass
