from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import undetected_chromedriver as uc
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
import random

def signup_hotmail(email, password, first_name, last_name):
    options = uc.ChromeOptions()
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--incognito")

    driver = uc.Chrome(options=options)
    driver.get("https://signup.live.com/ ")

    wait = WebDriverWait(driver, 20)

    # Step 1: Email
    email_input = wait.until(EC.presence_of_element_located((By.NAME, "Email")))
    email_input.send_keys(email)
    driver.find_element(By.XPATH, "//button[contains(., 'Next')]").click()

    # Step 2: Password
    password_input = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='password']")))
    password_input.send_keys(password)
    driver.find_element(By.XPATH, "//button[contains(., 'Next')]").click()

    # Step 3: Country Selection
    country_dropdown = wait.until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "button[data-testid='countryDropdown']"))
    )
    driver.execute_script("arguments[0].click();", country_dropdown)
    time.sleep(1)

    # พิมพ์ "Thailand" เพื่อเลือกประเทศ
    country_dropdown.send_keys("Thailand")
    time.sleep(1)
    country_dropdown.send_keys(Keys.RETURN)

    # Step 4: Birthdate (Random Date between 1998 - 2005)
    year = str(random.randint(1998, 2005))
    month = random.choice([
        "January", "February", "March", "April", "May", "June",
        "July", "August", "September", "October", "November", "December"
    ])
    day = str(random.randint(1, 28))

    # Month Dropdown
    month_dropdown = wait.until(
        EC.element_to_be_clickable((By.ID, "BirthMonthDropdown"))  # ใช้ ID แทน data-testid
    )
    driver.execute_script("arguments[0].click();", month_dropdown)
    time.sleep(0.5)
    month_dropdown.send_keys(month)
    time.sleep(0.5)
    month_dropdown.send_keys(Keys.RETURN)

    # Day Dropdown
    day_dropdown = wait.until(
        EC.element_to_be_clickable((By.XPATH, "//button[@aria-label='Birth day']"))  # ใช้ aria-label
    )
    driver.execute_script("arguments[0].click();", day_dropdown)
    time.sleep(0.5)
    day_dropdown.send_keys(day)
    time.sleep(0.5)
    day_dropdown.send_keys(Keys.RETURN)

    # Year Input
    year_input = wait.until(
        EC.visibility_of_element_located((By.XPATH, "//input[@aria-label='Birth year']"))  # ใช้ aria-label
    )
    year_input.clear()
    year_input.send_keys(year)

    # Next Button
    next_button = wait.until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "button[data-testid='nextButton']"))
    )
    next_button.click()

    # Step 5: First Name
    first_name_input = wait.until(
        EC.presence_of_element_located((By.ID, "firstNameInput"))
    )
    first_name_input.send_keys(first_name)

    # Step 6: Last Name
    last_name_input = wait.until(
        EC.presence_of_element_located((By.ID, "lastNameInput"))
    )
    last_name_input.send_keys(last_name)

    # Final Next Button
    final_next_button = wait.until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "button[data-testid='primaryButton']"))
    )
    final_next_button.click()

    print(f"[INFO] ข้อมูลที่กรอก: {first_name} {last_name}, {day}/{month}/{year}")
    print("[INFO] กรุณากรอก Captcha / SMS ด้วยมือหากจำเป็น")
    input("[ACTION] กด Enter เมื่อทำเสร็จแล้ว...")

    print("[SUCCESS] สมัคร hotmail สำเร็จ! โปรดตรวจสอบอีเมล")
    time.sleep(3)
    driver.quit()

# 🚀 เรียกใช้งาน
signup_hotmail(
    email="nihneh462@hotmail.com",
    password="nihneh_462!",
    first_name="nihneh",
    last_name="Doesaffd"
)