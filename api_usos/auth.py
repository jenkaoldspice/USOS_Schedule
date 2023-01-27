import requests
import lxml.html
from core.settings import headers


def cas_login(username, password):
    params = {'service': 'https://usosweb.wab.edu.pl/kontroler.php'}
    LOGIN_URL = 'https://usos-cas.wab.edu.pl/cas/login'

    session = requests.session()
    login = session.get(LOGIN_URL, params=params, headers=headers)

    login_html = lxml.html.fromstring(login.text)
    hidden_elements = login_html.xpath('//form//input[@type="hidden"]')
    hidden_elements.pop()
    form = {x.attrib['name']: x.attrib['value'] for x in hidden_elements}

    form['geolocation'] = ''
    form['username'] = username
    form['password'] = password

    request = session.post(LOGIN_URL, data=form, params=params)

    if request.status_code == 200:
        return session

