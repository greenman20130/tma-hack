import time
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By

SECRET_URL = "secret"

def setup_driver():
    mobile_emulation = {
        "deviceMetrics": {"width": 360, "height": 640, "pixelRatio": 3.0},
        "userAgent": "Mozilla/5.0 (iPhone; CPU iPhone OS 10_3 like Mac OS X) AppleWebKit/602.1.50 (KHTML, like Gecko) CriOS/56.0.2924.75 Mobile Safari/535.19"
    }
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_experimental_option("mobileEmulation", mobile_emulation)
    chrome_options.add_argument("--window-size=389,713")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument('--disable-blink-features=AutomationControlled')
    return webdriver.Chrome(options=chrome_options)

def open_site(driver, url):
    driver.get(url)

def remove_element(driver, selector):
    driver.execute_script("document.querySelector('{}').remove();".format(selector))

def wait_for_element(driver, selector):
    try:
        element = driver.find_element(by=By.CSS_SELECTOR, value=selector)
        return element
    except NoSuchElementException:
        return None

def click_take_button(driver):
    try:
        take_button = driver.find_element(by=By.XPATH, value="/html/body/div[3]/div[2]/div[3]")
        take_button.click()
        time.sleep(1)
    except NoSuchElementException:
        print('Отсутствует кнока получения афк валюты')

def find_product(driver, keyword):
    try:
        target_div = driver.find_element(by=By.XPATH, value=f"//div[contains(text(), '{keyword}')]")
        parent_div = target_div.find_element(by=By.XPATH, value="..")
        next_sibling = parent_div.find_element(by=By.XPATH, value="following-sibling::*")
        child_div = next_sibling.find_element(by=By.TAG_NAME, value="div")
        print(f"{keyword}, Текст: {child_div.text}, Состояние: {child_div.get_attribute('class')}")
        if child_div.text != "Скоро":
            child_div.click()
            buy_accept = driver.find_element(by=By.XPATH, value="/html/body/div[3]/div[2]/div[4]")
            buy_accept.click()
            return True
        else:
            return False
    except NoSuchElementException:
        pass

def check_shop(driver):
    shop = driver.find_element(by=By.XPATH, value="/html/body/div/div/nav/a[5]")
    shop.click()

    find_first = find_product(driver, "До 10 друзей")
    if find_first:
        return True
    
    find_second = find_product(driver, "От 10 друзей")
    if find_second:
        return True
    
    return False

def main():
    driver = setup_driver()
    open_site(driver, SECRET_URL)

    while True:
        time.sleep(1)
        blocker = driver.find_element(by=By.CSS_SELECTOR, value='#app > div > div.orientation-lock')
        blocker.click()
        remove_element(driver, '#app > div > div.orientation-lock')
        time.sleep(1)
        click_take_button(driver)
        if check_shop(driver):
            break
        driver.refresh()

    driver.quit()

if __name__ == "__main__":
    main()