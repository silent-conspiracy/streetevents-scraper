from requests import session

payload = {
    'action': 'login',
    'username': USERNAME,
    'password': PASSWORD
}

with session() as c:
    c.post('http://example.com/login.php', data=payload)
    request = c.get('http://example.com/protected_page.php')
    print request.headers
    print request.text
