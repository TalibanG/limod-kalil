# -*- coding: utf-8 -*-
"""לימוד קליל — אפליקציית חלון. מריץ את השרת ברקע ופותח חלון תוכנה."""
import os
import socket
import sys
import threading
import time
import traceback

import webview

from app import app, DATA_DIR

PORT = 8765
LOCK_PORT = 8764
LOG_PATH = os.path.join(DATA_DIR, "error.log")
_lock_sock = None  # held for process lifetime to enforce single instance


def acquire_single_instance():
    """Bind a lock port. If it's taken, another instance is already running."""
    global _lock_sock
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.bind(("127.0.0.1", LOCK_PORT))
        s.listen(1)
        _lock_sock = s  # keep a reference so it stays bound
        return True
    except OSError:
        s.close()
        return False


def log(msg):
    """Append a timestamped line to the error log (so crashes aren't silent)."""
    try:
        with open(LOG_PATH, "a", encoding="utf-8") as f:
            f.write(time.strftime("[%Y-%m-%d %H:%M:%S] ") + msg + "\n")
    except Exception:
        pass


def excepthook(exc_type, exc, tb):
    log("UNCAUGHT:\n" + "".join(traceback.format_exception(exc_type, exc, tb)))


sys.excepthook = excepthook


def port_open():
    s = socket.socket()
    s.settimeout(0.3)
    try:
        s.connect(("127.0.0.1", PORT))
        return True
    except OSError:
        return False
    finally:
        s.close()


def run_server():
    try:
        # use_reloader=False is implied by debug=False; threaded handles concurrency
        app.run(host="127.0.0.1", port=PORT, debug=False, threaded=True)
    except Exception:
        log("SERVER CRASH:\n" + traceback.format_exc())


def main():
    log("=== app starting ===")
    # single instance: if already running, don't open a duplicate window
    if not acquire_single_instance():
        log("another instance is already running — exiting")
        sys.exit(0)

    threading.Thread(target=run_server, daemon=True).start()
    for _ in range(80):
        if port_open():
            break
        time.sleep(0.1)
    else:
        log("server did not come up within 8s")

    try:
        webview.create_window(
            "לימוד קליל 🎓",
            f"http://127.0.0.1:{PORT}",
            width=1240, height=820,
            min_size=(940, 620),
            text_select=True,
        )
        # gui='edgechromium' is the Windows default; pass explicitly for stability
        webview.start()
        log("window closed normally")
    except Exception:
        log("WEBVIEW CRASH:\n" + traceback.format_exc())
        raise


if __name__ == "__main__":
    main()
