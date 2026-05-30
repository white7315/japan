import os

paths = [
    r"C:\Program Files\Git",
    r"C:\Program Files (x86)\Git",
    r"E:\Git",
    r"E:\git",
]

for p in paths:
    print(f"Path '{p}' exists?", os.path.exists(p))
    if os.path.exists(p):
        try:
            print(f"Contents of {p}:", os.listdir(p))
        except Exception as e:
            print(f"Error listing {p}: {e}")
