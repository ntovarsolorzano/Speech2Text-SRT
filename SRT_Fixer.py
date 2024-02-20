import re

srt_file = '''
[45.60s -> 51.08s] 70s 80s y 90s y 100s tendrás más energía cuando cuides tu
[51.08s -> 55.20s] cuerpo físico de estas maneras para hacer las obras que Dios te llamó a hacer algunas de
[55.20s -> 58.72s] crees que es un asunto espiritual piensas que tienes un espíritu de pereza un espíritu
[58.72s -> 63.16s] de lentitud pero no estás comiendo la comida adecuada, comida sana, no estás
[63.16s -> 67.82s] haciendo ejercicio no estás bebiendo suficiente agua y esa es la razón por la que puedo
[67.82s -> 72.80s] ora por ti todo el día y nada cambiará hasta que cambies tu estilo de vida
[72.80s -> 76.04s] y empieza a cuidar tu cuerpo y empieza a tratarlo como un templo que es.
'''

import os
import random
random_number = random.randint(10, 99)

filepath = input("Paste here the filepath including the extension: ")

# If you have not explicitly defined dest_folder, specify the path here
dest_folder = os.path.dirname(filepath)
file_name = os.path.basename(filepath)

# Construct the full file path
output_file_path = os.path.join(dest_folder, f'Fixed.SRT.{file_name}_{random_number}.srt')


with open(f'{filepath}', 'r') as file:
    # Read the contents of the file
    srt_file = file.read()

# Function to convert seconds to HH:MM:SS,MS
def convert_to_srt_time(seconds):
    ms = int((seconds % 1) * 1000)
    seconds = int(seconds)
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    seconds = (seconds % 60)
    return f"{hours:02d}:{minutes:02d}:{seconds:02d},{ms:03d}"

# Split content into lines
lines = srt_file.strip().split('\n')

# Process each line and apply fixes
fixed_srt = []
for index, line in enumerate(lines, 1):
    # Extract time and text
    time_info, text = re.match(r'\[(.*?)\](.*)', line).groups()
    start, end = time_info.split(' -> ')
    
    # Convert times
    start_srt_time = convert_to_srt_time(float(start[:-1]))
    end_srt_time = convert_to_srt_time(float(end[:-1]))
    
    # Create the correct SRT block
    srt_block = f"{index}\n{start_srt_time} --> {end_srt_time}\n{text.strip()}\n"
    
    # Add to the final SRT content
    fixed_srt.append(srt_block)

# Join all blocks into final SRT content
final_srt_content = '\n'.join(fixed_srt)
print(final_srt_content)

# If needed, save the final SRT content to a file
with open(output_file_path, 'w') as srt_file:
    srt_file.write(final_srt_content)

"""
pseudo_srt_file = '''
[45.60s -> 51.08s] 70s 80s y 90s y 100s tendrás más energía cuando cuides tu
[51.08s -> 55.20s] cuerpo físico de estas maneras para hacer las obras que Dios te llamó a hacer algunas de
[55.20s -> 58.72s] crees que es un asunto espiritual piensas que tienes un espíritu de pereza un espíritu
[58.72s -> 63.16s] de lentitud pero no estás comiendo la comida adecuada, comida sana, no estás
[63.16s -> 67.82s] haciendo ejercicio no estás bebiendo suficiente agua y esa es la razón por la que puedo
[67.82s -> 72.80s] ora por ti todo el día y nada cambiará hasta que cambies tu estilo de vida
[72.80s -> 76.04s] y empieza a cuidar tu cuerpo y empieza a tratarlo como un templo que es.
''' 

Converted into:

11
00:00:45,600 --> 00:00:51,079
70s 80s y 90s y 100s tendrás más energía cuando cuides tu

12
00:00:51,079 --> 00:00:55,200
cuerpo físico de estas maneras para hacer las obras que Dios te llamó a hacer algunas de

13
00:00:55,200 --> 00:00:58,719
crees que es un asunto espiritual piensas que tienes un espíritu de pereza un espíritu

14
00:00:58,719 --> 00:01:03,159
de lentitud pero no estás comiendo la comida adecuada, comida sana, no estás

15
00:01:03,159 --> 00:01:07,819
haciendo ejercicio no estás bebiendo suficiente agua y esa es la razón por la que puedo
"""
