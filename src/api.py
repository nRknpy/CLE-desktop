from selenium import webdriver
import requests
import pickle
import os
from datetime import datetime
from urllib import parse

from const import CACHE_DIR, COOKIES_PATH

def selenium_client():
    if not os.path.exists(COOKIES_PATH):
        raise RuntimeError('NonCookiesError')

    options = webdriver.ChromeOptions()
    options.add_experimental_option('detach', True)
    driver = webdriver.Chrome(options=options)
    cookies = pickle.load(open(COOKIES_PATH, 'rb'))
    for cookie in cookies:
        driver.add_cookie(cookie)
    return driver

def requests_client():
    if not os.path.exists(COOKIES_PATH):
        raise RuntimeError('NonCookiesError')

    session = requests.session()
    cookies = pickle.load(open(COOKIES_PATH, 'rb'))
    for cookie in cookies:
        session.cookies.set(cookie["name"], cookie["value"])
    return session

def check_auth():
    session = requests_client()
    res = session.get('https://www.cle.osaka-u.ac.jp/learn/api/v1/users/me?expand=systemRoles,insRoles')
    print(res)
    if res.status_code == 401:
        return False
    elif res.status_code != 200:
        raise RuntimeError('auth error')
    else:
        return True

def get_userinfo():
    session = requests_client()
    res = session.get('https://www.cle.osaka-u.ac.jp/learn/api/v1/users/me?expand=systemRoles,insRoles').json()
    return res

def get_homeworks():
    session = requests_client()
    date_query = datetime.now().strftime('%Y-%m-%dT%H:%M:%S.%fZ')
    query = parse.urlencode({
        'date': date_query,
        'date_compare': 'lessOrEqual',
        # 'date_compare': 'greaterOrEqual',
        'includeCount': 'true',
        'limit': 50,
        'offset': 0,
    }, safe=':')
    print(query)
    homeworks = session.get('https://www.cle.osaka-u.ac.jp/learn/api/v1/calendars/dueDateCalendarItems?' + query).json()
    print(homeworks)
    if homeworks['results']:
        output = homeworks['results']
    else:
        output = []
    return output

def get_message():
    session = requests_client()
    res = session.get('https://www.cle.osaka-u.ac.jp/institution/api/module/d47c98c8-6c12-4460-b0f4-a31060843995/resources').json()
    return res['return_body'][0]['details']['bbml']

def get_courses():
    user_id = pickle.load(open(os.path.join(CACHE_DIR, 'user-id.pkl'), 'rb'))
    session = requests_client()
    courses = session.get(f'https://www.cle.osaka-u.ac.jp//learn/api/v1/users/{user_id}/memberships').json()['results']
    course_info_list = []
    for course in courses:
        course_id = course['courseId']
        course_info = session.get(f'https://www.cle.osaka-u.ac.jp/learn/api/v1/courses/{course_id}').json()
        course_info_list.append(course_info)
    print(course_info_list)
    print(len(course_info_list))
    return course_info_list
