import os

from flask import session

from services.ParseService import parseServiceConfig, parseDeployRequest, parseMemoryQuery, getServiceByName
from flask_socketio import SocketIO, emit
import common.ConfigUtils as cf
import subprocess

from services.dao.LogDao import LogDao
from vo.LogVO import LogVO
from vo.ServiceVO import ServiceVO


class DeployView:

    logDao = LogDao()

    @staticmethod
    def loadView():
        return parseServiceConfig()

    @staticmethod
    def deployService(service: str):
        print("deploy service parameter is " + service)
        r = os.system("cd /Users/liujiage/tmp/services/;./tiny.sh")
        return r

    '''
    @Help How to use the shell  
    $1 server name you want to deploy (eg:tiny)
    $2 version package's version by jenkis (eg:100)
    $3 resource code branch by gitlab (eg:dp)
    $4 ip address you want to deploy (eg:192.168.1.0)
    $5 enable testing (0 disable 1 enable)
    For example:
    ./deploy-web.sh account 397 dp 10.30.0.48,10.30.0.49 1
    @request 
       data, the data format version-100,tiny-192.168.1.0,tiny-192.168.1.2,.....
    '''

    @staticmethod
    def socketRequest(app, msg):
        event = msg['event']
        data = msg['data']
        if event == 'connect':
            app.logger.info('the client connecting and send message is ' + data)
        elif event == 'start_deploy':
            app.logger.info('the client sending start_deploy event, the message is ' + data)
            # call a shell to deploy the service and receiving the process log from the shell
            dds = parseDeployRequest(data)
            app.logger.info('the deploy command is ' + dds.cmd)
            with subprocess.Popen(dds.cmd, shell=True, stdout=subprocess.PIPE, bufsize=50, universal_newlines=True) as p:
                for line in iter(p.stdout.readline, ""):
                    emit('response', {'event': 'log', 'data': line.replace("\n", "")})
            # save deploys log into the database
            dds.service.userName = session['userid']
            service = getServiceByName(dds.service.serviceName)[0]
            dds.service.port = service.port
            DeployView.logDao.updateOrInsert(dds.service)
        elif event == 'query_memory':
            app.logger.info('the client sending query_memory event, the message is ' + data)
            cmd = parseMemoryQuery()
            with subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, bufsize=50, universal_newlines=True) as p:
                for line in iter(p.stdout.readline, ""):
                    emit('response', {'event': 'log-memory', 'data': line.replace("\n", "")})
        else:
            app.logger.error('Error, received a wrong request!')
