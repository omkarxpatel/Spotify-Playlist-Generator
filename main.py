############################
#   MADE BY: OMKAR PATEL   #
############################

import os
import time
import random
import string
import spotipy
import webbrowser
import spotipy.util as util
from colorama import Fore as fore

##################################
#   CONFIG VALUES -> README.md   #
##################################

try:
    from utils.user_secrets import username, clientID, clientSecret, redirectURI, banner
except:
    print("Error: utils/user_secrets.py NOT found\nView https://github.com/omkarxpatel/Spotify-Playlist-Generator#getting-started")

##########################
#   CHECKLIST FUNCTION   #
##########################

not_completed = "❌"
completed = "✅"

topbot = "----------------------------------------"
step1 = f"| {not_completed} | Extracting songs                |"
step2 = f"| {not_completed} | Extracting song-ids             |"
step3 = f"| {not_completed} | Create playlist                 |"
step4 = f"| {not_completed} | Adding songs                    |"
step5 = f"| {not_completed} | Task Finished                   |"

def checklist(step):
    clear(0)
    global step1,step2,step3,step4,step5

    if step == 1:
        step1 = f"| {completed} | Extracting songs                |"

    elif step == 2:
        step2 = f"| {completed} | Extracting song-ids             |"

    elif step == 3:
        step3 = f"| {completed} | Create playlist                 |"

    elif step == 4:
        step4 = f"| {completed} | Adding songs                    |"

    elif step == 5:
        step5 = f"| {completed} | Finished playlist               |"
    

    print(topbot); print(step1); print(step2); print(step3); print(step4); print(step5); print(topbot)

########################
#   HELPER FUNCTIONS   #
########################

def roundPlaylistLen(val):
    return (val+(20-val%20))/4

def isvalid(option, min, max):
    return min <= option <= max

def raiseError(error):
    print(f"{fore.RED}Error: {fore.RESET}{error}")

def clear(val):
    if val != 0:
        os.system("clear")
    else:
        time.sleep(val)
        os.system("clear")

###################
#   PLAY A SONG   #
###################

def playSong(spotifyObject, searchQuery):
    searchResults = spotifyObject.search(searchQuery,1,0,"track")
    track = searchResults["tracks"]["items"][0]
    
    openSong = input("Would you like to open this song in your browser [yes/no]: ").lower()
    song = searchResults["tracks"]["items"][0]["external_urls"]["spotify"]

    if openSong in ["y","yes"]:
        try:
            webbrowser.open(song)
        except:
            raiseError(f"Could not open: {song}")

    print(f"{fore.GREEN}✅ Playing {track['name']} - {track['artists'][0]['name']}{fore.RESET}")

    scope = "user-modify-playback-state"
    token = util.prompt_for_user_token(username, scope, client_id=clientID, client_secret=clientSecret, redirect_uri=redirectURI)

    sp = spotipy.Spotify(auth=token)
    sp.start_playback(uris=[song])

##############################
#   GET A RECOMMENDED SONG   #
##############################

def recommendSong(spotifyObject, song1, song2, song3):
    
    results_1 = spotifyObject.search(q=song1, type="track")
    song_1_id = results_1["tracks"]["items"][0]["id"]
    
    results_2 = spotifyObject.search(q=song2, type="track")
    song_2_id = results_2["tracks"]["items"][0]["id"]

    results_3 = spotifyObject.search(q=song3, type="track")
    song_3_id = results_3["tracks"]["items"][0]["id"]
    

    recommendations = spotifyObject.recommendations(seed_tracks=[song_1_id, song_2_id, song_3_id])
    recommended_song = recommendations["tracks"][0]["name"]
    recommended_song_id = recommendations["tracks"][0]["id"]
    recommended_song_url = recommendations["tracks"][0]["external_urls"]["spotify"]

    track = spotifyObject.track(recommended_song_id)
    artist = track["artists"][0]["name"]

    print(f"\nRecommended song: {recommended_song} - {artist}")
    play = input("Would you like to play this song [yes/no]: ").lower()

    if play in ["y","yes"]:

        print(f"{fore.GREEN}✅ Playing {recommended_song} - {artist}{fore.RESET}")
        
        scope = "user-modify-playback-state"
        token = util.prompt_for_user_token(username, scope, client_id=clientID, client_secret=clientSecret, redirect_uri=redirectURI)
        
        sp = spotipy.Spotify(auth=token)
        sp.start_playback(uris=[recommended_song_url])

    else:
        clear(0); exit

#########################
#   GENERATE PLAYLIST   #
#########################

def generate_similar_playlist(spotifyObject, playlist_url):

    checklist(0)

    playlist_id = playlist_url.split("/")[-1]
    playlist = spotifyObject.playlist(playlist_id)

    song_names = []
    tracks = playlist['tracks']

    for item in tracks['items']:
        song_names.append(item['track']['name'])

    checklist(1)
    
    song_ids = []
    total_songs = []

    for item in song_names:
        result = spotifyObject.search(q=item, type="track")
        song_id = result["tracks"]["items"][0]["id"]

        song_ids.append(song_id)
    

    for _ in range(int(roundPlaylistLen(len(song_ids))/4)):
        recommendations = spotifyObject.recommendations(seed_tracks=random.sample(song_ids, 20))

        for y in range(len(recommendations["tracks"])):
            song = recommendations["tracks"][y]["name"]
            song_uri = recommendations["tracks"][y]["uri"]

            value = f"{song}:{song_uri}"
            total_songs.append(value)
        
    checklist(2)

    scope = 'playlist-modify-public playlist-modify-private'
    token = util.prompt_for_user_token(username, scope, client_id=clientID, client_secret=clientSecret, redirect_uri=redirectURI)
    sp = spotipy.Spotify(auth=token)

    generated_name = ''.join(random.choices(string.ascii_letters, k=10))
    gen_playlist = sp.user_playlist_create(username, name=generated_name)
    gen_playlist_id = gen_playlist['id']

    checklist(3)

    for item in total_songs:
        item = item.split(":")

        sp.user_playlist_add_tracks(username, gen_playlist_id, [item[-1]])

    checklist(4)
    checklist(5)
    print(f"Generated playlist: {generated_name}")

####################
#   MAIN STARTER   #
####################

def main():
    spotifyObject = spotipy.Spotify(auth=spotipy.SpotifyOAuth(clientID,clientSecret,redirectURI).get_access_token()["access_token"])
    user = spotifyObject.current_user()
    clear(0)

    while True:
        print(banner.format(user["display_name"]))

        while True:
            choice = input("Enter a choice: ")
            
            
            try:
                choice = int(choice)
            except:
                raiseError(f"\"{choice}\" is not an integer")
                clear(5)

            if isvalid(choice, 0, 4):
                clear(0); break

        if choice == 0:
            clear(0); exit()

        elif choice == 1:
            searchQuery = input("Enter Song Name: ")
            playSong(spotifyObject, searchQuery)

        elif choice == 2:
            values = []
            for x in range(3):
                value = input(f"Enter song {x+1}: ")
                values.append(value)

            recommendSong(spotifyObject, values[0],values[1],values[2])

        elif choice == 3:
            playlistUrl = input("Enter playlist url: ")
            generate_similar_playlist(spotifyObject, playlistUrl)
        
        # DEBUG COMMAND
        elif choice == 10:
            scope = 'playlist-modify-public playlist-modify-private'
            token = util.prompt_for_user_token(username, scope, client_id=clientID, client_secret=clientSecret, redirect_uri=redirectURI)
            sp = spotipy.Spotify(auth=token)

            generated_name = ''.join(random.choices(string.ascii_letters, k=10))

            gen_playlist = sp.user_playlist_create(username, name=generated_name)
            gen_playlist_id = gen_playlist['id']

            song = input("Enter song name: ")
            results = sp.search(q=song, type='track')

            song_uri = results["tracks"]["items"][0]["uri"]

            sp.user_playlist_add_tracks(username, gen_playlist_id, [song_uri])

            print(f"Generated playlist - {generated_name}")



        repeat = input("\nWould you like to try again [yes/no]: ").lower()
        if repeat in ["y","yes"]:
            clear(3)

        else:
            clear(0); exit()
    
main()