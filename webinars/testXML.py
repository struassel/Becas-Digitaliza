
import xmltodict
from pprint import pprint

xml=open("test.xml").read()
print("xml: "+xml)
xmldict=xmltodict.parse(xml)
pprint(xmldict)
del xmldict["Hola"]["Gah"]
xml_final=xmltodict.unparse(xmldict, pretty=True)
print("XML Final: ",xml_final)