ndrive
========

ndrive is a python wrapper for Naver Ndrive

Below is the sample code to use ndrive module in python

    >>> from ndrive import Ndrive
    >>> nd = Ndrive()
    >>> nd.login("YOUR_ID","YOUR_PASSWORD")
    >>> nd.uploadFile("FILE_NAME", "/FILE_NAME")
    >>> nd.download("FILE_NAME")


Installation
---------------
To install ndrive, simply:

    $ pip install ndrive

Or, you can use:

    $ easy_install ndrive

Or, you can also install manually:

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
3. ???


Copyright
---------

Copyright © 2014 Kim Tae Hoon.
