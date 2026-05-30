import os

search_paths = [
    r"C:\Program Files\Git\bin\git.exe",
    r"C:\Program Files\Git\cmd\git.exe",
    r"C:\Program Files (x86)\Git\bin\git.exe",
    r"C:\Program Files (x86)\Git\cmd\git.exe",
    os.path.join(os.environ.get("LOCALAPPDATA", ""), r"Programs\Git\bin\git.exe"),
    os.path.join(os.environ.get("LOCALAPPDATA", ""), r"Programs\Git\cmd\git.exe"),
    os.path.join(os.environ.get("USERPROFILE", ""), r"AppData\Local\Programs\Git\bin\git.exe"),
]

found = False
print("--- Searching for git.exe in common paths ---")
for path in search_paths:
    if os.path.exists(path):
        print(f"FOUND Git at: {path}")
        found = True
        break

if not found:
    print("Git was not found in common default locations.")
