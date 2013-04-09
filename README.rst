Intro
=====

This module uses Parcel to build a debian package of a local pypiserver. The debian package also
installs an upstart service with some default configuration.

How to Build
============

::
    
    $ fab -H hostname deb #this builds the debian package on host


