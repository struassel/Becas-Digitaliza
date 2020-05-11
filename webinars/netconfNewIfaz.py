from webinars.device_info import ios_xe1
from ncclient import manager
import xml.dom.minidom


if __name__ == '__main__':
    with manager.connect(host=ios_xe1["address"], port=ios_xe1["netconf_port"],
                         username=ios_xe1["username"],
                         password=ios_xe1["password"],
                         hostkey_verify=False) as con:
        filter = """
        <filter>
            <native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">
               <interface/>
            </native>
        </filter>
        """

        config = """
                <config>
                    <native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">
                       <interface>
                            <Loopback>
                                <name>1</name>
                                <description>Test</description>
                                <ip>
                                    <address>
                                        <primary>
                                            <address>192.168.123.2</address>
                                            <mask>255.255.255.0</mask>
                                        </primary>
                                    </address>
                                </ip>
                            </Loopback>
                        </interface>
                    </native>
                </config>
        """

        set_conf_reply = con.edit_config(target='running', config=config)

        print(xml.dom.minidom.parseString(set_conf_reply.xml).toprettyxml())

        # Get config and state info for interface
        get_conf_reply = con.get_config(source='running', filter=filter)

        print(xml.dom.minidom.parseString(get_conf_reply.xml).toprettyxml())