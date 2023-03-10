

# Commented out IPython magic to ensure Python compatibility.
# the scipy version packaged with colab is not tolerant of misformated WAV files.
# install the latest version.
# !pip3 install -U scipy

# !git clone https://github.com/jnordberg/tortoise-tts.git
# %cd tortoise-tts
# !pip3 install transformers==4.19.0
# !pip3 install -r requirements.txt
# !python3 setup.py install

# Imports used through the rest of the notebook.
import torch
import torchaudio
import torch.nn as nn
import torch.nn.functional as F

import IPython

from tortoise.api import TextToSpeech
from tortoise.utils.audio import load_audio, load_voice, load_voices

# This will download all the models used by Tortoise from the HuggingFace hub.
tts = TextToSpeech()

# This is the text that will be spoken.
text = "Joining two modalities results in a surprising increase in generalization! What would happen if we combined them all?"

# Here's something for the poetically inclined.. (set text=)
text = """[Talking with fear and Scared about the end of the world, In an Indian accent]My dear friends, it is with a heavy heart that I must speak to you about the end of the world. The signs are all around us - from the changing climate to the escalating conflicts between nations. We are facing a crisis of unprecedented magnitude, and the time for action is now."""


# Pick a "preset mode" to determine quality. Options: {"ultra_fast", "fast" (default), "standard", "high_quality"}. See docs in api.py
preset = "fast"

# Tortoise will attempt to mimic voices you provide. It comes pre-packaged
# with some voices you might recognize.

# Let's list all the voices available. These are just some random clips I've gathered
# from the internet as well as a few voices from the training dataset.
# Feel free to add your own clips to the voices/ folder.
#%ls tortoise/voices

IPython.display.Audio('tortoise/voices/mol/1.wav')

# Pick one of the voices from the output above
voice = 'mol'

# Load it and send it through Tortoise.
voice_samples, conditioning_latents = load_voice(voice)
gen = tts.tts_with_preset(text, voice_samples=voice_samples, conditioning_latents=conditioning_latents, 
                          preset=preset)
torchaudio.save('generated.wav', gen.squeeze(0).cpu(), 24000)
IPython.display.Audio('generated.wav')

# Tortoise can also generate speech using a random voice. The voice changes each time you execute this!
# (Note: random voices can be prone to strange utterances)
gen = tts.tts_with_preset(text, voice_samples=None, conditioning_latents=None, preset=preset)
torchaudio.save('generated.wav', gen.squeeze(0).cpu(), 24000)
IPython.display.Audio('generated.wav')

# Optionally, upload use your own voice by running the next two cells. I recommend
# you upload at least 2 audio clips. They must be a WAV file, 6-10 seconds long.
CUSTOM_VOICE_NAME = "chirag"

import os
from google.colab import files

custom_voice_folder = f"tortoise/voices/{CUSTOM_VOICE_NAME}"
os.makedirs(custom_voice_folder)
for i, file_data in enumerate(files.upload().values()):
  with open(os.path.join(custom_voice_folder, f'{i}.wav'), 'wb') as f:
    f.write(file_data)

# Generate speech with the custotm voice.
voice_samples, conditioning_latents = load_voice(CUSTOM_VOICE_NAME)
gen = tts.tts_with_preset(text, voice_samples=voice_samples, conditioning_latents=conditioning_latents, 
                          preset=preset)
torchaudio.save(f'generated-{CUSTOM_VOICE_NAME}.wav', gen.squeeze(0).cpu(), 24000)
IPython.display.Audio(f'generated-{CUSTOM_VOICE_NAME}.wav')

# You can also combine conditioning voices. Combining voices produces a new voice
# with traits from all the parents.
#
# Lets see what it would sound like if Picard and Kirk had a kid with a penchant for philosophy:
voice_samples, conditioning_latents = load_voices(['pat', 'william'])

gen = tts.tts_with_preset("They used to say that if man was meant to fly, he’d have wings. But he did fly. He discovered he had to.", 
                          voice_samples=voice_samples, conditioning_latents=conditioning_latents, 
                          preset=preset)
torchaudio.save('captain_kirkard.wav', gen.squeeze(0).cpu(), 24000)
IPython.display.Audio('captain_kirkard.wav')