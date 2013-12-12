#!/usr/bin/python

import sys, os, re, threading, difflib, multiprocessing
from numpy import matrix, unique
from multiprocessing.pool import ThreadPool as Pool

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "library_call_analysis.settings")
from library_call_analysis import models

method_call_pattern = re.compile('(.+\=)?\W*(\w+\.)?(\w+)\(.*?(\)\W*;)?')
method_calls = []
method_calls_dict = {}
num_method_calls = 0
method_call_sets = {}
pool = Pool()

def find_rules(transactions, minSup=.05, minConf=.5, nRules=100, sortFlag=1):
   Rules = [] # tuples of sets
   FreqItemSets = [] # itemsets of size 1, 2, 3 ...

   M = transactions.shape[0]
   N = transactions.shape[1]
   # print M, N
   # print transactions
   T = set()
   means = transactions.mean(0)
   for i in xrange(means.size):
      if means.item(i) >= minSup:
         T.add(i)
   FreqItemSets.append(T)

   for steps in xrange(2, N+1):
      T = frozenset(T)
      if len(T) < 2:
         break
      # TODO

   # print FreqItemSets

   return Rules, FreqItemSets

def print_rules(rules, labels):
   for rule in rules:
      left_str = ''
      for fea in rule[0]:
         left_str = left_str + labels[fea] + ', '
      left_str = left_str[:-2]
      rigtht_str = ''
      for fea in rule[1]:
         rigtht_str = rigtht_str + labels[fea] + ', '
      rigtht_str = rigtht_str[:-2]
      print "{%s} => {%s}, support: %d, confidence: %d" % \
            (left_str, rigtht_str, rule[2], rule[3])


def analyze():
   # Analyze minus/plus, minus, and plus association
   mats = [[], [], []]
   for method_call_set in method_call_sets.itervalues():
      rows = {}
      for type in ['-', '+']:
         rows[type] = [0] * num_method_calls
         for method_call in method_call_set[type]:
            rows[type][method_calls_dict[method_call]] = 1
      mats[0].append(rows['-'] + [1, 0])
      mats[0].append(rows['+'] + [0, 1])
      mats[1].append(rows['-'])
      mats[2].append(rows['+'])

   # minus/plus
   Rules0, FreqItemSets0 = find_rules(matrix(mats[0]))
   # minus
   Rules1, FreqItemSets1 = find_rules(matrix(mats[1]))
   # plus
   Rules2, FreqItemSets2 = find_rules(matrix(mats[2]))

if __name__ == "__main__":
   if len(sys.argv) < 2:
      print "Please provide project name"
      quit(-1)

   slug = sys.argv[1]

   repos = models.Repository.objects.filter(slug=slug).prefetch_related('patch_set')

   method_calls = set()

   for repo in repos:
      for patch in repo.patch_set.all().prefetch_related('diff_set'):
         if patch.sha1 not in method_call_sets:
            method_call_sets[patch.sha1] = {'-':set(), '+':set()}
         for diff in patch.diff_set.all():
            for match in re.finditer(method_call_pattern, diff.code):
               method_call = match.groups()[2]
               method_calls.add(method_call)
               method_call_sets[patch.sha1][diff.type].add(method_call)

   method_calls = list(method_calls)

   num_method_calls = len(method_calls)
   for i in xrange(num_method_calls):
      method_calls_dict[method_calls[i]] = i

   analyze()
