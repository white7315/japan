import os
print("Does E:\\Git exist?", os.path.exists("E:\\Git"))
if os.path.exists("E:\\Git"):
    try:
        print("Contents of E:\\Git:", os.listdir("E:\\Git"))
    except Exception as e:
        print("Error listing E:\\Git:", e)
