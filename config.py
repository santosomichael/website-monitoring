import os
import sys
from dotenv import load_dotenv

# Load environment variables from a .env file
load_dotenv()

# --- ⚙️ Configuration ---
# All configuration is centralized here.
CONFIG = {
    'base_url': os.getenv('BASE_URL'),
    'username': os.getenv('LOGIN_USERNAME'),
    'password': os.getenv('LOGIN_PASSWORD'),
    'headless': os.getenv('HEADLESS', 'true').lower() == 'true',
    'telegram_chat_id': os.getenv('TELEGRAM_CHAT_ID'),
    'telegram_bot_token': os.getenv('TELEGRAM_BOT_TOKEN'),
    'screenshots_dir': './screenshots'
}
# -------------------------

def validate_config():
    """Checks if all required environment variables are loaded."""
    required_vars = ['base_url', 'username', 'password']
    missing_vars = [var for var in required_vars if not CONFIG[var]]
    
    if missing_vars:
        print("❌ ERROR: Missing required environment variables.", file=sys.stderr)
        print(f"Please define the following in your .env file: {', '.join(missing_vars)}", file=sys.stderr)
        return False
    return True
