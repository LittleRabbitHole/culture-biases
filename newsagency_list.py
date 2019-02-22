#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb 20 16:45:43 2019

http://www.abyznewslinks.com/allco.htm

@author: angli
"""


import json
import pandas as pd
import re


def generalizeLink(link):
    generalizedLink = link[link.find('://') + 3:]
    return generalizedLink


def moreGeneralizeLink(link):
    moreGeneralizedLink_lst = re.findall(r"//(?:[-\w.]|(?:%[\da-fA-F]{2}))+/", link)
    if len(moreGeneralizedLink_lst)>0:
        moreGeneralizedLink = moreGeneralizedLink_lst[0]
    else:
        moreGeneralizedLink = None
    return moreGeneralizedLink


def abyznewsDict():
    filedir = "/Users/angli/Ang/OneDrive/Documents/Pitt_PhD/ResearchProjects/WikiWorldEvent/Project_IS_Neutrality/abyznewslinks/"
    
#    with open(filedir+'mediasources.json') as f:
#        data = json.load(f)
#    f.close()
    
    data = pd.read_table(filedir+"mediasources.csv", sep=',')
    data["generalizedLink"] = data['link'].apply(generalizeLink)
    data["moreGeneralizedLink"] = data['link'].apply(moreGeneralizeLink)
    
    
    
    
#    allnewslinks = list(data['link'])
#    allnewslinks = [x for x in allnewslinks if x is not ""]
#    allnewslinks = [x for x in allnewslinks if x is not None]
#    generalizedLinks = []
#    for link in allnewslinks:
#        link = link[link.find('://') + 3:] 
#        generalizedLinks.append(link)
#    generalizedLinks = list(set(generalizedLinks))    
#    
#    
#    link_dict = {}
#    for lst in data:
#        link = lst['link']
#        name = lst['name']
#        media_type = lst['media_type']
#        media_focus = lst['media_focus']
#        language = lst['language']
#        notes = lst['notes']
#        region = lst['region']
#        subcountry = lst['subcountry']
#        country = lst['country']
#        link_dict[link] = [name, media_type, media_focus, language, notes, region, subcountry, country]
#    
#    return allnewslinks, link_dict
    return data