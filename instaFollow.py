from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

def attemptLogin(userName, passWord): 
    try:
        print('\nEntering credentials...')
        WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.XPATH, "//input[@name='username']"))).send_keys(userName)
        browser.find_element_by_xpath("//input[@name='password']").send_keys(passWord)
        browser.find_element_by_xpath("//button/div[text()='Log In']").click()

    except Exception as e:
        print("Login attempt failed. Instagram may have updated its login form & broken this program\n\n")
        print("You can provide the following error message to the developer:\n")
        print(e)


if __name__ == "__main__":
    userName = input("Enter your instagram username. This is case sensitive:\n")
    passWord = input("\nEnter your password. This will be used to log into your Instagram and will not be shared anywhere else:\n")
    browser = webdriver.Chrome(ChromeDriverManager().install())
    browser.get("https://www.instagram.com/")
    attemptLogin(userName, passWord)