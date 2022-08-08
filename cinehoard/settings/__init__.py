"""
Settings for cinehoard
"""


from .base import *

if os.environ.get('HEROKU_PROD'):
   from .prod import *
else:
   from .dev import *
