ndrive
========

ndrive is a python wrapper for Naver Ndrive

Below is the sample code to use ndrive module in python

    >>> from ndrive import ndrive
    >>> n = ndrive()
    >>> n.login("YOUR_ID","YOUR_PASSWORD")
    >>> n.uploadFile("FILE_NAME")


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


To-do
-----

1. Implement all APIs
2. command-line tool
3. ???


Copyright
---------

Copyright © 2014 Kim Tae Hoon.
