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
from explicit import waiter

import os    # Utilized only for knowing which command to use for clearing terminal (easy viewing for noobs)
import getpass  # Utilized only for obtaining the users password without showing it out in the open
import itertools # Utilized only for iteration through scraping process  

def obtainFollowers(browser): 
    follower_css = "ul div li:nth-child({}) a.notranslate"  # CSS's nth-child functionality lets you pick all follower children
    for group in itertools.count(start=1, step=12):     # Step through 12 at a time to scroll follower list
        for follower_index in range(group, group + 12):
            yield waiter.find_element(browser, follower_css.format(follower_index)).text

        # Keep last element from going stale (aka make sure the scrolling view doesn't forget who the last follwer was)
        last_follower = waiter.find_element(browser, follower_css.format(follower_index))   
        browser.execute_script("arguments[0].scrollIntoView();", last_follower)

def navigateToFollowers(browser): 
    print("\nGathering your followers\n")
    followerHREF = "/" + userName + "/followers/" 
    totalFollowerCount = WebDriverWait(browser, WAIT_TIME_GLOBAL).until(EC.presence_of_element_located((By.XPATH, '//li/a[text()=" followers"]/span'))).text
    WebDriverWait(browser, WAIT_TIME_GLOBAL).until(EC.element_to_be_clickable((By.XPATH, '//a[@href="'+followerHREF+'"]'))).click() 
    global followerList; 
    followerList = []; 
    for count, follower in enumerate(obtainFollowers(browser)):
        print("{}: {}".format(count, follower))
        followerList.append(follower)
        if count >= int(totalFollowerCount) - 1:
            break; 
    # print("\nYour total follower list is:\n\n" + ' ||| '.join(followerList) + "\n")


def navigateProfile(browser): # User has definitely logged in at this point. These elements exist for all users, so no error handling is needed
    print("Navigating to your profile...\n")
    WebDriverWait(browser, WAIT_TIME_GLOBAL).until(EC.element_to_be_clickable((By.XPATH, "//*[@id='react-root']/section/nav/div[2]/div/div/div[3]/div/div[5]/span"))).click()
    WebDriverWait(browser, WAIT_TIME_GLOBAL).until(EC.element_to_be_clickable((By.XPATH, "//*[@id='react-root']/section/nav/div[2]/div/div/div[3]/div/div[5]/div[2]/div[2]/div[2]/a[1]"))).click()
    navigateToFollowers(browser); 


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
            print("\nThe login info you entered was incorrect\n")
            main()
        except:     # Assuming no slfErrorAlert loaded means login credentials accepted
            print("\nLogged in successfully\n")
            navigateProfile(browser)

    except Exception as e:  # If something went wrong, this exception block will catch it & land the program gently instead of a messy crash
        print("\nSomething went wrong. The program has been halted\n")
        print("\nYou can provide the following error message (if available) to the developer:\n")
        print("\n" + str(e) + "\n")         
        return


def main(): 
    global userName;            # We will use the userName in many functions

    userName = input("\nEnter your instagram username. This is case sensitive:\n")
    passWord = getpass.getpass("\nEnter your password. This will be used to log into your Instagram and will not be shared anywhere else. For privacy, typing your password will not move the cursor or show characters:\n")

    # Enabling experimental options to allow for a persistent browser to exist (but minimized) for the user even if program terminated
    chrome_options = Options() 
    chrome_options.add_experimental_option("detach", True)
    browser = webdriver.Chrome(options=chrome_options, executable_path=ChromeDriverManager().install())
    print("\nMinimizing window\n")
    
    browser.get("https://www.instagram.com/")
    attemptLogin(userName, passWord, browser)


if __name__ == "__main__":
    WAIT_TIME_GLOBAL = 10
    main()