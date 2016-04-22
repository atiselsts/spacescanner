#!/usr/bin/env python

# Copyright (c) 2009, Giampaolo Rodola'. All rights reserved.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.

"""This module is deprecated as exceptions are defined in _error.py
and are supposed to be accessed from 'psutil' namespace as in:
- psutil_local.NoSuchProcess
- psutil_local.AccessDenied
- psutil_local.TimeoutExpired
"""

import warnings
from psutil_local._error import *

warnings.warn("psutil_local.error module is deprecated and scheduled for removal; " \
              "use psutil namespace instead", category=DeprecationWarning,
               stacklevel=2)
