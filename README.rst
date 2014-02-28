.. figure:: http://1.bp.blogspot.com/-4YYXRULcA6E/UwsBlXow3FI/AAAAAAAACSM/k2MC9klWoI8/s1600/ndrive.png
   :align: center
   :alt: alt tag

   alt tag
ndrive is a python wrapper for Naver Ndrive

Below is the sample code to use ndrive module in python

::

    >>> from ndrive import Ndrive
    >>> nd = Ndrive()
    >>> nd.login("YOUR_ID","YOUR_PASSWORD")
    >>> nd.uploadFile("FILE_NAME", "/FILE_NAME")
    >>> nd.downloadFile("FILE_NAME")
    >>> nlist = nd.getList("/Photo/", type=3)
    >>> f = nd.downloadFile(nlist[-1]['href'])

Installation
------------

To install ndrive, simply:

::

    $ pip install ndrive

Or, you can use:

::

    $ easy_install ndrive

Or, you can also install manually:

::

    $ git clone https://github.com/carpedm20/ndrive.git
    $ cd ndrive-master
    $ python setup.py install

Documentation
-------------

The documentation is available at http://carpedm20.github.io/ndrive/

To-do
-----

1. Implement all APIs
2. command-line tool

.. figure:: http://2.bp.blogspot.com/-pwk0vl3XcAQ/UwsYboRWXlI/AAAAAAAACSw/5d8lKu4RuYg/s1600/cmd2.png
   :align: center
   :alt: alt tag

   alt tag
Copyright
---------

Copyright © 2014 Kim Tae Hoon.

The MIT License (MIT)
