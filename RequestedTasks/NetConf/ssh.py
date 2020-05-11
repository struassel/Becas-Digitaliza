#!/usr/bin/env python3

from netmiko import ConnectHandler
from RequestedTasks.exceptions import ConnectionError, AuthError, DataError
import netmiko


def create_connection(device):
    try:
        conn = ConnectHandler(
            ip=device["address"],
            port=device["ssh_port"],
            username=device["username"],
            password=device["password"],
            device_type=device["device"])
    except KeyError as e:
        raise ConnectionError("Invalid device data, some fields are missing") from e
    except netmiko.ssh_exception.NetmikoTimeoutException as e:
        raise ConnectionError(
            "Connection timeout while connecting to {}:{}".format(device["address"], device["ssh_port"])) from e
    except netmiko.ssh_exception.NetmikoAuthenticationException as e:
        raise AuthError("Invalid username or password") from e
    return conn


def get_ifaz_ip(connection):
    resp = connection.send_command("show ip int brief")
    try:
        resp_data = resp.split("\n")[1:]
        i = 0
        interfaces = []
        for data in resp_data:
            interface = data.split()
            ifaz = {
                "index": i,
                "name": interface[0],
                "ip": interface[1],
            }
            i += 1
            interfaces.append(ifaz)
    except (IndexError, TypeError, AttributeError) as e:
        raise DataError("Error obtaining interfaces IP") from e

    return interfaces


if __name__ == '__main__':
    device = {
        "name": "Router CSR1000v",
        "ssh_port": 22,
        "netconf_port": 830,
        "username": "cisco",
        "password": "cisco123!",
        "device": "cisco_ios"
    }
    try:
        create_connection(device)
    except ConnectionError:
        pass

    try:
        device["address"] = "192.168.56.111"
        create_connection(device)
    except ConnectionError:
        pass

    try:
        device["address"] = "192.168.56.101"
        device["ssh_port"] = "23"
        create_connection(device)
    except ConnectionError:
        pass

    try:
        device["username"] = "cisc"
        device["ssh_port"] = "22"
        create_connection(device)
    except AuthError:
        pass

    device["username"] = "cisco"
    con = create_connection(device)

    try:
        get_ifaz_ip(None)
    except AttributeError:
        pass

    get_ifaz_ip(con)
