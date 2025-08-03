import subprocess
import time
import os

BASE_PATH = os.path.join("1 log in page", "3D Ai")

scripts = [
    os.path.join(BASE_PATH, "deep fake image detection", "app.py"),
    os.path.join(BASE_PATH, "fake news detecton", "server.py"),
    os.path.join(BASE_PATH, "health_care", "health.py"),
    os.path.join(BASE_PATH, "3d_ai", "ai_backend.py"),
    os.path.join(BASE_PATH, "talk ai", "talk.py")
]

processes = []
for script in scripts:                                                                                                                                                                                                                                          
    if os.path.exists(script):
        print(f"Starting {script}...")
        p = subprocess.Popen(["python", script])
        processes.append(p)
    else:
        print(f"[ERROR] Script not found: {script}")

time.sleep(5)

print("All backends started and login page opened!")
