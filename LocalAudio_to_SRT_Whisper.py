# Use Whisper from 'github.com/openai/whisper' to transcribe an audio. 
# Whisper is more accurate than Faster-Whisper despite being around 10-20% slower.

import whisper
from datetime import timedelta
import os
import random
import time
import torch

def remove_extension(filename):
    name, extension = os.path.splitext(filename)
    return name

def format_time(seconds):
    td = timedelta(seconds=seconds)
    hours, remainder = divmod(td.seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    milliseconds = td.microseconds // 1000
    return f"{hours:02d}:{minutes:02d}:{seconds:02d},{milliseconds:03d}"

file = input("Paste the filepath including its extension: ")
folder_location = os.path.dirname(file)

filename = os.path.basename(file)
filename = remove_extension(filename)
random_number = random.randint(1, 20)

#%% Define the mapping from numbers to model names
models = {
    1: "large-v2",
    2: "medium",
    3: "medium.en",
    4: "small",
    5: "small.en",
    6: "base",
    7: "base.en",
    8: "tiny",
    9: "tiny.en"
}

# Print the options
print("Now select a model:")
for number, model in models.items():
    print("(%d) > %s" % (number, model))

while True:
    # Ask the user to pick a number
    user_input = int(input("Please enter a number: "))

    # Get the model name corresponding to the number
    model_name = models.get(user_input)

    if model_name is not None:
        print("Model to be used: %s" % model_name)
        break
    else:
        print("Invalid selection. Please try again.")

# Load model Models: tiny, base, small, medium, large.
model = model_name

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(f"Using device: {device}")

print("Starting process...")
print("(Patiently wait)...")

#%% Record the start time
init_time = time.time()

# Do the whole body transcription
trans = model.transcribe(file)

# Record the end time
completition_time = time.time()

# Create .srt file
with open(f"fl_{filename}_{random_number}.srt", "w", encoding="utf-16") as srt_file, \
     open(f"fl_{filename}_{random_number}.txt", "w", encoding="utf-16") as txt_file:
    
    for i, segment in enumerate(trans['segments'], start=1):
        # Write to SRT file
        srt_file.write(f"{i}\n")
        start_time = format_time(segment['start'])
        end_time = format_time(segment['end'])
        srt_file.write(f"{start_time} --> {end_time}\n")
        srt_file.write(f"{segment['text'].strip()}\n\n")
        
        # Write to plain text file
        txt_file.write(f"{segment['text'].strip()}\n")

print(f"SRT file and plain text file have been created:\n fl_{filename}_{random_number}.srt and fl_{filename}_{random_number}.txt")


#%% Calculate the elapsed time in seconds
elapsed_time_seconds = completition_time - init_time

total_seconds = elapsed_time_seconds

# Convert to hours, minutes, seconds
hours = int(total_seconds // 3600)
minutes = int((total_seconds % 3600) // 60)
seconds = total_seconds % 60

# Build the output string
duration_str = "\nElapsed Time: "
if hours > 0:
    duration_str += f"{hours} hours, "
if minutes > 0:
    duration_str += f"{minutes} min, "
duration_str += f"{int(seconds)} seconds"

print(duration_str)

print("Done")

#%% Github WhisperAI
# URL: https://github.com/openai/whisper

# small: 4.5min → 58s


