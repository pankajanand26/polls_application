#!/usr/bin/python 
import os, sys  

os.environ['DJANGO_SETTINGS_MODULE'] = 'mysy.settings'
sys.path.append(os.path.join(os.environ['OPENSHIFT_REPO_DIR'],'mysy'))

virtenv = os.path.join(os.environ['OPENSHIFT_PYTHON_DIR'],'virtenv') 
virtualenv = os.path.join(virtenv, 'bin/activate_this.py') 
  
try:     
	execfile(virtualenv, dict(__file__=virtualenv)) 
except IOError:     
	pass  
# 
# IMPORTANT: Put any additional includes below this line.  If placed above this 
# line, it's possible required libraries won't be in your searchable path 
#  
from django.core.handlers import wsgi 
application = wsgi.WSGIHandler()
