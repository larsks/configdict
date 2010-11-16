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
        super(Section, self).__init__(default=DDMaker(None))
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

        if v is not None:
            v = self.parent.transform(k, v % self)
        else:
            v = self.parent.transform(k, v)

        return v

    def __str__ (self):
        return '<Section "%s">' % self.name

    def __repr__ (self):
        return self.__str__()

    def tostring (self):
        if self.name == '__GLOBAL__':
            text = []
        else:
            text = [ '[%s]' % self.name ]

        for k,v in self.items():
            text.append('%s = %s' % (k, v))

        if text:
            return '\n'.join(text)
        else:
            return ''

class SectionFactory(object):

    def __init__(self, cf):
        self.cf = cf

    def __call__ (self, name):
        return Section(name, self.cf)

class ConfigDict(DefaultDict):
    '''A class for parsing INI style configuration files into Python
    dictionaries.
    
    - src -- A file path or file-like object
    - defaults -- a dictionary of default values
    - k_transform -- a function for transforming option names.
      By default, option names are converted to lower case.
    - v_transforms -- a dictionary of functions for converting
      option values.
    - keyerror -- if True, a request for a missing key will raise
      KeyError, otherwise it will return None.'''

    def __init__ (self,
            src=None,
            defaults=None,
            k_transform=None,
            v_transforms=None,
            keyerror=False):

        super(ConfigDict, self).__init__(default=SectionFactory(self))

        self.defaults = {}
        self.k_transform = lambda x: x.lower()
        self.v_transforms = {}
        self.k_list = []
        self.keyerror = keyerror

        if defaults:
            self.defaults.update(defaults)

        if k_transform:
            self.k_transform = k_transform

        if v_transforms:
            self.v_transforms = v_transforms

        if src:
            self.parse(src)

    def __setitem__ (self, k, v):
        self.k_list.append(k)
        super(ConfigDict, self).__setitem__(k,v)

    def __delitem__ (self, k):
        self.k_list.remove(k)
        super(ConfigDict, self).__delitem__(k)

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
        if 'DEFAULT' in self and k in self['DEFAULT']:
            return self['DEFAULT'][k]
        elif k in self.defaults:
            return self.defaults[k]
        elif self.keyerror:
            raise KeyError(k)
        else:
            return None

    def tostring(self):
        text = []

        for k in self.k_list:
            s = self[k].tostring()
            if s:
                text.append(s)
                text.append('')

        return '\n'.join(text)

if __name__ == '__main__':
    import pprint
    p = ConfigDict(src = sys.argv[1])
    print '=== STRUCTURE ==='
    pprint.pprint(p)
    print '=== TEXT ==='
    print p.tostring()

