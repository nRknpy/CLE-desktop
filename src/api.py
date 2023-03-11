from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import requests
import pickle
import os
from datetime import datetime
from urllib import parse
import copy

from const import CACHE_DIR, COOKIES_PATH

def selenium_client():
    if not os.path.exists(COOKIES_PATH):
        raise RuntimeError('NonCookiesError')

    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_experimental_option('detach', True)
    driver = webdriver.Chrome(options=options)
    cookies = pickle.load(open(COOKIES_PATH, 'rb'))
    driver.get('https://www.cle.osaka-u.ac.jp')
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

def get_content_html(course_id):
    # driver = copy.deepcopy(base_driver)
    driver = selenium_client()
    driver.get(f'https://www.cle.osaka-u.ac.jp/webapps/blackboard/content/listContent.jsp?course_id={course_id}')
    html = driver.page_source
    driver.quit()
    soup = BeautifulSoup(html, "html.parser")
    elem = soup.find(id='content_listContainer')
    if(elem == None):
        if soup.find(id='pageBanner') != None:
            return True, f'<h4><a href=\"https://www.cle.osaka-u.ac.jp/webapps/blackboard/content/listContent.jsp?course_id={course_id}">https://www.cle.osaka-u.ac.jp/webapps/blackboard/content/listContent.jsp?course_id={course_id}</a><h4><br><p>現在，このページの表示は実装されていません．リンクから直接確認してください．</p>'
        return False, f'<h4><a href=\"https://www.cle.osaka-u.ac.jp/webapps/blackboard/content/listContent.jsp?course_id={course_id}">https://www.cle.osaka-u.ac.jp/webapps/blackboard/content/listContent.jsp?course_id={course_id}</a><h4><br><p>表示するコンテンツがありません</p>'
    ext_elems = []
    try:
        ext_elems.extend(elem.find_all('script'))
        ext_elems.extend(elem.find_all(class_='item_icon'))
        ext_elems.extend(elem.find_all(class_='cmimg editmode jsInit cmimg-hide'))
        ext_elems.extend(elem.find_all(class_='reorder editmode hideme'))
        for e in ext_elems: e.extract()
        elem.prettify()
        return False, (f'<h4><a href=\"https://www.cle.osaka-u.ac.jp/webapps/blackboard/content/listContent.jsp?course_id={course_id}">https://www.cle.osaka-u.ac.jp/webapps/blackboard/content/listContent.jsp?course_id={course_id}</a><h4>'
                       + str(elem)
                       .replace('/bbcswebdav/', 'https://www.cle.osaka-u.ac.jp/bbcswebdav/')
                       .replace('/webapps/', 'https://www.cle.osaka-u.ac.jp/webapps/'))
    except:
        return True, f'<h4><a href=\"https://www.cle.osaka-u.ac.jp/webapps/blackboard/content/listContent.jsp?course_id={course_id}">https://www.cle.osaka-u.ac.jp/webapps/blackboard/content/listContent.jsp?course_id={course_id}</a><h4><br><p>現在，このページの表示は実装されていません．リンクから直接確認してください．</p>'

def _get_content_html(url, res):
    driver = selenium_client()
    driver.get(url)
    elem = WebDriverWait(driver, 100).until(
        EC.presence_of_element_located((By.ID, "content_listContainer"))
    )
    html = elem.get_attribute('outerHTML')
    res.append(html)
