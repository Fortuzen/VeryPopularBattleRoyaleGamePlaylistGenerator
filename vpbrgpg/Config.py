import argparse


class Config:
    """Keep arguments in one, nice place"""
    def __init__(self, args):
        self.music_folder: str = args.musicfolder
        self.image_folder: str = args.imagefolder
        self.output_folder: str = args.outputfolder
        self.output_prefix: str = args.outputprefix

        self.playlist_count: int = args.count
        self.create_meta: bool = args.create_meta

        self.random_pick_images: bool = None
        self.save_audio: bool = None

        # Fading
        self.fade_in: float = args.fadein
        self.fade_out: float = args.fadeout
        self.crossfade: float = args.crossfade
        self.fade_first: bool = args.fadefirst


def parse_args():
    parser = argparse.ArgumentParser(description="Create music playlist")

    parser.add_argument("-musicfolder", metavar="folder", type=str, default="music")
    parser.add_argument("-imagefolder", metavar="folder", type=str, default="images")
    parser.add_argument("-outputfolder", metavar="folder", type=str, default="output")
    parser.add_argument("-outputprefix", metavar="prefix", type=str, default="out_")

    parser.add_argument("-count", metavar="n", type=int, default=1, help="How many playlist you want to create")

    parser.add_argument("-metafile", metavar="b", type=bool, default=True, help="Create playlist metafile")
    parser.add_argument("-randomimages", metavar="b", type=bool, default=True, help="Pick random images for videos.")
    parser.add_argument("-saveaudio", metavar="b", type=bool, default=False, help="Create audiofile also")

    parser.add_argument("-fadein", metavar="f", type=float, default=0.0, help="Add fade in. Seconds.")
    parser.add_argument("-fadeout", metavar="f", type=float, default=0.0, help="Add fade out. Seconds.")
    parser.add_argument("-crossfade", metavar="f", type=float, default=0.0, help="Add Crossfade between clips.")
    parser.add_argument("--fadefirst", type=bool, default=False, help="Fade in first song")

    args = parser.parse_args()
    return args
