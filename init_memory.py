import os
from instagrapi import Client
from dotenv import load_dotenv

# Configuration
SESSION_FILE = "session.json"
GREETED_THREADS_FILE = "greeted_threads.txt"

def save_id(filename, new_id):
    """Append a new ID to the file."""
    with open(filename, "a") as f:
        f.write(f"{new_id}\n")

def main():
    load_dotenv()
    
    print("🚀 Initializing Bot Memory...")
    print("   This script will mark ALL your recent groups as 'greeted'.")
    print("   This prevents the bot from spamming 'hi' to groups you are already in.\n")

    if not os.path.exists(SESSION_FILE):
        print(f"❌ Session file '{SESSION_FILE}' not found. Please run 'login.py' first.")
        return

    cl = Client()
    try:
        print(f"📂 Loading session from {SESSION_FILE}...")
        cl.load_settings(SESSION_FILE)
        cl.login_by_sessionid(cl.sessionid)
    except Exception as e:
        print(f"❌ Login failed: {e}")
        return

    # Load existing greeted threads to avoid duplicates
    existing_ids = set()
    if os.path.exists(GREETED_THREADS_FILE):
        with open(GREETED_THREADS_FILE, "r") as f:
            existing_ids = set(line.strip() for line in f if line.strip())

    print("🔍 Fetching recent threads...")
    # Fetch a large number of threads to be safe (e.g., last 50)
    threads = cl.direct_threads(amount=50)
    
    count = 0
    for thread in threads:
        is_group = thread.thread_type == 'group' or len(thread.users) > 1
        
        if is_group and str(thread.pk) not in existing_ids:
            save_id(GREETED_THREADS_FILE, thread.pk)
            existing_ids.add(str(thread.pk))
            count += 1
            print(f"   📌 Marked as seen: {thread.thread_title} (ID: {thread.pk})")

    print(f"\n✅ Done! Added {count} groups to memory.")
    print("   You can now run 'python main.py' safely without spamming these groups.")

if __name__ == "__main__":
    main()
