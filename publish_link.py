import os
import sys
import subprocess
import re
import time

def copy_to_clipboard(text):
    try:
        p = subprocess.Popen("clip", stdin=subprocess.PIPE, shell=True)
        p.communicate(text.encode("utf-8"))
    except Exception:
        pass

def find_ssh():
    try:
        res = subprocess.run(["where", "ssh"], capture_output=True, text=True)
        if res.returncode == 0:
            lines = res.stdout.strip().splitlines()
            if lines:
                return lines[0].strip()
    except Exception:
        pass
    win_ssh = os.path.expandvars(r"%SystemRoot%\System32\OpenSSH\ssh.exe")
    if os.path.exists(win_ssh):
        return win_ssh
    return "ssh"

def try_cloudflared():
    cloudflared_bin = os.path.abspath("tools/cloudflared.exe")
    if not os.path.exists(cloudflared_bin):
        return False
    
    print("  Connecting via Cloudflare Secure High-Speed Tunnel...")
    print("  (100% Free - No Credit Card - No Ads - Direct HTTPS)")
    print()
    cmd = [cloudflared_bin, "tunnel", "--url", "http://localhost:8000"]
    try:
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, bufsize=1, encoding="utf-8", errors="replace")
    except Exception as e:
        print(f"  Cloudflare error: {e}")
        return False

    url_found = False
    for line in iter(p.stdout.readline, ""):
        match = re.search(r"https://[a-zA-Z0-9-]+\.trycloudflare\.com", line)
        if match:
            url = match.group(0)
            copy_to_clipboard(url)
            print("=" * 72)
            print("  SPMA 2026 - ONLINE PUBLIC HTTPS LINK:")
            print("=" * 72)
            print()
            print(f"  >>> {url} <<<")
            print()
            print("=" * 72)
            print("  [OK] تم نسخ الرابط تلقائياً إلى الحافظة (Clipboard)!")
            print("  يمكنك الآن لصقه (Ctrl + V) في متصفح الموبايل أو إرساله لأي شخص.")
            print("  بيانات الدخول: asem / Admin123")
            print("  (اترك هذه النافذة السوداء مفتوحة طوال فترة رغبتك بتشغيل الرابط)")
            print("=" * 72)
            print()
            url_found = True
            break
            
    if url_found:
        try:
            p.wait()
        except KeyboardInterrupt:
            p.terminate()
        return True
    return False

def try_serveo():
    ssh_bin = find_ssh()
    print("  Falling back to Serveo HTTPS Tunnel...")
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
        print(f"  Serveo error: {e}")
        return False

    url_found = False
    for line in iter(p.stdout.readline, ""):
        if "https://" in line:
            match = re.search(r"https://[^\s]+", line)
            if match:
                url = match.group(0).rstrip(".")
                copy_to_clipboard(url)
                print("=" * 72)
                print(f"  PUBLIC LINK: {url}")
                print("=" * 72)
                url_found = True
                break

    if url_found:
        try:
            p.wait()
        except KeyboardInterrupt:
            p.terminate()
        return True
    return False

def main():
    print("=" * 72)
    print("  Smart Project Manager Assistant (SPMA) - Public Link Generator")
    print("=" * 72)
    print()
    if not try_cloudflared():
        try_serveo()

if __name__ == "__main__":
    main()
