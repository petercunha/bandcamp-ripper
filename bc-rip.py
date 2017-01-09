import sys
import os
import urllib2
import json

def main():
	# Check for command line args
	if len(sys.argv) == 1:
		exit("\nYou didn't provide a URL!\nusage: python bc-rip.py <bandcamp album URL>\n")
	else:
		startRip(sys.argv[1])
	pass

# Rips 128-bitrate MP3's from bandcamp album URL
def startRip(URL):

	# Grab HTML source of Bandcamp album page
	req = urllib2.Request(URL)
	response = urllib2.urlopen(req)
	source = response.read()

	# Parse HTML into meaningful arrays of data
	download_arr = source.split('"mp3-128":"//')
	name_arr = source.split('"title":"')

	# dirname format: Artist - Album Name
	dirname = (URL.split('://')[1].split('.bandcamp')[0] + " - " + URL.split('album/')[1].replace("-", " ")).title()
	
	# Create dir to download music if it doesn't exist
	if not os.path.exists(dirname):
		os.makedirs(dirname)

	# Download each file with some split witchcraft
	for x in xrange(len(download_arr)-1):
		download("https://" + download_arr[x+1].split('"')[0], 
				 dirname + "/" + str(x+1) + ".) " + name_arr[x+2].split('"')[0])
		pass

# Downloads file at URL to specified location and filename
def download(url, filename):
	mp3file = urllib2.urlopen(url)
	with open(filename + ".mp3",'wb') as output:
		output.write(mp3file.read())
	pass

# Finds string between two other strings
def find_between( s, first, last ):
    try:
        start = s.index( first ) + len( first )
        end = s.index( last, start )
        return s[start:end]
    except ValueError:
        return ""

if __name__ == '__main__':
    sys.exit(main())