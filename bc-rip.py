import sys
import os
import urllib2
import json

URL = "https://pogomix.bandcamp.com/album/kindred-shadow"

def main():
	req = urllib2.Request(URL)
	response = urllib2.urlopen(req)
	source = response.read()

	arr = source.split('"mp3-128":"//')

	# dirname format: Artist - Album name
	dirname = URL.split('://')[1].split('.bandcamp')[0] + " - " + URL.split('album/')[1].replace("-", " ")
	
	if not os.path.exists(dirname):
		os.makedirs(dirname)

	for x in xrange(1,10):
		download("https://" + arr[x].split('"')[0], dirname + "/" + str(x))
		pass

def download(url, filename):
	mp3file = urllib2.urlopen(url)
	with open(filename + ".mp3",'wb') as output:
		output.write(mp3file.read())
	pass


def find_between( s, first, last ):
    try:
        start = s.index( first ) + len( first )
        end = s.index( last, start )
        return s[start:end]
    except ValueError:
        return ""

if __name__ == '__main__':
    sys.exit(main())