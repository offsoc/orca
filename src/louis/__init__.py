# Liblouis Python bindings
#
# Copyright 2007-2008 Eitan Isaacson
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Library General Public
# License as published by the Free Software Foundation; either
# version 2 of the License, or (at your option) any later version.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Library General Public License for more details.
#
# You should have received a copy of the GNU Library General Public
# License along with this library; if not, write to the
# Free Software Foundation, Inc., 59 Temple Place - Suite 330,
# Boston, MA 02111-1307, USA.

"""Liblouis Python bindings"""

__copyright__ = "Copyright (c) 2007-2008 Eitan Isaacson"
__license__   = "LGPL"

from _louis import *
from constants import *
import os

def listTables():
   tables = {}
   try:
      for fname in os.listdir(TABLES_DIR):
         if fname[-4:] in ('.utb', '.ctb'):
            alias = fname[:-4]
            tables[TABLE_NAMES.get(alias, alias)] = \
                                          os.path.join(TABLES_DIR, fname)
   except OSError:
      pass

   return tables

def getDefaultTable():
   try:
      for fname in os.listdir(TABLES_DIR):
         if fname[-4:] in ('.utb', '.ctb'):
            if fname.startswith('en-us'):
               return os.path.join(TABLES_DIR, fname)
   except OSError:
      pass

   return ''
