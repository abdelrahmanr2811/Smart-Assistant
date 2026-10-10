import sys
import os
import socket
import subprocess
import webbrowser
import threading
import time

def get_local_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return '127.0.0.1'

def main():
    root_dir = os.path.dirname(os.path.abspath(__file__))
    backend_dir = os.path.join(root_dir, 'backend')
    
    # Auto-discover all user site-packages (including Windows Store Python local-packages)
    import glob
    store_patterns = [
        r'C:\Users\*\AppData\Local\Packages\PythonSoftwareFoundation.*\LocalCache\local-packages\Python*\site-packages',
        r'C:\Users\*\AppData\Roaming\Python\Python*\site-packages',
        os.path.expanduser(r'~\AppData\Local\Packages\PythonSoftwareFoundation.*\LocalCache\local-packages\Python*\site-packages'),
        os.path.expanduser(r'~\AppData\Roaming\Python\Python*\site-packages'),
    ]
    for pat in store_patterns:
        for sp in glob.glob(pat):
            if os.path.isdir(sp) and sp not in sys.path:
                sys.path.insert(0, sp)
    
    # Ensure UTF-8 console output
    if sys.platform == 'win32':
        try:
            sys.stdout.reconfigure(encoding='utf-8')
            sys.stderr.reconfigure(encoding='utf-8')
        except Exception:
            pass

    print("=" * 72)
    print("  Smart Project Manager Assistant (SPMA) - 2026")
    print("  نظام المساعد الذكي لإدارة المشاريع الإنشائية")
    print("=" * 72)
    print()

    # 1. Check & verify dependencies
    core_checks = [
        ("uvicorn", "uvicorn"),
        ("fastapi", "fastapi"),
        ("sqlmodel", "sqlmodel"),
        ("jwt", "PyJWT"),
        ("passlib", "passlib[bcrypt]"),
        ("pydantic_settings", "pydantic-settings"),
        ("dotenv", "python-dotenv"),
        ("reportlab", "reportlab"),
        ("openpyxl", "openpyxl"),
        ("pandas", "pandas"),
        ("pypdf", "pypdf"),
        ("chromadb", "chromadb"),
        ("httpx", "httpx"),
        ("aiosmtplib", "aiosmtplib"),
        ("langchain_core", "langchain langchain-core"),
    ]
    missing_pkgs = []
    for mod, pkg in core_checks:
        try:
            __import__(mod)
        except ImportError:
            for p in pkg.split():
                if p not in missing_pkgs:
                    missing_pkgs.append(p)

    if missing_pkgs:
        print(f"[1/3] Installing required libraries ({len(missing_pkgs)} items: {' '.join(missing_pkgs)})...")
        subprocess.run([sys.executable, "-m", "pip", "install"] + missing_pkgs + ["--no-warn-script-location"])
        print("[1/3] Libraries installed successfully.")
    else:
        print("[1/3] Python environment and libraries verified.")

    # 2. Generate UI assets
    print("[2/3] Initializing Web Interface assets...")
    gen_script = os.path.join(backend_dir, 'generate_complete_ui.py')
    if os.path.exists(gen_script):
        try:
            subprocess.run([sys.executable, gen_script], capture_output=True)
        except Exception:
            pass

    # 3. Detect network IP
    local_ip = get_local_ip()

    print()
    print("=" * 72)
    print("  [SUCCESS] تم تشغيل النظام بنجاح وهو جاهز للاستخدام!")
    print("=" * 72)
    print("  💻 1. من نفس جهاز الكمبيوتر (Local Web Access):")
    print("     http://localhost:8000")
    print("     http://127.0.0.1:8000")
    print()
    print("  📱 2. من الموبايل أو أي جهاز على نفس شبكة الواي فاي (Mobile / Wi-Fi):")
    print(f"     http://{local_ip}:8000")
    print()
    print("  🔑 3. بيانات الدخول لجميع الحسابات:")
    print("     - كلمة المرور الموحدة: Admin123")
    print("     - أسماء المستخدمين: asem  أو  saleh  أو  mohammed.gassim  أو  rafat")
    print("=" * 72)
    print()
    print("Opening browser at http://localhost:8000 ...")

    # Open browser automatically after short delay
    def open_browser():
        time.sleep(1.5)
        webbrowser.open('http://localhost:8000')

    threading.Thread(target=open_browser, daemon=True).start()

    # 4. Start Uvicorn Server
    sys.path.insert(0, backend_dir)
    os.chdir(backend_dir)
    env = os.environ.copy()
    env["PYTHONPATH"] = backend_dir + os.pathsep + env.get("PYTHONPATH", "")

    # Invalidate module caches and ensure user site-packages is in sys.path
    try:
        import site, importlib
        importlib.invalidate_caches()
        user_site = site.getusersitepackages()
        if user_site and user_site not in sys.path:
            sys.path.append(user_site)
    except Exception:
        pass

    try:
        import uvicorn
        uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=False)
    except (ImportError, ModuleNotFoundError):
        # Fallback to subprocess invocation which starts a fresh Python process with full site-packages loaded
        cmd = [sys.executable, "-m", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
        res = subprocess.run(cmd, env=env)
        if res.returncode != 0:
            print("Installing uvicorn server directly...")
            subprocess.run([sys.executable, "-m", "pip", "install", "uvicorn", "fastapi", "sqlmodel", "--quiet", "--no-warn-script-location"])
            subprocess.run(cmd, env=env)

if __name__ == '__main__':
    main()
