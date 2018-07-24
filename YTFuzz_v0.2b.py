# YTFuzz v0.2b
# Find unlisted/private videos because
# why the fuck not you're bored at 2am
#
# @soymjolk, 2018

from bs4 import BeautifulSoup
import requests 
import time
import random
import string
import argparse
import threading # -t --threads

# -- argument parsing -- #
a = argparse.ArgumentParser(prog='ytfuzz.py', usage='%(prog)s (options)', description='Fuzz for unlisted/private YouTube videos', add_help=True)
a.add_argument('-o', '--out', action='store_true', dest='isOutput', help='output to a file - not working')
a.add_argument('-v', action='store_true', dest='isVerbose', help='verbosity')
a.add_argument('-t', '--title', action='store_true', dest='isTitle', help="show valid video's title")
a.add_argument('-c', '--channel', action='store_true', dest='isChannel', help="show valid video's channel")
a.add_argument('-r', dest='threads', help='run with x threads')
a.add_argument('-w', '--wait', action='store_true', dest='isWait', help="wait x seconds for next request")
a.add_argument('-p', '--public', action='store_true', dest='isPublic', help='log public videos as well')
a.add_argument('-x', dest='proxIn', help='http/https proxy')
r = a.parse_args()
# -- end of argument parsing -- #

proxy = {"https": r.proxIn}

def fuzzer(r):
	# -- tested URL count --
	count = 0
	invCount = 0
	invCountLimit = 50
	# -- end count --
	while True:
		g = ''.join([random.choice(string.ascii_letters + string.digits) for n in range(11)]) #gen video ID - need
		u = ('https://www.youtube.com/watch?v=' + g) # join URL + ID - need
		e = requests.get(u, proxies = proxy) # proxy
		x = e.text # make request readable
		b = BeautifulSoup(x, 'html.parser') # parse request w/ bs
		t = str(b.title) # title of request
		
		count += 1
		if r.isVerbose == True:
			print(str(count) + " - " + u + " - " + t)
			# verbose text (36 - https://www.youtube.com/watch?v=h8fh98HjhF3 - <title>Video title</title>)
		
		if (t == '<title>YouTube</title>'): # this is the title used when a video doesn't exist
			invCount += 1 # idk why not
			if (invCount == invCountLimit) and (r.isVerbose == True): # only do this if -v
				print(str(invCountLimit) + ' invalid') # only do this if -v
				invCountLimit += 50 # only do this if -v
		elif (t != '<title>YouTube</title>'): # if not YouTube, video should exist
			print('Valid! Title: ' + t + ' and URL: ' + u)
		else: # if we didn't get any (expected) results
			print("prolly got ip ban'd")
			# break # self explanatory
		# time.sleep(2)
		
fuzzer(r)
	