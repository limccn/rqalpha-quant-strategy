#!/usr/bin/env python  
# -*- coding: utf-8 -*-

from operator import itemgetter  
import sys  

maxName = None  
maxPre = 0

# input comes from STDIN  
for line in sys.stdin:  
    # remove leading and trailing whitespace  
    line = line.strip()  
  
    # parse the input we got from mapper.py  
    name, preClose = line.split('\t', 1)

    if float(preClose) - float(maxPre) > 0:
        maxPre = preClose
        maxName = name
    # write result to STDOUT  
    print '%s\t%s' % (name, preClose)
# write result to STDOUT
print '涨幅最大的股票:%s\t涨幅:%s' % (maxName, maxPre)