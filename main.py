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
    def list_objects(self, bucket_name, dir=""):

        # Unsigned Connection
        response = self.s3.list_objects_v2(Bucket=bucket_name, Prefix=dir)

        if not dir:
            print(f"Listing objects from: {bucket_name}\n")

        if 'Contents' in response:
            for obj in response['Contents']:
                time = obj.get('LastModified').strftime('%Y-%m-%d %H:%M:%S')
                size = str(obj.get('Size'))
                archive = obj.get('Key')
                next_dir = archive if archive.endswith("/") else None
                
                if args.output:
                    self.download(archive)

                if not dir:
                    print(f"{time} | {str(size).rjust(10)} | {archive}")

                # Enter in a directory
                if next_dir:
                    self.list_objects(bucket_name, dir+next_dir)

    def download(self, file, dir=""):
        os.makedirs(f"results/{self.bucket_name}", exist_ok=True)
        data = file.rsplit('/', 1)

        if len(data) > 1:
            dir = f"results/{self.bucket_name}/{data[0]}"
            os.makedirs(dir, exist_ok=True)

        if "" not in data: 
            self.s3.download_file(self.bucket_name, file, f"results/{self.bucket_name}/{file}")
    
def main():
    print(banner())
    aws = aws_commands(args.url)
    aws.list_objects(args.url)

try:
    main()
except KeyboardInterrupt:
    exit()
