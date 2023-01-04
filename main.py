import os
import time
import spotipy
import webbrowser
from colorama import Fore as fore
import spotipy.util as util

username = "9mjw6j7712eqyhu54vu5dsag6"
clientID = "fbe9c56baeb24b4e83331867cb867e34"
clientSecret = "20d4c1e7719641ccb02559bedcdbd7b2"
redirectURI = "https://open.spotify.com" 

def isvalid(option, min, max):
    return min <= option <= max


def clear(val):
    if val != 0:
        os.system("clear")
    else:
        time.sleep(val)
        os.system("clear")


def raiseError(error):
    print(f"{fore.RED}Error: {fore.RESET}{error}")

def main():
    spotifyObject = spotipy.Spotify(auth=spotipy.SpotifyOAuth(clientID,clientSecret,redirectURI).get_access_token()["access_token"])
    user = spotifyObject.current_user()
    clear(0)

    while True:

        print(f"""
Welcome, {user["display_name"]}
---------------------------------------
| 0 - Exit                            |
| 1 - Play a Song                     |
| 2 - Get a song reccomendation       |
---------------------------------------
                """)

        while True:
            choice = input("Enter a choice: ")
            
            try:
                choice = int(choice)
            except:
                raiseError(f"\"{choice}\" is not an integer")
                clear(5)

            if isvalid(choice, 0, 3):
                clear(0); break
        
        if choice == 0:
            clear(0); exit()
        
        elif choice == 1:
            searchQuery = input("Enter Song Name: ")
            searchResults = spotifyObject.search(searchQuery,1,0,"track")
            track = searchResults['tracks']['items'][0]
            
            try:
                song = searchResults["tracks"]["items"][0]["external_urls"]["spotify"]
                webbrowser.open(song)
            except:
                raiseError(f"Could not open: {song}")

            print(f"{fore.GREEN}✅ Playing {track['name']} - {track['artists'][0]['name']}{fore.RESET}")


            scope = 'user-modify-playback-state'
            token = util.prompt_for_user_token(username, scope, client_id=clientID, client_secret=clientSecret, redirect_uri=redirectURI)
            sp = spotipy.Spotify(auth=token)
            sp.start_playback(uris=[song])

        elif choice == 2:
            values = []
            for x in range(3):
                value = input(f"Enter song {x+1}: ")
                values.append(value)

            results_1 = spotifyObject.search(q=values[0], type='track')
            song_1_id = results_1['tracks']['items'][0]['id']
            
            results_2 = spotifyObject.search(q=values[1], type='track')
            song_2_id = results_2['tracks']['items'][0]['id']

            results_3 = spotifyObject.search(q=values[2], type='track')
            song_3_id = results_3['tracks']['items'][0]['id']
            
            recommendations = spotifyObject.recommendations(seed_tracks=[song_1_id, song_2_id, song_3_id])
            recommended_song = recommendations['tracks'][0]['name']
            recommended_song_id = recommendations['tracks'][0]['id']

            track = spotifyObject.track(recommended_song_id)
            artist = track['artists'][0]['name']

            song = recommendations["tracks"][0]["external_urls"]["spotify"]
    
            print(f"\nRecommended song: {recommended_song} - {artist}")
            play = input("Would you like to play this song [yes/no]: ").lower()

            if play in ['y','yes']:

                print(f"{fore.GREEN}✅ Playing {recommended_song} - {artist}{fore.RESET}")
                
                scope = 'user-modify-playback-state'
                token = util.prompt_for_user_token(username, scope, client_id=clientID, client_secret=clientSecret, redirect_uri=redirectURI)
                sp = spotipy.Spotify(auth=token)
                sp.start_playback(uris=[song])
            
            else:
                clear(0); exit



        repeat = input("\nWould you like to try again [yes/no]: ").lower()
        if repeat in ['y','yes']:
            clear(3)

        else:
            clear(0); exit()
    
            
main()