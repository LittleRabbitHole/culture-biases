#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov 15 14:41:23 2018

This is to collect all the revisions from all articles


@author: angli
"""
import pandas as pd
import numpy as np
import pickle
from utilities import AllArticlesRevisions


#main#####collect all the revisions for the articles

datadir1 = "/Users/angli/Ang/OneDrive/Documents/Pitt_PhD/ResearchProjects/WikiWorldEvent/data/"
datadir2 = "/Users/jiajunluo/OneDrive/Documents/Pitt_PhD/ResearchProjects/WikiWorldEvent/data/"


def OutAllRevisions(datadir):
    all_articles = pd.read_table("all_article_pages_notitle.txt", 
                                 sep=',', error_bad_lines = False)
    
    all_articles = all_articles.loc[all_articles['PageType']=='orig']
    all_articles = all_articles[['Ori_PageID', 'Lang', 'Red_PgId']].drop_duplicates()
    allarticlerevisions = AllArticlesRevisions(all_articles)#as json
    #write as json
    f = open('all_article_revisions.pkl', 'wb')
    pickle.dump(allarticlerevisions, f)          # dump data to f
    f.close() 
    #finish collecting





f = open(datadir1+'all_article_revisions.pkl', 'rb')   # 'r' for reading; can be omitted
allarticlerevisions = pickle.load(f)         # load file content as mydict
f.close()

for key, item in allarticlerevisions.items():
    rpageid, rlang = key
    pageid = str(rpageid)
    lang = str(rlang)
    for revision in item:
        revid = str(revision['revid'])
        parentid = str(revision['parentid'])
        timestamp = revision['timestamp']
        username = revision.get('user')
        userid = str(revision.get('userid'))




#write out
filename = "/Users/angli/Ang/OneDrive/Documents/Pitt_PhD/ResearchProjects/WikiWorldEvent/data/all_article_revisions.csv"
with open(filename, 'w') as f:
    lineOutstring = '"pageid","lang","revid","parentid","timestamp","userid","size","username"\n'
    f.write(lineOutstring)
    for key, item in allarticlerevisions.items():
        rpageid, rlang = key
        pageid = '"{}"'.format(str(rpageid))
        lang = '"{}"'.format(str(rlang))
        for revision in item:
            revid = '"{}"'.format(str(revision['revid']))
            parentid = '"{}"'.format(str(revision['parentid']))
            timestamp = '"{}"'.format(revision['timestamp'])
            username = '"{}"'.format(revision.get('user'))
            userid = '"{}"'.format(str(revision.get('userid')))
            size = '"{}"'.format(str(revision.get('size')))
            revision_lst = [pageid, lang, revid, parentid, timestamp, userid, size, username]
            revision_lineOutstring = ",".join(revision_lst)+"\n"
            f.write(revision_lineOutstring)
    f.close()    

