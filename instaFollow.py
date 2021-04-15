# Things to note: 
# 1. Instagram dynamically assigns class names to elements and therefore shouldn't be used for driver filtering
# 2. It is important to utilize Expected Conditions to account for the dynamic loading behavior of Instagram

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC   
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

import os    # Utilized only for knowing which command to use for clearing terminal (easy viewing for noobs)
import getpass  # Utilized only for obtaining the users password without showing it out in the open
import itertools # Utilized only for iteration through scraping process  
import gc       # Utilied only for memory cleanup at the end of the program for a more clean termination

def cleanClose():
    greenPrint("\nThanks for using instaFollow.\n")
    if input('\33[32m' + "Press [Enter] to exit\n" + '\033[0m'):
        gc.collect()
        quit()

def listCompare():
    greenPrint("\n\nComparing Lists now\n")
    notFollowing = list(set(followerList) - set(followingList))  # These people follow you, but you do not follow them back 
    notFollower = list(set(followingList) - set(followerList))  # You are following these people, but they are not following you back
    match = list(set(followerList) & set(followingList)) # These people are on both lists (the good peeps)
    greenPrint("\nThis is the final list of people who follow you, but you do not follow them back:\n\n" + ' || '.join(notFollowing) + "\n")
    greenPrint("\nThis is the final list of people that you are following, but they do not follow you back:\n\n" + ' || '.join(notFollower) + "\n")
    greenPrint("\nThis is the final list of people who follow you, & you follow them back:\n\n" + ' || '.join(match) + "\n")
    writeToFile = input('\33[45m' + "\nDo you want to write these results to a text file? Y/N\n" + '\033[0m')
    if(writeToFile.upper() == "YES" or writeToFile.upper() == "Y"):
        greenPrint("\nThe file will be located in the same location as this program. It is titled 'instaResults.txt'\n")
        instaResults = open("instaResults.txt", "w")

        instaResults.write("List 1 - People who follow you, but you do not follow them back:\n\n")
        for count, following in enumerate(notFollowing):
            instaResults.write(("{:02d}: {}\n".format(count+1, following)))
        
        instaResults.write("\n=================================\n\nList 2 - People that you are following, but they do not follow you back:\n\n")
        for count, follower in enumerate(notFollower):
            instaResults.write(("{:02d}: {}\n".format(count+1, follower)))

        instaResults.write("\n=================================\n\nList 3 - These people follow you, and you follow them:\n\n")
        for count, matchingUser in enumerate(match):
            instaResults.write(("{:02d}: {}\n".format(count+1, matchingUser)))

        instaResults.close()
        cleanClose()

    else:
        cleanClose()

def navigateToFollowing(browser):
    print('\33[32m' + "\nGathering your following list" + '\033[0m', end = "")
    followingHREF = "/" + userName + "/following/"
    totalFollowingCount = WebDriverWait(browser, WAIT_TIME_GLOBAL).until(EC.presence_of_element_located((By.XPATH, '//li/a[text()=" following"]/span'))).text
    WebDriverWait(browser, WAIT_TIME_GLOBAL).until(EC.element_to_be_clickable((By.XPATH, '//a[@href="'+followingHREF+'"]'))).click() 
    global followingList 
    followingList = [] 
    for count, following in enumerate(obtainList(browser)):
        print('\33[32m' + "." + '\033[0m', sep=' ', end='', flush=True)
        followingList.append(following)
        if count >= int(totalFollowingCount) - 1:
            break 
    browser.delete_all_cookies()
    browser.quit()
    listCompare(); 

def obtainList(browser): 
    follower_css = "ul div li:nth-child({}) a.notranslate"  # CSS's nth-child functionality lets you pick all follower children
    global follower_index   # have to make this global to avoid warning about possibleUnboundVariable when assigning last_follower
    for group in itertools.count(start=1, step=12):     # Step through 12 at a time to scroll follower list
        for follower_index in range(group, group + 12):
            yield WebDriverWait(browser, WAIT_TIME_GLOBAL).until(EC.presence_of_element_located((By.CSS_SELECTOR, follower_css.format(follower_index)))).text
            # yield waiter.find_element(browser, follower_css.format(follower_index)).text

        # Keep last element from going stale (aka make sure the scrolling view doesn't forget who the last follwer was)
        last_follower = WebDriverWait(browser, WAIT_TIME_GLOBAL).until(EC.presence_of_element_located((By.CSS_SELECTOR, follower_css.format(follower_index))))     
        browser.execute_script("arguments[0].scrollIntoView()", last_follower)

def navigateToFollowers(browser): 
    print('\33[32m' + "\nGathering your followers list" + '\033[0m', end = "")
    followerHREF = "/" + userName + "/followers/" 
    totalFollowerCount = WebDriverWait(browser, WAIT_TIME_GLOBAL).until(EC.presence_of_element_located((By.XPATH, '//li/a[text()=" followers"]/span'))).text
    WebDriverWait(browser, WAIT_TIME_GLOBAL).until(EC.element_to_be_clickable((By.XPATH, '//a[@href="'+followerHREF+'"]'))).click() 
    global followerList 
    followerList = [] 
    for count, follower in enumerate(obtainList(browser)):
        print('\33[32m' + "." + '\033[0m', sep=' ', end='', flush=True)
        followerList.append(follower)
        if count >= int(totalFollowerCount) - 1:
            break 
    browser.find_element_by_xpath("/html/body/div[5]/div/div/div[1]/div/div[2]/button").click()     # close out of hover list
    navigateToFollowing(browser)


def navigateProfile(browser, userName): # User has definitely logged in at this point. These elements exist for all users, so no error handling is needed
    greenPrint("\nNavigating to your profile...\n")
    #============METHOD 1 (OLD METHOD) - MANUALLY CLICK ON USER PROFILE ON EXISTING SITE ====================#
    # WebDriverWait(browser, WAIT_TIME_GLOBAL).until(EC.element_to_be_clickable((By.XPATH, "//*[@id='react-root']/section/nav/div[2]/div/div/div[3]/div/div[5]/span"))).click()
    # WebDriverWait(browser, WAIT_TIME_GLOBAL).until(EC.element_to_be_clickable((By.XPATH, "//*[@id='react-root']/section/nav/div[2]/div/div/div[3]/div/div[5]/div[2]/div[2]/div[2]/a[1]"))).click()


    #===========METHOD 2 (BETTER METHOD) - NAVIGATE BROWSER TO INSTAGRAM LINK DIRECTLY. INSTAGRAM COOKIES/SESSION KEEPS USER FROM HAVING TO RE-LOGIN==#
    newLink = "https://www.instagram.com/" + userName
    browser.get(newLink)

    navigateToFollowers(browser) 


def attemptLogin(userName, passWord, browser): 
    try:  # Many things can go wrong in login attempt, hence try except block (in case the world explodes?!?!)
        greenPrint('\nEntering credentials...\n')
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
            greenPrint("\nThe login info you entered was incorrect\n")
            main()
        except:     # Assuming no slfErrorAlert loaded means login credentials accepted
            greenPrint("\nLogged in successfully\n")
            navigateProfile(browser, userName)

    except Exception as e:  # If something went wrong, this exception block will catch it & land the program gently instead of a messy crash
        greenPrint("\nSomething went wrong. The program has been halted\n")
        greenPrint("\nYou can provide the following error message (if available) to the developer:\n")
        greenPrint("\n" + str(e) + "\n")         
        return

def greenPrint(message):
    CGREEN = '\33[32m'
    CEND = '\033[0m'
    print(CGREEN + message + CEND)
    return


def main(): 
    global userName            # We will use the userName in many functions
    os.system("")              # Hack to make Windows command prompt show color text output
    
    greenPrint("\nWelcome to instaFollow. This program will automate the process of comparing your followers & following list on Instagram\n")
    greenPrint("\nAll data collected by this program is flushed upon termination, and will not be shared with anyone. The source code is available at https://github.com/hannad4/instaFollow\n")    

    userName = input('\33[45m' + "Enter your instagram username. This is case sensitive:\n" + '\033[0m')
    passWord = getpass.getpass('\33[45m' + "\nEnter your password. This will be used to log into your Instagram and will not be shared anywhere else. For privacy, typing your password will not move the cursor or show characters:\n" + '\033[0m')

    greenPrint("\nAn automated browser will be opened. You may keep it in the background but DO NOT MINIMZE IT.\n\nPlease do not interfere with it while the program is running\n")
    chrome_options = Options()
    chrome_options.add_experimental_option("detach", True)
    chrome_options.add_argument("--incognito")
    browser = webdriver.Chrome(executable_path=ChromeDriverManager().install()) 
    
    browser.delete_all_cookies()
    browser.get("https://www.instagram.com/")
    attemptLogin(userName, passWord, browser)


if __name__ == "__main__":
    WAIT_TIME_GLOBAL = 10
    main()