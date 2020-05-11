from device_info import ios_xe1
from ncclient import manager
import xml.dom.minidom
import xmltodict
from tabulate import tabulate

if __name__ == '__main__':
    with manager.connect(host=ios_xe1["address"], port=ios_xe1["netconf_port"],
                         username=ios_xe1["username"],
                         password=ios_xe1["password"],
                         hostkey_verify=False) as con:
        netconf_filter = """
        <filter>
            <interfaces-state xmlns="urn:ietf:params:xml:ns:yang:ietf-interfaces"/>
        </filter>
        """
        # Get config and state info for interface
        reply = con.get(filter=netconf_filter)

        print(xml.dom.minidom.parseString(reply.xml).toprettyxml())

        # Process XML and store useful dictionaries
        netconf_reply_dict = xmltodict.parse(reply.xml)

        interfaces=list(netconf_reply_dict["rpc-reply"]["data"]["interfaces-state"]["interface"])
        for interface in interfaces:
            print("Name: {} MAC: {} Input: {} Output {}".format(
                interface["name"],
                interface["phys-address"],
                interface["statistics"]["in-octets"],
                interface["statistics"]["out-octets"]
               )
            )
