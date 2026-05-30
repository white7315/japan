import os

print("--- Searching for git.exe everywhere ---")

# Let's search inside C:\Users\dee
user_dir = os.path.expanduser("~")
print(f"Searching in user directory: {user_dir}")
found_paths = []

for root, dirs, files in os.walk(user_dir):
    # Skip some big directories to make it fast
    if any(p in root for p in ["AppData\\Local\\Microsoft", "AppData\\Local\\Google", "AppData\\Local\\Packages"]):
        continue
    if "git.exe" in files:
        full_path = os.path.join(root, "git.exe")
        print(f"FOUND: {full_path}")
        found_paths.append(full_path)
        break

# Let's search inside E:\
print("Searching on E:\\ drive...")
e_root = "E:\\"
try:
    for entry in os.listdir(e_root):
        full_path = os.path.join(e_root, entry)
        if os.path.isdir(full_path):
            if "git" in entry.lower():
                print(f"Checking E:\\{entry}...")
            # Walk one level deep or fully if not too large
            for r, ds, fs in os.walk(full_path):
                if "git.exe" in fs:
                    git_path = os.path.join(r, "git.exe")
                    print(f"FOUND: {git_path}")
                    found_paths.append(git_path)
                    break
except Exception as e:
    print(f"Error searching E:\\: {e}")

if not found_paths:
    print("Could not locate git.exe anywhere on C:\\Users\\dee or E:\\ drive.")
else:
    print("Search completed. Found:", found_paths)
