#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os
import sys
import time
from subprocess import Popen, PIPE, STDOUT
import requests

curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath)
import Config

class AutoCase(object):
    cmd ='python3 -m unittest Entry/run.py'
    def RunCase(self):
        self.ProcessCMD = Popen(self.cmd, stdout=PIPE, stderr=STDOUT, shell=True)
        Check_Name = True
        Check_Result = False
        all =[]
        while self.ProcessCMD.poll() is None:
            Results = self.ProcessCMD.stdout.readline().decode("utf-8").strip().replace('\\n', '')
            print (Results)
            if Check_Name:
                item={}
                if 'INSTRUMENTATION_STATUS: CaseName=' in Results:
                    item['case']=Results.split('=')[1]
                    Check_Name = False
                    Check_Result = True
                    continue
            if Check_Result:
                if 'INSTRUMENTATION_STATUS: Detail' in Results:
                    item['caseName'] = Results.split('=')[1]
                if 'INSTRUMENTATION_STATUS: charger' in Results:
                    item['charger'] = Results.split('=')[1]
                if 'INSTRUMENTATION_STATUS: api' in Results:
                    item['api'] = Results.split('=')[1]
                if 'INSTRUMENTATION_STATUS: path' in Results:
                    item['model'] = Results.split('=')[1]
                if 'INSTRUMENTATION_STATUS: time' in Results:
                    item['useTime'] = int(Results.split('=')[1])
                if 'INSTRUMENTATION_STATUS: result' in Results:
                    if Results.split('=')[1] == 'Pass':
                        item['res'] = 0
                    else:
                        item['res'] = -1
                if 'INSTRUMENTATION_STATUS: log' in Results:
                    item['comment'] = Results.split('=')[1].replace('\'', '')\
                        .replace('"', '').replace('{', ' ')\
                        .replace('}', ' ').replace('[', ' ')\
                        .replace(']', ' ')
                    Check_Result = False
                    Check_Name = True
                    all.append(item)
                    continue
        jd = self.createDict(all)
        print(jd)

        res = requests.post('http://152.136.202.79:9092/server/monitor/push', json=jd)
        print(res.status_code)
        print('url:http://152.136.202.79:9092/web/watcher?only={0}'.format(jd['data']['only']))


    def createDict(self, item):
        result = {}
        data = {}
        data['rt'] = time.strftime("%Y-%m-%d %X", time.localtime())
        data['allCaseNum'] = len(item)
        data['FailCaseName'] = self.getFailed(item)
        data['only'] = time.strftime("%Y%m%d%H%M", time.localtime())
        data['result'] = item
        result['data'] = data
        return result

    def getFailed(self, lists):
        i = 0
        for line in lists:
            if line['res'] == -1:
                i += 1
        return i

Auto = AutoCase()
Auto.RunCase()