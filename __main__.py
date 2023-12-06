#!/usr/bin/env python

# Developed by Michael Orozco
# iBit IT
# Start dev: 10/16/2015 11:38pm
# End dev: 10/17/2015 1:45am

# from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
# from selenium.webdriver.firefox.firefox_profile import FirefoxProfile
# from selenium.webdriver.common.action_chains import ActionChains
import sys, argparse, string, ctypes, os, re
import urllib.request, urllib.parse, urllib.error, urllib.request, urllib.error, urllib.parse, http.cookiejar, http.client
import http.cookiejar, time, base64

from os import path
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException

from pyvirtualdisplay import Display
import spintax

class craigslistBot:
    def debug(self, inString):
        print((" [LOG] {BOT} - %s" % inString.encode('utf-8').strip()),flush=True)

    def __init__(self, loginEmail = "", loginPass = "", contactNumber = "", contactName = "", postTitle = "", postCode = "", postContentFile = "", waitTime = 10):
        self.display = ""

        if not os.name == 'nt':
            self.display = Display(visible=0,size=(800,600))
            self.display.start()

        self.options=Options()
        self.options.add_argument("--headless")
        self.client        = webdriver.Firefox(options=self.options)
        self.isLoggedIn    = False
        self.loginEmail    = loginEmail
        self.loginPass     = loginPass
        self.contactNumber = contactNumber
        self.contactName   = contactName
        self.postTitle     = postTitle
        self.postCode      = postCode
        self.postContent   = postContentFile
        self.waitTime      = waitTime

    def __del__(self):
        if not os.name == 'nt':
            self.display.stop()

        self.client.quit()
        return 0

    def login(self):
        self.debug("Navigating to craigslist login")
        self.client.get("https://accounts.craigslist.org/login")
        self.debug("Logging in")
        self.client.find_element(By.NAME, "inputEmailHandle").send_keys(self.loginEmail)
        self.client.find_element(By.NAME, "inputPassword").send_keys(self.loginPass)
        self.client.find_element(By.CLASS_NAME, "accountform-btn").click()

        try:
            self.client.find_element(By.CSS_SELECTOR,'.tab')
        except NoSuchElementException:
            self.debug("Not logged in")
            return
        self.debug("Logged in")
        self.isLoggedIn = True

    def createPost(self):
        if not self.isLoggedIn:
            return 0

        self.debug("Navigating to post page")
        self.client.get("https://orlando.craigslist.org/search/fua")
        self.client.find_element(By.CLASS_NAME,"cl-goto-post").click()
        time.sleep(self.waitTime)
        self.client.find_elements(By.CLASS_NAME,"start-of-grouping")[1].click()
        time.sleep(self.waitTime)
        self.client.find_element(By.XPATH,'//input[@type="radio" and @value="141"]').click()
        time.sleep(self.waitTime)
        self.debug("Checking 'Okay to contact by phone'")
        self.client.find_element(By.CSS_SELECTOR,".show_phone_ok").click()
        time.sleep(self.waitTime)
        self.client.find_element(By.CSS_SELECTOR,".contact_phone_ok").click()
        time.sleep(self.waitTime)
        self.debug("Checking 'Okay to contact by text'")
        self.client.find_element(By.CSS_SELECTOR,".contact_text_ok").click()
        time.sleep(self.waitTime)
        self.debug("Filling in contact phone number")
        self.client.find_element(By.NAME,"contact_phone").send_keys(self.contactNumber)
        time.sleep(self.waitTime)
        self.debug("Filling in contact name")
        self.client.find_element(By.NAME,"contact_name").send_keys(self.contactName)
        time.sleep(self.waitTime)
        self.debug("Filling in post title")
        self.client.find_element(By.NAME,"PostingTitle").send_keys(spintax.parse(self.postTitle))
        time.sleep(self.waitTime)
        self.debug("Filling in zip code")
        self.client.find_element(By.ID,"postal_code").send_keys(self.postCode)
        time.sleep(self.waitTime)
        self.debug("Getting post content")
        f = open(self.postContent, "r")
        content = f.read()
        f.close()

        self.debug("Filling in post content")
        self.client.find_element(By.NAME,"PostingBody").send_keys(content)
        time.sleep(self.waitTime)
        dropdown_menu = self.client.find_element(By.ID, 'ui-id-1-button')
        dropdown_menu.click()
        wait = WebDriverWait(self.client, 10)
        option_excellent = wait.until(EC.visibility_of_element_located((By.XPATH, '//li[text()="excellent"]'))).click()

        self.debug("Checking 'Okay to contact for other offers'")
        self.client.find_element(By.CLASS_NAME,"contact_ok").click()
        time.sleep(self.waitTime)

        time.sleep(self.waitTime)
        self.debug("Clicking continue")
        self.client.find_element(By.CLASS_NAME,'submit-button').click()
        time.sleep(self.waitTime)
        self.client.find_element(By.CLASS_NAME,'continue').click()
        self.client.find_element(By.CLASS_NAME,"medium-pickbutton").click()
        self.client.find_elements(By.TAG_NAME,"label")[0].click()
        time.sleep(self.waitTime)


        self.client.find_elements(By.CLASS_NAME,"start-of-grouping")[1].click()
        self.client.find_element(By.CLASS_NAME,"pickbutton").click()
        time.sleep(self.waitTime)
        self.client.find_element(By.XPATH,'//input[@type="radio" and @value="141"]').click()
        time.sleep(self.waitTime)
        self.debug("Clicking continue")
        self.client.find_element(By.CLASS_NAME,'submit-button').click()
        time.sleep(self.waitTime)
        self.client.find_element(By.CLASS_NAME,'continue').click()

        self.client.find_element(By.CLASS_NAME,"bigbutton").click()
        self.debug("Clicking publish")
        self.client.find_element(By.CLASS_NAME,'bigbutton').click()
        time.sleep(10)
        
def main(loginEmail,loginPass,contactNumber,contactName,postTitle,postCode,postContentFile,waitTime):
    startExecTime = time.time()

    clBot = craigslistBot(loginEmail,loginPass,contactNumber,contactName,postTitle,postCode,postContentFile,waitTime)
    clBot.login()
    clBot.createPost()
    endExecTime = time.time()
    clBot.debug("Execution time: %s seconds" % int(endExecTime - startExecTime))

    print("Finished",flush=True)

    return 0


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Craigslist Poster Script")
    parser.add_argument('loginEmail',metavar='LOGINEMAIL',type=str,help='Email to use for login')
    parser.add_argument('loginPass',metavar='LOGINPASS',type=str,help='Password to use for login')
    parser.add_argument('contactNumber',metavar='CONTACTNUM',type=str,help='Contact number for post')
    parser.add_argument('contactName',metavar='CONTACTNAME',type=str,help='Contact name for post')
    parser.add_argument('postTitle', metavar='POSTTITLE', type=str, help='Title of the post to be made')
    parser.add_argument('postCode',metavar='POSTCODE',type=str,help='Zip code for post')
    parser.add_argument('postContent',metavar='POSTCONTENT',type=str, help='Path to file for post content')
    parser.add_argument('waitTime',metavar='WAITTIME',type=int,help='Time to wait in between actions (Recommend 3)')
    args = parser.parse_args()
    main(args.loginEmail,args.loginPass,args.contactNumber,args.contactName,args.postTitle,args.postCode,args.postContent,args.waitTime)

    # Test Execution
    # python {{SCRIPTNAME}} "example@example.com" "password" "123-456-7890" "Bob" "Post Title" "12345" "content.txt" 3
    # ENV CONTAINERIZED="True"
    # ENV LOGINEMAIL="PGTutoring1@proton.me"
    # ENV LOGINPASS="Exponentialm0ng00se!!"
    # ENV CONTACTNUM="123-456-7890"
    # ENV CONTACTNAME="Bob"
    # ENV POSTTITLE="Post Title101"
    # ENV POSTCODE="98104"
    # ENV POSTCONTENT="/app/content.txt"
    # ENV WAITTIME=4
    # ENV SE_OFFLINE false
        
