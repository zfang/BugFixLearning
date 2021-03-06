#!/usr/bin/python

from django.db import models

LANGUAGE_TYPES = (
      (0, 'C#'),
      (1, 'C/C++'),
      (2, 'Java')
)

DIFF_TYPES = (
      ('+', 'Plus'),
      ('-', 'Minus')
)

class DotnetLibraryClass(models.Model):
   namespace = models.CharField(max_length=255)
   classname = models.CharField(max_length=255)
   function = models.CharField(max_length=255)
   def __unicode__(self):
      return "namespace: %s\nclassname: %s\nfunction: %s\n" \
            % (namespace, classname, function)

class CSharpKeyword(models.Model):
   keyword = models.CharField(max_length=30)
   def __unicode__(self):
      return "keyword: %s\n" \
            % (keyword)

class CKeyword(models.Model):
   keyword = models.CharField(max_length=30)
   def __unicode__(self):
      return "keyword: %s\n" \
            % (keyword)

class Repository(models.Model):
   slug = models.CharField(max_length=50)
   language = models.IntegerField(choices=LANGUAGE_TYPES)
   def __unicode__(self):
      return "id: %d\nslug: %s\n" % (self.id, self.slug)

class Patch(models.Model):
   repo = models.ForeignKey(Repository)
   sha1 = models.CharField(max_length=40)
   filename = models.CharField(max_length=255)
   commit_time = models.DateTimeField()
   def __unicode__(self):
      return "repo_id: %d\nsha1: %s\nfilename: %s\n" \
            % (self.repo.id, self.sha1, self.filename)

class Diff(models.Model):
   patch = models.ForeignKey(Patch)
   start_line_number = models.IntegerField()
   line_number = models.IntegerField()
   code = models.TextField()
   type = models.CharField(max_length=1, choices=DIFF_TYPES)
   def __unicode__(self):
      return "patch_id: %d\nstart_line_number: %d\nline_number: %d\ncode: %s\ntype: %s\n" \
            % (self.patch.id, self.start_line_number, self.line_number, self.code, self.type)

class LibraryCallChangeDiff(models.Model):
   diff = models.ForeignKey(Diff)
   def __unicode__(self):
      return "diff_id: %d\n" \
            % (self.diff.id)
