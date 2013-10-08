import os
import sys
import site

# Add the site-packages of the chosen virtualenv to work with
site.addsitedir('~/ecm/env/local/lib/python2.7/site-packages')

# Add the app's directory to the PYTHONPATH
sys.path.append('/home/hemanth/ecm/email_campaign_manager')
sys.path.append('/home/hemanth/ecm/email_campaign_manager/email_campaign_manager')

#os.environ['DJANGO_SETTINGS_MODULE'] = 'email_campaign_manager.settings'
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "email_campaign_manager.pro_settings")

# Activate your virtual env
activate_env="/home/hemanth/ecm/env/bin/activate_this.py"
execfile(activate_env, dict(__file__=activate_env))

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
