import csv
import json
import os.path
import time
import  re
import random
from collections import Counter
from os import write
from string import whitespace

import undetected_chromedriver as uc
from bs4 import BeautifulSoup
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC 
from selenium.webdriver.support.ui import WebDriverWait

min_delay = 1
max_delay = 6

def initialize_browser():
    """Инициализация браузера с одной сессией"""
    driver = uc.Chrome()
    driver.implicitly_wait(3)
    return driver

def scroll_to_element(driver, element):
    actions = ActionChains(driver)
    actions.move_to_element(element)
    actions.perform()

def get_url(driver, url):
    """Открытие URL в переданном браузере"""
    driver.get(url)
    time.sleep(2)


def get_hash_prof_users():
    path = '../Parser-selers/date/my_save_prof.txt'
    with open(path, 'r', encoding='utf-8') as file:
        html_content = file.read()
        soup = BeautifulSoup(html_content, 'lxml')
        elements = soup.find_all(attrs={"data-hash-user-id": True})
        users = {}
        for element in elements:
            tag_name = element.find("span", attrs={"data-marker": "name"})
            name = tag_name.text.strip() or 'UNKNOWN'
            users[name] = element['data-hash-user-id']
    return users


def extract_item_title(review_text):
    # Регулярное выражение для поиска текста после "·" (точка + пробел)
    match = re.search(r"·\s*(.+)", review_text)
    if match:
        return match.group(1).strip()
    return "Название не найдено"

def get_page_user(driver, hash_id):
    url = f'https://www.avito.ru/user/{hash_id}/profile?src=fs#open-reviews-list'
    try:
        driver.get(url)
        time.sleep(random.uniform(2, 10))  # Задержка для полной загрузки страницы
        for _ in range(3):  # Прокрутить 3 раза
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(random.uniform(2, 8))  # Ждем подгрузку
        page_source = driver.page_source
        soup = BeautifulSoup(page_source, "lxml")
        reviews = soup.select(".style-snippet-E6g8Y")
        print(f"Найдено отзывов: {len(reviews)}")
        list_reviews = []
        for review in reviews:
            review_text = review.get_text(separator="\n").strip()
            item_title = extract_item_title(review_text)
            list_reviews.append(item_title)
        top_reviews = Counter(list_reviews).most_common(3)
        print(top_reviews)
        return top_reviews
    except Exception as e:
        print(f"Ошибка при открытии {url}: {e}")


def check_file_exists():
    if not os.path.exists('data_sellers.csv'):
        with open('data_sellers.csv', 'w', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(['name', 'most_reviews'])


def initialize_data_file(file_path):
    """Проверяет существование файла JSON, если его нет, создает пустую структуру."""
    if not os.path.exists(file_path):
        with open(file_path, 'w', encoding='utf-8') as file:
            json.dump({}, file, indent=4)
        print(f"Файл {file_path} был создан.")
    else:
        print(f"Файл {file_path} уже существует.")


def load_data(file_path):
    """Загружает данные из JSON-файла."""
    with open(file_path, 'r', encoding='utf-8') as file:
        return json.load(file)

def save_data(file_path, data):
    """Сохраняет данные в JSON-файл."""
    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(data, file, indent=4, ensure_ascii=False)
        print(f"Данные сохранены в {file_path}.")

def update_user_data(data, name, reviews):
    """Обновляет или добавляет данные пользователя."""
    if name not in data:
        data[name] = {
            # "hash_id": hash_id,
            "reviews": reviews
        }
    else:
        # Обновление существующих данных (например, добавление новых отзывов)
        data[name]["reviews"] = reviews

def main():
    data_file = 'data_sellers.json'
    initialize_data_file(data_file)
    data = load_data(data_file)
    driver = initialize_browser()
    try:
        time.sleep(random.randrange(min_delay, max_delay))
        users = get_hash_prof_users()
        print(f"Найдено пользователей: {len(users)}")
        for name, hash_id in users.items():
            print(f"Открываю профиль: {name} ({hash_id})")
            reviews = get_page_user(driver, hash_id)
            update_user_data(data, name, reviews)
            save_data(data_file, data)
    finally:
        driver.quit()


if __name__ == '__main__':
    main()