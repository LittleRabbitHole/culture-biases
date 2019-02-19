#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb 19 11:47:39 2019

wikitext parser:
    https://www.mediawiki.org/wiki/API:Parsing_wikitext#parse

compare to:
    https://www.mediawiki.org/wiki/API:Compare


@author: angli
"""


import pandas as pd
import os
import datetime
import numpy as np
import urllib.parse
import json
import csv
import os
#import urllib
import pickle
import itertools
import requests
import sys
from lxml import html
import re

def returnJsonCheck(response) -> dict:
    try:
        return response.json()
    except:
        print("ERROR")
        print(response)
        print(response.text)
        sys.exit("json error")


api = "https://en.wikipedia.org/w/api.php?action=parse&pageid=39750126&prop=externallinks|revid|text&format=json"

response=requests.get(api)
responsedata = returnJsonCheck(response)

infosources = responsedata["parse"]["externallinks"]
url_implifies = list(set([re.match('(|https?:)//(?:[-\w.]|(?:%[\da-fA-F]{2}))+/', url)[0] for url in infosources]))

url_implifies = [re.findall(r"//(?:[-\w.]|(?:%[\da-fA-F]{2}))+/", url) for url in infosources]



raw_html = responsedata["parse"]["text"]["*"]
document = html.document_fromstring(raw_html)
paragraphs = document.xpath('//p')
len(paragraphs)
p1 = paragraphs[2].text_content()

diffapi = "https://en.wikipedia.org/w/api.php?action=compare&fromrev=883641819&torev=883139142&format=json"
"https://en.wikipedia.org/w/api.php?action=compare&fromrev=883641819&torev=883139142&prop=diff|size|user|parsedcomment"

response=requests.get(diffapi)
responsedata = returnJsonCheck(response)


raw_html = responsedata["compare"]["*"]
document = html.document_fromstring(raw_html)
dels = document.xpath('//del')
deltext = dels[1].text_content()
adds = document.xpath('//ins')
adds[0].text_content()

re.findall(r"//(?:[-\w.]|(?:%[\da-fA-F]{2}))+/", deltext)








