from requests import session
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import re

pattern = re.compile('["\']http://text\.thomsonone\.com/.*format=Text.*["\']')
counter = 0
timeout = 20
browser = webdriver.Firefox()

browser.get("https://www.streetevents.com/login.aspx")
username = browser.find_element_by_css_selector('#username')
password = browser.find_element_by_css_selector('#password')
username.send_keys('1927907@ThomsonONESolution')
password.send_keys('5KL54kEWz2')
browser.find_element_by_css_selector('#submit').click()
while browser.current_url == "https://www.streetevents.com/login.aspx":
    time.sleep(0.5)
    if counter > timeout: break;
    counter += 1

browser.get('https://www.streetevents.com/transcript/ListView.aspx')
#start_date = browser.find_element_by_css_selector('#filterArea_ctl01_hiddenDate')
#end_date = browser.find_element_by_css_selector('#filterArea_ctl02_hiddenDate')
#start_date.send_keys('06/04/2013')
#end_date.send_keys('06/16/2013')
browser.execute_script('document.getElementById("filterArea_ctl01_hiddenDate").value="06/04/2013"')
browser.execute_script('document.getElementById("filterArea_ctl01_ctl00").value="06/04/2013"')
browser.execute_script('document.getElementById("filterArea_ctl02_hiddenDate").value="06/16/2013"')
browser.find_element_by_tag_name('form').submit()
while True:
    try:
        browser.find_element_by_css_selector("#gridTranscriptList")
        break
    except:
        pass
    
links = pattern.findall(browser.page_source)
all_cookies = browser.get_cookies()
cookies = {}

for s_cookie in all_cookies:
    for key in s_cookie:
        cookies[key]=s_cookie[key]
    
with session() as c:
    a = c.get(links[0], cookies=cookies)
    print a