#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2018-12-28 15:37:48
# @Author  : Your Name (you@example.org)
# @Link    : http://example.org
# @Version : $Id$

import os
import hashlib
import datetime
import re

url = 'http://baidu.com/word.png'
on_time = str(datetime.datetime.now().strftime('%Y%m%d%H%M%S'))

name = os.path.basename(url)
name = on_time+'_'+name
print(name)
