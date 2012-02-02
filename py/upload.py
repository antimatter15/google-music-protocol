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

cookie = {'SID': SID[4:]}

print cookie

from uuid import getnode as getmac
mac = hex(getmac())[2:-1]
mac = ':'.join([mac[x:x+2] for x in range(0, 10, 2)])

from socket import gethostname
hostname = gethostname()

print mac, hostname

import metadata_pb2


uauth = metadata_pb2.UploadAuth()
uauth.address = mac
uauth.hostname = hostname

#print uauth.SerializeToString()

r = requests.post("https://android.clients.google.com/upsj/upauth", 
					data=uauth.SerializeToString(),
					cookies=cookie,
					verify = False)
uauthresp = metadata_pb2.UploadAuthResponse()
uauthresp.ParseFromString(r.content)
print uauthresp

clientstate = metadata_pb2.ClientState()
clientstate.address = mac

#print uauth.SerializeToString()

r = requests.post("https://android.clients.google.com/upsj/clientstate", 
					data=clientstate.SerializeToString(),
					cookies=cookie,
					verify = False)

clientstateresp = metadata_pb2.ClientStateResponse()
clientstateresp.ParseFromString(r.content)
print clientstateresp

metadata = metadata_pb2.MetadataRequest()
metadata.address = mac
track = metadata.tracks.add()

from mutagen.easyid3 import EasyID3
from mutagen.mp3 import MP3
audio = MP3(filename, ID3 = EasyID3)

import random
import string
chars = string.ascii_letters + string.digits 
id = ''.join(random.choice(chars) for i in range(20))

import os
filesize = os.path.getsize(filename)
print filesize
track.fileSize = filesize

track.bitrate = audio.info.bitrate / 1000
track.duration = int(audio.info.length * 1000)
if "album" in audio: track.album = audio["album"][0]

if "title" in audio: track.title = audio["title"][0]
if "artist" in audio: track.artist = audio["artist"][0]
if "composer" in audio: track.composer = audio["composer"][0]
#if "albumartistsort" in audio: track.albumArtist = audio["albumartistsort"][0]
if "genre" in audio: track.genre = audio["genre"][0]
if "date" in audio: track.year = int(audio["date"][0])
if "bpm" in audio: track.beatsPerMinute = int(audio["bpm"][0])
if "tracknumber" in audio: track.track = int(audio["tracknumber"][0])
if "discnumber" in audio: track.disc = int(audio["discnumber"][0])

import tempfile
tmp = tempfile.TemporaryFile()
metastr = metadata.SerializeToString()
size = len(metastr)
tmp.write(metastr)


r = requests.post("https://android.clients.google.com/upsj/metadata?version=1", 
					data=tmp,
					cookies=cookie,
					headers={"Content-Length": str(size)},
					verify = False)
print r.content
metadataresp = metadata_pb2.MetadataResponse()
metadataresp.ParseFromString(r.content)
#print utfencode(metadataresp)
print metadataresp

#tags = EasyID3(filename)
#print tags



#print "discnumber" in audio #audio["discnumber"]
