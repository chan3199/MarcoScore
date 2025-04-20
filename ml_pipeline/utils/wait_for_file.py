import time
import os

def wait_for_file(filepath, timeout=10):
    print(f"⏳ Waiting for {filepath} to be created...")
    for _ in range(timeout * 10):  # check every 0.1s
        if os.path.exists(filepath):
            print(f"✅ Found file: {filepath}")
            return True
        time.sleep(0.1)
    raise TimeoutError(f"Timeout waiting for {filepath}")
