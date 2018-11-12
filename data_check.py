#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Nov 11 21:15:47 2018

@author: jiajunluo
"""

import pandas as pd

data = pd.read_table("/Users/jiajunluo/OneDrive/Documents/Pitt_PhD/ResearchProjects/WikiWorldEvent/data/all_contributors.txt", 
                             sep='||', error_bad_lines = False)
