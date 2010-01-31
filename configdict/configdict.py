#!/usr/bin/python

'''Configuration file parser.

A setup file consists of sections, lead by a "[section]" header,
and followed by "name = value" entries, with continuations allowed
by escaping EOL with a backslash (\).

For example::

    options = this \
            is \
            a \
            test

The option values can contain format strings which refer to other values in
the same section, or values in a special [DEFAULT] section::

    [widgets]
    size = large
    description = %(size)s widgets

'''

import sys
import re

from utils import DefaultDict
from utils import FileReader

re_set_val = re.compile('\s*(\S[^=]*[^\s=])\s*=\s*(.*)')

class NoSourceError (Exception):
    pass

def DDMaker(default):
    def _():
        return DefaultDict(default=default)

    return _

class Section(DefaultDict):
    '''This represents a section of a configuration file.  A section 
    receives a references to a parent configuration object, which is where
    it will look for default values.'''

    def __init__ (self, name, parent):
        super(Section, self).__init__(default=DDMaker({}))
        self.name = name
        self.parent = parent

    def __getitem__ (self, k):
        k = self.parent.k_transform(k)

        if k in self:
            v = dict.__getitem__(self, k)
        elif '__parent__' in self:
            v = self.parent[self['__parent__']][k]
        else:
            v = self.parent.getdefault(k)

        return self.parent.transform(k, v % self)

class ConfigDict(DefaultDict):
    '''A class for parsing INI style configuration files into Python
    dictionaries.
    
    - src -- A file path or file-like object
    - defaults -- a dictionary of default values
    - k_transform -- a function for transforming option names.
      By default, option names are converted to lower case.
    - v_transforms -- a dictionary of functions for converting
      option values.'''

    def __init__ (self,
            src=None,
            defaults=None,
            k_transform=None,
            v_transforms=None):

        super(ConfigDict, self).__init__(default=DDMaker({}))

        self.defaults = {}
        self.k_transform = lambda x: x.lower()
        self.v_transforms = {}

        if defaults:
            self.defaults.update(defaults)

        if k_transform:
            self.k_transform = k_transform

        if v_transforms:
            self.v_transforms = v_transforms

        if src:
            self.parse(src)

    def parse(self, src):
        cur_sec = '__GLOBAL__'
        self.clear()
        self['__GLOBAL__'] = Section('__GLOBAL__', self)

        for line in FileReader(src).vreadlines():
            if not line:
                continue
            elif line.startswith('['):
                cur_sec = line[1:-1]
                if not cur_sec in self:
                    self[cur_sec] = Section(cur_sec, self)
            else:
                mo = re_set_val.match(line)
                if not mo:
                    raise ValueError('cannot parse: %s' % line)
                k = self.k_transform(mo.group(1))
                self[cur_sec][k] = mo.group(2)

    def transform (self, k, v):
        '''This is called to transform option values, based on the contents
        of self.v_transforms.'''

        return self.v_transforms.get(k, lambda x: x)(v)

    def getdefault(self, k):
        if k in self['DEFAULT']:
            return self['DEFAULT'][k]
        elif k in self.defaults:
            return self.defaults[k]
        else:
            raise KeyError(k)

if __name__ == '__main__':
    import pprint
    p = ConfigDict(src = sys.argv[1])
    pprint.pprint(p)
