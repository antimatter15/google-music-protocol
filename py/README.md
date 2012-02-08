## Usage

Once you have the dependencies installed, using it should be fairly intuitive.

```
Usage: upload.py [options] filename

Options:
  -h, --help            show this help message and exit
  -v, --verbose         verbose
  -r, --relogin         force relogin
  -f AUTHFILE, --authfile=AUTHFILE
                        authentication credentials file
```

The authfile contains the cookie information needed to login to a Google Music session. The contents are not encrypted, and it is percievable for someone to use the contents to log in as you on Google. However, it does not contain the user's password or username. It should be possible to login without storing user information on disk with `-f /dev/null`, but this has not been tested.

The relogin option disregards the contents of the authfile, prompts the user for credentials, gets an access token and saves it to the authfile.

## Dependencies

I'm not sure exactly which ones are part of the standard library, but the ones that seem less standard have been moved to the top of the list for your sake. It has been tested with Python 2.7, but 2.6 should probably work as well.

* mutagen
* google.protobuf
* json
* optparse
* urllib
* getpass
* httplib
* uuid
* socket
* random
* string
* os
* time

Those using Ubuntu can probably install the dependencies with `sudo apt-get install python-mutagen python-protobuf`