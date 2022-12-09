import os

from SFTP import SftpClient
from connection import sshConnect


class Services(sshConnect, SftpClient):

    def __init__(self, hostname=None, port=None, user=None, password=None):
        super().__init__(hostname, port, user, password)
        # print(hostname, port, user, password)

    def supplyCertsAndKeys(self):

        certList_localePath = ["CMS.key", "Server.cer", "ca-bundle22.cer", "Chain.cer"]
        certList_remotePath = ["/CMS.key", "/Server.cer", "/ca-bundle22.cer", "/Chain.cer"]
        self.upload(certList_localePath, certList_remotePath)

    # def setDNS(self):
    #     # Setting DNS
    #     self.execCommand("dns add forwardzone xchange.lab 10.77.197.55")
    #     self.execCommand("dns add forwardzone xchange.lab 10.77.205.244")
    #
    def webadminConfigure(self, sshClient_Object):
        # for webadmin
        try:
            self.execCommand("webadmin disable", sshClient_Object)
            self.execCommand("webadmin certs CMS.key Server.cer", sshClient_Object)
            self.execCommand("webadmin listen a 443", sshClient_Object)
            self.execCommand("webadmin enable", sshClient_Object)
            self.execCommand("webadmin", sshClient_Object)
            return "Success"
        except Exception as e:
            print(str(e))

    def callBridgeConfigure(self, sshClient_Object):
        # for callbridge
        try:
            self.execCommand("callbridge certs CMS.key Server.cer ca-bundle22.cer", sshClient_Object)
            self.execCommand("callbridge trust c2w ca-bundle22.cer", sshClient_Object)
            self.execCommand("callbridge listen a", sshClient_Object)
            self.execCommand("callbridge restart", sshClient_Object)
            self.execCommand("callbridge", sshClient_Object)
            return "Success"
        except Exception as e:
            print(str(e))

    def webbridgeConfigure(self, sshClient_Object):
        # for webbridge
        try:
            self.execCommand("webbridge3 disable", sshClient_Object)
            self.execCommand("webbridge3 https certs CMS.key Chain.cer", sshClient_Object)
            self.execCommand("webbridge3 https listen a:344", sshClient_Object)
            self.execCommand("webbridge3 c2w certs CMS.key Chain.cer", sshClient_Object)
            self.execCommand("webbridge3 c2w listen a:9999", sshClient_Object)
            self.execCommand("webbridge3 c2w trust ca-bundle22.cer", sshClient_Object)
            self.execCommand("webbridge3 restart", sshClient_Object)
            self.execCommand("webbridge3", sshClient_Object)
            return "Success"
        except Exception as e:
            print(str(e))

    def verifyServices(self, message):
        if message == "Success":
            print("Services configured successfully")
        else:
            print(Exception)

#
# ob = Services()
# ob.supplyCertsAndKeys()