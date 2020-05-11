#!/usr/bin/env python3
import RequestedTasks.APICEM.apicem_http as apicem
from RequestedTasks.exceptions import DataError, RequestError
from tabulate import tabulate


def get_hosts(endpoint, host_id=""):
    host_list = []
    try:
        if host_id == "":
            response = apicem.get(endpoint, "host")
            i = 0
            for item in response[1]["response"]:
                host = [
                    i,
                    item["id"],
                    item["hostType"],
                    item["hostIp"],
                    item["hostMac"]
                ]
                i += 1
                host_list.append(host)
        else:
            response = apicem.get(endpoint, "host/{}".format(host_id))
            host = [
                0,
                response[1]["response"]["id"],
                response[1]["response"]["hostType"],
                response[1]["response"]["hostIp"],
                response[1]["response"]["hostMac"]
            ]
            host_list.append(host)
    except KeyError as e:
        raise DataError("Cannot parse host info") from e

    return host_list


def get_devices(endpoint, device_id=""):
    dev_list = []
    try:
        if device_id == "":
            response = apicem.get(endpoint, "network-device")
            i = 0
            for item in response[1]["response"]:
                dev = [
                    i,
                    item["id"],
                    item["hostname"],
                    item["type"],
                    item["managementIpAddress"],
                    item["macAddress"]
                ]
                i += 1
                dev_list.append(dev)
        else:
            response = apicem.get(endpoint, "network-device/{}".format(device_id))
            dev = [
                0,
                response[1]["response"]["id"],
                response[1]["response"]["hostname"],
                response[1]["response"]["type"],
                response[1]["response"]["managementIpAddress"],
                response[1]["response"]["macAddress"]
            ]
            dev_list.append(dev)
    except KeyError as e:
        raise DataError("Cannot parse network-device info") from e
    return dev_list


def get_reachability_info(endpoint, addr=""):
    reachability_info = []
    try:
        if addr == "":
            response = apicem.get(endpoint, "reachability-info")
            i = 0
            for data in response[1]["response"]:
                info = [
                    i,
                    data["mgmtIp"],
                    data["discoveryStartTime"],
                    data["reachabilityStatus"],
                    data["reachabilityFailureReason"]
                    if "reachabilityFailureReason" in data else ""
                ]
                i += 1
                reachability_info.append(info)
        else:
            response = apicem.get(endpoint, "reachability-info/ip-address/{}".format(addr))
            info = [
                0,
                response[1]["response"]["mgmtIp"],
                response[1]["response"]["discoveryStartTime"],
                response[1]["response"]["reachabilityStatus"],
                response[1]["response"]["reachabilityFailureReason"]
                if "reachabilityFailureReason" in response[1]["response"] else ""
            ]
            reachability_info.append(info)
    except KeyError as e:
        raise DataError("Cannot parse reachability info") from e
    return reachability_info


def get_interfaces(endpoint, device_id=""):
    interfaces = []

    try:
        device_list = get_devices(endpoint, device_id)

        if device_id == "":
            response = apicem.get(endpoint, "interface")
        else:
            response = apicem.get(endpoint, "interface/network-device/{}".format(device_id))

        i = 0
        for data in response[1]["response"]:
            device = None
            for dev in device_list:
                if dev[1] == data["deviceId"]:
                    device = dev

            info = [
                i,
                device[2] if device is not None else "",
                data["portName"],
                data["status"],
                data["adminStatus"],
                data["interfaceType"],
                data["portMode"],
                data["ipv4Address"],
                data["ipv4Mask"]
            ]
            i += 1
            interfaces.append(info)
    except KeyError as e:
        raise DataError("Cannot parse interfaces info") from e
    return interfaces


def print_apic_endpoints(endpoints):
    i = 0
    err = False
    for endpoint in endpoints:
        try:
            print(i, ": ", endpoint["name"], " (", endpoint["host"], ")", sep="")
            i += 1
        except KeyError:
            print("Malformed endpoint entry, ignoring it")
            err = True
    if i == 0 and err:
        raise DataError("All entries are malformed")


def __print_hosts(host_list):
    table_header = ["Index", "Id", "Type", "IP", "MAC"]
    print(tabulate(host_list, table_header))


def print_hosts(endpoint, host_id=""):
    try:
        host_list = get_hosts(endpoint, host_id)
        __print_hosts(host_list)
    except (RequestError, DataError) as e:
        print(e)


def __print_devices(dev_list):
    table_header = ["Index", "Id", "Name", "Type", "IP", "MAC"]
    print(tabulate(dev_list, table_header))


def print_devices(endpoint, device_id=""):
    try:
        dev_list = get_devices(endpoint, device_id)
        __print_devices(dev_list)
    except (RequestError, DataError) as e:
        print(e)


def __print_reachability_info(reachability_info):
    table_header = ["Index", "IP", "Discovery Time", "Status", "Failure Reason"]
    print(tabulate(reachability_info, table_header))


def print_reachability_info(endpoint, addr=""):
    try:
        reachability_info = get_reachability_info(endpoint, addr)
        __print_reachability_info(reachability_info)
    except (RequestError, DataError) as e:
        print(e)


def __print_interfaces(interfaces):
    table_header = ["Index", "Hostname", "Ifaz Name", "Status", "Admin Status", "Type", "Mode", "IP", "Netmask"]
    print(tabulate(interfaces, table_header))


def print_interfaces(endpoint, device_id=""):
    try:
        interfaces = get_interfaces(endpoint, device_id)
        __print_interfaces(interfaces)
    except (RequestError, DataError) as e:
        print(e)


def print_interfaces_of_device(endpoint):
    try:
        dev_list = get_devices(endpoint)
        __print_devices(dev_list)

        opt = int(input("Select device (index): "))
        if opt < 0 or opt > len(dev_list):
            raise ValueError()

        print_interfaces(endpoint, dev_list[opt][1])
    except (RequestError, DataError) as e:
        print(e)
    except ValueError:
        print("Invalid option, try again")
