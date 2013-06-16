from HTMLParser import HTMLParser
from lxml import etree
from requests import session
from StringIO import StringIO

USERNAME = '1927907@ThomsonONESolution'
PASSWORD = '5KL54kEWz2'
URL = 'https://www.streetevents.com/login.aspx'

payload = {
    'post': 'true',
    'uname': USERNAME,
    'pwd': PASSWORD,
    'rempass': 'OFF',
    'Destinations': ''
}

with session() as c:
    c.post(url=URL, data=payload)
    response = c.get('https://www.streetevents.com/transcript/ListView.aspx')
    html = etree.parse(StringIO(response.text), parser=etree.HTMLParser())
    input_list = html.findall('//input')
    for each in input_list:
        print each.attrib.get('name')