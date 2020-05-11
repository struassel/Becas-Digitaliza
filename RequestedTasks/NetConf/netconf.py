#!/usr/bin/env python3

from ncclient import manager
import ncclient
import xmltodict
from xml.parsers.expat import ExpatError as ExpatError
from RequestedTasks.exceptions import ConnectionError, AuthError, DataError, RequestError


def create_connection(device):
    conn = None
    try:
        conn = manager.connect(
            host=device["address"],
            port=device["netconf_port"],
            username=device["username"],
            password=device["password"],
            hostkey_verify=False)
    except KeyError as e:
        raise ConnectionError("Invalid device data, some fields are missing") from e
    except ncclient.transport.errors.SSHError as e:
        raise ConnectionError(
            "Connection timeout while connecting to {}:{}".format(device["address"], device["ssh_port"])) from e
    except ncclient.transport.errors.AuthenticationError as e:
        raise AuthError("Invalid username or password") from e
    return conn


def get_config(connection, filter=None):
    try:
        reply = connection.get_config(source="running", filter=filter)
        data = xmltodict.parse(reply.xml)
    except ncclient.operations.RPCError as e:
        raise RequestError("Netconf get-config request returned an error") from e
    except ExpatError as e:
        raise DataError("Malformed response") from e
    return data


def get(connection, filter):
    try:
        reply = connection.get(filter=filter)
        data = xmltodict.parse(reply.xml)
    except ncclient.operations.RPCError as e:
        raise RequestError("Netconf get request returned an error") from e
    except ExpatError as e:
        raise DataError("Malformed response") from e
    return data


def edit_config(connection, config):
    try:
        reply = connection.edit_config(target="running", config=config)
        data = xmltodict.parse(reply.xml)
    except ncclient.operations.RPCError as e:
        raise RequestError("Netconf edit-config request returned an error") from e
    except ExpatError as e:
        raise DataError("Malformed response") from e
    return data


def get_ifaz_mac(connection):
    # Get-config not working for this filter. It just works with <get> command
    filter_get = """
       <filter>
           <interfaces-state xmlns="urn:ietf:params:xml:ns:yang:ietf-interfaces">
             <interface>
                 <name/>
                 <type/>
                 <if-index/>
                 <phys-address/>
              </interface>
            </interfaces-state>
       </filter>
       """

    get_res = get(connection, filter_get)

    try:
        interfaces = []
        i = 0
        data = get_res["rpc-reply"]["data"]["interfaces-state"]["interface"]
        if type(data) != list:
            data = [data]
        for interface in data:
            item = {
                "index": i,
                "name": interface["name"],
                "mac": interface["phys-address"],
                "if-index": interface["if-index"],
                "type": interface["type"]["#text"],
            }
            i += 1
            interfaces.append(item)
    except (TypeError, KeyError) as e:
        raise DataError("Error parsing interface info") from e

    return interfaces


def get_ifaz_ip(connection):
    filter_get_config = """
    <filter>
      <interfaces xmlns="urn:ietf:params:xml:ns:yang:ietf-interfaces">
        <interface>
          <name/>
          <ipv4 xmlns="urn:ietf:params:xml:ns:yang:ietf-ip"/>
          <ipv6 xmlns="urn:ietf:params:xml:ns:yang:ietf-ip"/>
        </interface>
      </interfaces>
    </filter>
    """

    get_res = get_config(connection, filter_get_config)
    try:
        interfaces = []
        i = 0
        data = get_res["rpc-reply"]["data"]["interfaces"]["interface"]
        if type(data) != list:
            data = [data]
        for interface in data:
            item = {}
            try:
                item["index"] = i
                item["name"] = interface["name"]
                item["ip"] = interface["ipv4"]["address"]["ip"]
                item["mask"] = interface["ipv4"]["address"]["netmask"]
            except KeyError:
                pass

            if "ip" not in item:
                print("Cannot obtain IP for " + item["name"] + " interface using netconf")

            i += 1
            interfaces.append(item)
    except (TypeError, KeyError) as e:
        raise DataError("Error parsing interface IPs") from e

    return interfaces


def get_routing(connection):
    filter_get_config = """
    <filter>
        <routing-state xmlns="urn:ietf:params:xml:ns:yang:ietf-routing">
            <routing-instance>
              <ribs>
                <rib>
                  <routes/>
                </rib>
              </ribs>
            </routing-instance>
      </routing-state>
    </filter>
    """

    get_res = get(connection, filter_get_config)

    try:
        routing_table = []
        i = 0
        data = get_res["rpc-reply"]["data"]["routing-state"]["routing-instance"]["ribs"]["rib"]["routes"]["route"]
        if type(data) != list:
            data = [data]
        for route in data:
            item = {
                "index": i,
                "dest_net": route["destination-prefix"]
            }

            try:
                item["egress_ifaz"] = route["next-hop"]["outgoing-interface"]
            except KeyError:
                print("Cannot obtain output interface for network ", route["destination-prefix"],
                      ". Adding it anyway...", sep="")
            i += 1
            routing_table.append(item)
    except (TypeError, KeyError) as e:
        raise DataError("Error parsing routing table") from e

    return routing_table


def get_session_stats(connection):
    filter_get_config = """
        <filter>
            <netconf-state xmlns="urn:ietf:params:xml:ns:yang:ietf-netconf-monitoring" >
                <sessions/>
                <statistics/>
            </netconf-state>
        </filter>
        """

    get_res = get(connection, filter_get_config)

    try:
        sessions = []
        i = 0
        data = get_res["rpc-reply"]["data"]["netconf-state"]["sessions"]["session"]
        if type(data) != list:
            data = [data]

        for session in data:
            item = {
                "index": i,
                "id": session["session-id"],
                "host": session["source-host"],
                "time": session["login-time"]
            }
            i += 1
            sessions.append(item)

        stats = {
            "active_sessions": sessions,
            "sessions_total": get_res["rpc-reply"]["data"]["netconf-state"]["statistics"]["in-sessions"],
            "req_total": get_res["rpc-reply"]["data"]["netconf-state"]["statistics"]["in-rpcs"],
            "req_fail": get_res["rpc-reply"]["data"]["netconf-state"]["statistics"]["in-bad-rpcs"],
            "res_fail": get_res["rpc-reply"]["data"]["netconf-state"]["statistics"]["out-rpc-errors"]
        }
    except (TypeError, KeyError) as e:
        raise DataError("Error parsing netconf statistics") from e

    return stats


def get_memory_usage(connection):
    filter_get_config = """
         <filter>
            <memory-usage-processes xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-process-memory-oper">
                <memory-usage-process/>
            </memory-usage-processes>
         </filter>
         """

    get_res = get(connection, filter_get_config)

    try:
        mem_usage = []
        i = 0
        data = get_res["rpc-reply"]["data"]["memory-usage-processes"]["memory-usage-process"]
        if type(data) != list:
            data = [data]
        for usage in data:
            item = {
                "index": i,
                "pid": usage["pid"],
                "name": usage["name"],
                "alloc": usage["allocated-memory"],
                "freed": usage["freed-memory"],
                "hold": usage["holding-memory"]
            }
            i += 1
            mem_usage.append(item)
    except (TypeError, KeyError) as e:
        raise DataError("Error parsing netconf statistics") from e

    return mem_usage


def create_ifaz(connection, index, address, mask="255.255.255.0", description=""):
    try:
        value = int(index)
        if value < 0:
            raise DataError("Invalid loopback interface index")
    except ValueError as e:
        raise DataError("Invalid loopback interface index") from e

    data = """<config>
             <native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">
              <interface>
               <Loopback>
                <name>""" + str(index) + """</name>
                """
    if description != "":
        data += """<description>""" + str(description) + """</description>
                """
    data += """<ip>
                 <address>
                  <primary>
                   <address>""" + str(address) + """</address>
                   <mask>""" + str(mask) + """</mask>
                  </primary>
                 </address>
                </ip>
               </Loopback>
              </interface>
             </native>
            </config>
            """
    reply = edit_config(connection, data)
    try:
        if "ok" in reply["rpc-reply"]:
            print("OK response received to interface creation request")
    except KeyError as e:
        raise DataError("Cannot parse data received as response to interface creation request") from e


def delete_ifaz(connection, index):
    try:
        value = int(index)
        if value < 0:
            raise DataError("Invalid loopback interface index")
    except ValueError as e:
        raise DataError("Invalid loopback interface index") from e

    data = """
            <config>
             <interfaces xmlns="urn:ietf:params:xml:ns:yang:ietf-interfaces">
                <interface operation="delete">
                    <name>Loopback""" + str(index) + """</name>
                </interface>
            </interfaces>
            </config>
            """
    reply = edit_config(connection, data)
    try:
        if "ok" in reply["rpc-reply"]:
            print("OK response received to interface removal request")
    except KeyError as e:
        raise DataError("Cannot parse data received as response to interface removal request") from e


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
        device["netconf_port"] = "23"
        create_connection(device)
    except ConnectionError:
        pass

    try:
        device["username"] = "cisc"
        device["netconf_port"] = "830"
        create_connection(device)
    except AuthError:
        pass

    device["username"] = "cisco"
    con = create_connection(device)

    print(get_ifaz_mac(con))
    print(get_ifaz_ip(con))
    print(get_routing(con))
    print(get_session_stats(con))
    print(get_memory_usage(con))
    # try:
    #     create_ifaz(con, "a71", "192.168.199.26", "255.255.255.0")
    # except DataError:
    #     pass

    create_ifaz(con, "71", "192.168.199.26", "255.255.255.0")

    # try:
    #     create_ifaz(con, "13", "192.168.199.26", "255.255.255.0")
    # except RequestError:
    #     pass
    #
    # try:
    #     delete_ifaz(con, "13")
    # except RequestError:
    #     pass
    #
    delete_ifaz(con, "71")
