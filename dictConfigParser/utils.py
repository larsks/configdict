import re

re_comment = re.compile('\s*#')

def stripped (fd):
    for line in fd:
        yield line.strip()

class DefaultDict (dict):
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
    def __init__ (self, src):
        if hasattr(self, 'read'):
            self.fd = src
        else:
            self.fd = open(src)

    def vreadlines(self):
        acc = []

        for line in stripped(self.fd):
            if re_comment.match(line):
                continue
        
            if line.endswith('\\'):
                line = line[:-1].strip()
                acc.append(line)
                next
            else:
                acc.append(line)
                yield(' '.join(acc))
                acc = []

