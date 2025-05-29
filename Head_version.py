from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import time

submission = "You can't convice me Jacks' isn't mid"

# Configure visible Chrome window
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--start-maximized")
driver = webdriver.Chrome(options=chrome_options)

try:

    print("🌐 Opening Petfess page...")
    driver.get("https://www.crush.ninja/en-us/pages/petfess/")
    
    # Wait for cookie popup to appear (up to 10 seconds)
    try:
        print("🍪 Handling cookie consent popup...")
        cookie_popup = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div[class*='cookie'], div[class*='consent']"))
        )
        
        # Scroll the popup into view if needed
        driver.execute_script("arguments[0].scrollIntoView();", cookie_popup)
        time.sleep(1)
        
        # Try to find and click the "Consent" button
        try:
            consent_button = cookie_popup.find_element(By.XPATH, 
                ".//button[contains(., 'Consent') or contains(., 'Accept') or contains(., 'Agree')]")
            consent_button.click()
            print("✅ Clicked consent button")
        except:
            # Fallback: Try to click the "Manage options" button first
            manage_button = cookie_popup.find_element(By.XPATH, 
                ".//button[contains(., 'Manage') or contains(., 'Options')]")
            manage_button.click()
            time.sleep(1)
            # Then try to find consent button again
            consent_button = driver.find_element(By.XPATH, 
                "//button[contains(., 'Consent') or contains(., 'Accept All')]")
            consent_button.click()
            print("✅ Clicked consent through manage options")
            
    except Exception as e:
        print(f"⚠️ Could not handle cookie popup: {e}")
        print("Attempting to proceed anyway...")
    
    # Now proceed with Petfess submission
    print("⌨️ Typing message...")
    textarea = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "id_text"))
    )
    textarea.send_keys(submission)
    
    print("✅ Text entered. Check the textarea in the browser.")
    input("Press Enter to continue to submission...")
    
    print("🔄 Waiting for submit button...")
    submit_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "submission-form-submit"))
    )
    
    # Highlight and click
    driver.execute_script("arguments[0].style.border='3px solid yellow';", submit_button)
    time.sleep(2)
    submit_button.click()
    print("🖱️ Submit button clicked!")
    
    # Wait for submission
    print("⏳ Waiting 5 seconds to observe...")
    time.sleep(5)
    
    if "petfess" not in driver.current_url.lower():
        print("🎉 Possible successful submission!")
    else:
        print("❌ Possible submission failure")
    
except Exception as e:
    print(f"🔥 Error: {e}")
    driver.save_screenshot('error.png')
    print("📸 Saved screenshot as error.png")
finally:
    input("Press Enter to close browser...")
    driver.quit()