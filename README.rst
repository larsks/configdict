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

editini script
==============

The ``editini`` script included in recent versions of ``configdict`` allows
you to edit ini-style configuration files "on the fly".  The script
supports the following options:

  -g GROUP, --group=GROUP
  -v VALUE, --value=VALUE
  -d DELETE, --delete=DELETE
  -D, --delete-group    

These options allow you to add, modify, or remote items from a
configuration file.  For example, you can do this::

  $ editini -g widgets \
    -v 'comment=These are great!' \
    -d options < sample.conf

And get this::

  [DEFAULT]
  in stock = yes

  [widgets]
  comment = These are great!
  price = 110.00
  size = large

Or you delete entire sections:

  $ editini -g widgets -D < sample.conf
  [DEFAULT]
  in stock = yes

