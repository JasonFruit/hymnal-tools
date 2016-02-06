# hymnal-tools

## Description

A set of scripts to query hymnary.org, edit texts found there, and
store them in databases for further use.  Originally written for the
preparation of the Old-Line Primitive Baptist Hymn and Tune Book, and
being open-sourced for the use of others.

## State of the Stuff

Right now, it is just barely usable, but the libraries, and even more
so the `find-text.py` script, are a brittle mess.  It relies on
Emacs/emacsclient for editing hymns, and it lacks error handling in
most areas, especially regarding menu selections and reading hymns
from their text representation.

## Future plans

Cleanup that is needed:

 - Sensible reactions to errors in reading hymns from text
 - A built-in editor option in addition to emacsclient
 - Less brittle menu system
 
Long-term, it would be good to replace the text-based menus with an
equally-efficient GUI tool, if such a thing is possible.
