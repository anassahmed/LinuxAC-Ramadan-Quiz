'''
Created on Jul 19, 2012

@author: anass
'''

import sys, os.path
from main import linuxQuiz

d=os.path.dirname(sys.argv[0])
print d

from paste import httpserver

lookup=[os.path.join(d,'themes')]
app=linuxQuiz(
lookup, 'default', '/_theme/',
staticBaseDir={'/static/':os.path.join(d, 'default/static/'),}
  );
# for options see http://pythonpaste.org/modules/httpserver.html
httpserver.serve(app, host='127.0.0.1', port='8080') # to serve publically
#httpserver.serve(app, host='127.0.0.1', port='8080') # to serve localhost