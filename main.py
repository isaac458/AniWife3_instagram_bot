import os
import time
import random
import requests
from instagrapi import Client
from dotenv import load_dotenv

# Configuration
SESSION_FILE = "session.json"
GREETED_THREADS_FILE = "greeted_threads.txt"
REPLIED_MESSAGES_FILE = "replied_messages.txt"
POLL_INTERVAL = 5  # Seconds between checks (Faster)
WELCOME_MESSAGE = "hi Im AniWife"

def load_ids(filename):
    """Load a set of IDs from a file."""
    if not os.path.exists(filename):
        return set()
    with open(filename, "r") as f:
        return set(line.strip() for line in f if line.strip())

def save_id(filename, new_id):
    """Append a new ID to the file."""
    with open(filename, "a") as f:
        f.write(f"{new_id}\n")

def main():
    load_dotenv()
    
    # 1. Initialize Client
    cl = Client()
    # Speed up request delays (Risky but faster)
    cl.delay_range = [1, 3]

    # 2. Login Logic
    if not os.path.exists(SESSION_FILE):
        print(f"❌ Session file '{SESSION_FILE}' not found. Please run 'login.py' first.")
        return

    print(f"📂 Loading session from {SESSION_FILE}...")
    try:
        cl.load_settings(SESSION_FILE)
        cl.login_by_sessionid(cl.sessionid)
        
        my_info = cl.account_info()
        my_pk = str(my_info.pk)
        print(f"✅ Logged in as: {my_info.username} (ID: {my_pk})")
    except Exception as e:
        print(f"❌ Login failed: {e}")
        print("Try running 'login.py' again.")
        return

    # 3. Load state
    greeted_threads = load_ids(GREETED_THREADS_FILE)
    replied_messages = load_ids(REPLIED_MESSAGES_FILE)
    print(f"ℹ️  Loaded {len(greeted_threads)} greeted threads.")
    print(f"ℹ️  Loaded {len(replied_messages)} replied messages.")

    print("\n🚀 Bot is now running!")
    print("   - Auto-Welcomes new groups.")
    print("   - Replies to '!ani' with 'Hi (Username)'.")
    print("   (Press Ctrl+C to stop)")

    # 4. Polling Loop
    while True:
        try:
            print(f"\n🔍 Check at {time.strftime('%H:%M:%S')}...")
            
            # Fetch recent threads
            threads = cl.direct_threads(amount=20)
            
            for thread in threads:
                # -----------------------------------------------
                # FEATURE 1: Reply to '!ani' command
                # -----------------------------------------------
                # Fix: Some versions don't have 'last_permanent_item', use messages list instead
                last_msg = thread.messages[0] if thread.messages else None
                
                # Check if there is a last message and it's text
                if last_msg and last_msg.item_type == 'text':
                    msg_text = last_msg.text.strip()
                    lower_text = msg_text.lower()
                    
                    # ----------------------------------------------------
                    # COMMAND 1: !ani (Ping)
                    # ----------------------------------------------------
                    if lower_text == '!ani':
                        # Ensure we haven't replied to this exact message ID yet
                        if str(last_msg.id) not in replied_messages and str(last_msg.user_id) != my_pk:
                            sender_name = "User"
                            for user in thread.users:
                                if str(user.pk) == str(last_msg.user_id):
                                    sender_name = user.username
                                    break
                            
                            print(f"🤖 Ping '!ani' from @{sender_name}")
                            cl.direct_send(f"Hi {sender_name}", thread_ids=[thread.pk])
                            
                            replied_messages.add(str(last_msg.id))
                            save_id(REPLIED_MESSAGES_FILE, last_msg.id)
                            time.sleep(random.randint(1, 3))

                    # ----------------------------------------------------
                    # COMMAND 2: !ani say <text> (Echo)
                    # ----------------------------------------------------
                    elif lower_text.startswith('!ani say '):
                        if str(last_msg.id) not in replied_messages and str(last_msg.user_id) != my_pk:
                            # Extract the message to say (preserve original case)
                            content_to_say = msg_text[9:].strip() # Remove '!ani say '
                            
                            if content_to_say:
                                print(f"🗣️ Echoing: {content_to_say}")
                                cl.direct_send(content_to_say, thread_ids=[thread.pk])
                                
                                replied_messages.add(str(last_msg.id))
                                save_id(REPLIED_MESSAGES_FILE, last_msg.id)
                                time.sleep(random.randint(1, 3))

                    # ----------------------------------------------------
                    # COMMAND 3: !ani help (List Features)
                    # ----------------------------------------------------
                    elif lower_text == '!ani help':
                        if str(last_msg.id) not in replied_messages and str(last_msg.user_id) != my_pk:
                            print(f"ℹ️ Sending help menu")
                            help_text = (
                                "🤖 **AniWife Commands**\n"
                                "1. `!ani` - I'll say hello back!\n"
                                "2. `!ani say <text>` - I'll repeat what you say.\n"
                                "3. `!ani joke` - I'll tell you a joke!\n"
                                "4. `!ani help` - Show this menu.\n"
                                "5. (Auto) I say hi to new groups!"
                            )
                            cl.direct_send(help_text, thread_ids=[thread.pk])
                            
                            replied_messages.add(str(last_msg.id))
                            save_id(REPLIED_MESSAGES_FILE, last_msg.id)
                            time.sleep(random.randint(1, 3))

                    # ----------------------------------------------------
                    # COMMAND 4: !ani joke (Fetch Joke)
                    # ----------------------------------------------------
                    elif lower_text == '!ani joke':
                        if str(last_msg.id) not in replied_messages and str(last_msg.user_id) != my_pk:
                            # Identify username
                            sender_name = "User"
                            for user in thread.users:
                                if str(user.pk) == str(last_msg.user_id):
                                    sender_name = user.username
                                    break

                            print(f"🃏 Fetching joke for @{sender_name}...")
                            
                            try:
                                response = requests.get("https://v2.jokeapi.dev/joke/Any?safe-mode", timeout=5)
                                if response.status_code == 200:
                                    joke_data = response.json()
                                    
                                    # Format Joke
                                    if joke_data['type'] == 'single':
                                        joke_text = f"😂 Here is a joke for @{sender_name}:\n\n{joke_data['joke']}"
                                    else:
                                        joke_text = f"😂 Here is a joke for @{sender_name}:\n\n{joke_data['setup']}\n...\n{joke_data['delivery']}"
                                    
                                    cl.direct_send(joke_text, thread_ids=[thread.pk])
                                    print("   ↪️ Joke sent.")
                                else:
                                    cl.direct_send("❌ Couldn't find a joke right now :(", thread_ids=[thread.pk])
                            
                            except Exception as e:
                                print(f"⚠️ Joke API failed: {e}")
                                cl.direct_send("⚠️ Error fetching joke.", thread_ids=[thread.pk])

                            replied_messages.add(str(last_msg.id))
                            save_id(REPLIED_MESSAGES_FILE, last_msg.id)
                            time.sleep(random.randint(1, 3))

                # -----------------------------------------------
                # FEATURE 2: Welcome New Groups
                # -----------------------------------------------
                is_group = thread.thread_type == 'group' or len(thread.users) > 1
                
                if str(thread.pk) not in greeted_threads and is_group:
                    print(f"🆕 Found NEW group: {thread.thread_title} (ID: {thread.pk})")
                    
                    print(f"   👋 Sending welcome: '{WELCOME_MESSAGE}'")
                    cl.direct_send(WELCOME_MESSAGE, thread_ids=[thread.pk])
                    
                    # Save state
                    greeted_threads.add(str(thread.pk))
                    save_id(GREETED_THREADS_FILE, thread.pk)
                    
                    time.sleep(random.randint(2, 5))
            
            # Wait for next poll
            time.sleep(POLL_INTERVAL)

        except KeyboardInterrupt:
            print("\n👋 Bot stopped by user.")
            break
        except Exception as e:
            print(f"⚠️ Error during polling: {e}")
            print("   Retrying in 60 seconds...")
            time.sleep(60)

if __name__ == "__main__":
    main()
