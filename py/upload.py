from optparse import OptionParser
parser = OptionParser(usage="usage: %prog [options] filename")
#parser.add_option("-r", "--raw",action="store_true", dest="raw",help="include raw JSON")
parser.add_option("-v", "--verbose", action="store_true", help="verbose")
parser.add_option("-r", "--relogin", action="store_true", help="force relogin")
parser.add_option("-f", "--authfile", action="store", type="string", dest="authfile",
					help="authentication credentials file", default=".AUTH")

(options, args) = parser.parse_args()

if len(args) != 1:
	parser.print_help()
	exit()

filename = args[0]

SID = ''
try:
	SID = open(options.authfile, "r").read()
except:
	pass

import requests

if SID == '':
	import getpass
	email = raw_input("Enter Google Music Email Address: ")
	pwd = getpass.getpass("Enter Google Music Password: ")
	payload = {
		'Email': email,
		'Passwd': pwd,
		'service': 'sj',
		'accountType': 'GOOGLE'
	}
	r = requests.post("https://google.com/accounts/ClientLogin", payload)
	SID = str(r.content).split("\n")[0]
	print "Logged In Successfully"
	open(options.authfile, "w").write(SID)

from uuid import getnode as getmac
mac = hex(getmac())[2:-1]
mac = ':'.join([mac[x:x+2] for x in range(0, 10, 2)])

print mac
#from mutagen.easyid3 import EasyID3
#tags = EasyID3(filename)
#print tags

from mutagen.mp3 import MP3
audio = MP3(filename, ID3 = EasyID3)
#print "discnumber" in audio #audio["discnumber"]
print audio.info.length * 1000
print audio.info