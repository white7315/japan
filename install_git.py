import os
import urllib.request

url = "https://github.com/git-for-windows/git/releases/download/v2.44.0.windows.1/Git-2.44.0-64-bit.exe"
dest = r"E:\japan\Git-2.44.0-64-bit.exe"

print("Downloading Git for Windows Installer from GitHub...")
try:
    urllib.request.urlretrieve(url, dest)
    print("Download completed successfully!")
    print(f"Installer saved at: {dest}")
except Exception as e:
    print(f"Error downloading: {e}")
    exit(1)
