# Spotify Playlist Generator
![Current Version](https://img.shields.io/badge/version-1.0.7-green.svg) [![Python 3](https://img.shields.io/github/pipenv/locked/python-version/omkarxpatel/Spotify-Playlist-Generator)](https://www.python.org/downloads/)


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
1. Play a song via your terminal
- Enter a song name and it will start playing in your spotify application
2. Get recommended a song based off of user input
- Enter 3 songs and it will generate a song based off of your input
3. Get a generated playlist made off of an existing playlist
- Enter a playlist url and it will generate a brand new playlist with similar songs

# Getting started:
## Create a user_secrets file
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
## How to get secrets:
A full set of examples can be found in the [online documentation](http://spotipy.readthedocs.org/) and in the [Spotipy examples directory](https://github.com/plamere/spotipy/tree/master/examples).

To get started, install spotipy and create an app on https://developers.spotify.com/.
Add your new ID and SECRET to your environment:

## Reporting issues:
If you find any bugs, leave a comment or a push request
