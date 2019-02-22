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
    shortlink = re.findall(r"//(?:[-\w.]|(?:%[\da-fA-F]{2}))+/", longlinks)    
    #simplifies = list(set(simplifies))
    return shortlink
        

def WriteOut(lst, filedir, filename):
    i = 0
    #outString = '"link","Count"'
    #name, media_type, media_focus, language, notes, region, subcountry, country
    outString = '"WikiExternalLink","MediaLink","MediaName","MediaType","MediaFocus","MediaLanguage","notes","MediaRegion","MediaSubcountry","MediaCountry","WikiExternalLink_short"'
    for item in lst:
        item_str = ["" if x is None else x for x in item]
        item_str_format = ['"{}"'.format(x) for x in item_str]
        i += 1
        outString += '\n'
        outString += ','.join(item_str_format)
        
#    result_path = '{}/results'.format(file_loc)
#    if not os.path.exists(result_path):
#        os.makedirs(result_path)
        
    with open(filedir+filename, 'w') as f:
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
       


def matchMediaLinks(originallink_list, generalizedLink_list, moreGeneralizedLink_list, all_full_externalLinks):
    
    fulllink_medialink = []
    i=1
    for fulllink in all_full_externalLinks:
        i+=1
        if i%100==0: print (i)
        
        matched = None
        
        for orglink in originallink_list:
            #generalizedLink = row['generalizedLink']
            #moreGeneralizedLink = row['moreGeneralizedLink']
            if orglink in fulllink:#if found from original link
                matched = orglink
                break
        
        if matched is None:#if not found from original link, find from genealized link
            for j in range(len(generalizedLink_list)):
                generalizedLink = generalizedLink_list[j]
                #moreGeneralizedLink = row['moreGeneralizedLink']
                if generalizedLink is not None and generalizedLink in fulllink:#if found
                    orglink2 = originallink_list[j]
                    matched = orglink2
                    break
        
        if matched is None:#not found, found the more generalized link
            for w in range(len(moreGeneralizedLink_list)):
                moreGeneralizedLink = moreGeneralizedLink_list[j]
                #generalizedLink = row['generalizedLink']
                if moreGeneralizedLink is not None and moreGeneralizedLink in fulllink:
                    orglink3 = originallink_list[w]
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
    
    #match links
    originallink_list, generalizedLink_list, moreGeneralizedLink_list, link_dict = abyznewsDict()
    
    matchMediaLinks = matchMediaLinks(originallink_list, generalizedLink_list, moreGeneralizedLink_list, all_full_externalLinks)
    #fulllink_medialink_count = sum([1 if x[1] is not None else 0 for x in matchMediaLinks])
    
    #match media information
    final_media_output = []
    for lst in matchMediaLinks:
        medialink = lst[1]
        if medialink is not None:
            mediaInfo = link_dict[medialink]
            lst_updated = lst + mediaInfo
        else:
            mediaInfo = 8*[None]
            lst_updated = lst + mediaInfo
        
        final_media_output.append(lst_updated)
    
    final_media_output_final = [lst+LinkSimplify(lst[0]) for lst in final_media_output]
    
    #pickle write
#    f = open(filedir+'all_fullexternalLinks_mediamatched.pkl', 'wb')   # Pickle file is newly created where foo1.py is
#    pickle.dump(final_media_output_final, f)          # dump data to f
#    f.close() 

    f = open(filedir+'all_fullexternalLinks_mediamatched.pkl', 'rb')   # 'r' for reading; can be omitted
    final_media_output_final = pickle.load(f)         # load file content as mydict
    f.close()
    
    WriteOut(final_media_output_final, filedir, "all_fullexternalLinks_mediamatched.csv")
    
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

    

















































