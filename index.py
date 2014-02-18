#!/usr/bin/env python
# -*- coding: utf-8 -*-

import urllib2, re, urllib, cgi, codecs
import cgitb

def search(c, q):
  out = []
  regex = re.compile(q, re.IGNORECASE)
  for k in c:
    linehits = regex.findall(c[k]["msg"])
    if linehits:
      out.append((str(k), c[k]["uname"], c[k]["msg"]))
  return out

def readCorpus():
  fin = codecs.open("moroccorp.txt", "r", "utf-8")
  lines = fin.readlines()
  fin.close()
  crp = {}
  i = 1
  for line in lines:
    uname = line.split("\t")[0]
    msg = " ".join(line.split("\t")[1:]).strip()
    crp[i] = {"uname": uname, "msg": msg}
    i += 1
  return crp

def format_table(hits):
  out = "<table>\n"
  for line in hits:
    out += "  <tr>\n"
    for cell in line:
      out += "    <td>" + cell + "</td>\n"
    out += "  </tr>\n"
  out += "</table>\n"
  return out

def search_moroccorp(q):
  moroccorp = readCorpus()
  hits = search(moroccorp, q)
  return format_table(hits)

def cgiFieldStorageToDict( fieldStorage ):
  params = {}
  for key in fieldStorage.keys():
    params[key] = fieldStorage.getlist(key)
  return params

def form2table(form):
  d = cgiFieldStorageToDict(form)
  return search_moroccorp(d["query"])

cgitb.enable(display=1)
form = cgi.FieldStorage()
resulttable = form2table(form)

print "Content-Type: text/html\n"
print '<html>'
print '<body>'
print '<p>you are redirected in 0 seconds</p>'
print resulttable
print '</body></html>'
