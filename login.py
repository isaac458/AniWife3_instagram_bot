import os
from instagrapi import Client
from dotenv import load_dotenv

def login_with_sessionid():
    load_dotenv()
    session_file = os.getenv("SESSION_FILE", "session.json")

    print("=" * 60)
    print("🚀 INSTAGRAM SESSION LOGIN")
    print("=" * 60)
    
    print("\n--- HOW TO GET YOUR SESSION ID ---")
    print("1. Open Instagram.com on your PC browser (Chrome/Edge).")
    print("2. Log in to your Instagram account.")
    print("3. Right-click anywhere -> Inspect -> Application (tab).")
    print("4. On the left, click 'Cookies' -> https://www.instagram.com.")
    print("5. Find 'sessionid' in the list and copy the long Value.")
    print("----------------------------------")
    
    sessionid = input("\nPaste your 'sessionid' here: ").strip()
    
    if not sessionid:
        print("❌ Error: No session ID provided.")
        return

    cl = Client()
    
    try:
        print("\n📡 Validating Session ID...")
        cl.login_by_sessionid(sessionid)
        
        # Verify it works before saving
        print("🔍 Verifying session...")
        cl.account_info()
        
        cl.dump_settings(session_file)
        print(f"\n✅ Success! Session saved to: {session_file}")
        print("✨ You can now run 'python main.py' to start the bot!")
        
    except Exception as e:
        print(f"\n❌ Session ID login failed: {e}")
        print("Make sure you copied the ENTIRE sessionid value correctly.")

if __name__ == "__main__":
    login_with_sessionid()
