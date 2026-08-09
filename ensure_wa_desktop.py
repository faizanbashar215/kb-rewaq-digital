#!/usr/bin/env python3
# Ensures the KB Rewaq WhatsApp Desktop automation stays running (single instance).
# Called by cron every 5 min. The actual script needs Python 3.12 (pywin32 registered),
# so we spawn it with that interpreter; this launcher itself only needs stdlib.
import os, subprocess

HERE = os.path.dirname(os.path.abspath(__file__))
PID_FILE = os.path.join(HERE, "wa_desktop.pid")
PY = r"C:\Users\faiza\AppData\Local\Programs\Python\Python312\python.exe"
SCRIPT = os.path.join(HERE, "wa_desktop_automation.py")

def is_alive(pid):
    if not pid:
        return False
    try:
        out = subprocess.run(["tasklist"], capture_output=True, text=True, timeout=5).stdout
        return f" {pid}\r\n" in out or f" {pid}\n" in out
    except Exception:
        return False

def main():
    pid = None
    if os.path.exists(PID_FILE):
        try:
            pid = int(open(PID_FILE).read().strip())
        except Exception:
            pid = None
    if is_alive(pid):
        print(f"wa_desktop_automation already running (pid {pid})")
        return
    if os.path.exists(PID_FILE):
        os.remove(PID_FILE)
    p = subprocess.Popen([PY, SCRIPT], cwd=HERE,
                         creationflags=0x00000008)  # DETACHED_PROCESS
    open(PID_FILE, "w").write(str(p.pid))
    print(f"started wa_desktop_automation pid {p.pid}")

if __name__ == "__main__":
    main()
