import os
import time
import paramiko
import sys


class sshConnect:
    def __init__(self, hostname=None, port=22, user="admin", password="wombat"):
        self.list1 = None
        self.fileCount = None
        self.hostname = hostname
        self.port = port
        self.user = user
        self.password = password
        print("h1", self.hostname, self.port, self.user, self.password)

    def SSH_Connect(self):
        try:
            global client
            client = paramiko.SSHClient()
            client.load_system_host_keys()
            client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            print("h2", self.hostname, self.port, self.user, self.password)
            client.connect(hostname=self.hostname, port=self.port, username=self.user, password=self.password)
            # client.close()

            return client
        except Exception as err:
            print(str(err))

    def execCommand(self, cmd, sshObject):
        try:
            self.cmd = cmd
            stdin, stdout, stderr = sshObject.exec_command(self.cmd)
            time.sleep(1.5)
            out = stdout.read().decode()
            # print(out)
            if out == "":
                pass
            else:
                with open("log.txt", "a") as f:
                    f.write("==================================\n"
                            + out + "==================================")
        except Exception as e:
            print(str(e))

