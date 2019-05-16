#!/usr/bin/python3
import sys

import logging
logging.basicConfig(stream=sys.stderr)

sys.path.insert(0,"/var/www/borkbook/")
sys.path.insert(0,"/var/www/borkbook/borkbook/")

from borkbook import app as application
