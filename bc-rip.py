# USAGE OF THIS PROGRAM IS ILLEGAL WITHOUT EXPRESS PERMISSION FROM THE ARTIST. USE AT YOUR OWN RISK!
# coding: utf-8

# Necessary modules
import sys
import os
import urllib2
import json

# Colored output
from colorama import Fore, Back, Style

def main():
	# Check for command line args
	if len(sys.argv) == 1:
		exit("\nYou didn't provide a URL!\nusage: python bc-rip.py <bandcamp album URL>\n")
	else:
		print("")
		print(Style.BRIGHT + "The Bandcamp Ripper" + Style.RESET_ALL)
		print("by https://github.com/petercunha")
		print(Fore.RED + "USAGE OF THIS PROGRAM IS ILLEGAL WITHOUT EXPRESS PERMISSION FROM THE ARTIST. USE AT YOUR OWN RISK!")
		print(Style.RESET_ALL + "")
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
	album = source.split('<title>')[1].split('</title>')[0].split(" | ")
	dirname = album[1] + " - " + album[0]

	# Create dir to download music if it doesn't exist
	if not os.path.exists(dirname):
		os.makedirs(dirname)

	print("Downloading MP3's from " + Style.BRIGHT + dirname + Style.RESET_ALL + "...")

	# Download each file
	for x in xrange(len(download_arr)-1):
		# String-splitting witchcraft
		dl = "https://" + download_arr[x+1].split('"')[0]
		fname = dirname + "/" + str(x+1) + ". " + name_arr[x+2].split('"')[0]

		download(dl, fname)
		print(Style.RESET_ALL + "[" + Fore.GREEN + Style.BRIGHT + "✓" + Style.RESET_ALL + "] " + Fore.MAGENTA + name_arr[x+2].split('"')[0])
		pass

	# Download complete
	print(Style.RESET_ALL + "" + Style.DIM)
	print("Download complete!")
	print("Thanks for using Bandcamp Ripper.")
	print("")


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
