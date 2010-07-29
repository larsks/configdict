import re

re_comment = re.compile('\s*#')

def stripped (fd):
    for line in fd:
        yield line.strip()

class DefaultDict (dict):
    '''Like
    http://docs.python.org/library/collections.html#collections.defaultdict.'''
    def __init__(self, default=None):
        self.default = default

    def __getitem__(self, k):
        try:
            return super(DefaultDict, self).__getitem__(k)
        except KeyError:
            if callable(self.default):
                self[k] = self.default()
            else:
                self[k] = self.default

            return self[k]


class FileReader (object):
    '''This class reads files line-by-line.  It strips out comments,
    and handles backslash-escaped line continuations.'''

    def __init__ (self, src):
        '''src may either a filename or a file-like object with a
        ``read`` method.'''

        if hasattr(src, 'read'):
            self.fd = src
        else:
            self.fd = open(src)

    def vreadlines(self):
        '''A generator that returns lines from a file.  Use like this::

          for line in thefile.vreadlines():
              print line
        '''

        acc = []

        for line in stripped(self.fd):
            if re_comment.match(line):
                continue
        
            if line.endswith('\\'):
                line = line[:-1].strip()
                acc.append(line)
            else:
                acc.append(line)
                yield(' '.join(acc))
                acc = []

