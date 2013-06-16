from HTMLParser import HTMLParser
from lxml import html
from requests import session
from StringIO import StringIO
import re

USERNAME = '1927907@ThomsonONESolution'
PASSWORD = '5KL54kEWz2'
LOGIN_URL = 'https://www.streetevents.com/login.aspx'
URL = 'https://www.streetevents.com/transcript/ListView.aspx'

payload = {
    'post': 'true',
    'uname': USERNAME,
    'pwd': PASSWORD,
    'rempass': 'OFF',
    'Destinations': ''
}

headers = {
    'content-type': "application/x-www-form-urlencoded; charset=utf-8"
}

# Search form parameters
# Date Format:  u'filterArea$ctl01$ctl00': u'Jun 16, 2013'
#               u'filterArea$ctl01$hiddenDate': u'06/16/2013'
filter_params = {
    # First row of filter options
    u'filterArea$ctl01$ctl00': u'Jun 08, 2013',
    u'filterArea$ctl01$hiddenDate': u'06/08/2013',
    u'filterArea$ctl02$ctl00': u'Jun 16, 2013',
    u'filterArea$ctl02$hiddenDate': u'06/16/2013',
}

# Regex for text download links
pattern = re.compile('["\']http://text\.thomsonone\.com/.*format=Text.*["\']')

def grab(url=URL):
    with session() as c:
        c.post(url=LOGIN_URL, data=payload)
        form = fill_filter_form(session=c, url=url, data=filter_params)
        print dict(form.fields)
        response = c.post(url=url, data=dict(form.fields), headers=headers)
        links = pattern.findall(response.text)
        print links
        print len(links)
    return response
        

def fill_filter_form(session=None, url=URL, data=None):
    if session is None: return
    response = session.get(url)
    form_page = html.fromstring(response.text)
    form = form_page.forms[0]
    for field in form.fields:
        if field in data:
            form.fields[field] = data[field]
    return form