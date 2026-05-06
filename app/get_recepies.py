import json
import time
import pyautogui
import pydirectinput
import pyperclip

from app.message_sender import send_text
from pyautogui import ImageNotFoundException

import os

confidence = 0.7
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

board_path = os.path.join(BASE_DIR, "knowledge_base", "task_board")
board_tasks = f"{board_path}/base_locators"
board_name = f"{board_tasks}/task_board.png"

auction_path = os.path.join(BASE_DIR, "knowledge_base", "auction_locators")
auction_board = f"{auction_path}/auction_board.png"
auction_search_button = f"{auction_path}/search_button.png"
auction_trash_button = f"{auction_path}/trash_button.png"
auction_set_price = f"{auction_path}/set_price.png"
auction_prise_goal = f"{auction_path}/prise_goal.png"
auction_prise_goal_low = f"{auction_path}/prise_goal_low.png"
auction_main_panel = f"{auction_path}/auction_main_panel.png"
auction_main_panel_unactive = f"{auction_path}/auction_main_panel_unactive.png"
auction_everything_items = f"{auction_path}/auction_everything_items.png"
auction_everything_items_unactive = f"{auction_path}/auction_everything_items_unactive.png"
auction_search_items = f"{auction_path}/auction_search_items.png"
buy_button = f"{auction_path}/buy_button.png"
auction_count = f"{auction_path}/count.png"

def search_tasks(task):
    collect = []
    while True:
        time.sleep(5)
        try:
            pyautogui.locateCenterOnScreen(task, confidence=confidence)
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
        time.sleep(5)
        recipes = f"{board_path}/recipes.json"
        with open(recipes, "r", encoding="utf-8") as f:
            recipes = json.load(f)
        for recipy in recipes:
            try:
                button = pyautogui.locateCenterOnScreen(os.path.join(BASE_DIR, recipy["image"]), confidence=confidence)
                if button:
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
            pyautogui.locateCenterOnScreen(auction_board, confidence=confidence)
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
        time.sleep(5)
        try:
            try:
                pyautogui.locateCenterOnScreen(auction_main_panel, confidence=confidence)
            except ImageNotFoundException:
                main_panel = pyautogui.locateCenterOnScreen(auction_main_panel_unactive, confidence=confidence)
                pyautogui.click(main_panel)
                continue
            except Exception as err:
                print("Неожиданная ошибка:", err)
                continue
            try:
                pyautogui.locateCenterOnScreen(auction_everything_items, confidence=confidence)
            except ImageNotFoundException:
                unactive_items = pyautogui.locateCenterOnScreen(auction_everything_items_unactive, confidence=confidence)
                pyautogui.click(unactive_items)
                continue
            except Exception as err:
                print("Неожиданная ошибка:", err)
                continue
            pyautogui.locateCenterOnScreen(auction_search_items, confidence=confidence)
            try:
                pyautogui.locateCenterOnScreen(auction_prise_goal, confidence=0.9, grayscale=False)
                pyautogui.locateCenterOnScreen(auction_prise_goal_low, confidence=confidence)
            except ImageNotFoundException:
                try:
                    price_set = pyautogui.locateCenterOnScreen(auction_set_price, confidence=confidence)
                    pyautogui.click(price_set)
                except ImageNotFoundException:
                    continue
                continue
            except Exception as err:
                print("Неожиданная ошибка:", err)
                continue
            pyautogui.locateCenterOnScreen(auction_search_button, confidence=confidence)
            buying_items(collect)
        except ImageNotFoundException:
            try:
                trash = pyautogui.locateCenterOnScreen(auction_trash_button, confidence=confidence)
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
            pyautogui.locateCenterOnScreen(auction_main_panel, confidence=confidence)
            send_text(f"Фаза 3\n Покупка предметов\n Аукцион готов\n {review} ...")
            recipes = f"{board_path}/recipes.json"
            with open(recipes, "r", encoding="utf-8") as f:
                recipes = json.load(f)
            for recipy in recipes:
                if recipy["name"] == collect[0]:
                    send_text(f"Фаза 3\n Покупка предметов\n Покупаю\n {recipy['name']}\n {review}")
                    if buy_item(recipy):
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

def buy_item(item):
    time.sleep(5)
    try:
        pyautogui.locateCenterOnScreen(auction_search_button, confidence=confidence)
    except ImageNotFoundException:
        trash = pyautogui.locateCenterOnScreen(auction_trash_button, confidence=confidence)
        pyautogui.click(trash)
    search_items = pyautogui.locateCenterOnScreen(auction_search_items, confidence=confidence)
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
    search_button = pyautogui.locateCenterOnScreen(auction_search_button, confidence=confidence)
    pyautogui.click(search_button)
    time.sleep(1)
    find_item = pyautogui.locateCenterOnScreen(os.path.join(BASE_DIR, item["auction_image"]), confidence=confidence)
    x, y = find_item
    pyautogui.click(x + 120, y)
    if item["amount"] == 1:
        pass
    else:
        count = pyautogui.locateCenterOnScreen(auction_count, confidence=confidence)
        pyautogui.click(count)
        for i in range(item["amount"]-1):
            pydirectinput.press('right')
    buy = pyautogui.locateCenterOnScreen(buy_button, confidence=confidence)
    if buy:
        pyautogui.click(buy)
        return True
    else:
        return False

def start_logic():
    search_tasks(board_name)





