import os

desktop = r"C:\Users\dee\OneDrive\바탕 화면"
print("--- Excel Files on Desktop ---")
for f in os.listdir(desktop):
    if f.endswith(".xlsx"):
        print(f"  {f} (size={os.path.getsize(os.path.join(desktop, f))} bytes)")
