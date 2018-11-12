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

def returnJsonCheck(response) -> dict:
    try:
        return response.json()
    except:
        print("ERROR")
        print(response)
        print(response.text)
        sys.exit("json error")


def GetRevisions(API, pageTitle):
    #pageTitle = 'Executive_Order_13769'
    #https://en.wikipedia.org/w/api.php?action=query&prop=revisions&titles=Executive_Order_13769&rvprop=timestamp|user|comment&generator=revisions
    #url = "https://en.wikipedia.org/w/api.php?action=query&format=json&rvdir=newer&rvlimit=500&prop=revisions&rvprop=ids|timestamp|user|userid|comment&titles=" + pageTitle
    url = API + pageTitle
    revisions = []                                        #list of all accumulated revisions
    next = ''                                             #information for the next request
    while True:
        #response = urllib2.urlopen(url + next).read()     #web request
        response=requests.get(url + next)
        responsedata = returnJsonCheck(response)        
        page_id = list(responsedata["query"]["pages"].keys())[0]
        revision_data_lst=responsedata['query']['pages'][page_id]['revisions']
        revisions += revision_data_lst  #adds all revisions from the current request to the list

        try:        
            cont = responsedata['continue']['rvcontinue']
        except KeyError:                                      #break the loop if 'continue' element missing
            break

        next = "&rvcontinue=" + cont             #gets the revision Id from which to start the next request

    return revisions


def GetPageContributors(lang, pageid):
    #this is to retrieve all contributors given a page id
    wiki_link = "https://{}.wikipedia.org/".format(lang)
    API = wiki_link + "/w/api.php?action=query&format=json&prop=contributors&pageids={}&pcexcludegroup=bot&pclimit=500".format(str(pageid))
    PageContributors = []
    next = ''                                             #information for the next request
    while True:
        response=requests.get(API + next)
        responsedata = returnJsonCheck(response)        
        page_id = list(responsedata["query"]["pages"].keys())[0]
        contributor_lst=responsedata['query']['pages'][page_id].get('contributors')
        if contributor_lst is not None:
            PageContributors += contributor_lst  #adds all contributors from the current request to the list
        #retrieve continue
        try:        
            cont = responsedata['continue']['pccontinue']
        except KeyError:                                      #break the loop if 'continue' element missing
            break
        next = "&pccontinue=" + cont             #gets the revision Id from which to start the next request
    return PageContributors
    


def GetAllContributors(all_article_pages):
    #collect all the contributors for articles from article lists
    i = 0
    all_contributors = []
    for item in all_article_pages:#'PageType||Ori_PageID||Lang||Red_PgId||title'
        i += 1
        if i%1000 == 0: print(i)
        lang = item[2]
        pageid = item[3]
        PageType = item[0]
        Ori_PageID = item[1]
        #get all contributors
        Contributors_lst = GetPageContributors(lang, pageid) #as [{},{}]
        #process the contributors_lst into lists
        if Contributors_lst != []:
            Contributors = []
            for contributor in Contributors_lst:
                Contributors.append([Ori_PageID, PageType, pageid, lang, str(contributor['userid']), contributor['name']])
            #add into all_contributors
            all_contributors += Contributors
    return all_contributors


def GetRedirectPages(lang, article):
    #collect all the redirects for a single article
    #redirectAPI = wiki_link + "w/api.php?action=query&pageids=31593941&redirects&prop=redirects&rdlimit=max"
    allpages = [] # [pgid, redir['pageid'], redir['title']]
    wiki_link = "https://{}.wikipedia.org/".format(lang)
    redirectAPI = wiki_link + "w/api.php?action=query&format=json&titles={}&redirects&prop=redirects&rdlimit=max".format(article)
    response=requests.get(redirectAPI)
    r_json = returnJsonCheck(response)
    pgid = list(r_json['query']['pages'].keys())[0]
    red_pg_lst = r_json['query']['pages'][pgid].get('redirects')
    #append original page
    allpages.append(["orig", pgid, lang, pgid, article])
    #if has the redirect
    if red_pg_lst is not None:
        for item in red_pg_lst:
            id_title = ["redirct", pgid, lang, item['pageid'], item['title']]
            allpages.append(id_title)
    #if without redirect
    else: allpages.append(["orig", pgid, lang, pgid, r_json['query']['pages'][pgid]['title']])
    return allpages
    


def GetAllPageswithDirect(article_df):
    #input all article as df, output list of all redirect articles
    directpages_alllist = []
    counter = 0
    for index, row in article_df.iterrows():
        counter += 1
        if counter%100 == 0: print (counter)
        lang = row.loc['wiki_lang']
        article = row.loc['article']  
        alldirectpages = GetRedirectPages(lang, article)
        directpages_alllist += alldirectpages
    #return
    return directpages_alllist
    

def WriteOut_Lst2Str1(lst, filename):
    i = 0
    #outString = 'PageType||Ori_PageID||Lang||Red_PgId||title'
    outString = 'Ori_PageID||PageType||pageid||lang||userid||name'
    for item in lst:
        i += 1
        #item[3] = str(item[3])
        outString += '\n'
        outString += '||'.join(item)
        
#    result_path = '{}/results'.format(file_loc)
#    if not os.path.exists(result_path):
#        os.makedirs(result_path)
        
    with open(filename, 'w') as f:
        f.write(outString)
        f.close()

def WriteOut_Lst2Str2(lst, filename):
    i = 0
    #outString = 'PageType, Ori_PageID, Lang, Red_PgId'
    outString = 'Ori_PageID, PageType, pageid, lang, userid'
    for item in lst:
        i += 1
        #item[3] = str(item[3])
        outString += '\n'
        outString += ', '.join([item[0],item[1],item[2], item[3], item[4]])
        
#    result_path = '{}/results'.format(file_loc)
#    if not os.path.exists(result_path):
#        os.makedirs(result_path)
        
    with open(filename, 'w') as f:
        f.write(outString)
        f.close()

###main   
#base_data_allarticles_1109 -- process_data_with_topic_location
data = pd.read_table("/Users/jiajunluo/OneDrive/Documents/Pitt_PhD/ResearchProjects/WikiWorldEvent/data/base_data_allarticles_1109.csv", 
                             sep=',', error_bad_lines = False)

data.columns.values

#all the event article pages = 4748
article_df = data[['wiki_lang','article']].drop_duplicates()#4748

#collect all the redirect pages for the current event articles = 26745
all_article_pages = GetAllPageswithDirect(article_df)
#pickle load
f = open('/Users/jiajunluo/OneDrive/Documents/Pitt_PhD/ResearchProjects/WikiWorldEvent/data/all_article_pages.pkl', 'wb')   # Pickle file is newly created where foo1.py is
pickle.dump(all_article_pages, f)          # dump data to f
f.close() 

#f = open('gradesdict.pkl', 'rb')   # 'r' for reading; can be omitted
#mydict = pickle.load(f)         # load file content as mydict
#f.close()

#write all the pages into csv
WriteOut_Lst2Str1(all_article_pages, "/Users/jiajunluo/OneDrive/Documents/Pitt_PhD/ResearchProjects/WikiWorldEvent/data/all_article_pages.txt") #with title
WriteOut_Lst2Str2(all_article_pages, "/Users/jiajunluo/OneDrive/Documents/Pitt_PhD/ResearchProjects/WikiWorldEvent/data/all_article_pages_notitle.txt") #without title

#collect all the contributors for articles
all_articles = pd.read_table("/Users/jiajunluo/OneDrive/Documents/Pitt_PhD/ResearchProjects/WikiWorldEvent/data/all_article_pages_notitle.txt", 
                             sep=',', error_bad_lines = False)
all_articles = all_articles[['Ori_PageID', ' "Lang"', ' "Red_PgId"']].drop_duplicates()


#collect all contributors
all_contributors = GetAllContributors(all_article_pages)
#pickle load
f = open('/Users/jiajunluo/OneDrive/Documents/Pitt_PhD/ResearchProjects/WikiWorldEvent/data/all_contributors.pkl', 'wb')   # Pickle file is newly created where foo1.py is
pickle.dump(all_article_pages, f)          # dump data to f
f.close() 

#f = open('gradesdict.pkl', 'rb')   # 'r' for reading; can be omitted
#mydict = pickle.load(f)         # load file content as mydict
#f.close()

WriteOut_Lst2Str1(all_contributors, "/Users/jiajunluo/OneDrive/Documents/Pitt_PhD/ResearchProjects/WikiWorldEvent/data/all_contributors.txt") #with title
WriteOut_Lst2Str2(all_contributors, "/Users/jiajunluo/OneDrive/Documents/Pitt_PhD/ResearchProjects/WikiWorldEvent/data/all_contributors_notitle.txt") #with title


   
wiki_link = "https://{}.wikipedia.org/".format(lang)
    
    
API = wiki_link + "w/api.php?action=query&format=json&prop=revisions&titles={}&redirects".format(article)
    
"/w/api.php?action=query&format=json&prop=contributors&pageids=1543230&pcexcludegroup=bot&pclimit=500"
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    