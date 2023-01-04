# Spotify Player

## Documentation

Spotipy's full documentation is online at [Spotipy Documentation](http://spotipy.readthedocs.org/).

## Installation

```bash
pip install spotipy
```

alternatively, for Windows users 

```bash
py -m pip install spotipy
```

or upgrade

```bash
pip install spotipy --upgrade
```

## Features:
- Play a song via console
- Get recommended a song based off of user input
- Get a generated playlist made off of an existing playlist

# Installation:
## Setup a user_secrets file
- Create a utils folder
- Add user_secrets.py to that folder
- Enter the following code
```py
username = "YOUR-USERNAME-ID"
clientID = "YOUR-CLIENT-ID"
clientSecret = "YOUR-CLIENT-SECRET"
redirectURI = "YOUR-REDIRECT-URI" 

banner = """Welcome, {}!
---------------------------------------
| 0 | Exit                            |
| 1 | Play a Song                     |
| 2 | Get a song recommendation       |
| 3 | Generate a new playlist         |
---------------------------------------"""
```
- 
