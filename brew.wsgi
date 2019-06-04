#!/usr/bin/env python3

import sys
import os

path = os.path.dirname(__file__)
if path not in sys.path:
    sys.path.insert(0, path)

import monitor
monitor.start(path)

from brew import app as application

