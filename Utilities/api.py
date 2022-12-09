from mimetypes import init

import requests
import xmltodict
import json
import urllib3
urllib3.disable_warnings()

class Api:
    def __init__(self, hostname="10.77.198.153", port=443, protocol="https://", user="admin", password="wombat"):
        self.hostname = hostname
        self.port = port
        self.user = user
        self.password = password
        self.protocol = protocol
        self.verify = False
        self.auth = ('admin', 'wombat')
        self.url = None

    def apiGet(self, method, params, id=None, timeout=10):
        # self.url = self.protocol+self.hostname+"/api/v1/"+method

        if params == "":
            self.url = self.protocol+self.hostname+"/api/v1/"+method
        else:
            self.url = self.protocol + self.hostname + "/api/v1/" + method + "/" + params

        r = requests.get(self.url, verify=self.verify, auth=self.auth)
        xpars = xmltodict.parse(r.text)
        self.json = json.dumps(xpars)
        return self.json

    def apiPut(self, method, data, params, timeout=10):
        # self.url = self.protocol+self.hostname+"/api/v1/"+method

        if params == "":
            self.url = self.protocol+self.hostname+"/api/v1/"+method
        else:
            self.url = self.protocol + self.hostname + "/api/v1/" + method + "/" + params

        r = requests.put(self.url, verify=self.verify, auth=self.auth)
        if r.status_code == 200:
            print("Method executed successfully...")
        else:
            print("Error: Api Put error")

    def apiPost(self, method, data, params="", timeout=10):
        self.verify = False
        self.auth = ('admin', 'wombat')
        self.data = data
        # self.params = params

        if params == "":
            self.url = self.protocol+self.hostname+"/api/v1/"+method
        else:
            self.url = self.protocol + self.hostname + "/api/v1/" + method + "/" + params

        r = requests.post(self.url, data=self.data, verify=self.verify, auth=self.auth)
        if r.status_code == 200:
            print("Method executed successfully...")
        else:
            print("Error: Api Put error")

api = Api()
post = {
    "url": "c2w://cms198-149.xchange.lab:9999"
}
post1 = {
    "name": "Server Default"
}
api.apiPost("webBridges", post)
jsonData = api.apiGet("webBridges", "status")
# print(json.loads(jsonData)["webBridges"]["webBridge"]["@id"])
# api.apiPost("webBridgeProfiles", post1)
jsonData1 = api.apiGet("webBridgeProfiles", "")
# print(json.loads(jsonData1)["webBridgeProfiles"])