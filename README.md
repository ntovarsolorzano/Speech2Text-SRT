# python_for_lazies
My scripts that I use to automate stuff, because I hate wasting time. You can use it if it's useful to you.   

# Requisites: 
Do not forget to install libraries:  
`pip install git+https://github.com/openai/whisper.git -q`  
`pip install setuptools-rust`  
`pip install ffmpeg-python`  
`pip install git+https://github.com/pytube/pytube.git -q`  
  
Paste it into your Python IDE or run as:  
`git clone https://github.com/ntovarsolorzano/python_for_lazies`  
`cd python_for_lazies`  
`python Youtube_to_SRT_whisperai.py`

## Youtube to SRT using Whisper  
Python script to Get a YouTube URL and return a SRT file in its language (English).   
Edit the 'whisper' model to adjust if language is not English.   
I suggest small, or medium. These are good enough. If you have a beast CPU you can do large.   

*Time to process: *  
(my experience ~ reference only)   
Base: 0.12 x VideoLength  
Small: 0.9 x VideoLength  
Medium: 2.1 x VideoLength  

# Credits to:  
[OpenAI](https://github.com/openai/whisper) for making this awesome tool available to the rest of us, simple mortals. 
