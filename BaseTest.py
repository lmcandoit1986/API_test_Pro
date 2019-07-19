#!/usr/bin/python3
# -*- coding: utf-8 -*-

import logging
import os
import unittest
import yaml

import Config
from Utils import Log


class BaseTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        Log.print_info(2,'cls setup')
        # Cases = cls.readConfig(cls)
        Config.Default =cls.readConfig(cls,'Cases/Default')


    @classmethod
    def tearDownClass(cls):
        Log.print_info(2,'cls teardown')

    def setUp(self):
        Log.print_info(2,'set')

    def tearDown(self):
        Log.print_info(2,'teardown')

    def readConfig(self,file):
        filePath = os.path.dirname(__file__)
        yamlPath = os.path.join(filePath,file)
        f = open(yamlPath, 'r', encoding='utf-8')
        cont = f.read()
        x = yaml.load(cont,Loader=yaml.FullLoader)
        f.close()
        return x