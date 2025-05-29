# Module for scraping the Petfess page, retrieving relevant submissions.
# Copyright (c) 2025 Ryan Jon Zhang

'''
Defines a class "Scraper" which opens a browser and allows for the scraping of the Petfess page.
Simply delete Scraper object to close the browser.
'''

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import random

class Scraper:
    
    FB_USERNAME = "whatdasigmer@gmail.com"
    FB_PASSWORD = "sigma123!"
    FB_LOGIN_URL = "https://www.facebook.com/login"
    FB_PETFESS_URL = "https://www.facebook.com/petfess"

    def __init__(self, open_GUI=False):
        self.open_GUI = open_GUI
        self.driver = webdriver.Chrome()
        self.logged_in = False

        # Configure visible Chrome window
        chrome_options = webdriver.ChromeOptions()
        if self.open_GUI:
            chrome_options.add_argument("--start-maximized") # Makes window visible
        else:
            chrome_options.add_argument("--headless=new") # Runs in headless mode
        self.driver = webdriver.Chrome(options=chrome_options)

    def __del__(self):
        self.driver.quit()

    class Post: # Inner class for storing post data
        def __init__(self, id = None, text_contents = None):
            self.id = id
            self.text_contents = text_contents

        def __str__(self):
            return f"Post ID: #Petfess{self.id}\nText Contents: {self.text_contents}"

    # Source: AbdelRhman_Sabry @ Medium.com
    def simulate_human_typing(self, element, text):
        '''
        Auxillary functino to simulate human-like typing patterns
        '''
        for char in text:
            element.send_keys(char)
            time.sleep(random.uniform(0.1, 0.3))
            if random.random() < 0.1:
                time.sleep(random.uniform(0.3, 0.7))

    def login(self):
        '''
        Logs into FaceBook and brings you to the required page (PetFess).
        '''

        print("Logging in to Facebook...")

        try:
            self.driver.get(Scraper.FB_LOGIN_URL)
        except Exception as e:
            print(f"Exception occurred while navigating to Facebook URL: {e}")
            return

        # Get past cookies page
        try:
            print("Waiting for 'Allow all cookies' button...")
            # Wait for any element containing the text "Allow all cookies" to appear and click it using JavaScript
            WebDriverWait(self.driver, 10).until(
                lambda d: "allow all cookies" in d.page_source.lower()
            )
            print("Detected 'Allow all cookies' text on the page.")
            time.sleep(2)
            # Try to click the element containing the text
            elements = self.driver.find_elements(By.XPATH, "//*[normalize-space(translate(., 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'))='allow all cookies']")
            if elements:
                for el in elements:
                    self.driver.execute_script("arguments[0].scrollIntoView();", el)
                    time.sleep(1)
                    try:
                        el.click()
                    except Exception:
                        try:
                            self.driver.execute_script("arguments[0].click();", el)
                        except Exception:
                            pass
            else:
                print("Could not find element to click for 'Allow all cookies'. Maybe cookies already accepted?")
        except Exception as e:
            print("(Probably) Successfully accepted cookies.")

        # Log in 
        # Source: AbdelRhman_Sabry @ Medium.com

        try:
            # Enter email
            email_input = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.NAME, "email"))
            )
            self.simulate_human_typing(email_input, Scraper.FB_USERNAME)

            # Enter password
            password_input = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.NAME, "pass"))
            )
            self.simulate_human_typing(password_input, Scraper.FB_PASSWORD)

            # Click login button
            login_button = self.driver.find_element(By.XPATH, "//button[@type='submit']")
            login_button.click()
            print("Clicked login button")
            
            time.sleep(7)

            print("Login complete.")

            self.logged_in = True

        except Exception as e:
            print(f"Exception occurred during login attempt: {e}")
            self.logged_in = False
            return

    def get_latest_post(self):
        '''
        Retrieves the latest post from the Petfess page. Returns a Post object.
        '''
        
        print("** Retrieving latest post from Petfess FaceBook page... **")

        # Check if logged in; if not, log in.
        if not self.logged_in:
            self.login()    

        # Navigate to the right page
        self.driver.get(Scraper.FB_PETFESS_URL)
        
        # Look for the first instance of "#Petfess", and then copy that entire post

        # Wait for posts to load
        try:
            # Wait for the main feed to load (arbitrary wait for posts to appear)
            WebDriverWait(self.driver, 15).until(
                EC.presence_of_element_located((By.XPATH, "//*[contains(text(), '#Petfess')]"))
            )
        except Exception as e:
            print(f"Could not find any post containing #Petfess: {e}")
            return None

        # Find all elements containing "#Petfess"
        posts = self.driver.find_elements(By.XPATH, "//*[contains(text(), '#Petfess')]")
        if not posts:
            print("No posts containing #Petfess found.")
            return None

        # For the first such post, try to extract the full post text
        post_element = posts[0]

        # Try to get the full post container (may need to go up the DOM tree)
        # Facebook post structure is complex; try to get the ancestor with role="article"
        try:
            ancestor = post_element
            for _ in range(6):  # Go up a few levels to find the article
                ancestor = ancestor.find_element(By.XPATH, "./..")
                if ancestor.get_attribute("role") == "article":
                    break
            else:
                ancestor = post_element  # fallback to original if not found

            # Try to expand "See more" if present
            try:
                see_more = ancestor.find_element(By.XPATH, ".//div[contains(@role, 'button') and (contains(text(), 'See more') or contains(text(), 'See More'))]")
                self.driver.execute_script("arguments[0].click();", see_more)
                time.sleep(1)
            except Exception:
                pass  # No "See more" button

            # Now, get all text content in the post
            post_text = ancestor.text
        except Exception as e:
            print(f"Could not extract full post text: {e}")
            post_text = post_element.text

        print("Latest #Petfess post:")
        print(post_text)
        return post_text

        time.sleep(20)

        
        
            



        
    
    
