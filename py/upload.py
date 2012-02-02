from optparse import OptionParser
parser = OptionParser(usage="usage: %prog [options] filename")
#parser.add_option("-r", "--raw",action="store_true", dest="raw",help="include raw JSON")
parser.add_option("-v", "--verbose",
                  action="store_true", dest="verbose",help="verbose")
(options, args) = parser.parse_args()
if len(args) != 1:
	parser.print_usage()
	exit
filename = args[0]

from mutagen.easyid3 import EasyID3
tags = EasyID3(filename)
print tags

from mutagen.mp3 import MP3
audio = MP3(filename)
print audio