# -*- coding: utf-8 -*-
"""
Created on Wed Mar 21 11:25:56 2018

@author: Theo
"""


import datetime


date_beginning2016 = datetime.datetime(2016, 4, 1).timestamp() #year, month, day,
date_release = datetime.datetime(2016, 10, 16).timestamp() 
date_6months = datetime.datetime(2017, 4, 16).timestamp()
date_1year = datetime.datetime(2017, 10, 16).timestamp()

def six_months(commit):
    if commit.committed_date > date_release and commit.committed_date< date_6months:
        return True
    return False
    
      
def one_year(commit):
    if commit.committed_date > date_release and commit.committed_date< date_1year:
        return True
    return False
    
def beginning_2016(commit):
    if commit.committed_date > date_beginning2016 and commit.committed_date< date_release:
        return True
    return False