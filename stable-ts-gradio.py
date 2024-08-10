# Github: https://github.com/jianfch/stable-ts.git
# To install use: !pip install -U git+https://github.com/jianfch/stable-ts.git

import os
import stable_whisper
import time
import gradio as gr
from pytubefix import YouTube

# Available Whisper models
MODEL_CHOICES = [
    "tiny.en",
    "tiny",
    "base.en",
    "base",
    "small.en",
    "small",
    "medium.en",
    "medium",
    "large-v3",
]


def transcribe_audio(audio_path, selected_model):
    # Load the Whisper model
    model = stable_whisper.load_model(selected_model)
    
    start_time = time.time()
    result = model.transcribe(audio_path)
    end_time = time.time()

    # Save the transcription result as an SRT file
    srt_filename = os.path.splitext(os.path.basename(audio_path))[0] + ".srt"
    result.to_srt_vtt(srt_filename, word_level=False)

    # Save the transcription result as a TXT file
    txt_filename = os.path.splitext(os.path.basename(audio_path))[0] + ".txt"
    result.to_txt(txt_filename)

    # Calculate the time taken
    time_taken = end_time - start_time
    minutes, seconds = divmod(time_taken, 60)

    return (
        f"Transcription saved as {txt_filename}! Time taken: {int(minutes)} minutes and {int(seconds)} seconds",
        result.text,
        [txt_filename, srt_filename],  # Return the filename instead of gr.File object
    )


def transcribe_youtube(youtube_link, selected_model, delete_audio):
    try:
        yt = YouTube(youtube_link)
        stream = yt.streams.filter(only_audio=True).first()
        downloaded_file = stream.download()
        
        result = transcribe_audio(downloaded_file, selected_model)

        if delete_audio:
            os.remove(downloaded_file)

        return result
    except Exception as e:
        return f"Error: {e}", None, None


def transcribe_local_file(file, selected_model):
    try:
        audio_path = file.name
        return transcribe_audio(audio_path, selected_model)
    except Exception as e:
        return f"Error: {e}", None, None


with gr.Blocks() as interface:
    gr.Markdown("## Speech-to-Text Transcription with Stable Whisper")
    
    # Dropdown for model selection
    model_dropdown = gr.Dropdown(
        choices=MODEL_CHOICES,
        value="small",  # Default model
        label="Select Whisper Model",
    )
    
    with gr.Tabs():
        with gr.TabItem("YouTube"):
            youtube_link = gr.Textbox(label="Enter YouTube Link")
            delete_audio_checkbox = gr.Checkbox(label="Delete downloaded audio after transcription?", value=True)
            youtube_button = gr.Button("Transcribe")
            youtube_output = gr.Textbox(label="Output")
            youtube_transcription = gr.Textbox(label="Transcription")
            youtube_download = gr.Files(label="Download Transcription")
            youtube_button.click(
                transcribe_youtube,
                inputs=[youtube_link, model_dropdown, delete_audio_checkbox],  # Pass selected model
                outputs=[youtube_output, youtube_transcription, youtube_download],
            )

        with gr.TabItem("Local File"):
            local_file = gr.File(label="Upload Audio File")
            local_button = gr.Button("Transcribe")
            local_output = gr.Textbox(label="Output")
            local_transcription = gr.Textbox(label="Transcription")
            local_download = gr.Files(label="Download Transcription")
            local_button.click(
                transcribe_local_file,
                inputs=[local_file, model_dropdown],  # Pass selected model
                outputs=[local_output, local_transcription, local_download],
            )

interface.launch(server_port=7950)