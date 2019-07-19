#!/usr/bin/python3
# -*- coding: utf-8 -*-
import datetime

Lev = 2
global log

def print_info(level,context):
    if level<=Lev:
        print('{0}:{1}'.format(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), context))

