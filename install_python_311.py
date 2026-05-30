import os
import urllib.request

url = "https://www.python.org/ftp/python/3.11.9/python-3.11.9-amd64.exe"
dest = r"E:\japan\python-3.11.9-amd64.exe"

print("Downloading Python 3.11.9 Windows Installer from python.org...")
try:
    urllib.request.urlretrieve(url, dest)
    print("Download completed successfully!")
    print(f"Installer saved at: {dest}")
except Exception as e:
    print(f"Error downloading: {e}")
    exit(1)
