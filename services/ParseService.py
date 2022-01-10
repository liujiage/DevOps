from vo.DeployVO import DeployVO
from vo.LogVO import LogVO
from vo.ServiceVO import ServiceVO
from common.FileUtils import getFiles
import common.ConfigUtils as cf
import common.SortUtils as st

'''
@function parse the service's config
@Author Jiage
@Date 2021-08-20
@description 
    1) service name at first line
    2) after service name is service's ip addresses
    3) after service's ip is other service's parameter.
       service_port is service http port
'''


def parseServiceConfig():
    confs = cf.getConfig()
    dcf = confs.get(cf.CUR_SERVICE_CONFIG_FOLDER)
    res = {}
    fs = getFiles(dcf)
    for f in fs:
        # get service's information from config os file
        c = getServices(f)
        if len(c) == 0: break
        serviceName = c[0].name
        res.setdefault(serviceName, c)
    # sort the result asc
    return st.sort(res)

def getServiceByName(serviceName) -> []:
    services = parseServiceConfig()
    return services.get(serviceName)

'''
@function parse the service's config
@Author Jiage
@Date 2021-08-20
'''


def getServices(fileName: str):
    res = []
    with open(fileName, mode='r', encoding='utf-8', errors='ignore') as f:
        ips = []
        serviceName = ""
        servicePort = 0
        # get all ip
        n = 0
        isIp = True
        # parse service's config from a file
        for item in f:
            s = item.strip()
            if len(s) == 0: continue
            n = n + 1
            # 1) get service's name. At first,it is a service's name
            if n == 1:
                serviceName = s.replace("[", "").replace("]", "")
                continue
            if s.__contains__(serviceName + ":vars"):
                isIp = False
                continue
            if isIp:
                # 2) get service's all ips.
                ips.append(s)
            if s.startswith("service_port="):
                servicePort = int(s.replace("service_port=", ""))
        # mapping the config to a object
        if len(ips) == 0: return;
        for ip in ips:
            res.append(ServiceVO(ip, serviceName, enable=ip.startswith("#"), port=servicePort))

    print(res)
    return res


# the result format ./deploy-web.sh account 397 dp 10.30.0.48,10.30.0.49 1
# the param format version-100,tiny-192.168.1.0,tiny-192.168.1.2
# the command is sshpass -p 'pasword' ssh user_name@10.30.0.77 '/home/user_name/ansible/deploy-web.sh tiny 2591 dp 10.30.0.49'
def parseDeployRequest(param) -> DeployVO:
    conf = cf.getConfig()
    c = conf.get(cf.CUR_DEPLOY_SERVICE)
    es = conf.get(cf.EVN_SWITCH)
    sp = conf.get(cf.CUR_SSHPASS)
    n = "dp"
    if es == cf.EVN_PRODUCT_CONST:
        n = "master"
    # n = "dp"
    # c = "./deploy-web.sh"
    # param = "version-100,tiny-192.168.1.0,tiny-192.168.1.2"
    ps = param.split(",")
    v, s, ip = "", "", ""
    v = ps[0].split("-")[1]
    s = ps[1].split("-")[0]
    ip = param.replace(ps[0] + ",", "").replace(s + "-", "").replace("#", "")
    r = "{0} {1} {2} {3} {4}".format(c, s, v, n, ip)
    # running local shell if sp is empty
    if len(sp) == 0:
        print("{0}".format(r))
        return DeployVO(r, LogVO(serviceName=s, version=v, nodes=ip))
    # running a remote shell if sp is not empty
    r = sp + " '" + r + "'"
    print("{0}".format(r))
    return DeployVO(r, LogVO(serviceName=s, version=v, nodes=ip))


# the command is sshpass -p 'pasword' ssh user_name@10.30.0.77 '/home/user_name/watch/select_mem.sh'
def parseMemoryQuery():
    conf = cf.getConfig()
    c = conf.get(cf.CUR_MEMORY_SERVICE)
    sp = conf.get(cf.CUR_SSHPASS)
    # running local shell if sp is empty
    if len(sp) == 0:
        print("{0}".format(c))
        return c
    r = sp + " '" + c + "'"
    print("{0}".format(r))
    return r

'''
@Function get the history detail by deploy id
@Author Jiage
@Date 2021-09-13
'''
def parseHistoryDetailById(deployId):
    conf = cf.getConfig()
    c = conf.get(cf.CUR_HISTORY_FOLDER)
    sp = conf.get(cf.CUR_SSHPASS)
    # running local shell if sp is empty
    cmd = "cat {0}/{1}".format(c, deployId)
    if len(sp) == 0:
        print(cmd)
        return cmd
    r = sp + " '" + cmd + "'"
    print(r)
    return r