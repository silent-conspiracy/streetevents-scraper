from lxml import html
import cookielib
import re
import urllib
import urllib2

# Configurations
USERNAME = '1927907@ThomsonONESolution'
PASSWORD = '5KL54kEWz2'
LOGIN_URL = 'https://www.streetevents.com/login.aspx'
URL = 'https://www.streetevents.com/transcript/ListView.aspx'

# HTTP Post formats
login_data = urllib.urlencode({
    'post': 'true',
    'uname': USERNAME,
    'pwd': PASSWORD,
    'rempass': 'OFF',
    'Destinations': ''
})

headers = [
    ('User-agent', ('Mozilla/4.0 (compatible; MSIE 6.0; '
                           'Windows NT 5.2; .NET CLR 1.1.4322)'))
]

# Filter form parameters
# Overrides the values of the fields stated below retaining other values
# Date Format:  u'filterArea$ctl01$ctl00': u'Jun 16, 2013'
#               u'filterArea$ctl01$hiddenDate': u'06/16/2013'
filter_params = {
    # First row of filter options
    u'filterArea$ctl01$ctl00': u'Jun 08, 2013',
    u'filterArea$ctl01$hiddenDate': u'06/08/2013',
    u'filterArea$ctl02$ctl00': u'Jun 16, 2013',
    u'filterArea$ctl02$hiddenDate': u'06/16/2013',
}

# Regex for text files download links and login success
pattern = re.compile('http://text\.thomsonone\.com/.*;disposition=attachment\&amp;format=Text')
login_success = re.compile('.*success=yes.*')

cj = cookielib.CookieJar()
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
opener.addheaders = headers

def login(url=LOGIN_URL):
    return login_success.match(''.join(opener.open(url, data=login_data).readlines())) is not None

def grab(url=URL):
    doc = opener.open(url)
    page = html.fromstring(''.join(doc.readlines()))
    form = fill_filter_form(html_page=page, data=filter_params)
    response = opener.open(url, data=urllib.urlencode(form.fields))
    response_text = ''.join(response.readlines())
    response_html = html.fromstring(response_text)
    response_html.iter
    links = pattern.findall(response_text)
    print links
    print len(links)
    return response_text

def fill_filter_form(html_page=None, data=filter_params):
    if html_page is None: return
    form = html_page.forms[0]
    for field in form.fields:
        if field in data:
            form.fields[field] = data[field]
    return form