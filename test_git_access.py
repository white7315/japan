import os

paths_to_test = [
    r"E:\Git",
    r"E:\Git\cmd\git.exe",
    r"E:\Git\bin\git.exe",
]

print("--- Testing folder access directly ---")
for p in paths_to_test:
    print(f"\nTesting path: {p}")
    try:
        stat_info = os.stat(p)
        print("  Status: EXISTS (os.stat succeeded)")
        print(f"  Size: {stat_info.st_size} bytes")
    except Exception as e:
        print(f"  Exception: {type(e).__name__} - {e}")
