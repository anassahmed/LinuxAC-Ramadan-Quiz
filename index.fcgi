#!/usr/bin/python2.7
#_*_ coding: UTF-8 _*_

import os.path, sys

d=os.path.expanduser("~/python-modules/linuxac_quiz")
sys.path.insert(0, d)

import flup.server.fcgi
from main import linuxQuiz

lookup=[os.path.join(d,'themes')]
app=linuxQuiz(
lookup, 'default', '/_theme/',
staticBaseDir={'/static/':os.path.join(d, 'default/static/'),}
  );
  
flup.server.fcgi.WSGIServer(app).run()