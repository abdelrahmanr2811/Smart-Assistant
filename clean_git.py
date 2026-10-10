import subprocess
import shutil
import os

git = r".\mingit\cmd\git.exe"

# If previous commit has the 25MB setup binary in git history, let's delete .git and re-init cleanly
if os.path.exists(".git"):
    # Delete .git folder cleanly
    subprocess.run(["cmd.exe", "/c", "rmdir", "/s", "/q", ".git"], capture_output=True)

subprocess.run([git, "init"], check=True)
subprocess.run([git, "config", "user.name", "abdelrahmanr2811"], check=True)
subprocess.run([git, "config", "user.email", "abdelrahman@users.noreply.github.com"], check=True)
subprocess.run([git, "config", "http.postBuffer", "524288000"], check=True)
subprocess.run([git, "config", "http.lowSpeedLimit", "0"], check=True)
subprocess.run([git, "config", "http.lowSpeedTime", "999999"], check=True)

# Add all files (with .gitignore properly excluding setup/ and .exe)
subprocess.run([git, "add", "."], check=True)
subprocess.run([git, "commit", "-m", "Deploy Clean SPMA 2026 to Render"], check=True)
subprocess.run([git, "branch", "-M", "main"], check=True)
subprocess.run([git, "remote", "add", "origin", "https://github.com/abdelrahmanr2811/Smart-Assistant.git"], check=True)

print("CLEAN_GIT_INIT_SUCCESS")
