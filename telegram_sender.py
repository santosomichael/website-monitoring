import requests
from config import CONFIG # Import the configuration dictionary

def send_telegram_message(message: str):
    """
    Sends a message to a single Telegram chat ID using the bot token.
    Reads configuration from the central CONFIG dictionary.

    Args:
        message (str): The message text to send.
    
    Returns:
        bool: True if the message was sent successfully, False otherwise.
    """
    bot_token = CONFIG.get('telegram_bot_token')
    chat_id = CONFIG.get('telegram_chat_id')

    # --- Pre-flight Checks ---
    if not bot_token:
        print("Error: 'telegram_bot_token' not found in config.")
        return False
    if not chat_id:
        print("Error: 'telegram_chat_id' not found in config.")
        return False
    # -------------------------

    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    
    payload = {
        'chat_id': chat_id,
        'text': message,
        'parse_mode': 'Markdown'  # Or 'HTML'
    }

    try:
        response = requests.post(url, json=payload)
        response_data = response.json()

        if response.status_code == 200 and response_data.get('ok'):
            print(f"Telegram message sent successfully to chat ID {chat_id}.")
            return True
        else:
            print(f"Failed to send Telegram message to {chat_id}.")
            print(f"Response: {response_data}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"An error occurred while sending the Telegram message: {e}")
        return False
