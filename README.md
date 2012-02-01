This is the new home of research involving reverse-engineering the Google Music protocol, specifically, the uploading mechanism since most other parts are somewhat trivial.

##Authentication

This is the first thing the client does.

```
POST https://www.google.com/accounts/ClientLogin HTTP/1.1
User-Agent: Music Manager (1, 0, 24, 7712 - Windows)
Host: www.google.com
Accept: */*
Content-Type: application/x-www-form-urlencoded
Content-Length: 76
```

It's a POST request done over HTTPS with this content

```
Email=username%40gmail.com&Passwd=thisisntactuallymypassword&service=sj&accountType=GOOGLE
```

Also an interesting tidbit, the `service=sj` thing. At first I thought it was stood for steve jobs, but that wouldn't make too much sense. I had it stuck in the back of my mind for a bit and then it struck me while looking at the uploadsj part of the URL. I think it's short for "skyjam", the internal code name for Google Music.

The server thinks it's okay and then says.

```
HTTP/1.1 200 OK
Content-Type: text/plain
Cache-control: no-cache, no-store
Pragma: no-cache
Expires: Mon, 01-Jan-1990 00:00:00 GMT
Date: Tue, 31 Jan 2012 18:55:59 GMT
X-Content-Type-Options: nosniff
X-XSS-Protection: 1; mode=block
Content-Length: 881
Server: GSE
```

This responds with the SID=, LSID=, Auth= cookie values delimited by newlines.

```
SID=DQAAREDACTEDkV3izSm
LSID=DQAAAMMREDACTEDLLorHpA
Auth=DQAAREDACTEDep1i-o
```

There's also a trailing newline, if that matters. 

##/upsj/upauth

`POST https://android.clients.google.com/upsj/upauth HTTP/1.1`

To be continued, first I have to deem whether or not this is actually necessary for the process. Ostensibly, the only thing this does is send a protobuf-encoded list of the computer's magic address and its hostname. The server responds with a series of numbers denoting some kind of state.

##/upsj/clientstate

`POST https://android.clients.google.com/upsj/clientstate HTTP/1.1`

To be continued

This seems to send that magical address thing, this time with the last character substituted with a \n for no apparent reason (and nothing else).

The server responds with that same series of cryptic numbers denoting state as well as what I believe to be the number current upload quota state.

```
8 {
  1: 20000 //maximum number of songs that can be held for your current payment plan
  2: 1696 //total number of songs you have uploaded?
  3: 1402 //no clue what this is
}
```

Also, rather interestingly, replaying the message yields an ugly "Your client does not have permission to get URL `/upsj/clientstate` from this server" message, but if you instead send the file which was intended for /upsj/upauth, everything works fine.

Update: It seems that this is the product of the substitution of the last character of the data with a newline, possibly at Fiddler's end.

##/upsj/metadata?version=1

This is where the actual action begins.

Here's a basic overview of what I've gleaned of this process. The client sends a list of tracks which are to be uploaded, this includes all the ID3 metadata, and importantly, a random 22 character alphanumeric temporary ID. In response, the server returns a list which maps each of these temporary IDs, with a persistant track ID which is later used to actually upload stuff and to reference files.


`cat musicman2.saz_FILES/raw/08_c.txt | python strip.py | protoc --decode=MetadataRequest metadata.proto > test_proto.txt`


This is a piece of nice, human-readable JSON taken from the web interface API.

```
{
  "songs": [
    {
      "genre": "Other",
      "beatsPerMinute": 0,
      "albumArtistNorm": "",
      "album": "",
      "artistNorm": "colorpulse",
      "lastPlayed": 1328036402939798,
      "type": 2,
      "disc": "",
      "id": "31c4330d-b519-368d-9fd0-b800d2bde10c",
      "composer": "",
      "title": "Carl Sagan - Glorious Dawn (ft Stephen Hawking)",
      "albumArtist": "",
      "totalTracks": "",
      "name": "Carl Sagan - Glorious Dawn (ft Stephen Hawking)",
      "totalDiscs": "",
      "year": "",
      "titleNorm": "carl sagan - glorious dawn (ft stephen hawking)",
      "artist": "Colorpulse",
      "albumNorm": "",
      "paused": true,
      "track": "",
      "durationMillis": 213000,
      "deleted": false,
      "url": "",
      "creationDate": 1328032831429284,
      "playCount": 0,
      "rating": 0,
      "comment": ""
    }
  ],
  "success": true
}
```

`POST https://android.clients.google.com/upsj/metadata?version=1 HTTP/1.1`

```
1 {
  2: "lJE0p7HzgoeiBToyLpAoIA" #is this a random string?
  3: 1271984386 #04 / 22 / 10 @ 7:59:46pm EST - Probably Creation Date
  4: 1272400853 #04 / 27 / 10 @ 3:40:53pm EST - Probably Last Played Date
  6: "Carl Sagan - Glorious Dawn (ft Stephen Hawking)" #Title, this is quite self explanatory
  7: "Colorpulse" #Artist, TPE1
  8: ""
  9: ""
  10: ""
  11: 0
  12: ""
  13: 0
  14: "Other" #Genre
  15: 213000 #duration of the file in milliseconds
  16: 0
  20: 0
  26: 0
  27: 0
  28: 0
  31: 1
  32: 5115029 #no idea what this is
  37: 0
  38: 0
  44: 192 #bitrate, it seems
  53: "-383260437"
  61: 1
}

2: "00:1E:EC:6F:49:3\n"
```


This, my friends is the sound of success

```
u0: 1
response {
  ids: "lJE0p7HzgoeiBToyLpAoIA"
  uploads {
    id: "lJE0p7HzgoeiBToyLpAoIA"
    u0: 4
    serverId: "31c4330d-b519-368d-9fd0-b800d2bde10c"
  }
}
state {
  u0: 0
  u1: 0
  u2: 5
  u3: 6000
  u4: 0
  u5: 3000
}
```