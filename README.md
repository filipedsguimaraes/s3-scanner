# S3 Scanner Script

S3-scanner is a script to perform **file listing** in **misconfigured** S3 buckets

<img width="894" height="451" alt="image" src="https://github.com/user-attachments/assets/d8f5b740-3821-40f0-a48b-8a592eaf955c" />

# How to use

### main.py ```-u```

```
usage: main.py [-h] -u URL [-o]

A simple tool that checks if an s3 aws is listable

options:
  -h, --help     show this help message and exit
  -u, --url URL  main.py -u bucketname
  -o, --output   Use -o to set output true

```
##### Simple usage
```bash
python3 main.py -u bucketname
```

##### Download all files
```bash
python3 main.py -u bucket_name -o
```
**This will download all files from s3 recursively and save them in a folder with the bucket name.**
