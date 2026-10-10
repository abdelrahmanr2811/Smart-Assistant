import os
import sys
import subprocess
import re
import time

def find_ssh():
    # 1. Check PATH
    try:
        res = subprocess.run(["where", "ssh"], capture_output=True, text=True)
        if res.returncode == 0:
            lines = res.stdout.strip().splitlines()
            if lines:
                return lines[0].strip()
    except Exception:
        pass
    
    # 2. Check standard Windows OpenSSH directory
    win_ssh = os.path.expandvars(r"%SystemRoot%\System32\OpenSSH\ssh.exe")
    if os.path.exists(win_ssh):
        return win_ssh
        
    return "ssh"

def copy_to_clipboard(text):
    try:
        p = subprocess.Popen("clip", stdin=subprocess.PIPE, shell=True)
        p.communicate(text.encode("utf-8"))
    except Exception:
        pass

def main():
    print("=" * 72)
    print("  Smart Project Manager Assistant (SPMA) - Public Link Generator")
    print("=" * 72)
    print()
    print("  Generating secure public HTTPS link for remote evaluators...")
    print("  (Please wait a moment while connecting to the secure tunnel...)")
    print()

    ssh_bin = find_ssh()
    
    # Run SSH reverse tunnel to serveo.net
    cmd = [
        ssh_bin,
        "-o", "StrictHostKeyChecking=no",
        "-o", "UserKnownHostsFile=NUL",
        "-R", "80:localhost:8000",
        "serveo.net"
    ]
    
    try:
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, bufsize=1)
    except Exception as e:
        print(f"Error starting tunnel: {e}")
        input("\nPress Enter to exit...")
        return

    url_found = False
    for line in iter(p.stdout.readline, ""):
        if "https://" in line:
            match = re.search(r"https://[^\s]+", line)
            if match:
                url = match.group(0).rstrip(".")
                copy_to_clipboard(url)
                print()
                print("=" * 72)
                print(f"  your url is: {url}")
                print("=" * 72)
                print()
                print("  [OK] تم نسخ الرابط تلقائياً إلى الحافظة (Clipboard)!")
                print("  يمكنك الآن الضغط على (Ctrl + V) لإرساله للدكتور عبر الواتساب أو المتصفح.")
                print("  ملاحظة: اترك هذه الشاشة مفتوحة طوال فترة استخدام الرابط.")
                print("=" * 72)
                print()
                url_found = True
                break

    if not url_found:
        print("Could not retrieve tunnel URL automatically.")
    
    try:
        p.wait()
    except KeyboardInterrupt:
        p.terminate()

if __name__ == "__main__":
    main()
