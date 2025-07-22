from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import undetected_chromedriver as uc
import random
import time

def random_delay(min_t=0.3, max_t=0.8):
    time.sleep(random.uniform(min_t, max_t))

def fake_typing(element, text):
    for char in text:
        element.send_keys(char)
        time.sleep(random.uniform(0.05, 0.2))  # faster fake typing

def move_and_click(driver, element):
    actions = ActionChains(driver)
    actions.move_to_element(element).pause(random.uniform(0.1, 0.3)).click().perform()

def setup_driver():
    options = uc.ChromeOptions()
    user_agent = random.choice([
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.1 Safari/605.1.15",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36",
    ])
    options.add_argument(f"user-agent={user_agent}")
    width, height = random.choice([(400, 600), (420, 620), (450, 650)])
    options.add_argument(f"--window-size={width},{height}")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--incognito")

    driver = uc.Chrome(options=options)
    return driver


def signup_hotmail(email, password, first_name, last_name):
    driver = setup_driver()
    wait = WebDriverWait(driver, 20)
    print("[INFO] Going to signup page...")
    driver.get("https://signup.live.com/")

    # Email
    print("[INFO] Entering email...")
    email_field = wait.until(EC.presence_of_element_located((By.NAME, "Email")))
    fake_typing(email_field, email)
    random_delay()
    next_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Next')]")))
    move_and_click(driver, next_btn)

    # Password
    print("[INFO] Entering password...")
    pwd_field = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='password']")))
    fake_typing(pwd_field, password)
    random_delay()
    next_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Next')]")))
    move_and_click(driver, next_btn)

    # Country
    print("[INFO] Selecting country...")
    country_btn = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[data-testid='countryDropdown']")))
    move_and_click(driver, country_btn)
    random_delay()
    country_btn.send_keys("Thailand")
    country_btn.send_keys(Keys.RETURN)

    # Birth Date
    print("[INFO] Selecting birth date...")
    month_dropdown = wait.until(EC.element_to_be_clickable((By.ID, "BirthMonthDropdown")))
    move_and_click(driver, month_dropdown)
    month_dropdown.send_keys(Keys.ARROW_DOWN)
    month_dropdown.send_keys(Keys.RETURN)

    day_dropdown = wait.until(EC.element_to_be_clickable((By.ID, "BirthDayDropdown")))
    move_and_click(driver, day_dropdown)
    for _ in range(random.randint(1, 28)):
        day_dropdown.send_keys(Keys.ARROW_DOWN)
    day_dropdown.send_keys(Keys.RETURN)

    year_input = wait.until(EC.presence_of_element_located((By.ID, "floatingLabelInput24")))
    fake_typing(year_input, str(random.randint(1990, 2005)))

    submit_btn = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[type="submit"]')))
    move_and_click(driver, submit_btn)

    # Name
    print("[INFO] Entering name...")
    first_name_input = wait.until(EC.presence_of_element_located((By.ID, "firstNameInput")))
    fake_typing(first_name_input, first_name)
    last_name_input = wait.until(EC.presence_of_element_located((By.ID, "lastNameInput")))
    fake_typing(last_name_input, last_name)

    next_btn = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[data-testid='primaryButton']")))
    move_and_click(driver, next_btn)

    # Captcha
    try:
        print("[INFO] Checking for captcha...")
        wait.until(EC.presence_of_element_located((
            By.XPATH, "//p[contains(text(),'Press')] | //h1[contains(text(),\"Let's prove you're human\")]"
        )))
        print("[INFO] Captcha page detected. Holding Enter...")
        body = driver.find_element(By.TAG_NAME, "body")
        for _ in range(3):
            body.send_keys(Keys.TAB)
            time.sleep(0.5)
        actions = ActionChains(driver)
        actions.key_down(Keys.ENTER).perform()
        time.sleep(10)
        actions.key_up(Keys.ENTER).perform()
    except:
        print("[INFO] No captcha detected.")

    print("[INFO] Done, please finalize manually if needed...")
    input("Press Enter to close...")
    driver.quit()

# 🚀 Example
signup_hotmail(
    email="durlik559@hotmail.com",
    password="durlik_559",
    first_name="durlik",
    last_name="rdfgz"
)
