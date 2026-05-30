import os

paths_to_check = [
    r"E:\Git\bin\git.exe",
    r"E:\Git\cmd\git.exe",
    r"E:\Program Files\Git\bin\git.exe",
    r"E:\Program Files\Git\cmd\git.exe",
    r"E:\Program Files (x86)\Git\bin\git.exe",
    r"E:\Program Files (x86)\Git\cmd\git.exe",
    r"D:\Program Files\Git\bin\git.exe",
    r"D:\Program Files\Git\cmd\git.exe",
    r"C:\Git\bin\git.exe",
    r"C:\Git\cmd\git.exe",
]

# Let's search E:\ for folders containing 'git'
e_root = "E:\\"
try:
    for entry in os.listdir(e_root):
        if "git" in entry.lower():
            full_path = os.path.join(e_root, entry)
            if os.path.isdir(full_path):
                # check bin/git.exe and cmd/git.exe
                paths_to_check.append(os.path.join(full_path, "bin", "git.exe"))
                paths_to_check.append(os.path.join(full_path, "cmd", "git.exe"))
except Exception as e:
    print(f"Error listing E:\\: {e}")

found = False
for path in paths_to_check:
    if os.path.exists(path):
        print(f"FOUND Git at: {path}")
        found = True
        break

if not found:
    print("Git was not found in deep locations.")
