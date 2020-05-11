from device_info import ios_xe1
from ncclient import manager
import xml.dom.minidom

if __name__ == '__main__':
    with manager.connect(host=ios_xe1["address"], port=ios_xe1["netconf_port"],
                         username=ios_xe1["username"],
                         password=ios_xe1["password"],
                         hostkey_verify=False) as con:
        reply = con.get_config(source="running")
        print(reply)
        print(xml.dom.minidom.parseString(reply.xml).toprettyxml())

        filter = """
        <filter>
            <native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native"/>
        </filter>
        """
        # Get config and state info for interface
        reply = con.get_config(source='running', filter=filter)

        print(xml.dom.minidom.parseString(reply.xml).toprettyxml())
