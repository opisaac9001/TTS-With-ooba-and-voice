# TTS-With-ooba-and-voice
This is a basic code that uses oobabooga, whisper, and cuqui tts to allow you to talk to an llm and get a responce with a tts. 

This code utilizes XTTSv2 by coqui to turn a responce from oobabooga into speech. It also uses openAIs whisper model to take voice, transpose it and feed that to an LLM. Is this terrible spegetthi code? Yes. Does it work supprisingly well? Kind of. 

You will need to have Python 3.10 or 3.11 and anaconda/miniconda. 

Step one. Create a conda enviroment with python 3.10. 

Step two. Activate conda enroment and run "pip install -r requirements.txt". and "pip install ffmpeg" (Honestly i dont know how many of those requirements are actually needed and i believe you actually need a couple more. The code should yell at you and tell you what to install) 

Step three. Install Oobabooga from https://github.com/oobabooga/text-generation-webui and run it with the flags --verbose --api. Other flags may be needed for your specific set up. 

Step four. Download any small model from hugging face. The TTS model and whisper model take up about 5-6 gigs of VRAM so use a model that wont cause and OOM error when everything is loaded to gether. 

Step Five. Download TTS model from [https://huggingface.co/coqui/XTTS-v2/blob/v2.0.2/model.pth](https://huggingface.co/coqui/XTTS-v2/tree/v2.0.2). place the whole repository in teh folder Model_and_config_here.

Step six. Get a clip between 3-6 seconds long, (or longer it doesnt matter) and place it in voices. 

Step seven. Open the the aispeech.py file and path the three needed files. Line 15, 17, and line 22 need to be edited. 

Step eight. in the terminal with your conda env active run "python run.py" 

Step nine. Pray that you get no errors. 

Optional step ten. curse me forever because of my crappy code and the errors you are recieving. 

Step elevin. Press 1 or 2 depending on if you want to use Voice or text to interface in the terminal and enjoy. 

There are most likely many steps im missing or things im missing. This has taken me way to long to get working and i have forgotten all the things ive done to get it working. If you have a fix just submit it. I still need to do some stuff to it like get it to have discord integration and an API. But because my code knowledge is limited to ChatGPT 3.5 it takes a while. 

Thanks for checking this out. Have fun..... If you can get it to work. 


This works on windows and linux. Maybe on mac but i doubt it. 

