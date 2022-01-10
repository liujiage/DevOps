import configparser
import os

'''
Shell command config
'''
EVN_SWITCH = "evn.switch"
DT_DEPLOY_SERVICE = "dt.deploy.service"
DT_SERVICE_CONFIG_FOLDER = "dt.service.config.folder"
DT_SSHPASS = "dt.sshpass"
DT_MEMORY_SERVICE = "dt.memory.service"
DT_HISTORY_FOLDER = "dt.history.folder"
DT_SERVICE_LOG_FOLDER = "dt.service.log.folder"

PRE_DEPLOY_SERVICE = "pre.deploy.service"
PRE_SERVICE_CONFIG_FOLDER = "pre.service.config.folder"
PRE_SSHPASS = "pre.sshpass"
PRE_MEMORY_SERVICE = "pre.memory.service"
PRE_HISTORY_FOLDER = "pre.history.folder"
PRE_SERVICE_LOG_FOLDER = "pre.service.log.folder"

CUR_DEPLOY_SERVICE = "cur.deploy.service"
CUR_SERVICE_CONFIG_FOLDER = "cur.service.config.folder"
CUR_SSHPASS = "cur.sshpass"
CUR_MEMORY_SERVICE = "cur.memory.service"
CUR_HISTORY_FOLDER = "cur.history.folder"
CUR_SERVICE_LOG_FOLDER = "cur.service.log.folder"

EVN_DEVELOP_CONST = "dt"
EVN_TEST_CONST = "pre"
EVN_PRODUCT_CONST = "pro"

'''
LDAP authentication config
'''
LDAP_SERVER = "ldap.server"
LDAP_DOMAIN = "ldap.domain"
LDAP_ENABLE = "ldap.enable"

'''
Database config
'''
SQLITE_FILE = "sqlite.file"

'''
@function setting different environments
@Author Jiage
@Date 2021-08-20
@description 
   @see project/resources/config.properties
   evn.switch {dt|pre}
      dt is develop environment 
      pre is testing environment
      pro is product environment
'''


def getConfig():
    config = configparser.RawConfigParser()
    filePath = os.path.join(os.path.abspath(os.curdir), 'resources', 'config.properties')
    print("filePath "+filePath)
    config.read(filePath)
    # get shell command config
    cd = dict(config.items("SHELL_CONFIG"))
    es = cd.get(EVN_SWITCH)
    if (es == EVN_DEVELOP_CONST):
        cd.setdefault(CUR_DEPLOY_SERVICE, cd.get(DT_DEPLOY_SERVICE))
        cd.setdefault(CUR_SERVICE_CONFIG_FOLDER, cd.get(DT_SERVICE_CONFIG_FOLDER))
        cd.setdefault(CUR_SSHPASS, cd.get(DT_SSHPASS))
        cd.setdefault(CUR_MEMORY_SERVICE, cd.get(DT_MEMORY_SERVICE))
        cd.setdefault(CUR_HISTORY_FOLDER, cd.get(DT_HISTORY_FOLDER))
        cd.setdefault(CUR_SERVICE_LOG_FOLDER, cd.get(DT_SERVICE_LOG_FOLDER))
    elif (es == EVN_TEST_CONST):
        cd.setdefault(CUR_DEPLOY_SERVICE, cd.get(PRE_DEPLOY_SERVICE))
        cd.setdefault(CUR_SERVICE_CONFIG_FOLDER, cd.get(PRE_SERVICE_CONFIG_FOLDER))
        cd.setdefault(CUR_SSHPASS, cd.get(PRE_SSHPASS))
        cd.setdefault(CUR_MEMORY_SERVICE, cd.get(PRE_MEMORY_SERVICE))
        cd.setdefault(CUR_HISTORY_FOLDER, cd.get(PRE_HISTORY_FOLDER))
        cd.setdefault(CUR_SERVICE_LOG_FOLDER, cd.get(PRE_SERVICE_LOG_FOLDER))
    # get ldap config
    ld = dict(config.items("LDAP_CONFIG"))
    # get database config
    db = dict(config.items("DB_CONFIG"))
    rd = {**cd, **ld}
    rs = {**rd, **db}

    return rs
