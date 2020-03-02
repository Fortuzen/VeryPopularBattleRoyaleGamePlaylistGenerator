# VeryPopularBattleRoyaleGamePlaylistGenerator

Create randomized music playlists. Inspired by certain Youtube channels. Work in progress!


Notes: remove -an option from 
ffmpeg_writer.py file in
\site-packages\moviepy-1.0.1-py3.7.egg\moviepy\video\io

IF audio doesn't work.

## Install

You need moviepy and numpy.

Download and run `pip install -e .` where setup.py is.

## How to use
 
python -m vpbrgpg -imagefolder {} -musicfolder {} -outputfolder {} -outputprefix {}
 -count {}
 
Put your stuff (your boring, copyright free electronic music and images) in two folders like "music" and "images".
These are default folders. After this, run the program and wait. Finally, upload all the videos to Youtube
for profit $$$.

Examples:

Create 4 randomized playlist named "out_*.mp4" in output folder.

python -m vpbrgpg -imagefolder images -musicfolder music -outputfolder output -outputprefix out_
 -count 4

## Todo/Potential features
* GUI (PyQt5)
* Better image randomizer
* Multithreading
* Add artist to playlist info
* Add text(current song/artist)
* Visualizations