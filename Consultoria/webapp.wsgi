import os
import sys

PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
activate_this = PROJECT_ROOT + '/env/bin/activate_this.py'
execfile(activate_this, dict(__file__=activate_this))

sys.path.insert(0, PROJECT_ROOT)

from run import app as application
