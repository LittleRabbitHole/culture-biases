#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb 22 10:55:24 2019

@author: angli
"""

import pickle
import pandas as pd
import os
import requests
import sys
from lxml import html
import re
from collections import Counter
from newsagency_list import abyznewsDict

def returnJsonCheck(response) -> dict:
    try:
        return response.json()
    except:
        print("ERROR")
        print(response)
        print(response.text)
        sys.exit("json error")


def callExternalLink(url):
    response=requests.get(url)
    responsedata = returnJsonCheck(response)
    infosources = responsedata["parse"]["externallinks"]
    return infosources

def externalLinks(final_article):
    all_externalLinks = []
    n=0
    for ind, row in final_article.iterrows():
        n+=1
        if n%100==0: print (n)
        pageid = str(row['final_page_pgid'])
        #postid = row['post_id']
        url = "https://en.wikipedia.org/w/api.php?action=parse&pageid={}&prop=externallinks|revid&format=json".format(pageid)
        page_externalinks = callExternalLink(url)
        all_externalLinks = all_externalLinks + page_externalinks
    return all_externalLinks    


def LinkSimplify(longlinks):
    simplifies = []
    for longsource in longlinks:
        shortsource = re.findall(r"//(?:[-\w.]|(?:%[\da-fA-F]{2}))+/", longsource)
        simplifies = simplifies + shortsource
    
    #simplifies = list(set(simplifies))
    return simplifies
        

def WriteOutMostCommon(most_common, filedir):
    i = 0
    outString = '"link","Count"'
    for item in most_common:
        i += 1
        link = '"{}"'.format(item[0])
        count = '"{}"'.format(item[1])
        outString += '\n'
        outString += ','.join([link, count])
        
#    result_path = '{}/results'.format(file_loc)
#    if not os.path.exists(result_path):
#        os.makedirs(result_path)
        
    with open(filedir+"mostcommon_links.csv", 'w') as f:
        f.write(outString)
        f.close()
        
    
def processLinks(row, domain_dict):
   link = row['link']
   link_seg = link.split(".")
   last = link_seg[-1].replace('/','')
   lastsecond = '.'.join(link_seg[-2::]).replace('/','')
   if len(link_seg)>1:
       second = link_seg[-2].replace('/','')
   else:
       second = None
   domain_allretrieve = [domain_dict.get(last), domain_dict.get(second),domain_dict.get(lastsecond)]
   domain = list(set([x for x in domain_allretrieve if x is not None]))
   special_domain = [y for y in domain if y not in ["com","net"]]
   if len(special_domain) != 0:
       domain_str = "::".join(special_domain)
   else:
       domain_str = ""
   return domain_str
       


def matchMediaLinks(medialinks_df, all_full_externalLinks):
    fulllink_medialink = []
    i=1
    for fulllink in all_full_externalLinks:
        i+=1
        if i%50==0: print (i)
        
        matched = None
        
        for ind, row in medialinks_df.iterrows():
            orglink = row['link']
            #generalizedLink = row['generalizedLink']
            #moreGeneralizedLink = row['moreGeneralizedLink']
            if orglink in fulllink:#if found from original link
                matched = orglink
                break
        
        if matched is None:#if not found from original link, find from genealized link
            for ind, row in medialinks_df.iterrows():
                orglink2 = row['link']
                generalizedLink = row['generalizedLink']
                #moreGeneralizedLink = row['moreGeneralizedLink']
                if generalizedLink is not None and generalizedLink in fulllink:#if found
                    matched = orglink2
                    break
        
        if matched is None:#not found, found the more generalized link
            for ind, row in medialinks_df.iterrows():
                orglink3 = row['link']
                #generalizedLink = row['generalizedLink']
                moreGeneralizedLink = row['moreGeneralizedLink']
                if moreGeneralizedLink is not None and moreGeneralizedLink in fulllink:
                    matched = orglink3
                    break
                        
        fulllink_medialink.append([fulllink, matched])
    return fulllink_medialink

if __name__ == '__main__':
    filedir = "/Users/angli/Ang/OneDrive/Documents/Pitt_PhD/ResearchProjects/WikiWorldEvent/Project_IS_Neutrality/data/"
    #filedir = "/Users/jiajunluo/OneDrive/Documents/Pitt_PhD/ResearchProjects/WikiWorldEvent/Project_IS_Neutrality/data/"
    data = pd.read_table(filedir+"all_article_pages.csv", sep=',')
    #data.columns.values
    final_article = data[['final_page_pgid', 'post_id']].drop_duplicates()
    all_full_externalLinks = externalLinks(final_article)

    #pickle write
#    f = open(filedir+'all_fullexternalLinks.pkl', 'wb')   # Pickle file is newly created where foo1.py is
#    pickle.dump(all_full_externalLinks, f)          # dump data to f
#    f.close() 

    f = open(filedir+'all_fullexternalLinks.pkl', 'rb')   # 'r' for reading; can be omitted
    all_full_externalLinks = pickle.load(f)         # load file content as mydict
    f.close()
    
    medialinks_df = abyznewsDict()
    
    all_full_externalLinks = list(set(all_full_externalLinks))
    
    fulllink_medialink_count = sum([1 if len(x[1])>0 else 0 for x in fulllink_medialink])
    
    
    
    
    #simplify the full external links
    all_short_externalLinks = LinkSimplify(all_full_externalLinks)
    
    counter = Counter(all_short_externalLinks)
    most_common = counter.most_common(50000)
    WriteOutMostCommon(most_common, filedir)
    
    f = open(filedir+'domain_dict.pkl', 'rb')   # 'r' for reading; can be omitted
    domain_dict = pickle.load(f)         # load file content as mydict
    f.close()

    
    links_df = pd.read_table(filedir+"mostcommon_links.csv", sep=',')
    links_df['domain'] = links_df.apply(processLinks, axis=1, domain_dict = domain_dict)
    links_df.to_csv(filedir+"mostcommon_links_domain.csv", index=False)
    
    #some analysis for use -- comment out in the future
    allshortlinks = list(links_df['link'])
    allshortlinks = [x.replace("/","") for x in allshortlinks]
    allshortlinks = [x.split(".") for x in allshortlinks]
    linkwords_flat = [t for cell in allshortlinks for t in cell]
    counter = Counter(linkwords_flat)
    most_common_words = counter.most_common(30000)
    words_needsignore = ['www', 'com', 'org', 'gov', 'edu','net','www2','web','www1','www3']

    

















































