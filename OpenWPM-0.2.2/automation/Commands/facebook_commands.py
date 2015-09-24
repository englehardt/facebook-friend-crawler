from selenium.common.exceptions import NoSuchElementException
from bs4 import BeautifulSoup
import time
import os
import codecs

from utils.webdriver_extensions import scroll_to_bottom, wait_and_find

def login(webdriver, username_str, password_str, browser_params):
    try:
        form = wait_and_find(webdriver, 'id', 'email', timeout=5, check_iframes=False)
        form.clear()
        form.send_keys(username_str)
        form = webdriver.find_element_by_id('pass')
        form.send_keys(password_str)
        try:
            bttn = webdriver.find_element_by_id('u_0_n')
            bttn.click()
        except NoSuchElementException:
            bttn = webdriver.find_element_by_id('u_0_0')
            bttn.click()
    except NoSuchElementException:
        print "We are already logged in..."

def extract_friends(user, username_str, password_str, webdriver, browser_params):
    time.sleep(1)
    
    try:
        form = webdriver.find_element_by_id('pass')
        login(webdriver, username_str, password_str, browser_params)
        time.sleep(1)
    except NoSuchElementException:
        pass

    # Scroll to bottom (infinite scroll)
    page_len = 0
    while len(webdriver.page_source) > page_len:
        page_len = len(webdriver.page_source)
        scroll_to_bottom(webdriver)
        time.sleep(0.5)

    # Use beautifulsoup since selenium is slow to parse
    friends = dict()
    html = webdriver.page_source
    soup = BeautifulSoup(html, 'lxml')
    people = soup.find_all('div', {'class':'uiProfileBlockContent'})
    for box in people:
        link = box.find_all('a')[0]
        url = link.get('href')
        name = link.text
        friends[name] = url.split('?')[0]

    # save to flat files
    root_dir = os.path.dirname(__file__)
    data_dir = os.path.realpath(root_dir + '/../../../data/fbfriends/')

    with codecs.open(data_dir + '/' + user + '.friends', 'w', encoding='utf-8') as f:
        for name, url in friends.items():
            f.write(name + ',' + url + '\n')
