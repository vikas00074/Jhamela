from services import Services
from connection import sshConnect
# from cluster import Cluster

from SFTP import SftpClient
# from cerificate import Certificate


class Test(Services, SftpClient):

    def __init__(self, hostname=None, port=None, user=None, password=None):
        super().__init__(hostname, port, user, password)
        self.service = None
        self.call_verify = None
        self.web_admin_verify = None
        self.web_verify = None
        self.s1 = None

    def setup(self):
        self.sshClient = sshConnect(hostname, port, username, password)
        self.sshClient_Object = self.sshClient.SSH_Connect()

        self.sftpClient = SftpClient(hostname, port, username, password)
        self.sftpClient.create_connection(hostname, port, username, password)

        self.service = Services(hostname, port, username, password)
        self.service.supplyCertsAndKeys()
        pass

    def run(self):
        open('log.txt', 'w').close()
        self.web_admin_verify = self.webadminConfigure(self.sshClient_Object)
        self.verifyServices(self.web_admin_verify)
        self.call_verify = self.callBridgeConfigure(self.sshClient_Object)
        self.verifyServices(self.call_verify)
        self.web_verify = self.webbridgeConfigure(self.sshClient_Object)
        self.verifyServices(self.web_verify)

    def teardown(self):
        self.sftpClient.close()
        self.sshClient_Object.close()
        print("Connection closed successfully.....")
        pass


# Cluster_Size = int(input("Enter the cluster Size:"))
# Hostname = []
# for i in range(0, Cluster_Size):
#     Hostname.append(input("\n Enter the node IP: "))

# hostname = "10.77.198.149"
port = 22
username = "admin"
password = "wombat"

Cluster_Size = int(input("Enter the cluster Size:"))
Master = input("which Ip you want to choose as Master?")
role = {Master: 'master'}
Slave = []
Hostname = []
for i in range(0, Cluster_Size - 1):
    s = (input("\n Enter the slave node IP: "))
    Slave.append(s)
    role[s] = 'slave'
Hostname.append(Master)
Hostname = Hostname + Slave
for hostname in Hostname:
    test = Test(hostname, port, username, password)
    test.setup()
    test.run()
    test.teardown()
