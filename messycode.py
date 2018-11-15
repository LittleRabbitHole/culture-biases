#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov 15 12:58:39 2018

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
from utilities import GetAllPageswithDirect, WriteOut_Lst2Str1, WriteOut_Lst2Str2







#collect all the contributors for articles
all_contributors = GetAllContributors(all_article_pages)
#pickle load
f = open('/Users/angli/Ang/OneDrive/Documents/Pitt_PhD/ResearchProjects/WikiWorldEvent/data/all_contributors.pkl', 'wb')   # Pickle file is newly created where foo1.py is
pickle.dump(all_article_pages, f)          # dump data to f
f.close() 

#f = open('gradesdict.pkl', 'rb')   # 'r' for reading; can be omitted
#mydict = pickle.load(f)         # load file content as mydict
#f.close()

WriteOut_Lst2Str1(all_contributors, "/Users/angli/Ang/OneDrive/Documents/Pitt_PhD/ResearchProjects/WikiWorldEvent/data/all_contributors.txt") #with title
WriteOut_Lst2Str2(all_contributors, "/Users/angli/Ang/OneDrive/Documents/Pitt_PhD/ResearchProjects/WikiWorldEvent/data/all_contributors_notitle.txt") #with title


   
wiki_link = "https://{}.wikipedia.org/".format(lang)
    
    
API = wiki_link + "w/api.php?action=query&format=json&prop=revisions&titles={}&redirects".format(article)
    
"/w/api.php?action=query&format=json&prop=contributors&pageids=1543230&pcexcludegroup=bot&pclimit=500"
    
    
    