import json
import time
import pyautogui
import pydirectinput
import pyperclip
from app.config import *

from app.message_sender import send_text
from pyautogui import ImageNotFoundException

import os

def search_tasks():
    collect = []
    while True:
        time.sleep(5)
        try:
            pyautogui.locateCenterOnScreen(BOARD_NAME, confidence=CONFIDENCE)
            send_text("Фаза 1\n Доска задач обнаружена\n Ищём задачи ...")
            search_tasks_names(collect)
        except ImageNotFoundException:
            send_text("Фаза 1\n подойди к доске задач\n Доска задач не найдена ...")
            continue
        except Exception as err:
            print("Неожиданная ошибка:", err)
            continue


def search_tasks_names(collect):
    while True:
        #time.sleep(5)
        recipes = f"{BOARD_PATH}/recipes.json"
        with open(recipes, "r", encoding="utf-8") as f:
            recipes = json.load(f)
        for recipy in recipes:
            try:
                recipy_text = os.path.join(BASE_DIR, recipy["image"])
                recipy_image = os.path.join(BASE_DIR, recipy["image_board"])
                recipy_text = pyautogui.locateCenterOnScreen(recipy_text, confidence=CONFIDENCE)
                recipy_image = pyautogui.locateCenterOnScreen(recipy_image, confidence=CONFIDENCE)
                if recipy_text and recipy_image:
                    if recipy["name"] not in collect and recipy["necessity"] == "True":
                        collect.append(recipy["name"])
                    review = ", ".join(collect)
                    send_text(f"Фаза 1\n Доска задач обнаружена\n {review}")
            except ImageNotFoundException:
                continue
            except Exception as err:
                print("Неожиданная ошибка:", err)
                continue
        if collect != []:
            find_auction(collect)

def find_auction(collect):
    review = ", ".join(collect)
    send_text(f"Фаза 2\n Иди на аукцион\n Корзина сформирована\n {review}")
    while True:
        time.sleep(5)
        try:
            pyautogui.locateCenterOnScreen(AUCTION_BOARD, confidence=CONFIDENCE)
            send_text(f"Фаза 2\n Аукцион найден\n Настройка аукциона\n {review} ...")
            setup_auction(collect)
        except ImageNotFoundException:
            send_text(f"Фаза 2\n Иди на аукцион\n Корзина сформирована\n {review} ...")
            continue
        except Exception as err:
            print("Неожиданная ошибка:", err)
            continue

def setup_auction(collect):
    while True:
        #time.sleep(5)
        try:
            try:
                pyautogui.locateCenterOnScreen(AUCTION_MAIN_PANEL, confidence=CONFIDENCE)
            except ImageNotFoundException:
                main_panel = pyautogui.locateCenterOnScreen(AUCTION_MAIN_PANEL_UNACTIVE, confidence=CONFIDENCE)
                pyautogui.click(main_panel)
                continue
            except Exception as err:
                print("Неожиданная ошибка:", err)
                continue
            try:
                pyautogui.locateCenterOnScreen(EVERYTHING_ITEMS, confidence=CONFIDENCE)
            except ImageNotFoundException:
                unactive_items = pyautogui.locateCenterOnScreen(EVERYTHING_ITEMS_UNACTIVE, confidence=CONFIDENCE)
                pyautogui.click(unactive_items)
                continue
            except Exception as err:
                print("Неожиданная ошибка:", err)
                continue
            pyautogui.locateCenterOnScreen(AUCTION_SEARCH_ITEMS, confidence=CONFIDENCE)
            try:
                pyautogui.locateCenterOnScreen(AUCTION_PRICE_GOAL, confidence=HIGH_CONFIDENCE, grayscale=False)
                pyautogui.locateCenterOnScreen(AUCTION_PRICE_GOAL_LOW, confidence=CONFIDENCE)
            except ImageNotFoundException:
                try:
                    price_set = pyautogui.locateCenterOnScreen(AUCTION_SET_PRICE, confidence=CONFIDENCE)
                    pyautogui.click(price_set)
                except ImageNotFoundException:
                    continue
                continue
            except Exception as err:
                print("Неожиданная ошибка:", err)
                continue
            pyautogui.locateCenterOnScreen(AUCTION_SEARCH_BUTTON, confidence=CONFIDENCE)
            buying_items(collect)
        except ImageNotFoundException:
            try:
                trash = pyautogui.locateCenterOnScreen(AUCTION_TRASH_BUTTON, confidence=CONFIDENCE)
                pyautogui.click(trash)
                continue
            except ImageNotFoundException:
                continue
        except Exception as err:
            print("Неожиданная ошибка:", err)
            continue

def buying_items(collect):
    review = ", ".join(collect)
    while True:
        time.sleep(5)
        try:
            pyautogui.locateCenterOnScreen(AUCTION_MAIN_PANEL, confidence=CONFIDENCE)
            send_text(f"Фаза 3\n Покупка предметов\n Аукцион готов\n {review} ...")
            recipes = f"{BOARD_PATH}/recipes.json"
            with open(recipes, "r", encoding="utf-8") as f:
                recipes = json.load(f)
            for recipy in recipes:
                if recipy["name"] == collect[0]:
                    send_text(f"Фаза 3\n Покупка предметов\n Покупаю\n {recipy['name']}\n {review}")
                    if buy_item(recipy, recipy["amount"]):
                        collect.pop(0)
                        review = ", ".join(collect)
                        send_text(f"Фаза 3\n Покупка предметов\n Покупаю\n {recipy['name']}\n {review}")
                        if collect == []:
                            while True:
                                send_text("Покупка предметов завершена")
                                time.sleep(30)
                    else:
                        continue

        except ImageNotFoundException:
            send_text(f"Фаза 3\n Покупка предметов\n Открой аукцион обратно\n {review} ...")
            continue
        except Exception as err:
            print("Неожиданная ошибка:", err)
            continue

def buy_item(item, item_count):
    try:
        pyautogui.locateCenterOnScreen(AUCTION_SEARCH_BUTTON, confidence=CONFIDENCE)
    except ImageNotFoundException:
        trash = pyautogui.locateCenterOnScreen(AUCTION_TRASH_BUTTON, confidence=CONFIDENCE)
        pyautogui.click(trash)
    search_items = pyautogui.locateCenterOnScreen(AUCTION_SEARCH_ITEMS, confidence=CONFIDENCE)
    x, y = search_items
    pyautogui.click(x + 120, y)
    pydirectinput.keyDown('ctrl')
    pydirectinput.press('a')
    pydirectinput.keyUp('ctrl')
    pyautogui.press('backspace')
    pyperclip.copy(item["name"])
    pydirectinput.keyDown('ctrl')
    pydirectinput.press('v')
    pydirectinput.keyUp('ctrl')
    search_button = pyautogui.locateCenterOnScreen(AUCTION_SEARCH_BUTTON, confidence=CONFIDENCE)
    pyautogui.click(search_button)
    time.sleep(1)
    find_item = pyautogui.locateCenterOnScreen(os.path.join(BASE_DIR, item["auction_image"]), confidence=CONFIDENCE)
    x, y = find_item
    pyautogui.click(x + 120, y)
    if item_count == 1:
        pass
    else:
        real_count = 0
        count = pyautogui.locateCenterOnScreen(AUCTION_COUNT, confidence=HIGH_CONFIDENCE)
        pyautogui.click(count)
        for _ in range(item_count-1):
            pydirectinput.press('right')
        for num in range(10):
            try:
                amount = os.path.join(AUCTION_PATH, "count", f"{num + 1}.png")
                pyautogui.locateCenterOnScreen(amount, confidence=HIGH_CONFIDENCE)
                real_count = num + 1
                print(f"Осталось купить {item['name']} {item_count - real_count}")
                break
            except Exception as err:
                print("Неожиданная ошибка:", err)
                continue
    buy = pyautogui.locateCenterOnScreen(BUY_BUTTON, confidence=CONFIDENCE)
    if buy:
        pyautogui.click(buy)
        return True
    else:
        return False

def start_logic():
    search_tasks()





