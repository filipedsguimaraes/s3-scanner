from botocore.config import Config
from botocore import UNSIGNED
import botocore
import argparse
import boto3
import os

parser = argparse.ArgumentParser(
                    prog = 'main.py',
                    description = 'A tool to list and download files from an s3',
                    epilog = 'Github: filipedsguimaraes')
parser.add_argument('-u', '--url', required=True, type=str, help="main.py -u flaws.cloud")
parser.add_argument('-o', '--output', required=False, action='store_true', help="Use -o to download all files")
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
        print(banner())
        self.bucket_name = url.replace("s3://", "").replace("/", "")
        self.s3 = boto3.client('s3', config=Config(signature_version=UNSIGNED))
            
    # List all objects from an bucket
    def list_objects(self, dir=""):
        # Unsigned Connection
        response = self.s3.list_objects_v2(Bucket=self.bucket_name, Prefix=dir)

        if not dir:
            print(f"Listing objects from: {self.bucket_name}\n")

        if 'Contents' in response:
            for obj in response['Contents']:
                time = str(obj.get('LastModified')).split("+")[0]
                size = str(obj.get('Size'))
                archive = obj.get('Key')
                next_dir = archive if archive.endswith("/") else None
                
                if args.output:
                    self.download(archive)

                if not dir:
                    print(time, size.rjust(10), obj.get('Key'))

                # Enter in a directory
                if next_dir:
                    self.list_objects(dir+next_dir)

    # Download all s3 files
    def download(self, file, dir=""):
        os.makedirs(f"results/{self.bucket_name}", exist_ok=True)
        data = file.rsplit('/', 1)

        if len(data) > 1:
            dir = f"results/{self.bucket_name}/{data[0]}"
            os.makedirs(dir, exist_ok=True)

        if "" not in data: 
            self.s3.download_file(self.bucket_name, file, f"results/{self.bucket_name}/{file}")


def main():
    aws = aws_commands(args.url)
    aws.list_objects()

try:
    main()
except botocore.exceptions.ClientError as error:
    _, msg, bucket_name = error.response["Error"].values()
    print(f"Bucket Name: {bucket_name}\nError: {msg}")
except KeyboardInterrupt:
    exit()