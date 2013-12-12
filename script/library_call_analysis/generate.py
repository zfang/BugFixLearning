#!/usr/bin/python

import sys, os, re, threading, difflib, multiprocessing
from numpy import matrix
from itertools import combinations
from multiprocessing.pool import ThreadPool as Pool

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "library_call_analysis.settings")
from library_call_analysis import models

method_call_pattern = re.compile('(.+\=)?\W*(\w+\.)?(\w+)\(.*?(\)\W*;)?')
method_calls = []
method_calls_dict = {}
num_method_calls = 0
method_call_sets = {}
pool = Pool()
types = ['-', '+']

def generate_data():
   # Generate data for minus/plus, minus, and plus association
   mats = {'both' : [], '-' : [], '+' : []}
   type_values = {'-' : [1, 0], '+' : [0, 1]}
   for method_call_set in method_call_sets.itervalues():
      rows = {}
      for type in types:
         rows[type] = [0] * num_method_calls
         for method_call in method_call_set[type]:
            rows[type][method_calls_dict[method_call]] = 1
      for type in types:
         if len(rows[type]) > 0:
            mats['both'].append(rows[type] + type_values[type])
            mats[type].append(rows[type])
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

   method_calls = set()

   for repo in repos:
      for patch in repo.patch_set.all().prefetch_related('diff_set'):
         key = patch.filename
         if key not in method_call_sets:
            method_call_sets[key] = {'-':set(), '+':set()}
         for diff in patch.diff_set.all():
            for match in re.finditer(method_call_pattern, diff.code):
               method_call = match.groups()[2]
               method_calls.add(method_call)
               method_call_sets[key][diff.type].add(method_call)

   method_calls = list(method_calls)

   num_method_calls = len(method_calls)
   for i in xrange(num_method_calls):
      method_calls_dict[method_calls[i]] = i

   mats = generate_data()

   dir = os.getcwd()+'/'+slug+'/'
   try:
      os.mkdir(dir)
   except:
      pass

   write_data_to_file(mats['both'], dir+'minus_plus.txt')
   write_data_to_file(mats['-'], dir+'minus.txt')
   write_data_to_file(mats['+'], dir+'plus.txt')
   write_data_to_file([method_calls], dir+'method_calls.txt')
   write_data_to_file([method_calls+types], dir+'method_calls_with_types.txt')
