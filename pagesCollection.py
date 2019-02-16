#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov 15 12:52:05 2018
this for collecting all the pages + redirect pages
@author: angli
"""
import pandas as pd
import pickle
from utilities import GetAllPageswithDirect, WriteOut_Lst2Str1, WriteOut_Lst2Str2

###main   
#base_data_allarticles_1109 -- process_data_with_topic_location
data = pd.read_table("/Users/angli/Ang/OneDrive/Documents/Pitt_PhD/ResearchProjects/WikiWorldEvent/Project_IS_Neutrality/data/post_articles_set_filter_death.csv", sep=',', error_bad_lines = False)
data['wiki_lang'] = "en"
data['article'] = data['en_title']
#data.columns.values

#all the event article pages = 732
article_df = data[['post_id','wiki_lang','article', 'en_pageid']].drop_duplicates()#3265

#collect all the redirect pages for the current event articles = 26745
all_article_pages = GetAllPageswithDirect(article_df)
#pickle load
f = open('/Users/angli/Ang/OneDrive/Documents/Pitt_PhD/ResearchProjects/WikiWorldEvent/data/all_article_pages.pkl', 'wb')   # Pickle file is newly created where foo1.py is
pickle.dump(all_article_pages, f)          # dump data to f
f.close() 

#f = open('gradesdict.pkl', 'rb')   # 'r' for reading; can be omitted
#mydict = pickle.load(f)         # load file content as mydict
#f.close()

#write all the pages into csv
WriteOut_Lst2Str1(all_article_pages, "/Users/angli/Ang/OneDrive/Documents/Pitt_PhD/ResearchProjects/WikiWorldEvent/data/all_article_pages.txt") #with title
WriteOut_Lst2Str2(all_article_pages, "/Users/angli/Ang/OneDrive/Documents/Pitt_PhD/ResearchProjects/WikiWorldEvent/data/all_article_pages_notitle.txt") #without title

