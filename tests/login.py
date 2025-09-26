from playwright.sync_api import Page, expect

# Import the config from the parent directory
from config import CONFIG

def check_login_and_dashboard(global_var):
    """
    Checks the login process using specific locators and validates the dashboard.
    """
    print("  ➡️  Running Test: Login and Dashboard Validation")
    page = global_var['page']
    
    # 1. Go to the login page
    page.goto(f"{CONFIG['base_url']}/login")
    
    # 2. Fill in credentials using the specific locators you provided
    page.screenshot(path=global_var['get_path']('SUCCESS'), full_page=True)
    global_var['step'] += 1

    page.get_by_role("textbox", name="Phone Number").click()
    page.get_by_role("textbox", name="Phone Number").fill(CONFIG['username'])
    page.get_by_role("textbox", name="PIN").click()
    page.get_by_role("textbox", name="PIN").fill(CONFIG['password'])
    page.get_by_text("User").click()

    page.screenshot(path=global_var['get_path']('SUCCESS'), full_page=True)
    global_var['step'] += 1

    # 3. Click login and wait for the dashboard URL to load 
    with page.expect_navigation(url=f"{CONFIG['base_url']}/dashboard", wait_until='domcontentloaded'):
        page.get_by_role("button", name="Login").click()
    
    # 4. Validate the dashboard content
    expect(page.locator("h2")).to_contain_text("Dashboard", timeout=15000)
    print("  ✅  SUCCESS: Dashboard validation passed.")
