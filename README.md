This project aims to document the protocol for uploading music files to Google Music. This project is related to the [MusicAlpha](https://github.com/antimatter15/musicalpha) project as well as [Unofficial-Google-Music-API](https://github.com/simon-weber/Unofficial-Google-Music-API). Since there is no official documentation, much of the process involves guesswork, but the process is largely functional. In the `py` directory, which you can find in this git repository, there is a simple python implementation of this protocol, capable of uploading songs via the command line.

![Evidence that this works](http://dl.dropbox.com/u/1024307/Screenshots/MusicAlpha%20Redux.png)

##Overview

Here, I'd like to give an overview of how the process works without all the technical implementation details, and also present some of the more up-to-date information, since some of the rest of this file is quite dated and reflects older content. Note that many of these stages are mere guesses based on behavior and contracted names.

First is the process of logging in. This login process is surprisingly simple and involves a simple HTTPS POST request, and the response is just as simple: cookie values separated by newlines. This must be conducted over HTTPS, or else the response simply doesn't work. Also, the values seem equivalent to browser login cookies (the only one which is needed is the SID, everything else can pretty much be discarded), as in, a SID attained through the web based login is just as valid as one procured through this process, though unless you're making some browser extension (a la MusicAlpha), this method is probably a lot simpler (occam's razor behooves you).

Clutching that mighty `SID` token, you can finally begin the galliant quest of sending your music through a series of tubes. However, the next step involves Google's Protocol Buffers, a binary data format. Previously, this served as a huge roadblock in deciphering the protocol, since the Music Manager application ignored the operating system's list of trusted root certificates and communicated exclusively through SSL. However, we found a way to patch the executable to disable certificate checking and use a mitm ssl proxy (Fiddler) to glean insights into latter stages of the process.

The first of these is uploader authentication, and at fairly straightforward at that. The process involves sending the NIC's MAC address and the computer's hostname (protobuf encoded) to Google's servers, which in return, respond with some protobuf encoded status message consisting of indecipherable numbers. This is used to register a device with Google Music, which restricts you to "up to 10 devices" which can be managed from the web interface in the [settings page](https://music.google.com/music/listen?u=0#settings_pl). 

Once you have authenticated your Uploader ID (MAC address), you can query for things like the user's current quota status. That current quota status includes the maximum number of files of that current payment level, the total number of uploaded files and the available tracks. 

The actual uploading process commences when you send a list of tracks that you plan on uploading with the associated ID3 metadata. The whole impetus behind this seems quite odd since it appears Google does its own parsing of ID3 data on its end as well (but chooses not to display it). It seems that Google extracts the Album Art from the file but relies on the metadata submitted through this phase for textual things (Album Artist, Title, etc.), and the files which it sends to browsers are stripped of ID3 data (Presumably, this allows them to differentiate between MP3s downloaded through the restricted (two time only) download dialog and those which are simply used for playing audio. A less sinister theory is that they might just want to save on bandwidth. 

Anyway, each one of these requests contains several tracks worth of metadata. Along with metadata, there are several fields which have yet to be interpreted to any useful extent. Notably, each track is assigned a 20-character random alphanumeric string, later referenced as the ClientId. In the server's response, these ClientIds are paired with respective ServerIds, which are longer and resemble UUIDs. It's the ServerID which is used in the step which begins the actual transfer. The server's response also incorporates that mysterious status update motif.

The reason tracks are initialized in bulk, is because there's actually a period of time which must be waited before proceeding to the next step. This seems to be about 3 seconds after the server has responded with ServerIds, presumably for the uploadsj and android servers to sync up.

Once that duration has elapsed, the client opens an unencrypted HTTP channel to Google Music and POSTs some JSON, repeating some audio information (file name, bitrate), including some useless things and notably, including the ServerID. The server responds with more JSON, which includes a putUrl which is quite self explanatory. It's a URL, which you're supposed to send a PUT to, with the contents of that file. 

At this point, you're done. 

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

The server thinks it's okay and then says

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

It responds with the SID=, LSID=, Auth= cookie values delimited by newlines.

```
SID=DQAAREDACTEDkV3izSm
LSID=DQAAAMMREDACTEDLLorHpA
Auth=DQAAREDACTEDep1i-o
```

There's also a trailing newline, if that matters. It seems that the only value which is actually carried onto the cookies is SID, the other ones seem to be extraneous.

Also, omitting the GOOGLE and sj parts seems to return something without an auth token. It's not yet clear if that resultant SID is still valid.

##/upsj/upauth

`POST https://android.clients.google.com/upsj/upauth HTTP/1.1`

This is the first thing that a computer does once the authentication token has been generated. However, it is likely that this process only needs to be executed once. The purpose of this step seems to register the current client as a "device" from which Google Music content can be managed. Google places a restriction such that the Music library can only be accessed from "up to ten devices", each of which can be manually deauthorized from the settings page of the web interface. It is this restriction that also seems to be the reason Google does not allow the Music Manager software to run on Virtual Machines, for they each use stock MAC addresses that fail to differentiate between installations.

The contents of that POST request are reproduced below, decoded with our `.proto` file which may or may not reflect the original internal one. As you can see, there are two string fields named the "address" and "hostname", respectively. The address is the device's MAC address, and represents a unique identifier for a client. The hostname is the computer's name, and is used as user-facing text to identify the device. In later stages of the upload process (The JSON-encoded `/uploadsj/rupio` part), the address is also known as an `UploaderID`. From the web interface, the `/music/services/loadsettings` request refers to the address and hostname as `id` and `name`, respectively.

```
address: "02:11:DD:3B:1A:3A"
hostname: "my-pc"
```

The response consists of a series of numbers which are yet to be interpreted in any significant way. However, the contents do not seem to deviate from the values depicted below.

```
1: 6
6 {
  1: 0
  2: 0
  3: 5
  4: 6000
  5: 0
  6: 3000
}
11: 8
12: 10
```

However, their values do not seem to play any role in any subsequent steps, so they can be safely discarded.

##/upsj/clientstate

`POST https://android.clients.google.com/upsj/clientstate HTTP/1.1`

This doesn't matter nearly as much as the last stage, and the upload should be able to commence regardless of whether or not you send this message. All it does is give an update with regard to your quota details, ie. how many songs you can upload, how many you have, etc.

This seems to send that magical address thing, this time with the last character substituted with a \n for no apparent reason (and nothing else).

The server responds with that same series of cryptic numbers denoting state as well as what I believe to be the number current upload quota state.

```
8 {
  1: 20000 //maximum number of songs that can be held for your current payment plan
  2: 1696 //total number of songs you have uploaded?
  3: 1402 //available songs (what does that mean?)
}
```

As Simon Weber noted, it seems to correspond with the `/music/services/getstatus` json request.

```
"availableTracks":1671,
"totalTracks":1723
```

##/upsj/metadata?version=1

This is where the actual action begins.

Here's a basic overview of what I've gleaned of this process. The client sends a list of tracks which are to be uploaded, this includes all the ID3 metadata, and importantly, a random 22 character alphanumeric temporary ID (it seems that this is called the ClientID, TODO: update existing documentation to use this new name). In response, the server returns a list which maps each of these temporary IDs, with a persistant track ID (the ServerID) which is later used to actually upload stuff and to reference files.


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

`POST` to https://android.clients.google.com/upsj/metadata?version=1 

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


#/uploadsj/rupio

```
{
  "songs": [
    {
      "genre": "Other",
      "beatsPerMinute": 503,
      "albumArtistNorm": "unknowntwo",
      "album": "unknownone",
      "artistNorm": "antimatter15",
      "lastPlayed": 1328105084757673,
      "type": 2,
      "disc": 541,
      "id": "dc3307fd-be51-3048-b6d4-09184ff915cd",
      "composer": "unknownzero",
      "title": "This is not a song",
      "albumArtist": "unknowntwo",
      "totalTracks": 523,
      "name": "This is not a song",
      "totalDiscs": 547,
      "year": 467,
      "titleNorm": "this is not a song",
      "artist": "antimatter15",
      "albumNorm": "unknownone",
      "track": 479,
      "durationMillis": 499,
      "deleted": false,
      "url": "",
      "creationDate": 1328104614553584,
      "playCount": 521,
      "rating": 0,
      "comment": "unknownfour"
    }
  ],
  "success": true
}
```

This is the response to a successful request:

```
{
  "sessionStatus": {
    "state": "FINALIZED",
    "externalFieldTransfers": [
      {
        "name": "magic.mp3",
        "status": "COMPLETED",
        "bytesTransferred": 481237,
        "bytesTotal": 481237,
        "putInfo": {
          "url": "http://uploadsj.clients.google.com/uploadsj/rupio?upload_id=AEnB2UREDACTED-adSnQ&file_id=000"
        },
        "content_type": "audio/mpeg"
      }
    ],
    "additionalInfo": {
      "uploader_service.GoogleRupioAdditionalInfo": {
        "completionInfo": {
          "status": "SUCCESS",
          "customerSpecificInfo": {
            "ServerFileReference": "011a1REDACTEDaf881-19",
            "ResponseCode": 200
          }
        }
      }
    },
    "upload_id": "AEnB2REDACTEDh-adSnQ"
  }
}
```


##/upsj/uploadstate?version=1

`POST https://android.clients.google.com/upsj/uploadstate?version=1 HTTP/1.1`

Here's the protobuf-decoded thing, containing the uploader ID and something else which I have no idea about.

```
1: 1
2: "00:1F:3A:6D:42:21"
```

In return, the server returns more gobblygoop.

```
1: 8
6 {
  1: 0
  2: 0
  3: 5
  4: 6000
  5: 0
  6: 3000
}
11: 10
```


##/upsj/getjobs?version=1

`POST https://android.clients.google.com/upsj/getjobs?version=1 HTTP/1.1`

This seems to retrieve a list of upload jobs. It takes the Uploader ID.

```
1: "00:1F:3A:6D:42:21"
```

In return, the server responds with:

```
1: 5
6 {
  1: 0
  2: 0
  3: 5
  4: 6000
  5: 0
  6: 3000
}
7 {
  1 {
    1: "2xgHehGNCIrgHcBbiFnDhg"
    2: "3ed1f828-b44d-33aa-b11c-8986b8232344"
    5: 4
  }
  ...
  1 {
    1: "AlIp3uQMfEVwXBtKZr+gvA"
    2: "c5fb4b55-834a-3c51-ad67-acac072c201a"
    5: 4
  }
  2: 10
}
```
