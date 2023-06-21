import os
import time
import random
import string
import spotipy
import spotipy.util as util
from colorama import Fore as fore
from tkinter import messagebox

username = "9mjw6j7712eqyhu54vu5dsag6"
clientID = "fbe9c56baeb24b4e83331867cb867e34"
clientSecret = "20d4c1e7719641ccb02559bedcdbd7b2"
redirectURI = "https://open.spotify.com" 


not_completed = "❌"
completed = "✅"
working = "⏳"

topbot = "--------------------------------------------"
step1 = f"| {not_completed} | Extracting songs         |          |"
step2 = f"| {not_completed} | Extracting song-ids      |          |"
step3 = f"| {not_completed} | Generating songs         |          |"
step4 = f"| {not_completed} | Adding songs             |          |"
step5 = f"| {not_completed} | Playlist finished        |          |"


def checklist_helper(task):
    task = int(task)
    taskTime = round(time.time() - task, 2)
    spacing = " " * (6 - len(str(taskTime)))

    return [taskTime, spacing]


def checklist(step, working_bool=None, task=None, textbox=None):
    clear(0)
    global step1, step2, step3, step4, step5

    value = completed
    if working_bool == True:
        value = working

    if step == 1:
        if task:
            val = checklist_helper(task)
            step1 = f"| {value} | Extracting songs         | ({val[0]}s){val[1]}|"

    elif step == 2:
        if task:
            val = checklist_helper(task)
            step2 = f"| {value} | Extracting song-ids      | ({val[0]}s){val[1]}|"

    elif step == 3:
        if task:
            val = checklist_helper(task)
            step3 = f"| {value} | Generating songs         | ({val[0]}s){val[1]}|"

    elif step == 4:
        if task:
            val = checklist_helper(task)
            step4 = f"| {value} | Adding songs             | ({val[0]}s){val[1]}|"

    elif step == 5:
        if task:
            val = checklist_helper(task)
            step5 = f"| {value} | Playlist finished        | ({val[0]}s){val[1]}|"

    print(topbot)
    print(step1)
    print(step2)
    print(step3)
    print(step4)
    print(step5)
    print(topbot)
    
    str_val = f"{topbot}\n{step1}\n{step2}\n{step3}\n{step4}\n{step5}\n{topbot}"
    textbox[0]["text"] = str_val
    textbox[1].update()

def roundPlaylistLen(val):
    return (val + (20 - val % 20)) / 4


def isvalid(option, min, max):
    return min <= option <= max


def raiseError(error):
    print(f"{fore.RED}Error: {fore.RESET}{error}")


def clear(val):
    if val != 0:
        time.sleep(val)
    os.system("clear")



#########################
#   GENERATE PLAYLIST   #
#########################


def generate_similar_playlist(spotifyObject, playlist_url, error):
    tasktime = time.time()

    checklist(0, task=tasktime, textbox=error)
    checklist(1, True, textbox=error)
    onetime = time.time()

    playlist_id = playlist_url.split("/")[-1]
    playlist = spotifyObject.playlist(playlist_id)

    song_names = []
    tracks = playlist["tracks"]

    for z in range(len(tracks["items"])):
        item = tracks["items"][z]
        song_names.append(item["track"]["name"])

        checklist(1, True, task=tasktime, textbox=error)

    checklist(1, task=onetime, textbox=error)
    checklist(2, True, textbox=error)
    twotime = time.time()

    song_ids = []
    total_songs = []

    for z in range(len(song_names)):
        item = song_names[z]
        result = spotifyObject.search(q=item, type="track")
        song_id = result["tracks"]["items"][0]["id"]

        song_ids.append(song_id)
        checklist(2, True, task=twotime, textbox=error)

    checklist(2, task=twotime, textbox=error)
    checklist(3, True, textbox=error)
    threetime = time.time()

    for _ in range(int(roundPlaylistLen(len(song_ids)) / 4)):
        recommendations = spotifyObject.recommendations(
            limit=20, seed_tracks=random.sample(song_ids, 5)
        )

        for y in range(len(recommendations["tracks"])):
            song = recommendations["tracks"][y]["name"]
            song_uri = recommendations["tracks"][y]["uri"]

            value = f"{song}:{song_uri}"
            total_songs.append(value)
            checklist(3, True, task=threetime, textbox=error)

    scope = "playlist-modify-public playlist-modify-private"
    token = util.prompt_for_user_token(
        username,
        scope,
        client_id=clientID,
        client_secret=clientSecret,
        redirect_uri=redirectURI,
    )
    sp = spotipy.Spotify(auth=token)

    generated_name = "".join(random.choices(string.ascii_letters, k=10))
    gen_playlist = sp.user_playlist_create(username, name=generated_name)
    gen_playlist_id = gen_playlist["id"]

    checklist(3, task=threetime, textbox=error)
    checklist(4, True, textbox=error)
    fourtime = time.time()

    for item in total_songs:
        item = item.split(":")

        sp.user_playlist_add_tracks(username, gen_playlist_id, [item[-1]])
        checklist(4, True, task=fourtime, textbox=error)

    checklist(4, task=fourtime, textbox=error)
    checklist(5, True, textbox=error)

    time.sleep(1)
    checklist(5, task=tasktime, textbox=error)

    print(f"Generated playlist: {generated_name}")
    print(f"Playlist URL: {gen_playlist['external_urls']['spotify']}")
    messagebox.showinfo("showinfo", F"Playlist URL: {gen_playlist['external_urls']['spotify']}")


def start_gen(playlist_url, error):
    spotifyObject = spotipy.Spotify(auth=spotipy.SpotifyOAuth(clientID,clientSecret,redirectURI).get_access_token()["access_token"])
    generate_similar_playlist(spotifyObject, playlist_url, error)
    
# main("https://open.spotify.com/playlist/6awC1Tq3W35gFaF5mxVHTc")    