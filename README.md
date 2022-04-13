# thedatalab.org

This was the django project for http://thedatalab.org - this project has been replaced by https://github.com/ebmdatalab/bennett.ox.ac.uk

## Install

[Installation instructions for dokku](./INSTALL.md)

## TODO

@sebbacon Note to remind me to investigate tag library recursion:

tagulous/models/managers.py L65 (changed there) has recursion with descriptions.py L137 __get__
