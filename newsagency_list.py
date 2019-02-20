#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb 20 16:45:43 2019

http://www.abyznewslinks.com/allco.htm

@author: angli
"""

from lxml import html
import requests

response=requests.get(api)
raw_html = responsedata["compare"]["*"]
document = html.document_fromstring(raw_html)
dels = document.xpath('//del')
deltext = dels[1].text_content()
adds = document.xpath('//ins')
adds[0].text_content()