import os
from setuptools import setup

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(name='configdict',
        version='20101116.1',
        description='Parse INI files into dictionaries.',
        author='Lars Kellogg-Stedman',
        author_email='lars@oddbit.com',
        license = 'GPL',
        url='http://github.com/larsks/configdict',
        packages=['configdict'],
        classifiers=[
            'License :: OSI Approved :: GNU General Public License (GPL)',
            'Operating System :: OS Independent',
            ],
        long_description=read('README.rst'),
        scripts=['scripts/editini'],
        )

