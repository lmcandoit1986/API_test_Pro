#!/usr/bin/python3
# -*- coding: utf-8 -*-
import os
import sys
from subprocess import Popen, PIPE, STDOUT

curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath)

class AutoCase(object):
    cmd ='python3 ./Entry/run.py'
    def RunCase(self):
        self.ProcessCMD = Popen(self.cmd, stdout=PIPE, stderr=STDOUT, shell=True)
        Check_Name = True
        Check_Result = False
        while self.ProcessCMD.poll() is None:
            Results = self.ProcessCMD.stdout.readline()
            print (Results)
            if Check_Name:
                item={}
                if 'INSTRUMENTATION_STATUS: CaseName=' in Results:
                    print('CaseName:{0}'.format(Results.split('=')[1]))
                    item['case']=Results.split('=')[1]
                    Check_Name = False
                    Check_Result = True
                    continue
            if Check_Result:
                if 'INSTRUMENTATION_STATUS: Detail' in Results:
                    item['Detail'] = Results.split('=')[1]
                if 'INSTRUMENTATION_STATUS: charger' in Results:
                    item['charger'] = Results.split('=')[1]
                if 'INSTRUMENTATION_STATUS: path' in Results:
                    item['path'] = Results.split('=')[1]
                if 'INSTRUMENTATION_STATUS: reason' in Results:
                    print('Case Over Failed')
                    print('reason:{0}'.format(Results.split('=')[1]))
                    Check_Result = False
                    Check_Name = True
                    continue
                if 'INSTRUMENTATION_STATUS: end' in Results:
                    print('Case Over Pass')
                    Check_Result= False
                    Check_Name =True


Auto = AutoCase()
Auto.RunCase()