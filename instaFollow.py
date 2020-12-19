# Things to note: 
# 1. Instagram dynamically assigns class names to elements and therefore shouldn't be used for driver filtering
# 2. It is important to utilize Expected Conditions to account for the dynamic loading behavior of Instagram

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException        
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options

import os    # Utilized only for knowing which command to use for clearing terminal (easy viewing for noobs)


def navigateProfile(browser): # User has definitely logged in. These elements undeniably exist, so no error handling is needed
    print("Navigating to your profile...\n")
    WebDriverWait(browser, WAIT_TIME_GLOBAL).until(EC.element_to_be_clickable((By.XPATH, "//*[@id='react-root']/section/nav/div[2]/div/div/div[3]/div/div[5]/span"))).click()
    WebDriverWait(browser, WAIT_TIME_GLOBAL).until(EC.element_to_be_clickable((By.XPATH, "//*[@id='react-root']/section/nav/div[2]/div/div/div[3]/div/div[5]/div[2]/div[2]/div[2]/a[1]"))).click()


def attemptLogin(userName, passWord, browser): 
    try:  # Many things can go wrong in login attempt, hence try except block (in case the world explodes?!?!)
        print('\nEntering credentials...\n')
        WebDriverWait(browser, WAIT_TIME_GLOBAL).until(EC.element_to_be_clickable((By.XPATH, "//input[@name='username']"))).send_keys(userName)
        browser.find_element_by_xpath("//input[@name='password']").send_keys(passWord)
        browser.find_element_by_xpath("//button/div[text()='Log In']").click()

        try:    # Monitor to see if login failed via slfErrorAlert element dynamically loaded
            WebDriverWait(browser, 5).until(EC.presence_of_element_located((By.ID, "slfErrorAlert")))
            browser.quit()
            if os.name == 'nt':
                os.system('cls')
            else:
                os.system('clear')
            print("The login info you entered was incorrect\n")
            main()
        except:  # Assuming no slfErrorAlert loaded means login credentials accepted
            print("Logged in successfully\n")
            navigateProfile(browser)

    except Exception as e:
        print("Something went wrong. The program has been halted\n")
        print("You can provide the following error message to the developer:\n")
        print(str(e))         
        return


def main(): 
    userName = input("\nEnter your instagram username. This is case sensitive:\n")
    passWord = input("\nEnter your password. This will be used to log into your Instagram and will not be shared anywhere else:\n")

    # Enabling experimental options to allow for a persistent browser to exist for the user even if program terminated
    chrome_options = Options() 
    chrome_options.add_experimental_option("detach", True)
    browser = webdriver.Chrome(options=chrome_options, executable_path=ChromeDriverManager().install())

    browser.get("https://www.instagram.com/")
    attemptLogin(userName, passWord, browser)


if __name__ == "__main__":
    WAIT_TIME_GLOBAL = 10
    main()