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
import gc       # Utilied only for memory cleanup at the end of the program for a more clean termination

def cleanClose():
    print("\nSorry if you got dissappointing results.\n")
    print("\nThanks for using instaFollow.\n")
    gc.collect()
    quit()

def listCompare():
    print("\n\nComparing Lists now\n")
    notFollowing = list(set(followerList) - set(followingList))  # These people follow you, but you do not follow them back 
    notFollower = list(set(followingList) - set(followerList))  # You are following these people, but they are not following you back
    print("\nThis is the final list of people who follow you, but you do not follow them back:\n" + ' || '.join(notFollowing) + "\n")
    print("\nThis is the final list of people that you are following, but they do not follow you back:\n" + ' || '.join(notFollower) + "\n")
    writeToFile = input("\nDo you want to write these results to a text file? Y/N\n")
    if(writeToFile.upper() == "YES" or writeToFile.upper() == "Y"):
        print("\nThe file will be located in the same location as this program. It is titled 'instaResults.txt'\n")
        instaResults = open("instaResults.txt", "w")
        instaResults.write("List 1 - People who follow you, but you do not follow them back:\n\n")

        for count, following in enumerate(notFollowing):
            instaResults.write(("{}: {}\n".format(count, following)))
        
        instaResults.write("\n\n=================================\n\nList 2 - People that you are following, but they do not follow you back:\n\n")

        for count, follower in enumerate(notFollower):
            instaResults.write(("{}: {}\n".format(count, follower)))
        instaResults.close()
        cleanClose()

    else:
        cleanClose()

def navigateToFollowing(browser):
    print("\nGathering your following list", end = "")
    followingHREF = "/" + userName + "/following/"
    totalFollowingCount = WebDriverWait(browser, WAIT_TIME_GLOBAL).until(EC.presence_of_element_located((By.XPATH, '//li/a[text()=" following"]/span'))).text
    WebDriverWait(browser, WAIT_TIME_GLOBAL).until(EC.element_to_be_clickable((By.XPATH, '//a[@href="'+followingHREF+'"]'))).click() 
    global followingList 
    followingList = [] 
    for count, following in enumerate(obtainList(browser)):
        print(".", end = "")
        followingList.append(following)
        if count >= int(totalFollowingCount) - 1:
            break 
    browser.delete_all_cookies()
    browser.quit()
    listCompare(); 

def obtainList(browser): 
    follower_css = "ul div li:nth-child({}) a.notranslate"  # CSS's nth-child functionality lets you pick all follower children
    for group in itertools.count(start=1, step=12):     # Step through 12 at a time to scroll follower list
        for follower_index in range(group, group + 12):
            yield waiter.find_element(browser, follower_css.format(follower_index)).text

        # Keep last element from going stale (aka make sure the scrolling view doesn't forget who the last follwer was)
        last_follower = waiter.find_element(browser, follower_css.format(follower_index))   
        browser.execute_script("arguments[0].scrollIntoView()", last_follower)

def navigateToFollowers(browser): 
    print("\nGathering your followers list", end = "")
    followerHREF = "/" + userName + "/followers/" 
    totalFollowerCount = WebDriverWait(browser, WAIT_TIME_GLOBAL).until(EC.presence_of_element_located((By.XPATH, '//li/a[text()=" followers"]/span'))).text
    WebDriverWait(browser, WAIT_TIME_GLOBAL).until(EC.element_to_be_clickable((By.XPATH, '//a[@href="'+followerHREF+'"]'))).click() 
    global followerList 
    followerList = [] 
    for count, follower in enumerate(obtainList(browser)):
        print(".", end = "")
        followerList.append(follower)
        if count >= int(totalFollowerCount) - 1:
            break 
    browser.find_element_by_xpath("/html/body/div[5]/div/div/div[1]/div/div[2]/button").click()     # close out of hover list
    navigateToFollowing(browser)


def navigateProfile(browser): # User has definitely logged in at this point. These elements exist for all users, so no error handling is needed
    print("\nNavigating to your profile...\n")
    WebDriverWait(browser, WAIT_TIME_GLOBAL).until(EC.element_to_be_clickable((By.XPATH, "//*[@id='react-root']/section/nav/div[2]/div/div/div[3]/div/div[5]/span"))).click()
    WebDriverWait(browser, WAIT_TIME_GLOBAL).until(EC.element_to_be_clickable((By.XPATH, "//*[@id='react-root']/section/nav/div[2]/div/div/div[3]/div/div[5]/div[2]/div[2]/div[2]/a[1]"))).click()
    navigateToFollowers(browser) 


def attemptLogin(userName, passWord, browser): 
    try:  # Many things can go wrong in login attempt, hence try except block (in case the world explodes?!?!)
        print("An automated browser will be opened. You may keep it in the background but DO NOT MINIMZE IT.\nPlease do not interfere with it while the program is running\n")
        print('\nEntering credentials...\n')
        WebDriverWait(browser, WAIT_TIME_GLOBAL).until(EC.element_to_be_clickable((By.XPATH, "//input[@name='username']"))).send_keys(userName)
        browser.find_element_by_xpath("//input[@name='password']").send_keys(passWord)
        browser.find_element_by_xpath("//button/div[text()='Log In']").click()

        try:    # Monitor to see if login failed via slfErrorAlert element dynamically loaded
            WebDriverWait(browser, 5).until(EC.presence_of_element_located((By.ID, "slfErrorAlert")))
            browser.delete_all_cookies()
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
    global userName            # We will use the userName in many functions
    print("\nWelcome to instaFollow. This program will automate the process of comparing your followers & following list on Instagram\n")
    print("\nThis program will not share any data collected. The source code is available at https://github.com/hannad4/instaFollow\n\n")    

    userName = input("\nEnter your instagram username. This is case sensitive:\n")
    passWord = getpass.getpass("\nEnter your password. This will be used to log into your Instagram and will not be shared anywhere else. For privacy, typing your password will not move the cursor or show characters:\n")

    # Enabling experimental options to allow for a persistent browser to exist (but minimized) for the user even if program terminated
    chrome_options = Options() 
    chrome_options.add_experimental_option("detach", True)
    browser = webdriver.Chrome(options=chrome_options, executable_path=ChromeDriverManager().install())    
    browser.get("https://www.instagram.com/")
    attemptLogin(userName, passWord, browser)


if __name__ == "__main__":
    WAIT_TIME_GLOBAL = 10
    main()