"""
Note TO POFESSOR

I have a few user tokens/secrets which I have to use to run this program as it collborates with the spotify api. I dont feel comfortable
sharing these. But, if you do happen to be needing a video for grading/showing the class (hopefully), I am happy to provide that for you.
Thank you

"""

import tkinter as tk
from Spotify import start_gen

window = tk.Tk()
window.title("Playlist Generator")
window.geometry("1000x500")

playlist_link = tk.StringVar()

label = tk.Label(window, text="Enter Playlist Link", font=("Arial", 30))
label.pack(pady=10)

entry = tk.Entry(window, textvariable=playlist_link, font=("Arial", 20))
entry.pack(pady=10)

def main():
    global label, button
    
    val = playlist_link.get()
    if val:
        button["state"] = "disabled"
        label["text"] = "Generating playlist..."
        error["text"] = "Check console for generating progress"   
        window.update()
        
        start_gen(val, [error, window])
        label["text"] = "Playlist generation complete. Rerun the program to try again."
        button["state"] = "normal"
        window.update()
    
    else:
        error["text"] = "Please enter a playlist URL"    


error = tk.Label(window, text="", font=("Arial", 12))
error.pack(pady=10)

button = tk.Button(window, text="Generate Playlist", command=main, font=("Arial", 20))
button.pack(pady=20)


# Start the Tkinter event loop
window.mainloop()
