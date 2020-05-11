from webinars.device_info import ios_xe1
from ncclient import manager
import xml.dom.minidom
import xmltodict
from tabulate import tabulate


if __name__ == '__main__':
    with manager.connect(host=ios_xe1["address"], port=ios_xe1["netconf_port"],
                         username=ios_xe1["username"],
                         password=ios_xe1["password"],
                         hostkey_verify=False) as con:
        filter = """
        <filter>
            <interfaces-state xmlns="urn:ietf:params:xml:ns:yang:ietf-interfaces"/>
        </filter>
        """
        # Get config and state info for interface
        reply = con.get(filter)

        print(xml.dom.minidom.parseString(reply.xml).toprettyxml())

        # Process XML and store useful dictionaries
        intf_details = xmltodict.parse(reply.xml)["rpc-reply"]["data"]

        ifazList=[]
        for intf_config in intf_details["interfaces-state"]["interface"]:
            # print("")
            # print("Interface details:")
            # print("\tName: {}".format(intf_config["name"]))
            # print("\tType: {}".format(intf_config["type"]["#text"]))
            # print("\tMAC: {}".format(intf_config["phys-address"]))
            # print("\tPackets Input: {}".format(intf_config["statistics"]["in-unicast-pkts"]))
            # print("\tPackets output: {}".format(intf_config["statistics"]["out-unicast-pkts"]))
            ifaz = [
                intf_config["name"],
                intf_config["type"]["#text"],
                intf_config["phys-address"],
                intf_config["statistics"]["in-unicast-pkts"],
                intf_config["statistics"]["out-unicast-pkts"]
            ]
            ifazList.append(ifaz)

        header=["Name", "Type", "MAC", "Packets output", "Packets input"]
        print(tabulate(ifazList, header))