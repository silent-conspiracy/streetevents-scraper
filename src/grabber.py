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

# Search form parameters
# Date Format:  u'filterArea$ctl01$ctl00': u'Jun 16, 2013'
#               u'filterArea$ctl01$hiddenDate': u'06/16/2013'
filter_params = {
    # Hidden inputs (Programmatically obtain)
    u'__VIEWSTATE': u'',
    u'__EVENTTARGET': u'',
    u'__EVENTARGUMENT': u'',
    u'__LASTFOCUS': u'',
    
    # First row of filter options
    u'filterArea$watchlistFilter': u'0',
    u'filterArea$ctl01$ctl00': u'Jun 08, 2013',
    u'filterArea$ctl01$hiddenDate': u'06/08/2013',
    u'filterArea$ctl02$ctl00': u'Jun 16, 2013',
    u'filterArea$ctl02$hiddenDate': u'06/16/2013',
    u'filterArea$countryCodeFilter': u'ALL',
    u'filterArea$industryCodeFilter': u'0',
    u'filterArea$languageFilter': u'1',
    
    # Second row of filter
    u'filterArea$transcriptDocumentStatusFilter$Expected': u'off',
    u'filterArea$transcriptDocumentStatusFilter$Available': u'on',
    u'filterArea$briefSummaryFilter': u'on',
    
    # Third row of filter 
    u'filterArea$eventTypeFilter$ctl00': u'1089339387',
    u'filterArea$eventTypeFilter$ctl00group1': u'1074003971',
    u'filterArea$eventTypeFilter$ctl00group3': u'15302824',
    u'filterArea$eventTypeFilter$ctl00group2': u'24064',
    u'filterArea$eventTypeFilter$ctl00group8': u'8448',
    u'filterArea$eventTypeFilter$ctl00group5': u'80',
    u'filterArea$filter': u'GO',
    
    # Others
    u'siteId': u'1',
    u'companySearchText': u'',
    u'companySearchSilo': u'8',
    u'companySearchType': u'1'
}

# Regex for text download links
pattern = re.compile('["\']http://text\.thomsonone\.com/.*format=Text.*["\']')

def grab(url=URL):
    with session() as c:
        c.post(url=LOGIN_URL, data=payload)
        update_dynamic_values(session=c, url=url)
        response = c.post(url=url, data=filter_params)
        links = pattern.findall(response.text)
        print links
        print len(links)
    return response
        

def update_dynamic_values(session=None, url=URL):
    if session is None: return
    response = session.get(url)
    page = html.fromstring(response.text)
    filter_params['__VIEWSTATE'] = page.cssselect('#__VIEWSTATE').
    filter_params['__EVENTTARGET'] = page.cssselect('#__EVENTTARGET')
    filter_params['__EVENTARGUMENT'] = page.cssselect('#__EVENTARGUMENT')
    filter_params['__LASTFOCUS'] = page.cssselect('#__LASTFOCUS')
    return response