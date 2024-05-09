# Install Pre-Requisites
#@title Install ! 😉
!pip install -q faster-whisper
!pip install -q pytube
!pip install -q pydub
!pip install -q ffmpeg-python
!sudo wget https://github.com/yt-dlp/yt-dlp/releases/latest/download/yt-dlp -O /usr/local/bin/youtube-dl
!sudo chmod a+rx /usr/local/bin/youtube-dl
!apt install libcublas11 -y -q
!youtube-dl --version

# -----------------------------------------------------------------

#@title YouTube2Transcript [Auto-upload to Drive]

from google.colab import userdata
userdata.get('HF_TOKEN')

# Save files into Google Drive
save_drive = False

if save_drive:
  from google.colab import drive
  import shutil
  drive.mount('/content/drive/')

from faster_whisper import WhisperModel
import re
import time
import ffmpeg
import os
from pydub.utils import mediainfo
from pytube import YouTube

# Define the mapping from numbers to model names
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
for number, model in models.items():
    print("(%d) > %s" % (number, model))

# Get user input
user_input = input("Please enter the number of the model you want to use: ")

# Validate user input
while not user_input.isdigit() or int(user_input) not in models:
    print("Invalid input. Please enter a number corresponding to a model.")
    user_input = input("Please enter the number of the model you want to use: ")

# Get the model name corresponding to the number
user_input = int(user_input)
model_name = models.get(user_input)
print("Model to be used: %s" % model_name)
model_size = model_name

# Defining functions
def print_audio_duration(file_name):
    probe = ffmpeg.probe(file_name)
    duration = float(probe['format']['duration'])

    hours = int(duration // 3600)
    minutes = int((duration % 3600) // 60)
    seconds = int(duration % 60)
    print(f"Audio duration: {hours} hours, {minutes} minutes, and {seconds} seconds")

# Run on GPU with FP16
model = WhisperModel(model_size, device="cuda", compute_type="float16")

# or run on GPU with INT8
# model = WhisperModel(model_size, device="cuda", compute_type="int8_float16")
# or run on CPU with INT8
# model = WhisperModel(model_size, device="cpu", compute_type="int8")

url = input("Type the YouTube link: ")
yt = YouTube(url)
os.environ['URL'] = url
!youtube-dl  -o "audio.%(ext)s" -f 140  $URL
print("Found:")
!youtube-dl --get-title $URL
filename = "audio.m4a"
print_audio_duration(filename)

segments, info = model.transcribe(filename, beam_size=5)

print("Detected language '%s' with probability %f" % (info.language, info.language_probability))

# Start time read
begin_time = time.time()

def format_time(seconds):
  """Converts seconds to SRT time format (hh:mm:ss.mmm)"""
  hours = int(seconds // 3600)
  minutes = int((seconds % 3600) // 60)
  seconds = seconds % 60
  return f"{hours:02d}:{minutes:02d}:{seconds:.03f}"



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

new_filename = name_cleaner(filename)
# Open the files in write mode

with open(f'{new_filename}_segments.srt', 'w') as srt_file, \
     open(f'{new_filename}_text_only.txt', 'w') as text_file:
    
    for i, segment in enumerate(segments, start=1):
        start_time = format_time(segment.start)
        end_time = format_time(segment.end)
        text = segment.text

        # Write the subtitle number, time range, and text to the SRT file
        srt_file.write(f"{i}\n{start_time} --> {end_time}\n{text}\n\n")

        # Write only the text to the text-only file
        text_file.write(f"{text}\n")

        print(f"Progress: {end_time}")

end_time = time.time()

execution_time = end_time - begin_time

if execution_time > 60:
    if execution_time > 3600:
        execution_time = execution_time / 3600
        print(f"The program took {execution_time} hours to run.")
    else:
        execution_time = execution_time / 60
        print(f"The program took {execution_time} minutes to run.")
else:
    print(f"The program took {execution_time} seconds to run.")

new_filename2 = yt.title
new_filename2 = name_cleaner(new_filename2)

# Copying files into Google Drive
if save_drive:
  # Segments
  source_path = f'{new_filename}_segments.srt'
  dest_path = f"/content/drive/My Drive/Colab Notebooks/Transcriptions/{new_filename2}_segments.srt"
  shutil.copyfile(source_path, dest_path)
  # Full Text
  source_path = f'{new_filename}_text_only.txt'
  dest_path = f"/content/drive/My Drive/Colab Notebooks/Transcriptions/{new_filename2}_text_only.txt"
  shutil.copyfile(source_path, dest_path)

# Rename local filenames
os.rename(f'{new_filename}_segments.srt', 'segments_{}.srt'.format(new_filename2))
os.rename(f'{new_filename}_text_only.txt', 'text_only_{}.txt'.format(new_filename2))
