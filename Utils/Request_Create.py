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
import Config
from Utils import Log

def create(Cases,*args):
    if type(Cases) == dict:
        Server = numpy.where(Cases['Server']=='default', Config.Default['Server'], Cases['Server'])
        for Case in Cases['Cases']:
            if args:
                Log.print_info(1, '已指定测试用例：{0}'.format(args) )
                if Case['CaseName'] in args:
                    url ='{0}{1}'.format(Server, Case['api'])
                    Log.print_info(1, 'INSTRUMENTATION_STATUS: CaseName={0}'.format(Case['CaseName']) )
                    Log.print_info(1, 'INSTRUMENTATION_STATUS: Detail={0}'.format(Case['detail']) )
                    Log.print_info(1, 'INSTRUMENTATION_STATUS: charger={0}'.format(Case['charger']) )
                    Log.print_info(1, 'INSTRUMENTATION_STATUS: path={0}'.format(Cases['path']))
                    if Case['method'] == 'get':
                        param = ''
                        for key in Case['In']:
                            if key == 'default':
                                if Case['In'][key] == True:
                                    Log.print_info(2,'Need insert Default Keys')
                                    for dkey in Config.Default['param']:
                                        if Config.Default['param'][dkey] == 'time.time()':
                                            Config.Default['param'][dkey]= int(time.time())
                                    param += parse.urlencode(Config.Default['param'])
                                del Case['In']['default']
                                break
                        param += '&{0}'.format(parse.urlencode(Case['In']))
                        Log.print_info(2, param)
                        url_end = '{0}?{1}'.format(url,param.replace('=None','='))
                        Log.print_info(2,url_end)
                        start_= int(round(time.time() * 1000))
                        Response = get(url=url_end)
                        end_= int(round(time.time() * 1000))
                        Log.print_info(1, 'INSTRUMENTATION_STATUS: time={0}'.format(end_-start_))
                        Log.print_info(2,Response)
                        check(Case,Response)

                    elif Case['method']=='post':
                        inKey= Case['In']
                        print(parse.urlencode(inKey).encode('utf-8'))
            else:
                url = '{0}{1}'.format(Server, Case['api'])
                Log.print_info(1, 'INSTRUMENTATION_STATUS: CaseName={0}'.format(Case['CaseName']))
                Log.print_info(1, 'INSTRUMENTATION_STATUS: Detail={0}'.format(Case['detail']))
                Log.print_info(1, 'INSTRUMENTATION_STATUS: charger={0}'.format(Case['charger']))
                Log.print_info(1, 'INSTRUMENTATION_STATUS: path={0}'.format(Cases['path']))
                if Case['method'] == 'get':
                    param = ''
                    for key in Case['In']:
                        if key == 'default':
                            if Case['In'][key] == True:
                                Log.print_info(2, 'Need insert Default Keys')
                                for dkey in Config.Default['param']:
                                    if Config.Default['param'][dkey] == 'time.time()':
                                        Config.Default['param'][dkey] = int(time.time())
                                param += parse.urlencode(Config.Default['param'])
                            del Case['In']['default']
                            break
                    param += '&{0}'.format(parse.urlencode(Case['In']))
                    Log.print_info(2, param)
                    url_end = '{0}?{1}'.format(url, param.replace('=None', '='))
                    Log.print_info(2, url_end)
                    start_ = int(round(time.time() * 1000))
                    Response = get(url=url_end)
                    end_ = int(round(time.time() * 1000))
                    Log.print_info(1, 'INSTRUMENTATION_STATUS: time={0}'.format(end_ - start_))
                    Log.print_info(2, Response)
                    check(Case, Response)

                elif Case['method'] == 'post':
                    inKey = Case['In']
                    print(parse.urlencode(inKey).encode('utf-8'))
    elif type(Cases) == list:
        for cl in Cases:
            Server = numpy.where(cl['Server'] == 'default', Config.Default['Server'], cl['Server'])
            for Case in cl['Cases']:
                if args:
                    Log.print_info(1, '已指定测试用例：{0}'.format(args))
                    if Case['CaseName'] in args:
                        url = '{0}{1}'.format(Server, Case['api'])
                        Log.print_info(1, 'INSTRUMENTATION_STATUS: CaseName={0}'.format(Case['CaseName']))
                        Log.print_info(1, 'INSTRUMENTATION_STATUS: Detail={0}'.format(Case['detail']))
                        Log.print_info(1, 'INSTRUMENTATION_STATUS: charger={0}'.format(Case['charger']))
                        Log.print_info(1, 'INSTRUMENTATION_STATUS: path={0}'.format(cl['path']))
                        if Case['method'] == 'get':
                            param = ''
                            for key in Case['In']:
                                if key == 'default':
                                    if Case['In'][key] == True:
                                        Log.print_info(2, 'Need insert Default Keys')
                                        for dkey in Config.Default['param']:
                                            if Config.Default['param'][dkey] == 'time.time()':
                                                Config.Default['param'][dkey] = int(time.time())
                                        param += parse.urlencode(Config.Default['param'])
                                    del Case['In']['default']
                                    break
                            param += '&{0}'.format(parse.urlencode(Case['In']))
                            Log.print_info(2, param)
                            url_end = '{0}?{1}'.format(url, param.replace('=None', '='))
                            Log.print_info(2, url_end)
                            start_ = int(round(time.time() * 1000))
                            Response = get(url=url_end)
                            end_ = int(round(time.time() * 1000))
                            Log.print_info(1, 'INSTRUMENTATION_STATUS: time={0}'.format(end_ - start_))
                            Log.print_info(2, Response)
                            check(Case, Response)

                        elif Case['method'] == 'post':
                            inKey = Case['In']
                            print(parse.urlencode(inKey).encode('utf-8'))
                else:
                    url = '{0}{1}'.format(Server, Case['api'])
                    Log.print_info(1, 'INSTRUMENTATION_STATUS: CaseName={0}'.format(Case['CaseName']))
                    Log.print_info(1, 'INSTRUMENTATION_STATUS: Detail={0}'.format(Case['detail']))
                    Log.print_info(1, 'INSTRUMENTATION_STATUS: charger={0}'.format(Case['charger']))
                    Log.print_info(1, 'INSTRUMENTATION_STATUS: path={0}'.format(cl['path']))
                    if Case['method'] == 'get':
                        param = ''
                        for key in Case['In']:
                            if key == 'default':
                                if Case['In'][key] == True:
                                    Log.print_info(2, 'Need insert Default Keys')
                                    for dkey in Config.Default['param']:
                                        if Config.Default['param'][dkey] == 'time.time()':
                                            Config.Default['param'][dkey] = int(time.time())
                                    param += parse.urlencode(Config.Default['param'])
                                del Case['In']['default']
                                break
                        param += '&{0}'.format(parse.urlencode(Case['In']))
                        Log.print_info(2, param)
                        url_end = '{0}?{1}'.format(url, param.replace('=None', '='))
                        Log.print_info(2, url_end)
                        start_ = int(round(time.time() * 1000))
                        Response = get(url=url_end)
                        end_ = int(round(time.time() * 1000))
                        Log.print_info(1, 'INSTRUMENTATION_STATUS: time={0}'.format(end_ - start_))
                        Log.print_info(2, Response)
                        check(Case, Response)

                    elif Case['method'] == 'post':
                        inKey = Case['In']
                        print(parse.urlencode(inKey).encode('utf-8'))

def createThreading(Cases,num,*args):

    if type(Cases) == dict:
        Server = numpy.where(Cases['Server']=='default', Config.Default['Server'], Cases['Server'])
        for Case in Cases['Cases']:
            if args:
                Log.print_info(1, '已指定测试用例：{0}'.format(args) )
                if Case['CaseName'] in args:
                    url ='{0}{1}'.format(Server, Case['api'])
                    Log.print_info(1, 'INSTRUMENTATION_STATUS: CaseName={0}'.format(Case['CaseName']) )
                    Log.print_info(1, 'INSTRUMENTATION_STATUS: Detail={0}'.format(Case['detail']) )
                    Log.print_info(1, 'INSTRUMENTATION_STATUS: charger={0}'.format(Case['charger']) )
                    Log.print_info(1, 'INSTRUMENTATION_STATUS: path={0}'.format(Cases['path']))
                    if Case['method'] == 'get':
                        param = ''
                        for key in Case['In']:
                            if key == 'default':
                                if Case['In'][key] == True:
                                    Log.print_info(2,'Need insert Default Keys')
                                    for dkey in Config.Default['param']:
                                        if Config.Default['param'][dkey] == 'time.time()':
                                            Config.Default['param'][dkey]= int(time.time())
                                    param += parse.urlencode(Config.Default['param'])
                                del Case['In']['default']
                                break
                        param += '&{0}'.format(parse.urlencode(Case['In']))
                        Log.print_info(2, param)
                        url_end = '{0}?{1}'.format(url,param.replace('=None','='))
                        Log.print_info(2,url_end)
                        urls = []
                        for i in range(num):
                            urls.append(url_end)
                        [thread(url) for url in urls]

                    elif Case['method']=='post':
                        inKey= Case['In']
                        print(parse.urlencode(inKey).encode('utf-8'))
            else:
                url = '{0}{1}'.format(Server, Case['api'])
                Log.print_info(1, 'INSTRUMENTATION_STATUS: CaseName={0}'.format(Case['CaseName']))
                Log.print_info(1, 'INSTRUMENTATION_STATUS: Detail={0}'.format(Case['detail']))
                Log.print_info(1, 'INSTRUMENTATION_STATUS: charger={0}'.format(Case['charger']))
                Log.print_info(1, 'INSTRUMENTATION_STATUS: path={0}'.format(Cases['path']))
                if Case['method'] == 'get':
                    param = ''
                    for key in Case['In']:
                        if key == 'default':
                            if Case['In'][key] == True:
                                Log.print_info(2, 'Need insert Default Keys')
                                for dkey in Config.Default['param']:
                                    if Config.Default['param'][dkey] == 'time.time()':
                                        Config.Default['param'][dkey] = int(time.time())
                                param += parse.urlencode(Config.Default['param'])
                            del Case['In']['default']
                            break
                    param += '&{0}'.format(parse.urlencode(Case['In']))
                    Log.print_info(2, param)
                    url_end = '{0}?{1}'.format(url, param.replace('=None', '='))
                    Log.print_info(2, url_end)
                    urls = []
                    for i in range(num):
                        urls.append(url_end)
                    [thread(url) for url in urls]

                elif Case['method'] == 'post':
                    inKey = Case['In']
                    print(parse.urlencode(inKey).encode('utf-8'))
    elif type(Cases) == list:
        for cl in Cases:
            Server = numpy.where(cl['Server'] == 'default', Config.Default['Server'], cl['Server'])
            for Case in cl['Cases']:
                if args:
                    Log.print_info(1, '已指定测试用例：{0}'.format(args))
                    if Case['CaseName'] in args:
                        url = '{0}{1}'.format(Server, Case['api'])
                        Log.print_info(1, 'INSTRUMENTATION_STATUS: CaseName={0}'.format(Case['CaseName']))
                        Log.print_info(1, 'INSTRUMENTATION_STATUS: Detail={0}'.format(Case['detail']))
                        Log.print_info(1, 'INSTRUMENTATION_STATUS: charger={0}'.format(Case['charger']))
                        Log.print_info(1, 'INSTRUMENTATION_STATUS: path={0}'.format(cl['path']))
                        if Case['method'] == 'get':
                            param = ''
                            for key in Case['In']:
                                if key == 'default':
                                    if Case['In'][key] == True:
                                        Log.print_info(2, 'Need insert Default Keys')
                                        for dkey in Config.Default['param']:
                                            if Config.Default['param'][dkey] == 'time.time()':
                                                Config.Default['param'][dkey] = int(time.time())
                                        param += parse.urlencode(Config.Default['param'])
                                    del Case['In']['default']
                                    break
                            param += '&{0}'.format(parse.urlencode(Case['In']))
                            Log.print_info(2, param)
                            url_end = '{0}?{1}'.format(url, param.replace('=None', '='))
                            Log.print_info(2, url_end)
                            urls = []
                            for i in range(num):
                                urls.append(url_end)
                            [thread(url) for url in urls]

                        elif Case['method'] == 'post':
                            inKey = Case['In']
                            print(parse.urlencode(inKey).encode('utf-8'))
                else:
                    url = '{0}{1}'.format(Server, Case['api'])
                    Log.print_info(1, 'INSTRUMENTATION_STATUS: CaseName={0}'.format(Case['CaseName']))
                    Log.print_info(1, 'INSTRUMENTATION_STATUS: Detail={0}'.format(Case['detail']))
                    Log.print_info(1, 'INSTRUMENTATION_STATUS: charger={0}'.format(Case['charger']))
                    Log.print_info(1, 'INSTRUMENTATION_STATUS: path={0}'.format(cl['path']))
                    if Case['method'] == 'get':
                        param = ''
                        for key in Case['In']:
                            if key == 'default':
                                if Case['In'][key] == True:
                                    Log.print_info(2, 'Need insert Default Keys')
                                    for dkey in Config.Default['param']:
                                        if Config.Default['param'][dkey] == 'time.time()':
                                            Config.Default['param'][dkey] = int(time.time())
                                    param += parse.urlencode(Config.Default['param'])
                                del Case['In']['default']
                                break
                        param += '&{0}'.format(parse.urlencode(Case['In']))
                        Log.print_info(2, param)
                        url_end = '{0}?{1}'.format(url, param.replace('=None', '='))
                        Log.print_info(2, url_end)
                        urls = []
                        for i in range(num):
                            urls.append(url_end)
                        [thread(url) for url in urls]

                    elif Case['method'] == 'post':
                        inKey = Case['In']
                        print(parse.urlencode(inKey).encode('utf-8'))

def get(url):
    res = requests.get(url=url)
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
                if isinstance(Case['Out'][keyOut], int):
                    Error = numpy.where(Case['Out'][keyOut] == int(Response[keyOut]), 'Pass',
                                        'expect:{0},Actual:{1},Res:{2}'.format(Case['Out'][keyOut],
                                                                               Response[keyOut], Response))
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
        file = open('./Result/{0}'.format(Case['CaseName']),'w')
        file.write(str(Response))
        file.close()
        Actual = getMD5('./Result/{0}'.format(Case['CaseName']))
        expect = getMD5(os.getcwd().replace('Entry','Utils/Result/{0}'.format(Case['Out']['file'])))
        Error = numpy.where(Actual == expect, 'Pass',
                            '数据不匹配，检查返回:{0}'.format(Response))
        if 'Pass' != Error:
            Log.print_info(1, 'INSTRUMENTATION_STATUS: result=Failed')
            Log.print_info(1, 'INSTRUMENTATION_STATUS: log={0}'.format(Error))
        else:
            Log.print_info(1, 'INSTRUMENTATION_STATUS: result=Pass')
            os.remove('./Result/{0}'.format(Case['CaseName']))

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

def getMul(url):
    Log.print_info(1,'INSTRUMENTATION_STATUS: thread start={0}'.format(threading.currentThread().getName()))
    start_ = int(round(time.time() * 1000))
    res = requests.get(url)
    end_ = int(round(time.time() * 1000))
    Log.print_info(1, 'INSTRUMENTATION_STATUS: thread={0},time={1}'.format(threading.currentThread().getName(),end_ - start_))
    if res.status_code == 200:
        Log.print_info(1, 'INSTRUMENTATION_STATUS:thread={0}, res={1}'.format(threading.currentThread().getName(),
                                                                              json.loads(res.text)))
    else:
        res = {}
        res['code'] = -1
        res['msg'] ='接口404'
        Log.print_info(1, 'INSTRUMENTATION_STATUS: thread={0},res={1}'.format(threading.currentThread().getName(),
                                                                              json.loads(res)))
    Log.print_info(1, 'INSTRUMENTATION_STATUS: result=Pass')


