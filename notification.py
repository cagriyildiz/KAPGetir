from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import TimeoutException

from time import sleep
from threading import Timer


def print_notification(notification_number, notification_url, company_code):
    print('\nYeni bir bildirim var.')
    print('Bildirim No: ', notification_number)
    print('Bildirim URL: ', notification_url)
    print('Hisse Kodu: ', company_code)


def listen_notifications(driver):
    try:
        new_notification = WebDriverWait(driver, 86400).until(
            ec.visibility_of_element_located((By.CLASS_NAME, 'newNotifications'))
        )

        try:
            previous_notification_order = WebDriverWait(driver, 2).until(
                ec.visibility_of_element_located((By.CSS_SELECTOR, '.notifications-row > a'))
            ).text
            print('previous notification number: ', previous_notification_order)
        except TimeoutException:
            previous_notification_order = 0
            print('no previous notification found.')
        finally:
            ActionChains(driver).click(new_notification).perform()
            sleep(2)

        notification_list = driver.find_elements_by_tag_name('disclosure-list-item')
        for notification in reversed(notification_list):
            notification_order = notification.get_attribute('item-order')
            if notification_order != previous_notification_order:
                notification_id = notification.find_element_by_class_name('_12').get_attribute('href')
                stock_code = notification.find_element_by_css_selector('._3 span').get_attribute('title')
                print_notification(notification_order, notification_id, stock_code)
            else:
                break
    except TimeoutException:
        print('no new notification found in 24 hours.')
    finally:
        listen_notifications(driver)


web_driver = webdriver.Firefox()
web_driver.get('http://www.kap.org.tr')

listen_notifications(web_driver)

'''
filterButton = driver.find_element_by_id('Filtre')
ActionChains(driver).click(filterButton).perform()

rightArrow = WebDriverWait(driver, 2500).until(
    EC.visibility_of_element_located((By.ID, 'RightButton'))
)
ActionChains(driver).move_to_element(rightArrow).click(rightArrow).perform()

sleep(1)

doFilterButton = WebDriverWait(driver, 2500).until(
    EC.visibility_of_element_located((By.ID, 'disclosureFilterButton'))
)

#doFilterButton = driver.find_element_by_id('disclosureFilterButton')
ActionChains(driver).move_to_element(doFilterButton).click(doFilterButton).perform()
'''