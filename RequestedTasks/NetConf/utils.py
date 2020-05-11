#!/usr/bin/env python3
import RequestedTasks.NetConf.netconf as netconf
import RequestedTasks.NetConf.ssh as ssh
from tabulate import tabulate
from RequestedTasks.exceptions import DataError, RequestError


def get_interfaces(device):
    with ssh.create_connection(device) as con:
        interfaces = ssh.get_ifaz_ip(con)

    with netconf.create_connection(device) as con:
        macs = netconf.get_ifaz_mac(con)
        for mac in macs:
            for interface in interfaces:
                if interface["name"] == mac["name"]:
                    del mac["index"]  # Remove that key to avoid updating interface's index
                    interface.update(mac)

        # ips = netconf.get_ifaz_ip(con)  # Adding this netmask could be obtained
        # for ip in ips:
        #     for interface in interfaces:
        #         if interface["name"] == ip["name"]:
        #             del ip["index"]  # Remove that key to avoid updating interface's index
        #             interface.update(ip)  # Not checking again the IP as it should be the same
    return interfaces


# Internal function
def __print_interfaces(interfaces):
    table_header = ["Index", "Name", "IP", "MAC"]

    # Adjust the data to needed info
    data = []
    i = 0
    for interface in interfaces:
        item = [
            i,
            interface["name"],
            interface["ip"],
            interface["mac"]
        ]
        i += 1
        data.append(item)

    print("-- Interface table --")
    print(tabulate(data, table_header))


def print_interfaces(device):
    try:
        interfaces = get_interfaces(device)
        __print_interfaces(interfaces)
    except (DataError, RequestError) as e:
        print(e)


def create_interface(device):
    try:
        with netconf.create_connection(device) as con:
            print("Loopback interface creation wizard")
            name = input("Insert interface index: ")
            descr = input("Insert a short description: ")
            addr = input("Insert IP: ")
            mask = input("Insert mask: ")
            netconf.create_ifaz(con, name, addr, mask, descr)
    except (DataError, RequestError) as e:
        print(e)


def remove_interface(device):
    try:
        interfaces = get_interfaces(device)
        interfaces[:] = [ifaz for ifaz in interfaces if str(ifaz["name"]).startswith("Loopback")]
        if len(interfaces) > 0:
            print("CAUTION: If a previous request has failed this action might fail. If that is the case, please, be patient and try again later")
            __print_interfaces(interfaces)

            opt = int(input("Select which interface you want to remove (index): "))

            if opt < 0 or opt > len(interfaces):
                raise ValueError()

            with netconf.create_connection(device) as con:
                netconf.delete_ifaz(con, interfaces[opt]["name"].lstrip("Loopback"))
        else:
            print("There are no Loopback interfaces to remove")
    except (DataError, RequestError) as e:
        print(e)
    except ValueError:
        print("Invalid option, try again")


def get_routing(device):
    with netconf.create_connection(device) as con:
        routing_table = netconf.get_routing(con)

    return routing_table


def print_routing(device):
    try:
        routing = get_routing(device)
        table_header = {"index": "Index", "dest_net": "Dest Net", "egress_ifaz": "Egress Ifaz"}

        print("-- Routing table --")
        print(tabulate(routing, table_header))
    except (DataError, RequestError) as e:
        print(e)


def print_netconf_session_stats(device):
    try:
        with netconf.create_connection(device) as con:
            stats = netconf.get_session_stats(con)
            table_header = {"index": "Index", "id": "Id", "host": "Source host", "time": "Cx Time"}

            print("-- Netconf stats --")
            print("Total requests:", stats["req_total"])
            print("Malformed requests:", stats["req_fail"])
            print("Error responses:", stats["res_fail"])
            print("\n-- Netconf active sessions --")
            print(tabulate(stats["active_sessions"], table_header))
    except (DataError, RequestError) as e:
        print(e)


def print_memory_usage(device):
    try:
        with netconf.create_connection(device) as con:
            usage = netconf.get_memory_usage(con)
            table_header = {"index": "Index", "pid": "PID", "name": "Proc Name", "alloc": "Allocated Mem",
                            "freed": "Freed Mem",
                            "hold": "Holding Mem"}

            print("-- Memory usage stats --")
            print(tabulate(usage, table_header))
    except (DataError, RequestError) as e:
        print(e)
