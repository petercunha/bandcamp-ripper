# USAGE OF THIS PROGRAM IS ILLEGAL WITHOUT EXPRESS PERMISSION FROM THE ARTIST. USE AT YOUR OWN RISK!
# coding: utf-8

# Necessary modules
import sys
import os
import urllib2

# Colored output
from colorama import Fore, Style


# Main
def main():
	if len(sys.argv) == 1:
		# Check for command line args
		exit(Fore.RED + "\nYou didn't provide a URL!\nusage: python bc-rip.py <bandcamp album URL>\n")
	elif "/album/" not in sys.argv[1]:
		# Check for URL validity
		exit(
			Fore.RED + "\nYou did not provide a URL to the album!\nusage: python bc-rip.py <bandcamp album URL>\n\n" +
			"Make sure that you're using the album URL, not just a link to the artist's page.\n" +
			"Example of an album URL: https://CoolestArtist.bandcamp.com/album/CoolestAlbumEver")
	else:
		# Checks passed. Start the program.
		print("")
		print(Style.BRIGHT + "The Bandcamp Ripper" + Style.RESET_ALL)
		print("by https://github.com/petercunha")
		print(
			Fore.RED + "USAGE OF THIS PROGRAM IS ILLEGAL WITHOUT EXPRESS PERMISSION FROM THE ARTIST. USE AT YOUR OWN RISK!"
			+ Fore.RESET
		)
		print(Style.RESET_ALL + "")
		startRip(sys.argv[1])
	pass


# Rips 128-bitrate MP3's from bandcamp album URL
def startRip(URL):

	# Grab HTML source of Bandcamp album page
	req = urllib2.Request(URL)
	try:
		response = urllib2.urlopen(req)
		source = response.read()
	except urllib2.HTTPError as err:
		exit(Fore.RED + Style.BRIGHT + "HTTP Error " + str(err.code) + " occurred. Check the URL and try again?")

	# Parse HTML into meaningful arrays of data
	download_arr = source.split('"mp3-128":"//')
	song_number = len(download_arr) - 1
	name_arr = source.split('"title":"')

	# dirname format: Artist - Album Name
	album = source.split('<title>')[1].split('</title>')[0].split(" | ")
	dirname = album[1] + " - " + album[0]

	# Exit if album has no songs or is restricted
	if song_number == 0:
		exit(Fore.RED + "Unable to download the album. It appears that the artist has opted to restrict bandcamp downloads.")

	# Create dir to download music if it doesn't exist
	if not os.path.exists(dirname):
		os.makedirs(dirname)

	print("Downloading MP3's from " + Style.BRIGHT + dirname + Style.RESET_ALL)

	# Download each file
	for x in xrange(song_number):
		# String-splitting witchcraft
		dl = "https://" + download_arr[x+1].split('"')[0]
		fname = dirname + "/" + str(x+1) + ". " + name_arr[x+2].split('"')[0]

		# Download the file
		download(dl, fname)
		print(
			Style.RESET_ALL + "[" + Fore.GREEN + Style.BRIGHT + "✓" +
			Style.RESET_ALL + "] " + Fore.MAGENTA + name_arr[x+2].split('"')[0]
		)

	# Download complete
	print(Style.RESET_ALL + "" + Style.DIM)
	print("Download complete!")
	print("Downloaded into " + os.getcwd() + "/" + dirname + Style.RESET_ALL)
	print("")
	print("Thanks for using Bandcamp Ripper <3")
	print("")



# Downloads file at URL to specified location and filename
def download(url, filename):
	mp3file = urllib2.urlopen(url)
	with open(filename + ".mp3", 'wb') as output:
		output.write(mp3file.read())
	pass


# Finds string between two other strings
def find_between(s, first, last):
	try:
		start = s.index(first) + len(first)
		end = s.index(last, start)
		return s[start:end]
	except ValueError:
		return ""

if __name__ == '__main__':
	sys.exit(main())
