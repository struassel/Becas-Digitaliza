from device_info import ios_xe1
from ncclient import manager
import xml.dom.minidom


if __name__ == '__main__':
    with manager.connect(host=ios_xe1["address"], port=ios_xe1["netconf_port"],
                         username=ios_xe1["username"],
                         password=ios_xe1["password"],
                         hostkey_verify=False) as con:
        netconf_data = """
                <config>
                    <native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">
                       <hostname>NEWHOSTNAME</hostname>
                    </native>
                </config>
        """

        set_conf_reply = con.edit_config(target='running', config=netconf_data)

        print(xml.dom.minidom.parseString(set_conf_reply.xml).toprettyxml())

        netconf_data = """
        <config>
         <native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">
          <interface>
           <Loopback>
            <name>100</name>
            <description>TEST100</description>
            <ip>
             <address>
              <primary>
               <address>100.100.100.100</address>
               <mask>255.255.255.0</mask>
              </primary>
             </address>
            </ip>
           </Loopback>
          </interface>
         </native>
        </config>
        """


        set_conf_reply = con.edit_config(target='running', config=netconf_data)

        print(xml.dom.minidom.parseString(set_conf_reply.xml).toprettyxml())

        netconf_data = """
                <config>
                 <native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">
                  <interface>
                   <Loopback>
                    <name>111</name>
                    <description>TEST100</description>
                    <ip>
                     <address>
                      <primary>
                       <address>100.100.100.100</address>
                       <mask>255.255.255.0</mask>
                      </primary>
                     </address>
                    </ip>
                   </Loopback>
                  </interface>
                 </native>
                </config>
                """

        set_conf_reply = con.edit_config(target='running', config=netconf_data)

        print(xml.dom.minidom.parseString(set_conf_reply.xml).toprettyxml())