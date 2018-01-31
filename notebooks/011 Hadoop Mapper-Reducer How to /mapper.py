#!/usr/bin/env python  
# -*- coding: utf-8 -*-
  
import sys  

lastClose = -1
preClose = 0
name = None
# /usr/local/Cellar/hadoop/2.7.3/libexec/share/hadoop/tools/lib  
# input comes from STDIN (standard input)  
for line in sys.stdin:
    # remove leading and trailing whitespace  
    line = line.strip()
    # split the line into field  
    fields = line.split(',')
    if len(fields) > 3:
        # convert close to float  
        try:
            close = float(fields[3])
            if lastClose == -1:
               lastClose = close
            preClose = lastClose - close
            name = fields[2]
        except ValueError:
           # close was not a number, so silently  
           # ignore/discard this line  
           continue
    else:
        # ignore/discard this line
        continue
print '%s\t%s' % (name, preClose)