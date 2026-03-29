# -*- coding: utf-8 -*-
"""
Created on Sat Mar 28 19:47:31 2026

@author: pathouli
"""

from utils import *

data_path = "C:/Users/ultra/Desktop/data/"
out_path = "C:/Users/ultra/Desktop/data/output/"

the_data = file_crawler(data_path)

all_d = all_dictionary(the_data, "body")

the_data["body_sw"] = the_data["body"].apply(rem_sw)

print(the_data.head())

all_d_sw = all_dictionary(the_data, "body_sw")

print(all_d_sw.head())

the_data["body_sw_stem"] = the_data["body_sw"].apply(
    lambda x: ps_lemma(x, "ps"))


the_data["body_sw_lemma"] = the_data["body_sw"].apply(
    lambda x: ps_lemma(x, "lemma"))

all_d_sw_stem = all_dictionary(the_data, "body_sw_stem")

