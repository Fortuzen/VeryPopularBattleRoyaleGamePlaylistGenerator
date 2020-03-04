from moviepy.editor import *
import moviepy.audio.fx.all as afx
from moviepy.audio.fx.audio_fadein import audio_fadein
from moviepy.audio.fx.audio_fadeout import audio_fadeout
import os
import random
import copy
import numpy as np
import datetime

import Config



# Parse args
args = Config.parse_args()


def load_music(folder):
    files = os.listdir(folder)
    music_clips = [AudioFileClip(folder+"/"+file) for file in files]
    return music_clips


def load_images(folder):
    files = os.listdir(folder)
    image_clips = [ImageClip(folder+"/"+file) for file in files]
    return image_clips

# Note! These two separate because otherwise crash happens


def fade_audio_clips(clips):
    """Add fade in and out to songs"""
    fadein = args.fadein
    fadeout = args.fadeout
    for i in range(1, len(clips)):
        clip = clips[i].fx(audio_fadein, fadein).fx(audio_fadeout, fadeout)
        clips[i] = clip


def crossfade_audio_clips(clips):
    """Add transition between songs. Note: This merges clips to one!"""
    crossfade = args.crossfade
    for i in range(1, len(clips)):
        clip = clips[i]
        clips[i] = clip.set_start(clips[i-1].end-crossfade)

    return CompositeAudioClip(clips)


def create_music_video(image, music):
    count = args.count
    os.makedirs(args.outputfolder, exist_ok=True)

    # Add fade-in-out to all clips first
    fade_audio_clips(music)

    for i in range(count):
        if not args.randomimages and i >= count:
            break
        # shallow copy of the music clips
        music_shuffled = copy.copy(music)
        random.shuffle(music_shuffled)
        # Then crossfade them and combine them to one
        concat_music = crossfade_audio_clips(music_shuffled)
        # concat_music = concatenate_audioclips(music_shuffled)

        temp_image = random.choice(image) if args.randomimages else image[i]
        video = temp_image.set_audio(concat_music)
        video = video.set_duration(concat_music.duration)

        # Save playlist info as text
        if args.metafile:
            save_playlist_meta(music_shuffled, i)

        # Create video
        filepath = "{}/{}{}.mp4".format(args.outputfolder, args.outputprefix, str(i))
        temp_audio_file = args.outputfolder + "/" + args.outputprefix + str(i) + ".mp3"
        video.write_videofile(filepath, fps=30, remove_temp=(not args.saveaudio), temp_audiofile=temp_audio_file)


def save_playlist_meta(music_clips, video_id):
    filepath = "{}/{}{}.txt".format(args.outputfolder, args.outputprefix, str(video_id))
    # Take fading in account
    crossfade = args.crossfade
    with open(filepath, "w") as f:
        total_time = 0
        for i in range(len(music_clips)):
            clip = music_clips[i]

            # time
            rounded_time = round(clip.duration)

            start_time = datetime.timedelta(seconds=total_time)
            total_time += rounded_time - crossfade
            end_time = datetime.timedelta(seconds=total_time)
            duration = datetime.timedelta(seconds=rounded_time)

            # name
            start_i = clip.filename.find("/")+1
            end_i = clip.filename.rfind(".")
            clip_name = clip.filename[start_i:end_i]

            line = "{} {} {}-{}".format(clip_name, str(duration), start_time, end_time)
            f.write(line+"\n")
        print("Wrote", filepath)


def main():
    images = load_images(args.imagefolder)
    music = load_music(args.musicfolder)
    create_music_video(images, music)
    print("Done!")


if __name__ == "__main__":
    print(args)
    main()

