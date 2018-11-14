#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Nov 11 21:15:47 2018

@author: jiajunluo
"""

import pandas as pd

#check articles
all_articles = pd.read_table("/Users/jiajunluo/OneDrive/Documents/Pitt_PhD/ResearchProjects/WikiWorldEvent/data/all_article_pages.txt", 
                             sep='\\|\\|', error_bad_lines = False)
all_articles.columns.values

original_articles = all_articles[['Ori_PageID','title']].loc[all_articles['PageType'] == "orig"]
original_articles = original_articles.drop_duplicates()

all_articles = all_articles.drop_duplicates()

data = pd.read_table("/Users/jiajunluo/OneDrive/Documents/Pitt_PhD/ResearchProjects/WikiWorldEvent/data/all_contributors.txt", 
                             sep='\\|\\|', error_bad_lines = False)

