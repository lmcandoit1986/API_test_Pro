#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os
import yaml

from BaseTest import BaseTest
from Utils import Request_Create


class run(BaseTest):

    def test_example(self):
        case = self.readCasesFromDirectory('Medical') # 获取某个文件夹下的所有用例，用于获取各模块下的用例，目前不支持模块下再分文件夹
        #case = self.readCasesFromClass('Medical/List_bx') # 获取某个文件的所有用例
        #case = self.readAllCases() # 获取Cases/下的所有用例
        Request_Create.create(case) # 正常执行用例
        #Request_Create.create(case,'getBXList1') # 执行用例中的某个用例
        #Request_Create.create(case, 'getBXList1','getBXList2') # 执行用例中的多个用例

