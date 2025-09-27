import os
import sys
from datetime import datetime
from playwright.sync_api import sync_playwright

# Import the configuration and individual test functions
from config import CONFIG, validate_config
from tests.login import check_login_and_dashboard
from telegram_sender import send_telegram_message

def run_all_checks(playwright):
    """
    Main function to orchestrate all website checks.
    Initializes the browser and calls test functions sequentially.
    """
    # First, validate that the configuration is loaded and correct
    if not validate_config():
        sys.exit(1)

    screenshots_dir = CONFIG['screenshots_dir']
    if not os.path.exists(screenshots_dir):
        os.makedirs(screenshots_dir)

    browser = playwright.chromium.launch(headless=CONFIG['headless'])
    page = browser.new_page()
    timestamp = datetime.now().isoformat().replace(':', '-').replace('.', '-')

    global_var = {
        'page': page,
        'step': 1,
        'get_path': lambda status: os.path.join(screenshots_dir, f"step{global_var['step']}-{status}-{timestamp}.png"),
    }

    try:
        print(f"[{timestamp}] --- Starting all health checks...")
        
        # --- Run Test Suite ---
        # Each test function is now imported and called from here.
        # The same 'page' object is passed to each test, so the session is maintained.
        check_login_and_dashboard(global_var)
        # check_profile_page(page)
        # You can add more imported test functions here
        # --- End Test Suite ---
        
        # If all tests pass, take a final success screenshot of the last page
        page.screenshot(path=global_var['get_path']('SUCCESS'), full_page=True)
        global_var['step'] += 1
        signal_message = f"✅ All health checks passed successfully at {datetime.now().isoformat()}!"
        send_telegram_message(signal_message)
        
        print(f"\n✅ All checks passed successfully!")

    except Exception as e:
        signal_message = f"❌ ERROR: A test failed during the health check at {datetime.now().isoformat()}! Check the logs and screenshots."
        send_telegram_message(signal_message)
        print(f"\n❌ ERROR: A test failed during the health check!")
        print(e)
        page.screenshot(path=global_var['get_path']('ERROR'), full_page=True)
        print(f"📸 Screenshot of the failure page saved to {global_var['get_path']('ERROR')}")
        sys.exit(1)
        
    finally:
        browser.close()
        print(f"[{timestamp}] --- All health checks finished. ---\n")

if __name__ == "__main__":
    with sync_playwright() as playwright:
        run_all_checks(playwright)
