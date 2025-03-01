# instagram_bot.py

import time
import random
import os

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service

###############################################################################
# 1. HELPER FUNCTIONS
###############################################################################

def instagram_login(username, password, driver_path="chromedriver"):
    """
    Logs into Instagram using the provided username and password.
    Returns a Selenium webdriver object that’s logged in.
    """
    # 1. Create a new Chrome webdriver session
    service = Service(driver_path)
    driver = webdriver.Chrome(service=service)

    # 2. Go to Instagram login page
    driver.get("https://www.instagram.com/accounts/login/")
    time.sleep(3)  # Let the page load

    # 3. Locate login fields and enter credentials
    user_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.NAME, "username"))
    )
    pass_input = driver.find_element(By.NAME, "password")

    user_input.send_keys(username)
    pass_input.send_keys(password)
    pass_input.send_keys(Keys.ENTER)

    # 4. Wait for login to process (handle potential pop-ups)
    time.sleep(5)
    
    # Optional: Handle "Save Your Login Info?" or "Turn on Notifications" pop-ups
    try:
        not_now_buttons = WebDriverWait(driver, 5).until(
            EC.presence_of_all_elements_located((By.XPATH, "//button[contains(text(), 'Not Now')]"))
        )
        for btn in not_now_buttons:
            btn.click()
            time.sleep(2)
    except:
        pass

    print("[INFO] Logged in successfully.")
    return driver


def follow_user(driver, target_username):
    """
    Navigates to the target user's profile and clicks 'Follow' if not following already.
    """
    profile_url = f"https://www.instagram.com/{target_username}/"
    driver.get(profile_url)
    time.sleep(random.uniform(3, 5))

    try:
        follow_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[text()='Follow']"))
        )
        follow_button.click()
        time.sleep(random.uniform(2, 4))
        print(f"[INFO] Followed user: {target_username}")
    except:
        print(f"[WARN] Could not follow {target_username}. Possibly already following or button not found.")


def send_direct_message(driver, target_username, message_text):
    """
    Sends a direct message (DM) to the target user.
    Steps:
    1. Go to DMs page
    2. Click 'New Message'
    3. Search for user
    4. Send the message
    """
    # 1. Go to the DM inbox
    driver.get("https://www.instagram.com/direct/inbox/")
    time.sleep(random.uniform(4, 6))

    # 2. Click 'New Message' (paper-plane icon or a button)
    try:
        new_msg_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "svg[aria-label='New Message']"))
        )
        new_msg_button.click()
        time.sleep(random.uniform(2, 4))
    except:
        print("[WARN] Could not find 'New Message' button. UI might have changed.")
        return

    # 3. Search for the user
    try:
        search_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, "queryBox"))
        )
        search_input.send_keys(target_username)
        time.sleep(random.uniform(2, 3))

        # Select user from results
        user_result = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, f"//div[text()='{target_username}']"))
        )
        user_result.click()
        time.sleep(random.uniform(1, 2))

        # Click 'Next'
        next_button = driver.find_element(By.XPATH, "//div[text()='Next']")
        next_button.click()
        time.sleep(random.uniform(2, 3))
    except:
        print("[WARN] Could not search/select user. UI may differ.")
        return

    # 4. Type and send the message
    try:
        message_box = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//textarea"))
        )
        message_box.send_keys(message_text)
        time.sleep(random.uniform(1, 2))
        message_box.send_keys(Keys.ENTER)
        print(f"[INFO] Sent DM to '{target_username}'")
    except:
        print("[ERROR] Could not send DM. The message field or send mechanism changed.")


###############################################################################
# 2. MAIN SCRIPT ENTRY
###############################################################################

if __name__ == "__main__":
    # Retrieve credentials (could be stored in environment vars for safety)
    IG_USERNAME = "09645030965"
    IG_PASSWORD = "Stream7756*"

    # Path to your chromedriver, if not in PATH
    CHROME_DRIVER_PATH = "chromedriver.exe"

    # 1. Login
    driver = instagram_login(IG_USERNAME, IG_PASSWORD, driver_path=CHROME_DRIVER_PATH)

    # 2. Follow a user
    user_to_follow = "luis.scrd"
    follow_user(driver, user_to_follow)

    # 3. Send a DM
    message_text = "Hello, this is an automated test message!"
    send_direct_message(driver, user_to_follow, message_text)

    # 4. Let the script pause so you can see results, then quit
    time.sleep(10)
    driver.quit()
    print("[INFO] Done.")
