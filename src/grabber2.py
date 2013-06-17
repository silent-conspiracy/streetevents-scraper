from datetime import datetime
from datetime import timedelta
from lxml import html
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import cookielib
import os
import re
import time
import urllib2

pattern = re.compile('http://text\.thomsonone\.com/.*format=Text')
filename_pattern = re.compile('filename=.*\.txt')
# aspNetDisabled Forward
counter = 0
timeout = 20

time_format = '%m%d%Y'
time_format2 = ''
start_date = datetime.strptime(raw_input("Please input start date (MMDDYYYY): "), "%m%d%Y")
end_date = datetime.strptime(raw_input("Please input end date (MMDDYYYY): "), "%m%d%Y")

# Use the browser to get to the download page
browser = webdriver.Firefox()
browser.get("https://www.streetevents.com/login.aspx")
while True:
    try:
        username = browser.find_element_by_css_selector('#username')
        password = browser.find_element_by_css_selector('#password')
        break
    except:
        pass
username.send_keys('1927907@ThomsonONESolution')
password.send_keys('5KL54kEWz2')
browser.find_element_by_css_selector('#submit').click()
while browser.current_url == "https://www.streetevents.com/login.aspx":
    time.sleep(0.5)
    if counter > timeout: break;
    counter += 1

browser.get('https://www.streetevents.com/transcript/ListView.aspx')

#Always increment start_date by 1 until end_date to avoid hitting 1000 doc limit
temp_date = end_date
with open('log.txt', 'a') as log:
    while end_date >= temp_date:
        msg = "Downloading: %s" % temp_date.strftime("%m/%d/%Y")
        log.write(msg+"\n")            
        browser.execute_script('document.getElementById("filterArea_ctl01_hiddenDate").value="%s"'
                               % start_date.strftime("%m/%d/%Y"))
        browser.execute_script('document.getElementById("filterArea_ctl01_ctl00").value="%s"'
                               % start_date.strftime("%b %d, %Y"))
        browser.execute_script('document.getElementById("filterArea_ctl02_hiddenDate").value="%s"'
                               % temp_date.strftime("%m/%d/%Y"))
        browser.execute_script('document.getElementById("filterArea_ctl02_ctl00").value="%s"'
                               % temp_date.strftime("%b %d, %Y"))
        browser.find_element_by_tag_name('form').submit()
        time.sleep(2)
        while True:
            while True:
                try:
                    browser.find_element_by_css_selector("#gridTranscriptList")
                    break
                except:
                    pass
            
            # Get links by using regex and lxml
            page = html.fromstring(browser.page_source)
            link_tags = page.findall('.//*[@alt="Download a text file."]')
            links = []
            for link_tag in link_tags:
                match = pattern.search(link_tag.attrib.get('onclick'))
                if match:
                    links.append(match.group(0))
            
            # Use urllib2 to download files
            all_cookies = browser.get_cookies()
            cj = cookielib.CookieJar()
            for s_cookie in all_cookies:
                cookie = cookielib.Cookie(0, s_cookie.get('name'), s_cookie.get('value'), None, False,
                                 s_cookie.get('domain'), True, False, s_cookie.get('path'),
                                 True, s_cookie.get('secure'), s_cookie.get('expires'), True,
                                 None, None, {}, False)
                cj.set_cookie(cookie)
            opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
            
            if not os.path.exists(start_date.strftime("%m/%d/%Y")+'_'+end_date.strftime("%m/%d/%Y")):
                os.makedirs(start_date.strftime("%m/%d/%Y")+'_'+end_date.strftime("%m/%d/%Y"))
            
            for link in links:
                download = opener.open(link)
                filename = filename_pattern.findall(
                    ''.join(download.info().headers))[0].replace('filename=', '')
                with open(start_date.strftime("%m/%d/%Y")+'_'+end_date.strftime("%m/%d/%Y")+'/'+filename, 'w') as f:
                    f.write(''.join(download.readlines()))
                    counter += 1
                    msg = filename+" downloaded."
                    print msg
                    log.write(msg+"\n")
                    
            try:
                browser.find_element_by_css_selector("[class='Forward']").click()
                time.sleep(2)
            except:
                break
        msg = "End of %s with total %d files" % (temp_date.strftime("%m/%d/%Y"), counter)
        print msg
        log.write(msg+'\n')
        counter = 0
        temp_date = temp_date + timedelta(days=1)
