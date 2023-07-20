"""
Input: 
Youtube_URL

Output: 
SRT File. Hopefully with no errors. Otherwise you can use: https://subtitletools.com/srt-cleaner
.. to save your day. 
Nelson.

import torch
torch.backends.cudnn.enabled
torch.cuda.is_available()

print(torch.version.cuda)
torch.cuda.FloatTensor()
"""


import whisper
import re
from pytube import YouTube
from datetime import timedelta
import random
import time
import os
import torch

def name_cleaner(name):
    clean_name = re.sub(r'[^\w\-_\. ]', '', name)
    clean_name = re.sub(r'\s+', ' ', clean_name)
    clean_name = clean_name.strip()
    
    arr = clean_name.split(" ")
    if len(arr) > 5:
        clean_name = arr[0] + "_" +  arr[1] + "_"  + arr[2] + "_"  + arr[3] + "_"  + arr[4] + "_"  + arr[5]
    else:
         pass   
    return clean_name

def download_audio_from_youtube(url):
    video_name = "random"
    try:
        # Create a YouTube object with the given URL
        yt = YouTube(url)

        # Get the highest quality audio stream
        audio_stream = yt.streams.get_audio_only()

        # Check if audio stream is available
        if audio_stream:
            # Download the audio stream
            downloaded_audio = audio_stream.download(filename="audio")
            video_name = yt.title
            print(f"Found: {video_name}")
            print("Audio downloaded successfully.")
        else:
            print("No audio stream available.")
    except:
        print("No video found.")
   
    return downloaded_audio, video_name


# 1. Define the audio to be used
# Example usage
print("Paste the YouTube video URL: \n")
Youtube_URL = input() # Example "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
file, video_name = download_audio_from_youtube(Youtube_URL)
# Clean video_name
video_name = name_cleaner(video_name)
random_number = random.randint(1, 20)

if file:
    # 2. Use the trained model to transcript the audio
    #Load model Models: tiny, base, small, medium, large.
    device = "cuda" if torch.cuda.is_available() else "cpu"
    print("GPU detected") if torch.cuda.is_available() else print("Using CPU. This may take as long as the video or more.")

    # Select a model: 
    all_models = ["tiny", "tiny.en", "base", "base.en", "small", "small.en", "medium", "medium.en", "large"]

    print("Please select a model:")
    for i, model in enumerate(all_models):
        print(f"({i+1}) {model}")

    while True:
        try:
            selection = int(input("> "))
            if selection < 1 or selection > len(all_models):
                raise ValueError
            break
        except ValueError:
            print("Invalid selection. Please enter a number between 1 and 9.")

    selected_model = all_models[selection-1]
    print(f"Selected model: {selected_model}")

    # Make use of that model
    model = whisper.load_model(selected_model).to(device)
    time1 = time.time()
    trans = model.transcribe(file)

    # 3. Write the SRT file
    # Create .srt file
    with open(f"yt_{video_name}_{random_number}.srt", "w") as f:
        for segment in trans['segments']:
            # Write subtitle index
            f.write(f"{segment['id'] + 1}\n")

            # Write subtitle timestamp
            start_time = str(timedelta(seconds=segment['start']))
            if start_time.startswith("0:"): start_time = "00" + start_time[1:]
            start_time = start_time.replace('.', ',')
            try:
                parts = start_time.split(',')
                if len(parts) >= 2:
                    start_time = f"{parts[0]},{parts[1][:3]}"
                else:
                    start_time = start_time + ",000"
            except Exception:
                pass
            
            end_time = str(timedelta(seconds=segment['end']))
            if end_time.startswith("0:"): end_time = "00" + end_time[1:]
            end_time = end_time.replace('.', ',')
            try:
                parts = end_time.split(',')
                if len(parts) >= 2:
                    end_time = f"{parts[0]},{parts[1][:3]}"
                else:
                    end_time = end_time + ",000"
            except Exception():
                pass
            f.write(f"{start_time} --> {end_time}\n")

            # Write subtitle text
            add_text = str.lstrip(segment['text'])
            f.write(f"{add_text}\n\n")

    print(f"Subtitle file saved as: yt_{video_name}.srt")
    elapsed_time = time.time() - time1
    elapsed_time = round( (elapsed_time/60), 1)
    print(f"Took {elapsed_time} minutes")

    with open(f'yt_{video_name}.txt', 'w') as f:
        f.write(trans['text'])

    cwd = os.getcwd()
    print("File saved at: ", cwd)

    # Github WhisperAI
    # URL: https://github.com/openai/whisper
    
else:
    print("No video found.")
