#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov  9 14:49:00 2018

@author: Ang
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


def GetRevisions(API, pageTitle):
    #pageTitle = 'Executive_Order_13769'
    #https://en.wikipedia.org/w/api.php?action=query&prop=revisions&titles=Executive_Order_13769&rvprop=timestamp|user|comment&generator=revisions
    #url = "https://en.wikipedia.org/w/api.php?action=query&format=json&rvdir=newer&rvlimit=500&prop=revisions&rvprop=ids|timestamp|user|userid|comment&titles=" + pageTitle
    url = API + pageTitle
    revisions = []                                        #list of all accumulated revisions
    next = ''                                             #information for the next request
    while True:
        #response = urllib2.urlopen(url + next).read()     #web request
        response=urllib.request.urlopen(url + next)
        str_response=response.read()#.decode('utf-8')
        responsedata = json.loads(str_response)
        page_id = list(responsedata["query"]["pages"].keys())[0]
        revision_data_lst=responsedata['query']['pages'][page_id]['revisions']
        revisions += revision_data_lst  #adds all revisions from the current request to the list

        try:        
            cont = responsedata['continue']['rvcontinue']
        except KeyError:                                      #break the loop if 'continue' element missing
            break

        next = "&rvcontinue=" + cont             #gets the revision Id from which to start the next request

    return revisions



def returnJsonCheck(response) -> dict:
    try:
        return response.json()
    except:
        print("ERROR")
        print(response)
        print(response.text)
        sys.exit("json error")

def GetRedirectPages(lang, article):
    #collect all the redirects
    #redirectAPI = wiki_link + "w/api.php?action=query&pageids=31593941&redirects&prop=redirects&rdlimit=max"
    allpages = []
    wiki_link = "https://{}.wikipedia.org/".format(lang)
    redirectAPI = wiki_link + "w/api.php?action=query&format=json&titles={}&redirects&prop=redirects&rdlimit=max".format(article)
    response=requests.get(redirectAPI)
    r_json = returnJsonCheck(response)
    pgid = list(r_json['query']['pages'].keys())[0]
    red_pg_lst = r_json['query']['pages'][pgid]['redirects']
    for item in red_pg_lst:
        id_title = [pgid, item['pageid'], item['title']]
        allpages.append(id_title)
    return allpages
    


def GetAllPageswithDirect(article_df):
    directpages_alllist = []
    for index, row in article_df.iterrows():
        lang = row.loc['language']
        article = row.loc['article']  
        alldirectpages = GetRedirectPages(lang, article)
        directpages_alllist += alldirectpages
        return directpages_alllist
    
    
 data = pd.read_table("/Users/Ang/OneDrive/Documents/Pitt_PhD/ResearchProjects/WikiWorldEvent/data/base_data_allarticles_1109.csv", 
                             sep=',', error_bad_lines = False)

data.columns.values

article_df = data[['wiki_lang','article']].drop_duplicates()
all_article_pages = GetAllPageswithDirect(article_df)
   
wiki_link = "https://{}.wikipedia.org/".format(lang)
    
    
API = wiki_link + "w/api.php?action=query&format=json&prop=revisions&titles={}&redirects".format(article)
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    