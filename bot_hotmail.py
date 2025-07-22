from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import undetected_chromedriver as uc
import time
from selenium import webdriver
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains



def signup_hotmail(email, password, first_name, last_name):
    options = uc.ChromeOptions()
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--incognito")

    driver = uc.Chrome(options=options)
    driver.get("https://signup.live.com/")

    wait = WebDriverWait(driver, 20)

    # Step 1: Email
    wait.until(EC.presence_of_element_located((By.NAME, "Email")))
    driver.find_element(By.NAME, "Email").send_keys(email)
    # กดปุ่มถัดไป
    driver.find_element(By.XPATH, "//button[contains(., 'Next')]").click()
    wait = WebDriverWait(driver, 2)

    # รอ password field
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='password']")))
    driver.find_element(By.CSS_SELECTOR, "input[type='password']").send_keys(password)
    driver.find_element(By.XPATH, "//button[contains(., 'Next')]").click()
    wait = WebDriverWait(driver, 2)


    # country_dropdown = wait.until(EC.element_to_be_clickable((By.ID, "countryDropdownId")))
    # country_dropdown.click()
    # time.sleep(1)
    # country_dropdown.send_keys(Keys.ARROW_DOWN)
    # country_dropdown.send_keys(Keys.RETURN)

    country_dropdown = wait.until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "button[data-testid='countryDropdown']"))
    )
    driver.execute_script("arguments[0].click();", country_dropdown)
    time.sleep(1)

    # พิมพ์ "Thailand" เพื่อเลือกประเทศ
    country_dropdown.send_keys("Thailand")
    time.sleep(1)
    country_dropdown.send_keys(Keys.RETURN)


    # Birth Month
    month_dropdown = wait.until(EC.element_to_be_clickable((By.ID, "BirthMonthDropdown")))
    driver.execute_script("arguments[0].click();", month_dropdown)  # ใช้ JS คลิกแทน
    time.sleep(1)
    month_dropdown.send_keys(Keys.ARROW_DOWN)
    month_dropdown.send_keys(Keys.RETURN)

    wait = WebDriverWait(driver, 2)

    # day dropdown
    day_dropdown = wait.until(EC.element_to_be_clickable((By.ID, "BirthDayDropdown")))
    day_dropdown.click()
    time.sleep(1)
    day_dropdown.send_keys(Keys.ARROW_DOWN * 5)  # ตัวอย่างเลือกวันที่ 5
    day_dropdown.send_keys(Keys.RETURN)

    wait = WebDriverWait(driver, 2)

    # year input
    year_input = wait.until(EC.visibility_of_element_located((By.ID, "floatingLabelInput24")))
    year_input.send_keys("2000")

    wait = WebDriverWait(driver, 2)

    # submit form
    submit_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[type="submit"]')))
    submit_button.click()

    wait = WebDriverWait(driver, 2)

    # Step 3: First Name
    first_name_input = wait.until(EC.presence_of_element_located((By.ID, "firstNameInput")))
    first_name_input.send_keys(first_name)

    # Step 4: Last Name
    last_name_input = wait.until(EC.presence_of_element_located((By.ID, "lastNameInput")))
    last_name_input.send_keys(last_name)

    # Step 5: Next button
    next_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[data-testid='primaryButton']")))
    next_button.click()

    WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((
            By.XPATH, "//p[contains(text(),'Press')] | //h1[contains(text(),\"Let's prove you're human\")]"
        ))
    )
    wait = WebDriverWait(driver, 5)

    # Captcha
    body = driver.find_element(By.TAG_NAME, "body")  # หรือ element ที่จะส่ง key event

    wait = WebDriverWait(driver, 10)

    # กด Tab 3 ครั้ง
    for _ in range(3):
        body.send_keys(Keys.TAB)
        time.sleep(0.5)  # เว้นเล็กน้อยระหว่างกด Tab เพื่อให้ UI ตอบสนอง

    # กด Enter ค้าง (โดยส่ง key down + รอ + key up)
    

    actions = ActionChains(driver)
    actions.key_down(Keys.ENTER).perform()   # กดปุ่ม Enter ค้าง
    time.sleep(18)                           # รอ 10 วินาที
    actions.key_up(Keys.ENTER).perform()


    wait = WebDriverWait(driver, 20)

    # skip_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[text()='Skip for now']")))
    # skip_button.click()

    # wait = WebDriverWait(driver, 2)
    # no_button = wait.until(EC.element_to_be_clickable(
    # (By.XPATH, "//button[@data-testid='secondaryButton' and text()='No']")
    # ))
    # no_button.click()

    # wait = WebDriverWait(driver, 2)
    # profile_button = wait.until(EC.element_to_be_clickable((By.ID, "meInitialsButton")))

    # # คลิกปุ่ม
    # profile_button.click()

    # wait = WebDriverWait(driver, 2)

    # # รอให้ปุ่ม logout ปรากฏและกด
    # signout_button = wait.until(EC.element_to_be_clickable((By.ID, "mectrl_body_signOut")))
    # signout_button.click()

    # wait = WebDriverWait(driver, 2)
    # # รอจนเจอ div ที่เป็น avatar
    # profile_picture = wait.until(EC.element_to_be_clickable((By.ID, "mectrl_headerPicture")))

    # # คลิก
    # profile_picture.click()

    # wait = WebDriverWait(driver, 2)

    # # รอจนปุ่ม Create one! ปรากฏและคลิก
    # create_account_link = wait.until(EC.element_to_be_clickable((By.ID, "signup")))
    # create_account_link.click()

    # wait = WebDriverWait(driver, 2)









    print("กรอกเสร็จแล้ว (อาจต้องยืนยัน Captcha / SMS ด้วยมือ)")
    print("กด Enter หลังจากคุณทำผ่านแล้ว...")
    input()

    print("สมัคร hotmail สำเร็จ (check inbox)")
    time.sleep(3)
    driver.quit()

# 🚀 เรียกใช้
signup_hotmail(
    email="kerpit349@hotmail.com",
    password="kerpit_349",
    first_name="kerpit",
    last_name="ophdfg"
)
