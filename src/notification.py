from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import TimeoutException

import logging
from time import sleep


ONE_DAY = 86400


def get_previous_notification_order(driver):
    element = driver.find_elements_by_css_selector('#noDisclosuresToShow:not(.ng-hide)')
    previous_notifications_present = len(element) == 0
    if previous_notifications_present:
        notification_order = driver.find_element_by_css_selector('.notifications-row > a').text
    else:
        logging.info('LOG: no previous notification found')
        notification_order = 0

    logging.info('LOG: previous notification number: ', notification_order)
    return notification_order


def get_new_notifications(driver, previous_notification_number):
    notification_list = driver.find_elements_by_tag_name('disclosure-list-item')
    uppermost_notification_number = notification_list[0].get_attribute('item-order')
    length = int(uppermost_notification_number) - int(previous_notification_number)
    return notification_list[0:length]


def print_notification(notification_number, notification_url, company_code):
    print('\nYeni bir bildirim var.')
    print('Bildirim No: ', notification_number)
    print('Bildirim URL: ', notification_url)
    print('Hisse Kodu: ', company_code)


def listen_notifications(driver):
    try:
        new_notification = WebDriverWait(driver, ONE_DAY).until(
            ec.visibility_of_element_located((By.CLASS_NAME, 'newNotifications'))
        )
        previous_notification_order = get_previous_notification_order(driver)
        ActionChains(driver).click(new_notification).perform()
        notifications = get_new_notifications(driver, previous_notification_order)
        for notification in reversed(notifications):
            notification_order = notification.get_attribute('item-order')
            notification_id = notification.find_element_by_class_name('_12').get_attribute('href')
            stock_code = notification.find_element_by_css_selector('._3 span').get_attribute('title')
            print_notification(notification_order, notification_id, stock_code)
    except TimeoutException:
        logging.info('LOG: no new notification found in 24 hours')
    finally:
        listen_notifications(driver)


web_driver = webdriver.Firefox()
web_driver.get('http://www.kap.org.tr')

listen_notifications(web_driver)
