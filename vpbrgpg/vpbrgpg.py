from moviepy.editor import *
import argparse
import os
import random
import copy
import numpy as np
import datetime

def parse_args():
    parser = argparse.ArgumentParser(description="Create music playlist")

    parser.add_argument("-musicfolder", metavar="folder", type=str, default="music")
    parser.add_argument("-imagefolder", metavar="folder", type=str, default="images")
    parser.add_argument("-outputfolder", metavar="folder", type=str, default="output")
    parser.add_argument("-outputprefix", metavar="prefix", type=str, default="out_")
    parser.add_argument("-count", metavar="N", type=int, default=1, help="How many playlist you want to create")
    parser.add_argument("-infofile", metavar="Bool", type=bool, default=True, help="Create playlist infofile")
    parser.add_argument("-randomimages", metavar="Bool", type=bool, default=True, help="Pick random images for videos.")
    parser.add_argument("-saveaudio", metavar="Bool", type=bool, default=False, help="Create audiofile also")

    args = parser.parse_args()
    return args
# Parse args
args = parse_args()

def load_music(folder):
    files = os.listdir(folder)
    music_clips = [AudioFileClip(folder+"/"+file) for file in files]
    return music_clips


def load_images(folder):
    files = os.listdir(folder)
    image_clips = [ImageClip(folder+"/"+file) for file in files]
    return image_clips


def create_music_video(image, music):
    count = args.count
    os.makedirs(args.outputfolder, exist_ok=True)

    for i in range(count):
        if not args.randomimages and i >= count:
            break
        # shallow copy of the music clips
        music_shuffled = copy.copy(music)
        random.shuffle(music_shuffled)

        concat_music = concatenate_audioclips(music_shuffled)
        #img_index = random.randint(0, len(image)-1) if args.randomimages else i
        temp_image = random.choice(image) if args.randomimages else image[i]
        video = temp_image.set_audio(concat_music)
        video = video.set_duration(concat_music.duration)
        # Save playlist info as text
        if args.infofile:
            save_playlist_info(music_shuffled, i)

        # Create video
        filepath = "{}/{}{}.mp4".format(args.outputfolder, args.outputprefix, str(i))
        temp_audio_file = args.outputfolder + "/" + args.outputprefix + str(i) + ".mp3"
        video.write_videofile(filepath, fps=30, remove_temp=(not args.saveaudio), temp_audiofile=temp_audio_file)


def save_playlist_info(music_clips, video_id):
    filepath = "{}/{}{}.txt".format(args.outputfolder, args.outputprefix, str(video_id))
    with open(filepath, "w") as f:
        total_time = 0
        for i in range(len(music_clips)):
            clip = music_clips[i]

            # time
            rounded_time = round(clip.duration)
            start_time = datetime.timedelta(seconds=total_time)
            end_time = datetime.timedelta(seconds=(total_time + rounded_time))
            duration = datetime.timedelta(seconds=rounded_time)
            total_time += rounded_time

            # name
            start_i = clip.filename.find("/")+1
            end_i = clip.filename.rfind(".")
            clip_name = clip.filename[start_i:end_i]
            print(clip_name)

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

