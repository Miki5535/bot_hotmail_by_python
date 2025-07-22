from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import undetected_chromedriver as uc
import time
from selenium import webdriver
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import TimeoutException, WebDriverException, ElementNotInteractableException
import logging
import random
import traceback

# Setup logging in English without emojis
logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] %(message)s')
logger = logging.getLogger(__name__)

class HotmailSignup:
    def __init__(self, max_retries=3, debug=True):
        self.max_retries = max_retries
        self.debug = debug
        self.driver = None
        self.wait = None

    def debug_log(self, message, level="INFO"):
        """Debug logging function"""
        if self.debug:
            if level == "ERROR":
                logger.error(message)
            elif level == "WARNING":
                logger.warning(message)
            elif level == "SUCCESS":
                logger.info(f"{message}")
            else:
                logger.info(message)

    def random_delay(self, min_delay=1, max_delay=3):
        """Create random delay to avoid detection"""
        delay = random.uniform(min_delay, max_delay)
        time.sleep(delay)
        return delay

    def setup_driver(self):
        """Setup Chrome driver"""
        try:
            self.debug_log("Setting up Chrome driver...")
            options = uc.ChromeOptions()
            options.add_argument("--disable-blink-features=AutomationControlled")
            options.add_argument("--incognito")
            options.add_argument("--disable-web-security")
            options.add_argument("--disable-features=VizDisplayCompositor")
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-dev-shm-usage")
            options.add_argument("--disable-gpu")
            options.add_argument("--disable-extensions")
            options.add_argument("--disable-infobars")
            options.add_argument("--single-process")
            
            self.driver = uc.Chrome(options=options)
            self.driver.set_window_size(380, 400)
            # self.driver.maximize_window()
            self.wait = WebDriverWait(self.driver, 20)
            self.debug_log("Chrome driver is ready", "SUCCESS")
            return True
        except Exception as e:
            self.debug_log(f"Failed to set up Chrome driver: {str(e)}", "ERROR")
            return False

    def safe_click(self, element, method="click"):
        """Click an element safely using multiple methods"""
        try:
            if method == "js":
                self.driver.execute_script("arguments[0].click();", element)
            else:
                element.click()
            return True
        except Exception as e:
            self.debug_log(f"Could not click element: {str(e)}", "WARNING")
            try:
                self.driver.execute_script("arguments[0].click();", element)
                return True
            except:
                return False

    def safe_send_keys(self, element, text, clear_first=True):
        """Send keys safely"""
        try:
            if clear_first:
                element.clear()
            element.send_keys(text)
            return True
        except Exception as e:
            self.debug_log(f"Could not send keys: {str(e)}", "WARNING")
            return False

    def wait_and_find(self, locator, timeout=8, retry_count=2):
        """Wait and find element with retry"""
        for attempt in range(retry_count):
            try:
                element = WebDriverWait(self.driver, timeout).until(
                    EC.presence_of_element_located(locator)
                )
                self.debug_log(f"Found element: {locator}")
                return element
            except TimeoutException:
                self.debug_log(f"Attempt {attempt + 1} failed to find element: {locator}", "WARNING")
                if attempt < retry_count - 1:
                    self.random_delay(2, 4)
                else:
                    raise

    def step_email_input(self, email):
        """Step 1: Enter email address"""
        try:
            self.debug_log("Step 1: Entering email address")
            email_field = self.wait_and_find((By.NAME, "Email"))
            if self.safe_send_keys(email_field, email):
                self.debug_log(f"Email entered: {email}", "SUCCESS")
            else:
                raise Exception("Failed to enter email")
            self.random_delay(1, 2)
            next_button = self.wait_and_find((By.XPATH, "//button[contains(., 'Next')]"))
            if self.safe_click(next_button):
                self.debug_log("Clicked Next button", "SUCCESS")
            else:
                raise Exception("Failed to click Next button")
            return True
        except Exception as e:
            self.debug_log(f"Error in email input step: {str(e)}", "ERROR")
            return False

    def step_password_input(self, password):
        """Step 2: Enter password"""
        try:
            self.debug_log("Step 2: Entering password")
            password_field = self.wait_and_find((By.CSS_SELECTOR, "input[type='password']"))
            if self.safe_send_keys(password_field, password):
                self.debug_log("Password entered successfully", "SUCCESS")
            else:
                raise Exception("Failed to enter password")
            self.random_delay(1, 2)
            next_button = self.wait_and_find((By.XPATH, "//button[contains(., 'Next')]"))
            if self.safe_click(next_button):
                self.debug_log("Clicked Next button", "SUCCESS")
            else:
                raise Exception("Failed to click Next button")
            return True
        except Exception as e:
            self.debug_log(f"Error in password input step: {str(e)}", "ERROR")
            return False

    def step_country_selection(self):
        """Step 3: Select country"""
        try:
            self.debug_log("Step 3: Selecting country")
            country_dropdown = self.wait_and_find((By.CSS_SELECTOR, "button[data-testid='countryDropdown']"))
            if self.safe_click(country_dropdown, "js"):
                self.debug_log("Country dropdown opened", "SUCCESS")
            else:
                raise Exception("Failed to open country dropdown")
            self.random_delay(1, 2)
            if self.safe_send_keys(country_dropdown, "Thailand", clear_first=False):
                self.debug_log("Typed Thailand", "SUCCESS")
            else:
                raise Exception("Failed to type Thailand")
            self.random_delay(1, 2)
            country_dropdown.send_keys(Keys.RETURN)
            self.debug_log("Selected country: Thailand", "SUCCESS")
            return True
        except Exception as e:
            self.debug_log(f"Error in country selection step: {str(e)}", "ERROR")
            return False

    def step_birth_date(self):
        """Step 4: Select birth date"""
        try:
            self.debug_log("Step 4: Selecting birth date")
            month_dropdown = self.wait_and_find((By.ID, "BirthMonthDropdown"))
            if self.safe_click(month_dropdown, "js"):
                self.debug_log("Month dropdown opened", "SUCCESS")
            else:
                raise Exception("Failed to open month dropdown")
            self.random_delay(1, 2)
            month_dropdown.send_keys(Keys.ARROW_DOWN)
            month_dropdown.send_keys(Keys.RETURN)
            self.debug_log("Month selected", "SUCCESS")
            self.random_delay(1, 2)

            day_dropdown = self.wait_and_find((By.ID, "BirthDayDropdown"))
            if self.safe_click(day_dropdown):
                self.debug_log("Day dropdown opened", "SUCCESS")
            else:
                raise Exception("Failed to open day dropdown")
            self.random_delay(1, 2)
            random_day = random.randint(1, 28)
            for _ in range(random_day):
                day_dropdown.send_keys(Keys.ARROW_DOWN)
            day_dropdown.send_keys(Keys.RETURN)
            self.debug_log(f"Day selected: {random_day}", "SUCCESS")
            self.random_delay(1, 2)

            year_input = self.wait_and_find((By.ID, "floatingLabelInput24"))
            random_year = random.randint(1990, 2005)
            if self.safe_send_keys(year_input, str(random_year)):
                self.debug_log(f"Year entered: {random_year}", "SUCCESS")
            else:
                raise Exception("Failed to enter year")
            self.random_delay(1, 2)

            submit_button = self.wait_and_find((By.CSS_SELECTOR, 'button[type="submit"]'))
            if self.safe_click(submit_button):
                self.debug_log("Submit button clicked", "SUCCESS")
            else:
                raise Exception("Failed to click submit button")

            return True
        except Exception as e:
            self.debug_log(f"Error in birth date selection step: {str(e)}", "ERROR")
            return False

    def step_name_input(self, first_name, last_name):
        """Step 5: Enter first and last name"""
        try:
            self.debug_log("Step 5: Entering name")
            first_name_input = self.wait_and_find((By.ID, "firstNameInput"))
            if self.safe_send_keys(first_name_input, first_name):
                self.debug_log(f"First name entered: {first_name}", "SUCCESS")
            else:
                raise Exception("Failed to enter first name")
            self.random_delay(1, 2)

            last_name_input = self.wait_and_find((By.ID, "lastNameInput"))
            if self.safe_send_keys(last_name_input, last_name):
                self.debug_log(f"Last name entered: {last_name}", "SUCCESS")
            else:
                raise Exception("Failed to enter last name")
            self.random_delay(1, 2)

            next_button = self.wait_and_find((By.CSS_SELECTOR, "button[data-testid='primaryButton']"))
            if self.safe_click(next_button):
                self.debug_log("Next button clicked", "SUCCESS")
            else:
                raise Exception("Failed to click Next button")

            return True
        except Exception as e:
            self.debug_log(f"Error in name input step: {str(e)}", "ERROR")
            return False

    def step_captcha_handling(self):
        """Step 6: Handle Captcha"""
        try:
            self.debug_log("Step 6: Handling Captcha")
            WebDriverWait(self.driver, 7).until(
                EC.presence_of_element_located((
                    By.XPATH, "//p[contains(text(),'Press')] | //h1[contains(text(),\"Let's prove you're human\")]"
                ))
            )
            self.debug_log("Captcha page detected", "SUCCESS")

            time.sleep(5)

            body = self.driver.find_element(By.TAG_NAME, "body")
            for i in range(3):
                body.send_keys(Keys.TAB)
                self.debug_log(f"Pressed Tab {i+1}")
                time.sleep(0.5)
            self.debug_log("Holding Enter key for 18 seconds...")
            actions = ActionChains(self.driver)
            actions.key_down(Keys.ENTER).perform()
            time.sleep(16)
            actions.key_up(Keys.ENTER).perform()
            self.debug_log("Captcha completed", "SUCCESS")
            return True
        except Exception as e:
            self.debug_log(f"Error in captcha handling step: {str(e)}", "ERROR")
            return False

    def signup_with_retry(self, email, password, first_name, last_name):
        """Main function with retry logic"""
        for attempt in range(self.max_retries):
            try:
                self.debug_log(f"Starting sign-up attempt {attempt + 1}")
                if not self.setup_driver():
                    raise Exception("Driver setup failed")
                self.debug_log("Navigating to sign-up page")
                self.driver.get("https://signup.live.com/ ")
                self.random_delay(2, 4)

                if not self.step_email_input(email):
                    raise Exception("Email input step failed")
                if not self.step_password_input(password):
                    raise Exception("Password input step failed")
                if not self.step_country_selection():
                    raise Exception("Country selection step failed")
                if not self.step_birth_date():
                    raise Exception("Birth date step failed")
                if not self.step_name_input(first_name, last_name):
                    raise Exception("Name input step failed")
                if not self.step_captcha_handling():
                    raise Exception("Captcha step failed")
                
                
               

                self.debug_log("Sign-up completed successfully!", "SUCCESS")
                self.debug_log("Please verify manually on the webpage")
                input("Press Enter after completing manual steps...")
                return True
            except Exception as e:
                self.debug_log(f"Attempt {attempt + 1} failed: {str(e)}", "ERROR")
                if self.debug:
                    traceback.print_exc()
                if attempt < self.max_retries - 1:
                    self.debug_log(f"Retrying in 5 seconds...", "WARNING")
                    if self.driver:
                        self.driver.quit()
                    time.sleep(5)
                else:
                    self.debug_log("All attempts failed", "ERROR")
                    return False
        return False

    def cleanup(self):
        """Close the browser driver"""
        if self.driver:
            self.driver.quit()
            self.debug_log("Browser closed")


def signup_hotmail(email, password, first_name, last_name, max_retries=3, debug=True):
    """
    Function to sign up for Hotmail
    Args:
        email: desired email address
        password: account password
        first_name: user's first name
        last_name: user's last name
        max_retries: number of retry attempts
        debug: enable/disable debug mode
    """
    signup_bot = HotmailSignup(max_retries=max_retries, debug=debug)
    try:
        result = signup_bot.signup_with_retry(email, password, first_name, last_name)
        return result
    finally:
        signup_bot.cleanup()


# if __name__ == "__main__":
#     email = "sanxow337@hotmail.com"
#     password = "sanxow_337"
#     first_name = "sanxow"
#     last_name = "yhdfg"

#     success = signup_hotmail(
#         email=email,
#         password=password,
#         first_name=first_name,
#         last_name=last_name,
#         max_retries=3,
#         debug=True
#     )

#     if success:
#         print("Sign-up completed successfully!")
#     else:
#         print("Sign-up failed.")

if __name__ == "__main__":
    file_path = "infomail.txt" 
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            content = file.read().strip().split("\n\n")  

        for idx, block in enumerate(content):
            lines = block.strip().splitlines()
            if len(lines) != 4:
                print(f"[WARNING] Invalid account data at block {idx + 1}")
                continue

            email, password, first_name, last_name = lines

            print(f"\nStarting sign-up for: {email}")
            success = signup_hotmail(
                email=email,
                password=password,
                first_name=first_name,
                last_name=last_name,
                max_retries=3,
                debug=True
            )

            if success:
                print(f"Sign-up completed successfully for: {email}")
            else:
                print(f"Sign-up failed for: {email}")

    except FileNotFoundError:
        print(f"[ERROR] File not found: {file_path}")
    except Exception as e:
        print(f"[ERROR] An error occurred: {str(e)}")