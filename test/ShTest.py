import os
import subprocess
import sys
import unittest
from subprocess import call
from subprocess import Popen, PIPE


class MyTestCase(unittest.TestCase):
    def test_command(self):
        r = os.system("cd /Users/liujiage/tmp/services/;./tiny.sh")
        with subprocess.Popen("df -h", shell=True, stdout=subprocess.PIPE) as p:
            print("res %s", r)
            p.wait(1000)
            lines = p.stdout.readlines()
            for line in lines:
                print(line.strip())

    def test_sh(self):
        # r = os.system("cd /Users/liujiage/tmp/services/;./tiny.sh")
        with subprocess.Popen("/Users/liujiage/tmp/services/tiny.sh 1000", cwd="/Users/liujiage/tmp/services",
                              shell=True, stdout=subprocess.PIPE, bufsize=1, universal_newlines=True) as p:
            # lines = p.stdout.readlines()
            for line in iter(p.stdout.readline, ""):
                print(line)
                # sys.stdout.flush()

    def test_remote_sh(self):
        ssh_cmd = "sshpass -p '*******' ssh user_name@10.30.0.77 '/home/user_name/ansible/deploy-web.sh tiny 2588 dp 10.30.0.49'"
        # status, output = subprocess.getstatusoutput(ssh_cmd)
        with subprocess.Popen(ssh_cmd, shell=True, stdout=subprocess.PIPE, bufsize=1, universal_newlines=True) as p:
            for line in iter(p.stdout.readline, ""):
                print(line)

    def test_cat(self):
        with subprocess.Popen("cat /Users/liujiage/tmp/history/20210913094820-liujiage-reward-788",
                              shell=True, stdout=subprocess.PIPE, bufsize=1, universal_newlines=True) as p:
            for line in iter(p.stdout.readline, ""):
                print(line)

    def test_tail(self):
        with subprocess.Popen("tail /Users/liujiage/tmp/history/20210913094820-liujiage-reward-788",
                              shell=True, stdout=subprocess.PIPE, bufsize=1, universal_newlines=True) as p:
            for line in iter(p.stdout.readline, ""):
                print(line)




if __name__ == '__main__':
    unittest.main()
