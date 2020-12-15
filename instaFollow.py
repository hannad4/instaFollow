from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException        
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options

import os


def navigateProfile(browser): 
    print("Navigating to your profile...\n")
    WebDriverWait(browser, WAIT_TIME_GLOBAL).until(EC.element_to_be_clickable((By.XPATH, "//*[@id='react-root']/section/nav/div[2]/div/div/div[3]/div/div[5]/span"))).click()
    WebDriverWait(browser, WAIT_TIME_GLOBAL).until(EC.element_to_be_clickable((By.XPATH, "//*[@id='react-root']/section/nav/div[2]/div/div/div[3]/div/div[5]/div[2]/div[2]/div[2]/a[1]"))).click()


def attemptLogin(userName, passWord, browser): 
    try:
        print('\nEntering credentials...\n')
        WebDriverWait(browser, WAIT_TIME_GLOBAL).until(EC.element_to_be_clickable((By.XPATH, "//input[@name='username']"))).send_keys(userName)
        browser.find_element_by_xpath("//input[@name='password']").send_keys(passWord)
        browser.find_element_by_xpath("//button/div[text()='Log In']").click()

        try:
            WebDriverWait(browser, 5).until(EC.presence_of_element_located((By.ID, "slfErrorAlert")))
            browser.quit()
            if os.name == 'nt':
                os.system('cls')
            else:
                os.system('clear')
            print("The login info you entered was incorrect\n")
            main()
        except: 
            print("Logged in successfully\n")
            navigateProfile(browser)

    except Exception as e:
        print("Something went wrong. The program has been halted\n")
        print("You can provide the following error message to the developer:\n")
        print(e) 
        return


def main(): 
    userName = input("Enter your instagram username. This is case sensitive:\n")
    passWord = input("\nEnter your password. This will be used to log into your Instagram and will not be shared anywhere else:\n")

    chrome_options = Options() 
    chrome_options.add_experimental_option("detach", True)
    browser = webdriver.Chrome(options=chrome_options, executable_path=ChromeDriverManager().install())

    browser.get("https://www.instagram.com/")
    attemptLogin(userName, passWord, browser)


if __name__ == "__main__":
    WAIT_TIME_GLOBAL = 10
    main()