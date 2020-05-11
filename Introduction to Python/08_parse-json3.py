import urllib.parse
import requests

file=open("mapquest_key.txt", "r")
key=file.read()
file.close()
main_api = "https://www.mapquestapi.com/directions/v2/route?"

while True:
    orig = input("Starting Location: ")
    dest = input("Destination: ")

    url = main_api + urllib.parse.urlencode({"key": key, "from":orig, "to":dest})
    print("URL: " + (url))

    json_data = requests.get(url).json()
    #print(json_data)
    json_status = json_data["info"]["statuscode"]

    if json_status == 0:
        print("API Status: " + str(json_status) + " = A successful route call.\n")