#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Nov 11 21:15:47 2018

@author: jiajunluo
"""

import pandas as pd

#check articles
all_articles = pd.read_table("/Users/jiajunluo/OneDrive/Documents/Pitt_PhD/ResearchProjects/WikiWorldEvent/data/all_article_pages_notitle.txt", 
                             sep=',', error_bad_lines = False)
all_articles.columns.values
all_articles = all_articles.drop_duplicates()

data = pd.read_table("/Users/jiajunluo/OneDrive/Documents/Pitt_PhD/ResearchProjects/WikiWorldEvent/data/all_contributors.txt", 
                             sep='\\|\\|', error_bad_lines = False)

