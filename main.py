from botocore.config import Config
from botocore import UNSIGNED
import argparse
import boto3
import os

parser = argparse.ArgumentParser(
                    prog = 'main.py',
                    description = 'A simple tool that checks if an s3 aws is listable',
                    epilog = 'Github: filipedsguimaraes')
parser.add_argument('-u', '--url', required=True, type=str, help="main.py -u bucketname")
parser.add_argument('-o', '--output', required=False, action='store_true', help="Use -o to set output true")
args = parser.parse_args()

# ANSI COLORS
RESET = "\033[0m"
COLORS = {
    "red":     "\033[31m",
    "green":   "\033[32m",
    "yellow":  "\033[33m",
    "blue":    "\033[34m",
    "magenta": "\033[35m",
    "cyan":    "\033[36m",
}

# ls-like color mapping for file extensions

EXT_COLORS = {
    # compress
    ".tar.gz": COLORS["red"],
    ".tar.xz": COLORS["red"],
    ".tar.bz2":COLORS["red"],
    ".zip":    COLORS["red"],
    ".gz":     COLORS["red"],

    # images
    ".jpg": COLORS["magenta"],
    ".jpeg": COLORS["magenta"],
    ".png": COLORS["magenta"],
    ".gif": COLORS["magenta"],
    ".svg": COLORS["magenta"],

    # audio / video
    ".mp3": COLORS["cyan"],
    ".wav": COLORS["cyan"],
    ".mp4": COLORS["cyan"],
    ".mkv": COLORS["cyan"],

    # code ext
    ".py": COLORS["green"],
    ".sh": COLORS["green"],
    ".js": COLORS["yellow"],
    ".ts": COLORS["yellow"],
}

def banner():
    os.system("cls")
    return r"""
 ____ _____   ____                                  
/ ___|___ /  / ___|  ___ __ _ _ __  _ __   ___ _ __ 
\___ \ |_ \  \___ \ / __/ _` | '_ \| '_ \ / _ \ '__|
 ___) |__) |  ___) | (_| (_| | | | | | | |  __/ |   
|____/____/  |____/ \___\__,_|_| |_|_| |_|\___|_|   
    """

class aws_commands:
    def __init__(self, url):
        self.bucket_name = url
        self.s3 = boto3.client('s3', config=Config(signature_version=UNSIGNED))

    # List all objects from an bucket
    def list_objects(self, dir=""):

        # Unsigned Connection
        response = self.s3.list_objects_v2(Bucket=self.bucket_name, Prefix=dir)

        if not dir:
            print(f"Listing objects from: {self.bucket_name}\n")

        if 'Contents' in response:
            for obj in response['Contents']:
                time = obj.get('LastModified').strftime('%Y-%m-%d %H:%M:%S')
                size = str(obj.get('Size'))
                archive = obj.get('Key')
                next_dir = archive if archive.endswith("/") else None
                
                if args.output:
                    self.download(archive)

                if not dir:
                    print(f"{time} | {str(size).rjust(10)} | {colorized_extension(archive)}")

                # Enter in a directory
                if next_dir:
                    self.list_objects(dir+next_dir)

    def download(self, file, dir=""):
        os.makedirs(f"results/{self.bucket_name}", exist_ok=True)
        data = file.rsplit('/', 1)

        if len(data) > 1:
            dir = f"results/{self.bucket_name}/{data[0]}"
            os.makedirs(dir, exist_ok=True)

        if "" not in data: 
            self.s3.download_file(self.bucket_name, file, f"results/{self.bucket_name}/{file}")

# colorize filename by extension
def colorized_extension(name):
    lname = name.lower()

    # prioritize compound extensions
    for ext in sorted(EXT_COLORS, key=len, reverse=True):
        if lname.endswith(ext):
            return f"{EXT_COLORS[ext]}{name}{RESET}"

    # no matches
    return name

def main():
    print(banner())
    aws = aws_commands(args.url)
    aws.list_objects()

try:
    main()
except KeyboardInterrupt:
    exit()
