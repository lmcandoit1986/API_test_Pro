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
        Config.Default =cls.readCasesFromClass(cls,'Default')


    @classmethod
    def tearDownClass(cls):
        Log.print_info(2,'cls teardown')

    def setUp(self):
        Log.print_info(2,'set')

    def tearDown(self):
        Log.print_info(2,'teardown')

    def readCasesFromDirectory(self,file):
        '''
        读取文件下的用例
        :param file:
        :return:
        '''
        filePath = os.path.dirname(__file__)
        yamlPath_dic = os.path.join(filePath, 'Cases/' + file)
        files = os.listdir(yamlPath_dic)
        Cases =[]
        for item in files:
            print(item)
            yamlPath_item = os.path.join(yamlPath_dic, item)
            print(yamlPath_item)
            f = open(yamlPath_item, 'r', encoding='utf-8')
            cont = f.read()
            x = yaml.load(cont, Loader=yaml.FullLoader)
            f.close()
            x['path'] = 'Cases/{0}/{1}'.format(file, item)
            Cases.append(x)
        return Cases

    def readCasesFromClass(self,file):
        '''
        读取类中的用例
        :param file:
        :return:
        '''
        filePath = os.path.dirname(__file__)
        yamlPath = os.path.join(filePath, 'Cases/' + file)
        f = open(yamlPath, 'r', encoding='utf-8')
        cont = f.read()
        x = yaml.load(cont, Loader=yaml.FullLoader)
        f.close()
        x['path']= 'Cases/' + file
        return x

    def readAllCases(self):
        '''
        读取全部用例
        :return:
        '''
        filePath = os.path.dirname(__file__)
        yamlPath = os.path.join(filePath, 'Cases')
        files = os.listdir(yamlPath)
        Cases= []
        for file in files:
            if file != 'Default':
                yamlPath_dic = os.path.join(yamlPath, file)
                if os.path.isdir(yamlPath_dic):
                    files_sec = os.listdir(yamlPath_dic)
                    for item in files_sec:
                        yamlPath_item = os.path.join(yamlPath_dic, item)
                        print(yamlPath_item)
                        f = open(yamlPath_item, 'r', encoding='utf-8')
                        cont = f.read()
                        x = yaml.load(cont, Loader=yaml.FullLoader)
                        f.close()
                        x['path']='Cases/{0}/{1}'.format(file,item)
                        Cases.append(x)
                elif os.path.isfile(yamlPath_dic):
                    f = open(yamlPath_dic, 'r', encoding='utf-8')
                    cont = f.read()
                    x = yaml.load(cont, Loader=yaml.FullLoader)
                    f.close()
                    x['path'] = 'Cases/{0}'.format(file)
                    Cases.append(x)

        return Cases



