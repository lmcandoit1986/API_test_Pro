#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os
import yaml

from BaseTest import BaseTest
from Utils import Request_Create


class me(BaseTest):

    def test_ssa(self):
        case = self.readConfig('Cases/Medical/List_bx')
        Request_Create.create(case,'getBXList1','getBXList2')
