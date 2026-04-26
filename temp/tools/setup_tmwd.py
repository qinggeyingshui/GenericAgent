import time
import requests
import json

def force_reconnect():
    print("--- Attempting to trigger extension via WebSocket reset ---")
    try:
        # 1. Start or confirm TMWebDriver server
        import subprocess
        # Use a non-blocking check
        res = requests.get('http://127.0.0.1:18765', timeout=1)
        print("Server is already running.")
    except:
        print("Server not responding, please ensure TMWebDriver.py is running.")
        return

    print("Step 1: Checking for active sessions...")
    try:
        r = requests.get('http://127.0.0.1:18766/link', json={"cmd": "get_all_sessions"}, timeout=2)
        sessions = r.json().get('r', {})
        if sessions:
            print(f"Active sessions found: {list(sessions.keys())}")
        else:
            print("No sessions found. Extension might not be connected to WS.")
    except:
        print("HTTP link (18766) not ready.")

    print("\nNext Action: If you see the browser, please REFRESH any page (F5) to re-trigger the extension's connection to 18765.")

if __name__ == "__main__":
    force_reconnect()