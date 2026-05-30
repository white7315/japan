import os
import shutil
import subprocess

desktop = r"C:\Users\dee\OneDrive\바탕 화면"
workspace = r"E:\japan"

may_src = os.path.join(desktop, "26년5월 매출일지.xlsx")
june_src = os.path.join(desktop, "26년6월 매출일지.xlsx")

may_dest = os.path.join(workspace, "26년5월 매출일지.xlsx")
june_dest = os.path.join(workspace, "26년6월 매출일지.xlsx")

print("--- Copying Excel Files from Desktop to Workspace ---")
try:
    if os.path.exists(may_src):
        shutil.copy2(may_src, may_dest)
        print("Successfully copied 26년5월 매출일지.xlsx")
    else:
        print("Warning: 26년5월 매출일지.xlsx not found on Desktop.")
        
    if os.path.exists(june_src):
        shutil.copy2(june_src, june_dest)
        print("Successfully copied 26년6월 매출일지.xlsx")
    else:
        print("Warning: 26년6월 매출일지.xlsx not found on Desktop.")
except Exception as e:
    print(f"Error copying files: {e}")
    exit(1)

print("\n--- Creating .gitignore file ---")
gitignore_path = os.path.join(workspace, ".gitignore")
gitignore_content = """Git-2.44.0-64-bit.exe
python-*-amd64.exe
*.pyc
__pycache__/
install.log
"""
try:
    with open(gitignore_path, "w", encoding="utf-8") as f:
        f.write(gitignore_content)
    print(".gitignore created successfully.")
except Exception as e:
    print(f"Error creating .gitignore: {e}")

print("\n--- Running Git commands ---")
git_exe = r"E:\Git\cmd\git.exe"

def run_git(args):
    cmd = [git_exe] + args
    print(f"Running: {' '.join(cmd)}")
    res = subprocess.run(cmd, cwd=workspace, capture_output=True, text=True)
    if res.returncode != 0:
        print(f"Error running git {' '.join(args)}:")
        print("STDOUT:", res.stdout)
        print("STDERR:", res.stderr)
        return False
    else:
        print("STDOUT:", res.stdout)
        return True

# Initialize git if not already (it has .git, but let's be safe)
if not os.path.exists(os.path.join(workspace, ".git")):
    run_git(["init"])

# Set remote origin
# Try removing old origin if any
run_git(["remote", "remove", "origin"])
run_git(["remote", "add", "origin", "https://github.com/white7315/japan.git"])

# Set branch name to main
run_git(["branch", "-M", "main"])

# Add files
run_git(["add", "."])

# Commit
# We use a standard commit message
run_git(["commit", "-m", "Initialize sales journals and workspace scripts"])

print("\nGit synchronization preparation complete!")
print("To push to GitHub and authenticate, we will run the push command.")
