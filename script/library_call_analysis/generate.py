#!/usr/bin/python

import sys, os, re, threading, difflib, multiprocessing
from numpy import matrix
from itertools import combinations
from math import log
from multiprocessing.pool import ThreadPool as Pool

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "library_call_analysis.settings")
from library_call_analysis import models

method_call_pattern = re.compile('(.+\=)?\W*(\w+\.)?(\w+)\(.*?(\)\W*;)?')
method_calls = []
method_calls_dict = {}
num_method_calls = 0
method_call_sets = {}
types = ['-', '+']
keys = {'-' : set(), '+' : set()}
method_calls_per_type = {'-' : {'__method__calls___': set()}, '+' : {'__method__calls___': set()}}

pool = Pool()

def add_method_call(method_call, key, type):
   keys[type].add(key)
   method_calls_per_type[type]['__method__calls___'].add(method_call)
   if key not in method_call_sets:
      method_call_sets[key] = {'-':set(), '+':set()}
   method_call_sets[key][type].add(method_call)
   if method_call not in method_calls_dict:
      method_calls_dict[method_call] = {}
   if key not in method_calls_dict[method_call]:
      method_calls_dict[method_call][key] = {'-':0, '+':0}
   method_calls_dict[method_call][key][type] += 1

def generate_data():
   # Generate data for minus/plus, minus, and plus association
   mats = {'both' : [], '-' : [], '+' : [], 'tfidf': {'-':[], '+':[]}}
   type_values = {'-' : [1, 0], '+' : [0, 1]}
   for key, method_call_set in method_call_sets.iteritems():
      rows = {}
      for type in types:
         if len(method_call_set[type]) > 0:
            rows[type] = [0] * num_method_calls
            for method_call in method_call_set[type]:
               rows[type][method_calls_dict[method_call]['index']] = 1
      for type in types:
         if type in rows:
            mats['both'].append(rows[type] + type_values[type])

   for type in types:
      for key in keys[type]:
         N = len(method_calls_per_type[type])
         # association
         row = [0] * N
         for method_call in method_call_sets[key][type]:
            row[method_calls_per_type[type][method_call]] = 1
         mats[type].append(row)
         # tfidf
         row = [0] * N
         for method_call in method_call_sets[key][type]:
            row[method_calls_per_type[type][method_call]] = \
                  method_calls_dict[method_call][key][type] * log(N/float(method_calls_dict[method_call]['df'][type]))
         mats['tfidf'][type].append(row)
   return mats

def write_data_to_file(data, filename):
   with open(filename, 'wb') as f:
      for row in data:
         for item in row:
            f.write(str(item) + ' ')
         f.write('\n')

if __name__ == "__main__":
   if len(sys.argv) < 2:
      print "Please provide project name"
      quit(-1)

   slug = sys.argv[1]

   repos = models.Repository.objects.filter(slug=slug).prefetch_related('patch_set')

   for repo in repos:
      for patch in repo.patch_set.all().prefetch_related('diff_set'):
         key = patch.sha1
         for diff in patch.diff_set.all():
            for match in re.finditer(method_call_pattern, diff.code):
               method_call = match.groups()[2]
               add_method_call(method_call, key, diff.type)

   method_calls = set()
   for type in types:
      keys[type] = list(keys[type])
      method_calls.update(method_calls_per_type[type]['__method__calls___'])
      method_calls_per_type[type]['__method__calls___'] = list(method_calls_per_type[type]['__method__calls___'])
      for i in xrange(len(method_calls_per_type[type]['__method__calls___'])):
         method_calls_per_type[type][method_calls_per_type[type]['__method__calls___'][i]] = i

   method_calls = list(method_calls)

   for count_dict in method_calls_dict.itervalues():
      df_minus = reduce(lambda x, y: x + 1 if y['-'] > 0 else x, count_dict.itervalues(), 0)
      df_plus = reduce(lambda x, y: x + 1 if y['+'] > 0 else x, count_dict.itervalues(), 0)
      count_dict['df'] = {'-' : df_minus, '+' : df_plus}

   num_method_calls = len(method_calls)
   for i in xrange(num_method_calls):
      method_calls_dict[method_calls[i]]['index'] = i

   mats = generate_data()

   dir = os.getcwd()+'/'+slug+'/'
   try:
      os.mkdir(dir)
   except:
      pass

   write_data_to_file(mats['both'], dir+'assoc_minus_plus.txt')
   write_data_to_file(mats['-'], dir+'assoc_minus.txt')
   write_data_to_file(mats['+'], dir+'assoc_plus.txt')
   write_data_to_file([method_calls_per_type['-']], dir+'method_calls_minus.txt')
   write_data_to_file([method_calls_per_type['+']], dir+'method_calls_plus.txt')
   write_data_to_file([method_calls+types], dir+'method_calls_with_types.txt')
   write_data_to_file(mats['tfidf']['-'], dir+'tfidf_minus.txt')
   write_data_to_file(mats['tfidf']['+'], dir+'tfidf_plus.txt')
