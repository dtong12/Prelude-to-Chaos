from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options

import time

chrome_options = Options()
#chrome_options.add_argument("--headless")
# chrome_options.add_argument('--window-size=1325x744')
chrome_options.add_argument("--start-maximized")
driver = webdriver.Chrome('./chromedriver', options = chrome_options)

# driver.get("https://sportsbook.draftkings.com/event/rafael--nadal-vs-casper-ruud/27924250")
driver.get("https://www.sofascore.com/bolt-schoolkate/uryswjkc")

# driver.save_screenshot('test.png')
driver.quit()