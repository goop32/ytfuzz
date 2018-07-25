# YTFuzz v0.1b
# Find unlisted/private videos because
# why the fuck not you're bored at 2am
#
# @soymjolk, 2018

from bs4 import BeautifulSoup
import requests 
import time
import random
import string

# Here's what a YouTube video's URL looks like: https://www.youtube.com/watch?v=dwk0juwZJk8
# We want to replace everything after the ?v= with random [a-z], [A-Z], [0-9] strings
# BeautifulSoup checks if the Unlisted badge is found on the page
# <span class="style-scope ytd-badge-supported-renderer">Unlisted</span>
# If the Unlisted badge is found, URL is printed to terminal
# If the Unlisted badge is NOT found, skip it and move on

# TODO: make it work
#		add option support
#		that's about it honestly

### ./ytfuzz.py -h OR ./ytfuzz.py --help ###
# ytfuzz v0.1b by @soymjolk
# 
# -h	this menu
# -o	output to a file (./ytfuzz.py -o dir/out.txt)
# -v	verbose (show title, channel, and errors)
# -t	show title
# -c	show channel
# -r	multithread support (./ytfuzz.py -r 4 [four threads])
# -w	wait for next request (./ytfuzz.py -w 5 [five seconds])
# -p	log public videos as well

inv = "<title>YouTube</title>"
count = 0
invCount = 0
invCountLimit = 50

while True:
	gen = ''.join([random.choice(string.ascii_letters + string.digits) for n in range(11)])
	# url = "https://www.youtube.com/watch?v=HXNs9N4vj6Y" # - valid
	# url = "https://www.youtube.com/watch?v=jfWjEFr5B3" - invalid
	url = ("https://www.youtube.com/watch?v=" + gen)
	# print(url)
	req = requests.get(url)
	# req.encoding = 'ISO-8859-1'
	txt = req.text
	# print(req.encoding)
	# print(txt)

	# here's where shit gets interesting
	# invalid URL has <yt-icon class="style-scope yt-player-error-message-renderer">, valid does not

	bstxt = BeautifulSoup(txt, 'html.parser')
	t = str(bstxt.title)
	count += 1
	print(count)
	if (t == inv):
		invCount += 1
		if (invCount == invCountLimit):
			print(str(invCountLimit) + " invalid")
			invCountLimit += 50
		# print("Invalid! Title is: " + t)
	elif (t != inv):
		print("Valid! Title: " + t + " and URL: " + url)
	else:
		print("prolly got ip ban'd")
		break
	# time.sleep(2)