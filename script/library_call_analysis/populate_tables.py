#!/bin/python

import sys, os, re, threading, difflib, multiprocessing
from pygit2 import *
from functools import partial
from multiprocessing.pool import ThreadPool as Pool

path = os.path.dirname(os.path.abspath(sys.argv[0]))
sys.path.append(path)
sys.path.append(path+"/library_call_analysis")
os.environ['DJANGO_SETTINGS_MODULE'] = 'library_call_analysis.settings'

from library_call_analysis import models

re_cs_file_comment = re.compile(r"^\s*(/\*|\*\s|//)")
re_cs_file_misc = re.compile(r"^\s*({|})\s*$")
re_cs_file = re.compile(r"\.cs$", re.IGNORECASE)
re_fixing_commit_message = re.compile(r"(fix|patch|bug)", re.I)
re_unified_diff_line_numbers = re.compile(r"@@ -(\d+),\d+ \+(\d+),\d+ @@")

re_thread_id = re.compile(r"Thread-(\d+)")

master = "refs/heads/master"


repo = None
db_repo = None

def is_merge(git_commit):
   return len(git_commit.parents) > 1

def previous_revision(sha1):
   return "%s~1" % sha1

def update(hunk, context):
   _hunk = {
            'start_line_number' : hunk.new_start,
            '-' : [],
            '+' : [],
           }
   context['hunks'].append(_hunk);

   line_count = {
                  '-' : hunk.old_start - 1,
                  '+' : hunk.new_start - 1
                }

   for line in hunk.lines:
      if line[0] == '-' or line[0] == '+':
         line_count[line[0]] += 1
         line_content = line[1].encode('ascii','ignore').rstrip('\r\n').strip()
         if line_content and \
               not re_cs_file_comment.match(line_content) and\
               not re_cs_file_misc.match(line_content):
            _hunk[line[0]].append(
                  {
                     'line_number' : line_count[line[0]],
                     'code' : line_content
                  }
            )
      else:
         line_count['+'] += 1
         line_count['-'] += 1

   return context

def fini(context):
   db_patch, created = models.Patch.objects.get_or_create(
         repo=db_repo,
         sha1=context['sha1'],
         filename=context['filename']
         )
   models.Diff.objects.bulk_create([models.Diff(
      patch=db_patch,
      start_line_number=hunk['start_line_number'],
      line_number=diff['line_number'],
      code=diff['code'],
      type=type
      ) for hunk in context['hunks'] for type in ('+', '-') for diff in hunk[type]])
   return None

def process_diff(patch, hexsha):
   if not patch.old_file_path or not patch.new_file_path \
         or not patch.status == 'M' \
         or not patch.old_file_path == patch.new_file_path:
            return

   filename = patch.new_file_path

   if not re_cs_file.search(filename):
      return

   context = {
         'sha1'     : hexsha,
         'filename' : filename,
         'hunks'    : []
         }

   for hunk in patch.hunks:
      context = update(hunk, context)

   fini(context)

def is_fix_commit(commit):
   return not is_merge(commit) and re_fixing_commit_message.search(commit.message)

def analyze(hex):
   # An exception occurs if this commit does not have any previous commits
   try:
      diff = repo.diff(previous_revision(hex), hex)
      patches = [p for p in diff]
      map(partial(process_diff, hexsha=hex), patches)
   except:
      raise
      #pass

if __name__ == "__main__":
   if len(sys.argv) < 2:
      print "Please provide project directory"
      quit(-1)

   directory = sys.argv[1]

   repo = Repository(directory)

   slug = repo.workdir.split('/')[-2]

   db_repo, created = models.Repository.objects.get_or_create(slug=slug)

   master_ref = repo.lookup_reference("refs/heads/master").resolve()
   commits = repo.walk(master_ref.target, GIT_SORT_NONE)

   commit_hexs = [commit.hex for commit in commits if is_fix_commit(commit)]

   pool = Pool()

   pool.map(analyze, commit_hexs)
