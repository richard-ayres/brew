#!/usr/bin/env python3

import sys
sys.path.insert(0, '/var/www/brew/')

print(sys.path)

from brew import app as application

