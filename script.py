import time
import mailtrap as mt
import smtplib
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

url = 'https://www.hapimag.com/en-gb/marketplace/shares/'
rejectButtonSelector = '#onetrust-reject-all-handler'
submitButtonSelector = '#submit'
usernameSelector = '#username'
passwordSelector = '#password'
latestOfferId = '.MuiGrid-item > h6:first-child'
sharesInEuro = '[test-data*=sharesPointsLabel]:first-child'
pointsInEuro = 'p[test-data*=sharesPointsLabel]:first-child'

chrome_options = Options()
chrome_options.add_experimental_option("detach", True)

browser = webdriver.Chrome(options=chrome_options, service=Service(ChromeDriverManager().install()))
browser.get(url)

def init():
    latestOffer = 0

    time.sleep(10)

    rejectButton = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, rejectButtonSelector)))
    rejectButton.click()
    
    usernameInput = browser.find_element(By.CSS_SELECTOR, usernameSelector)
    usernameInput.send_keys("")
    
    passwordInput = browser.find_element(By.CSS_SELECTOR, passwordSelector)
    passwordInput.send_keys('')

    browser.find_element(By.CSS_SELECTOR, submitButtonSelector).click()
    
    time.sleep(12)
    
    def sendNotification(latestid, euro, point):
        smtp = smtplib.SMTP('smtp.gmail.com', 587)
        smtp.starttls()
        smtp.login("", "")

        message = f'latest offer -> {latestid}, \n shares in euro -> {euro}, \n points in euro -> {point}'

        smtp.sendmail("", "", str(message))

        print('sent')
        smtp.quit()

    def checkLastOfferId(latest):
        latestOfferIdElement = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, latestOfferId)))
        currentLatestOffer = [int(word) for word in latestOfferIdElement.text.split() if word.isdigit()][0]
        
        if latest != 0 and int(currentLatestOffer) > int(latest):
            sharesInEuroElement = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, sharesInEuro)))
            pointsInEuroElement = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, pointsInEuro)))
            sharesInEuroText = sharesInEuroElement.text
            pointsInEuroText = pointsInEuroElement.text

            sendNotification(latest, sharesInEuroText, pointsInEuroText)

        latest = currentLatestOffer
        
        return latest

    while True:
        time.sleep(2)
        browser.refresh()
        time.sleep(20)

        latestOffer = checkLastOfferId(latestOffer)
        print(latestOffer)
        
        time.sleep(2)

init()

while True:
    pass
