configdict: parse INI files into Python dictionaries
====================================================

``configdict`` parses INI-style configuration files into Python
dictionaries.  Given a file like this::

  [DEFAULT]

  in stock = yes

  [widgets]

  price = 110.00
  size = large

  options = this \
          that \
          and \
          the other thing

You can do this::

  >>> import configdict
  >>> cf = configdict.ConfigDict('sample.conf')

And get this::

  >>> import pprint
  >>> pprint.pprint(cf)
  {'DEFAULT': {'in stock': 'yes'},
   '__GLOBAL__': {},
   'widgets': {'options': 'this that and the other thing',
               'price': '110.00',
               'size': 'large'}}

And do this::

   >>> print cf['widgets']['in stock']
   yes

