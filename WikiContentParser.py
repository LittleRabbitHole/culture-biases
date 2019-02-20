#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb 19 11:47:39 2019

wikitext parser:
    https://www.mediawiki.org/wiki/API:Parsing_wikitext#parse

compare to:
    https://www.mediawiki.org/wiki/API:Compare

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
    simplifies = []
    for longsource in infosources:
        shortsource = re.findall(r"//(?:[-\w.]|(?:%[\da-fA-F]{2}))+/", longsource)
        simplifies = simplifies + shortsource
    
    #simplifies = list(set(simplifies))
    return simplifies

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
       


if __name__ == '__main__':
    filedir = "/Users/angli/Ang/OneDrive/Documents/Pitt_PhD/ResearchProjects/WikiWorldEvent/Project_IS_Neutrality/data/"
    #filedir = "/Users/jiajunluo/OneDrive/Documents/Pitt_PhD/ResearchProjects/WikiWorldEvent/Project_IS_Neutrality/data/"
    data = pd.read_table(filedir+"all_article_pages.csv", sep=',')
    #data.columns.values
    final_article = data[['final_page_pgid', 'post_id']].drop_duplicates()
    all_externalLinks = externalLinks(final_article)
    
    counter = Counter(all_externalLinks)
    most_common = counter.most_common(50000)
    WriteOutMostCommon(most_common, filedir)
    
    f = open(filedir+'domain_dict.pkl', 'rb')   # 'r' for reading; can be omitted
    domain_dict = pickle.load(f)         # load file content as mydict
    f.close()

    
    links_df = pd.read_table(filedir+"mostcommon_links.csv", sep=',')
    links_df['domain'] = links_df.apply(processLinks, axis=1, domain_dict = domain_dict)
    links_df.to_csv(filedir+"mostcommon_links_domain.csv", index=False)



api = "https://en.wikipedia.org/w/api.php?action=parse&pageid=39750126&prop=externallinks|revid|text&format=json"

response=requests.get(api)
responsedata = returnJsonCheck(response)

infosources = responsedata["parse"]["externallinks"]
url_implifies = list(set([re.match('(|https?:)//(?:[-\w.]|(?:%[\da-fA-F]{2}))+/', url)[0] for url in infosources]))

url_simplifies = [re.findall(r"//(?:[-\w.]|(?:%[\da-fA-F]{2}))+/", url) for url in infosources]



raw_html = responsedata["parse"]["text"]["*"]
document = html.document_fromstring(raw_html)
paragraphs = document.xpath('//p')
len(paragraphs)
p1 = paragraphs[2].text_content()

diffapi = "https://en.wikipedia.org/w/api.php?action=compare&fromrev=883641819&torev=883139142&format=json"
"https://en.wikipedia.org/w/api.php?action=compare&fromrev=883641819&torev=883139142&prop=diff|size|user|parsedcomment"

response=requests.get(diffapi)
responsedata = returnJsonCheck(response)


raw_html = responsedata["compare"]["*"]
document = html.document_fromstring(raw_html)
dels = document.xpath('//del')
deltext = dels[1].text_content()
adds = document.xpath('//ins')
adds[0].text_content()

re.findall(r"//(?:[-\w.]|(?:%[\da-fA-F]{2}))+/", deltext)








