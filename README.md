Ever wished you could have a heart-to-heart with an LLM (Laid-Back Llama)? Look no further! This code, though a tad spaghetti-ish, lets you chat with our llama friends using oobabooga, whisper, and cuqui TTS. Does it qualify as terrible spaghetti code? Absolutely. Does it mysteriously work? Kinda.

Setup Steps:

	1.	🚀 Clone this repo.
	2.	🐍 Create a conda environment with Python 3.10 (or 3.11, because why not).
	3.	🧙‍♂️ Activate conda environment and run pip install -r requirements.txt and pip install ffmpeg. Honestly, we’re not entirely sure about all those requirements, but the code will shout at you if something’s missing.
	4.	🚀 Install Oobabooga from here. Run it with flags --verbose --api. Note: Your setup might need additional flags; let the code guide you.
	5.	🤖 Download a petite model from Hugging Face. Our TTS model and whisper model hog around 5-6 gigs of VRAM, so pick wisely to avoid OOM errors.
	6.	📥 Download the TTS model from here. Drop the entire repository into the “Model_and_config_here” folder.
	7.	🗣️ Grab a 3-6 second (or longer) audio clip and toss it into the “voices” folder.
	8.	🖋️ Open aispeech.py and point it to the three crucial files (Line 15, 17, and 22 are your editing zones).
	9.	🚀 With your conda environment active, run python run.py in the terminal.
	10.	🙏 Cross your fingers for no errors.
	11.	🤷‍♂️ Optional: Forever curse the developer (that’s me!) and the errors haunting you.
	12.	1️⃣ or 2️⃣? Choose voice or text interaction in the terminal and enjoy!

This masterpiece (or mess, depending on your perspective) works on Windows and Linux. Maybe on a Mac, but let’s not get our hopes up.

Thanks for diving into this llama-filled adventure. Good luck making it work. If you find fixes, just toss them in. Still on the to-do list: Discord integration and an API. Bear with my limited coding knowledge; it’s a work in progress.


PS. Yes I know that normal Oobabooga can do this in the UI a millions times better, buuuuut i wanted to be able to use this in other projects like a discord bot or some API or just other things. So I took way to much time making this. Have fun. 