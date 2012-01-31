This is the new home of research involving reverse-engineering the Google Music protocol, specifically, the uploading mechanism since most other parts are somewhat trivial.

##Authentication

  POST https://www.google.com/accounts/ClientLogin HTTP/1.1
  User-Agent: Music Manager (1, 0, 24, 7712 - Windows)
  Host: www.google.com
  Accept: */*
  Content-Type: application/x-www-form-urlencoded
  Content-Length: 76

  Email=username%40gmail.com&Passwd=thisisntactuallymypassword&service=sj&accountType=GOOGLE


This responds with the SID=, LSID=, Auth= cookie values.


##/upsj/upauth

android.clients.google.com/upsj/upauth

To be continued

##/upsj/clientstate

To be continued

##/upsj/metadata?version=1

cat musicman2.saz_FILES/raw/08_c.txt | python strip.py | protoc --decode=MetadataRequest metadata.proto > test_proto.txt



antimatter15@antimatter15-desktop:~/google-music-protocol$ id3v2 -R glorious.mp3 

Filename: glorious.mp3
TCON: Other (12)
TIT2: Carl Sagan - Glorious Dawn (ft Stephen Hawking)
PRIV:  (unimplemented)
PRIV:  (unimplemented)
TPE1: Colorpulse
glorious.mp3: No ID3v1 tag

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

POST https://android.clients.google.com/upsj/metadata?version=1 HTTP/1.1


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
1 {
  2: "AlIp3uQMfEVwXBtKZr+gvA"
  3: 1271984185
  4: 1271984206
  6: "Our Place in the Cosmos"
  7: "Symphony of Science"
  8: ""
  9: ""
  10: ""
  11: 0
  12: ""
  13: 0
  14: "Other"
  15: 260000
  16: 0
  20: 0
  26: 0
  27: 0
  28: 0
  31: 1
  32: 10396779
  37: 0
  38: 0
  44: 320
  53: "-383260437"
  61: 1
}
1 {
  2: "6xVpl17f2h1U7MmEW9fOBg"
  3: 1271984163
  4: 1271984163
  6: "Symphony_of_Science-The_Poetry_of_Reality.mp3"
  7: ""
  8: ""
  9: ""
  10: ""
  11: 0
  12: ""
  13: 0
  14: "Other"
  15: 185000
  16: 0
  20: 0
  26: 0
  27: 0
  28: 0
  31: 1
  32: 5923343
  37: 0
  38: 0
  44: 256
  53: "-383260437"
  61: 1
}
1 {
  2: "w27GLq50DEWzjWZdd67zXg"
  3: 1271984174
  4: 1271984181
  6: "The Unbroken Thread"
  7: "Symphony of Science"
  8: ""
  9: ""
  10: ""
  11: 0
  12: ""
  13: 0
  14: "Other"
  15: 239000
  16: 0
  20: 0
  26: 0
  27: 0
  28: 0
  31: 1
  32: 7640338
  37: 0
  38: 0
  44: 256
  53: "-383260437"
  61: 1
}
1 {
  2: "O6dcgCLWhaAIwEnU9vbfFQ"
  3: 1271984204
  4: 1271984217
  6: "We Are All Connected"
  7: "Symphony of Science"
  8: ""
  9: ""
  10: ""
  11: 0
  12: ""
  13: 0
  14: "Other"
  15: 252000
  16: 0
  20: 0
  26: 0
  27: 0
  28: 0
  31: 1
  32: 8059133
  37: 0
  38: 0
  44: 256
  53: "-383260437"
  61: 1
}
2: "00:1E:EC:6F:49:3\n"
