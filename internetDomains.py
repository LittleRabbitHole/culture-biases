#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb 20 15:22:30 2019

this file is to prepare domain dict

@author: angli
"""


import pickle

def process(txt):
    sections = txt.split("\n\n")
    domain_dict = {}
    for section in sections:
        data_linelist = section.split("\n")
        data_linelist_clean = []
        for line in data_linelist:
            if line[:2] == '//': 
                pass
            else:
                data_linelist_clean.append(line) 
        for item in data_linelist_clean:
            domain_dict[item] = data_linelist_clean[0]
    return domain_dict


if __name__ == '__main__':
    filedir = "/Users/angli/Ang/OneDrive/Documents/Pitt_PhD/ResearchProjects/WikiWorldEvent/Project_IS_Neutrality/data/"
    #filedir = "/Users/jiajunluo/OneDrive/Documents/Pitt_PhD/ResearchProjects/WikiWorldEvent/Project_IS_Neutrality/data/"
    file = "effective_tld_names.dat.txt"
    
    f = open(filedir+file, 'r')
    txt = f.read()
    f.close()

    domain_dict = process(txt)
    #domain_dict['gov']
 
    
    #pickle load
    f = open(filedir+'domain_dict.pkl', 'wb')   # Pickle file is newly created where foo1.py is
    pickle.dump(domain_dict, f)          # dump data to f
    f.close() 
    
    #f = open('domain_dict.pkl', 'rb')   # 'r' for reading; can be omitted
    #domain_dict = pickle.load(f)         # load file content as mydict
    #f.close()

    
#    {
#            "com":"com",
#            "org":"org",
#            "net":"net",
#            "int":"int",
#            "edu":"edu",
#            "gov":"gov",
#            "mil":"mil",
#            
#            
#            
#            
#            
#            }