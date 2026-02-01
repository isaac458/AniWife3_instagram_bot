**AniWife3** is a Instagram GC Bot

A simple Instagram bot that auto-greets new group chats and replies to specific commands.

## Getting Started

### 1. Prerequisites
- Python 3.x installed.
- Valid Instagram account (preferably a secondary/bot account).

### 2. Installation

First Clone this repository:

```bash
git clone https://github.com/renfamilyguy/AniWife3_instagram_bot.git
```

Set up a virtual environment:
```bash
python -m venv myenv
```

Activate the virtual environment:
```bash
myenv\Scripts\activate
```

Install the necessary Python libraries:
```bash
pip install -r requirements.txt
```

### 3. Authentication (Important!)
Before running the bot, you must log in to save your session.
1.  Open `login.py` (or run it) and follow the instructions to get your **Session ID** from your browser (Inspect Element > Application > Cookies).
2.  Run the login script:
    ```bash
    python login.py
    ```
3.  Paste your session ID when prompted.
4.  This creates a `session.json` file. **Do not share this file.**

### 4. Setup Memory (Anti-Spam)
If you are already in many group chats, you should run this script **once** before starting the bot. It marks all your current groups as "seen" so the bot doesn't spam them with "hi".

```bash
python init_memory.py
```

### 5. Running the Bot
Start the bot using:
```bash
python main.py
```
The bot will now:
- Check for new messages every 5 seconds.
- Auto-reply to `!ani`.
- Auto-greet new groups.

**Send `!ani help` in chat to see bot available commands.**

## Notes & Safety
- **Rate Limits**: The bot is configured to be fast. If you see HTTP 429 or "Feedback Required" errors, stop the bot for a few hours.
- **Spam**: To reset the bot's memory (make it greet everyone again), delete `greeted_threads.txt`.
- **Existing Groups**: By default, if you start with a clean memory file, the bot will treat **ALL** your recent groups as "new" and greet them.

## Configuration
You can edit `main.py` to change:
- `POLL_INTERVAL`: How often to check for messages (default: 5s).
- `WELCOME_MESSAGE`: The text sent to new groups.
