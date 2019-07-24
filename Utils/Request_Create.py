#!/usr/bin/python3
# -*- coding: utf-8 -*-

import hashlib
import json
import os
import threading
import time
from urllib import parse
import numpy
import requests
from jsonpath import jsonpath
import Config
from Utils import Log

def create(Cases,*args):
    if type(Cases) == dict:
        Server = numpy.where(Cases['Server']=='default', Config.Default['Server'], Cases['Server'])
        for Case in Cases['Cases']:
            if args:
                if Case['CaseName'] in args:
                    Log.print_info(1, '已匹配到指定测试用例：{0}'.format(Case['CaseName']))
                    dealCases(Server,Case,Cases)
            else:
                dealCases(Server, Case, Cases)
    elif type(Cases) == list:
        for cl in Cases:
            Server = numpy.where(cl['Server'] == 'default', Config.Default['Server'], cl['Server'])
            for Case in cl['Cases']:
                if args:
                    if Case['CaseName'] in args:
                        Log.print_info(1, '已匹配到指定测试用例：{0}'.format(Case['CaseName']))
                        dealCases(Server, Case, cl)
                else:
                    dealCases(Server, Case, cl)

def dealCases(Server,Case,Cases):
    url = '{0}{1}'.format(Server, Case['api'])
    Log.print_info(1, 'INSTRUMENTATION_STATUS: CaseName={0}'.format(Case['CaseName']))
    Log.print_info(1, 'INSTRUMENTATION_STATUS: Detail={0}'.format(Case['detail']))
    Log.print_info(1, 'INSTRUMENTATION_STATUS: api={0}'.format(Case['api']))
    Log.print_info(1, 'INSTRUMENTATION_STATUS: charger={0}'.format(Case['charger']))
    Log.print_info(1, 'INSTRUMENTATION_STATUS: path={0}'.format(Cases['path']))
    if Case['method'] == 'get':
        paramDict = Config.Default['param']
        for key in Case['In']:
            if key in paramDict and Case['In'].get('default'):
                del paramDict[key]
        if 'default' in Case['In']:
            if Case['In']['default'] == True:
                Log.print_info(2, 'Need insert Default Keys')
                dict_def(paramDict)
                dict_def(Case['In'])
                del Case['In']['default']
        Case['In'].update(paramDict)
        Log.print_info(3, 'param:{0}'.format(Case['In']))
        param = parse.urlencode(Case['In'])
        url_end = '{0}?{1}'.format(url, param.replace('=None', '='))
        Log.print_info(2, url_end)
        start_ = int(round(time.time() * 1000))
        Response = get(url=url_end)
        end_ = int(round(time.time() * 1000))
        Log.print_info(1, 'INSTRUMENTATION_STATUS: time={0}'.format(end_ - start_))
        Log.print_info(2, Response)
        check(Case, Response)

    elif Case['method'] == 'post':
        paramDict = Config.Default['body']
        if Case['header'] == 'default':
            Case['header'] = Config.Default['header']

        if 'default' in Case['body']:
            if Case['body']['default'] == True:
                Log.print_info(2, 'Need insert Default Keys')
                dict_def(paramDict)
                dict_def(Case['body'])
                del Case['body']['default']
        for key in Case['body']:
            if key in paramDict and 'default' in Case['body']:
                del paramDict[key]
        Case['body'].update(paramDict)
        start_ = int(round(time.time() * 1000))
        Response = post(url, header=Case['header'], body=Case['body'])
        end_ = int(round(time.time() * 1000))
        Log.print_info(1, 'INSTRUMENTATION_STATUS: time={0}'.format(end_ - start_))
        Log.print_info(2, Response)
        check(Case, Response)

def createThreading(Cases,num,*args):
    if type(Cases) == dict:
        Server = numpy.where(Cases['Server']=='default', Config.Default['Server'], Cases['Server'])
        for Case in Cases['Cases']:
            if args:
                if Case['CaseName'] in args:
                    Log.print_info(1, '已匹配到指定测试用例：{0}'.format(Case['CaseName']))
                    dealCasesMulThreading(Server, Case, Cases, num)
            else:
                dealCasesMulThreading(Server, Case, Cases, num)
    elif type(Cases) == list:
        for cl in Cases:
            Server = numpy.where(cl['Server'] == 'default', Config.Default['Server'], cl['Server'])
            for Case in cl['Cases']:
                if args:
                    if Case['CaseName'] in args:
                        Log.print_info(1, '已匹配到指定测试用例：{0}'.format(Case['CaseName']))
                        dealCasesMulThreading(Server, Case, cl, num)
                else:
                    dealCasesMulThreading(Server, Case, cl, num)

def dealCasesMulThreading(Server,Case,Cases,num):
    url = '{0}{1}'.format(Server, Case['api'])
    Log.print_info(1, 'INSTRUMENTATION_STATUS: CaseName={0}'.format(Case['CaseName']))
    Log.print_info(1, 'INSTRUMENTATION_STATUS: Detail={0}'.format(Case['detail']))
    Log.print_info(1, 'INSTRUMENTATION_STATUS: charger={0}'.format(Case['charger']))
    Log.print_info(1, 'INSTRUMENTATION_STATUS: path={0}'.format(Cases['path']))
    if Case['method'] == 'get':
        paramDict = Config.Default['param']
        for key in Case['In']:
            if key in paramDict and Case['In'].get('default'):
                del paramDict[key]
        if 'default' in Case['In']:
            if Case['In']['default'] == True:
                Log.print_info(2, 'Need insert Default Keys')
                dict_def(paramDict)
                dict_def(Case['In'])
                del Case['In']['default']
        Case['In'].update(paramDict)
        Log.print_info(3, 'param:{0}'.format(Case['In']))
        param = parse.urlencode(Case['In'])
        url_end = '{0}?{1}'.format(url, param.replace('=None', '='))
        Log.print_info(2, url_end)
        urls = []
        for i in range(num):
            urls.append(url_end)
        [thread(url) for url in urls]

    elif Case['method'] == 'post':
        paramDict = Config.Default['body']
        if Case['header'] == 'default':
            Case['header'] = Config.Default['header']

        if 'default' in Case['body']:
            if Case['body']['default'] == True:
                Log.print_info(2, 'Need insert Default Keys')
                dict_def(paramDict)
                dict_def(Case['body'])
                del Case['body']['default']
        for key in Case['body']:
            if key in paramDict and 'default' in Case['body']:
                del paramDict[key]
        Case['body'].update(paramDict)
        urls = []
        for i in range(num):
            urls.append(url)
        [threadPost(url_item, Case['header'], Case['body']) for url_item in urls]

def get(url):
    res = requests.get(url=url)
    if res.status_code == 200:
        return (json.loads(res.text))
    else:
        res = {}
        res['code'] = -1
        res['msg'] ='接口404'
        return res

def post(url,header,body):
    Log.print_info(2, 'header:{0}'.format(header))
    Log.print_info(2, 'body:{0}'.format(body))
    res = requests.post(url=url, headers=header, json=body)
    if res.status_code == 200:
        return (json.loads(res.text))
    else:
        res = {}
        res['code'] = -1
        res['msg'] ='接口404'
        return res

def check(Case,Response):
    if Case['Out']['type'] == 'key':
        isPass = True
        for keyOut in Case['Out']:
            if keyOut == 'type':
                pass
            else:
                if '$' in keyOut:
                    Log.print_info(2,"use Jsonpath")
                    res = jsonpath(Response,keyOut)
                    if res:
                        Error = numpy.where(Case['Out'][keyOut] in res, 'Pass',
                                            'expect:{0},Actual:{1},Res:{2}'.format(Case['Out'][keyOut],
                                                                                   res, Response))
                    else:
                        Error = 'Failed,{0} 查找不到匹配 key'.format(keyOut)
                else:
                    Error = numpy.where(Case['Out'][keyOut] == Response[keyOut], 'Pass',
                                    'expect:{0},Actual:{1},Res:{2}'.format(Case['Out'][keyOut],
                                                                           Response[keyOut], Response))
                if 'Pass' != Error:
                    isPass = False
                    Log.print_info(1, 'INSTRUMENTATION_STATUS: result=Failed')
                    Log.print_info(1, 'INSTRUMENTATION_STATUS: log={0}'.format(Error))
                    break

        if isPass:
            Log.print_info(1, 'INSTRUMENTATION_STATUS: result=Pass')
            Log.print_info(1, 'INSTRUMENTATION_STATUS: log={0}'.format('null'))
    elif Case['Out']['type'] == 'type':
        isPass = True
        for keyOut in Case['Out']:
            if keyOut == 'type':
                pass
            else:
                if Case['Out'][keyOut] == 'int':
                    expect_type = int
                elif Case['Out'][keyOut] == 'str':
                    expect_type = str
                elif Case['Out'][keyOut] == 'dict':
                    expect_type = dict
                elif Case['Out'][keyOut] == 'list':
                    expect_type = list
                elif Case['Out'][keyOut] == 'bool':
                    expect_type = bool
                elif Case['Out'][keyOut] == 'none':
                    expect_type = type(None)

                Error = numpy.where(expect_type == type(Response[keyOut]), 'Pass',
                                    'expect:{0},Actual:{1},Res:{2}'.format(Case['Out'][keyOut],
                                                                           type(Response[keyOut]), Response))
                if 'Pass' != Error:
                    isPass = False
                    Log.print_info(1, 'INSTRUMENTATION_STATUS: result=Failed')
                    Log.print_info(1, 'INSTRUMENTATION_STATUS: log={0}'.format(Error))
                    break

        if isPass:
            Log.print_info(1, 'INSTRUMENTATION_STATUS: result=Pass')
    elif Case['Out']['type'] == 'file':
        Local = os.getcwd()
        if Local.endswith('API_test_Pro'):
            pass
        else:
            Local = Local.split('API_test_Pro')[0]+'API_test_Pro'
        file = open('{1}/Entry/Result/{0}'.format(Case['CaseName'], Local), 'w')
        file.write(str(Response))
        file.close()
        Actual = getMD5('{1}/Entry/Result/{0}'.format(Case['CaseName'], Local))
        expect = getMD5('{1}/Utils/Result/{0}'.format(Case['Out']['file'], Local))
        Error = numpy.where(Actual == expect, 'Pass',
                            '数据不匹配，检查返回:{0}'.format(Response))
        if 'Pass' != Error:
            Log.print_info(1, 'INSTRUMENTATION_STATUS: result=Failed')
            Log.print_info(1, 'INSTRUMENTATION_STATUS: log={0}'.format(Error))
        else:
            Log.print_info(1, 'INSTRUMENTATION_STATUS: result=Pass')
            os.remove('{1}/Entry/Result/{0}'.format(Case['CaseName'],Local))

def getMD5(file_path,Bytes=1024):
    md5_1 = hashlib.md5()
    with open(file_path, 'rb') as f:
        while 1:
            data = f.read(Bytes)
            if data:
                md5_1.update(data)
            else:
                break
    ret = md5_1.hexdigest()
    return ret

def thread(url):
    x = threading.Thread(target=getMul, args=(url,)) #这里的args=(url,) 逗号是必须的,因为加了逗号才是只有一个元素的元组
    x.start()

def threadPost(url,header,body):
    x = threading.Thread(target=postMul, args=(url,header,body,)) #这里的args=(url,) 逗号是必须的,因为加了逗号才是只有一个元素的元组
    x.start()

def getMul(url):
    Log.print_info(1,'INSTRUMENTATION_STATUS: thread start={0}'.format(threading.currentThread().getName()))
    start_ = int(round(time.time() * 1000))
    res = requests.get(url)
    end_ = int(round(time.time() * 1000))
    Log.print_info(1, 'INSTRUMENTATION_STATUS: thread={0},time={1}'.format(threading.currentThread().getName(),end_ - start_))
    if res.status_code == 200:
        Log.print_info(1, 'INSTRUMENTATION_STATUS: thread={0}, res={1}'.format(threading.currentThread().getName(),
                                                                              json.loads(res.text)))
    else:
        res = {}
        res['code'] = -1
        res['msg'] ='接口404'
        Log.print_info(1, 'INSTRUMENTATION_STATUS: thread={0},res={1}'.format(threading.currentThread().getName(),
                                                                              json.loads(res)))
    Log.print_info(1, 'INSTRUMENTATION_STATUS: thread={0},result=Pass'.format(threading.currentThread().getName()))

def postMul(url,header,body):
    Log.print_info(1,'INSTRUMENTATION_STATUS: thread start={0}'.format(threading.currentThread().getName()))
    start_ = int(round(time.time() * 1000))
    res = requests.post(url, headers=header, json=body)
    end_ = int(round(time.time() * 1000))
    Log.print_info(1, 'INSTRUMENTATION_STATUS: thread={0},time={1}'.format(threading.currentThread().getName(),end_ - start_))
    if res.status_code == 200:
        Log.print_info(1, 'INSTRUMENTATION_STATUS: thread={0}, res={1}'.format(threading.currentThread().getName(),
                                                                              json.loads(res.text)))
    else:
        res = {}
        res['code'] = -1
        res['msg'] ='接口404'
        Log.print_info(1, 'INSTRUMENTATION_STATUS: thread={0},res={1}'.format(threading.currentThread().getName(),
                                                                              res))
    Log.print_info(1, 'INSTRUMENTATION_STATUS: thread={0},result=Pass'.format(threading.currentThread().getName()))

def dict_def(targetDict):
    for key in targetDict:
        if targetDict[key] == 'time.time()':
            targetDict[key] = int(time.time())