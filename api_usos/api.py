import json

import requests
from bs4 import BeautifulSoup
from w3lib.url import url_query_parameter
from datetime import datetime

from .auth import cas_login
from core.settings import headers
from .response import Response


def take_plan(day, days_delay, LOGIN, PASSWORD):
    result = {}
    link = 'https://usos-api.wab.edu.pl/services/tt/classgroups'
    urls_list = lessons_list(LOGIN, PASSWORD)
    if urls_list == "Login or password is wrong":
        return urls_list
    else:
        for url in urls_list:
            params = {
                'classgroup_ids': f'{url_query_parameter(url, "zaj_cyk_id")}|{url_query_parameter(url, "gr_nr")}',
                'days': days_delay,
                'start': day,
                'fields': 'start_time|end_time|name|room_number|lecturer_ids'
            }
            request = requests.get(link, params=params)
            temp_result = request.content.decode('utf-8')
            temp_result = json.loads(temp_result)
            if temp_result:
                for i in range(len(temp_result)):
                    response = Response(temp_result[i]['name'],
                                        temp_result[i]['start_time'],
                                        temp_result[i]['end_time'],
                                        temp_result[i]['room_number'],
                                        temp_result[i]['lecturer_ids'],
                                        get_lecturer_name(temp_result[i]['lecturer_ids'][0], LOGIN, PASSWORD),
                                        len(result) + 1)
                    result.update(**response.get_repr())


    if not len(result):
        return "You have no classes in this period"
    else:
        sorted_result = dict(sorted(result.items(),
                                    key=lambda x: datetime.strptime(x[1].get("start_time"), "%Y-%m-%d %H:%M:%S")))
        return sorted_result


def get_lecturer_name(lecturer_id, LOGIN, PASSWORD):
    level = 0
    plus = []
    session = cas_login(LOGIN, PASSWORD)
    if session is None:
        return "Login or password is wrong"
    else:
        link = 'https://usosweb.wab.edu.pl/kontroler.php?_action=katalog2/osoby/pokazOsobe'
        soup = BeautifulSoup(session.get(link, params={'os_id': lecturer_id}).text, features="lxml")
        result = soup.find_all("div", class_="uwb-side-defs")[0].find_all("div", class_="uwb-clearfix")
        if len(result) > 2:
            level = result[2].text.split('\n')[3].strip()
            result.pop()
        for i in range(len(result)):
            i_result = result[i].text.split('\n')[2]
            plus.append(i_result)
        if level:
            return level + ' ' + plus[0] + plus[1]
        else:
            return plus[0] + plus[1]


def lessons_list(LOGIN, PASSWORD):
    results = []
    session = cas_login(LOGIN, PASSWORD)
    if session is None:
        return "Login or password is wrong"
    else:
        link = 'https://usosweb.wab.edu.pl/kontroler.php?_action=home/index'
        soup = BeautifulSoup(session.get(link, headers=headers).text, features="lxml")
        urls = soup.find_all("ul", class_="no-bullets lista-zajec")[0].find_all("ul", class_="no-bullets inlined-list")
        for i in urls:
            list_links = i.find_all("a", href=True)
            for item in list_links:
                item_href = item.get("href")
                results.append(item_href)
        return results
