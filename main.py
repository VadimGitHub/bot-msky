import datetime
import logging
import os
import random
import time

from dotenv import load_dotenv
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options

load_dotenv()

logging.basicConfig(filename="info.log", level=logging.INFO)
logging.basicConfig(filename="error.log", level=logging.ERROR)

COMPANY_URL = os.getenv('COMPANY_URL')


def get_date():
    today = datetime.datetime.today()
    return today.strftime("%Y-%m-%d %H:%M:%S")


def delay():
    return random.randint(
        int(os.getenv('MINUTES_FROM')),
        int(os.getenv('MINUTES_TO'))
    )


def log_info(message):
    message = get_date() + message
    logging.info(message)


def log_error(message):
    message = get_date() + message
    logging.error(message)


def main():
    log_info(": Start!\n\n")

    options = Options()
    options.add_argument("--disable-extensions")
    options.add_argument("--start-maximized")
    options.add_argument('--profile-directory=Profile 1')

    driver = webdriver.Chrome(options=options)

    driver.get(COMPANY_URL)
    driver.add_cookie({
        'name': 'msky-frontend',
        'value': os.getenv('COOKIE'),
    })
    driver.get(COMPANY_URL)

    minutes = 0
    while True:
        log_info(": Следующая проверка через " + str(minutes) + " минут\n")
        time.sleep(minutes * 60)
        minutes = delay()
        log_info(": Проверка")
        driver.refresh()

        try:
            plane_lists = driver.find_elements_by_css_selector('.plane-list-content')
            for plane_list in plane_lists:
                status_box = plane_list.find_element_by_css_selector('.row .col-sm-2')
                status = status_box.text

                index = status.lower().find('готов к вылету')
                if index == (-1):
                    log_info(": Не летим. Статус: " + status + "\n")
                    continue

                columns = plane_list.find_elements_by_css_selector('.row .col-sm-3')
                button_box = columns[1]

                try:
                    button = button_box.find_element_by_class_name('btn')
                    button.click()
                    log_info(": Самолет отправлен.\n")
                    minutes = 0

                    break
                except NoSuchElementException:
                    log_error(": Кнопка отправки не найдена\n")
                    continue
        except Exception:
            log_error(": Критическая ошибка.\n")


if __name__ == '__main__':
    main()
