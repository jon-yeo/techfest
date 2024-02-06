from flask import Flask, render_template, request, redirect, url_for,session

import os
from pathlib import Path
from openai import OpenAI


from pygoogle_image import image as pi


import requests

app = Flask(__name__)   

@app.route("/")
def main():
    return render_template('index.html')

@app.route('/search', methods = ['GET', 'POST'])
def search_func():
        data = request.args.get('data', '')
        return render_template("search.html", data=data)

@app.route("/submit", methods=["POST"])
def submit():
    keywords = request.form['keywords']

    
    #download imgs
    pi.download(keywords=keywords, limit=9)
    import shutil
    import os
        
    source_dir = 'images/'
    target_dir = 'static/images'
        
    file_names = os.listdir(source_dir)
        
    for file_name in file_names:
        shutil.move(os.path.join(source_dir, file_name), target_dir)
    #f
    text = keywords
    a = text
    for x in text:
        text = text + " " + x
        
    text += " " + a
    print(text)

    #text to speech
    CHUNK_SIZE = 1024
    url = "https://api.elevenlabs.io/v1/text-to-speech/ErXwobaYiN019PkySvjV"

    headers = {
    "Accept": "audio/mpeg",
    "Content-Type": "application/json",
    "xi-api-key": "a3dff5560e58b7f976a3cb86eff597c7"
    }

    data = {
    "text": text,
    "model_id": "eleven_monolingual_v1",
    "voice_settings": {
        "stability": 0.1,
        "similarity_boost": 0.5
    }
    }

    response = requests.post(url, json=data, headers=headers)
    with open("static/audio/"+keywords+'.mp3', 'wb') as f:
        for chunk in response.iter_content(chunk_size=CHUNK_SIZE):
            if chunk:
                f.write(chunk)

    #response.stream_to_file(speech_file_path)
    print(keywords)
    return redirect(url_for('search_func',data = keywords))

app.run()

    


# from mutagen.mp3 import MP3 
# from PIL import Image 
# from pathlib import Path 
# import os 
# import imageio 
# from moviepy import editor 
# audio_path = os.path.join(os.getcwd(), "music.mp3") 
# video_path = os.path.join(os.getcwd(), "static") 
# images_path = os.path.join(os.getcwd(), "Images") 
# audio = MP3(audio_path) 
# audio_length = audio.info.length 
  
# list_of_images = [] 
# for image_file in os.listdir(images_path): 
#     if image_file.endswith('.png') or image_file.endswith('.jpg'): 
#         image_path = os.path.join(images_path, image_file) 
#         image = Image.open(image_path)
#         list_of_images.append(image) 
  
# duration = audio_length/len(list_of_images) 
# imageio.mimsave('images.gif', list_of_images, fps=1/duration) 
  
# video = editor.VideoFileClip("images.gif") 
# audio = editor.AudioFileClip(audio_path) 
# final_video = video.set_audio(audio) 
# os.chdir(video_path) 
# final_video.write_videofile(fps=60, codec="libx264", filename="video.mp4") 