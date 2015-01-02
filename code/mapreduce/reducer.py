#!/usr/bin/env python
# 
# Adapted from script by Diana MacLean 2011
#
# Adapted fro CS448G from Michael Noll's tutorial on : http://www.michael-noll.com/tutorials/writing-an-hadoop-mapreduce-program-in-python/
#
#

from operator import itemgetter
import sys

# maps words to their counts
word2count = {}

# input comes from STDIN
for line in sys.stdin:
	# remove leading and trailing whitespace
	line = line.strip()

	# parse the input we got from mapper.py
	word, count = line.split('\t', 1)
	# convert count (currently a string) to int
	try:
		count = int(count)
		word2count[word] = word2count.get(word, 0) + count
	except ValueError:
		# count was not a number, so silently
		# ignore/discard this line
		pass

counted_words = word2count.items()

# write the results to STDOUT (standard output)
for word, count in counted_words:
	print '%s\t%s'% (word, count)
