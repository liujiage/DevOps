import subprocess
import pandas as pd

from common.StrUtils import isEmpty
from services.ParseService import parseHistoryDetailById
from services.dao.LogDao import LogDao


'''
@Author Jiage
@Date 2021-09-09
@Function get history deploys records
'''

class HistoryView:

    logDao = LogDao()

    @staticmethod
    def loadView() -> list:
        return HistoryView.logDao.query()

    @staticmethod
    def loadDetail(deployId) -> str:
        if isEmpty(deployId):
            return None
        str = ""
        cmd = parseHistoryDetailById(deployId)
        with subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, universal_newlines=True) as p:
            for line in iter(p.stdout.readline, ""):
                str = str + line
        #print("result {0}".format(str))
        return str