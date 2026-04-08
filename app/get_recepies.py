import json
import time
import pyautogui
from message_sender import send_text
from pyautogui import ImageNotFoundException

confidence = 0.7
board_path = r'../knowledge_base/task_board'
board_tasks = f"{board_path}/base_locators"
board_name = f"{board_tasks}/task_board.png"

auction_path = r'../knowledge_base/auction_locators'
auction_board = f"{auction_path}/auction_board.png"
auction_search_button = f"{auction_path}/search_button.png"
auction_trash_button = f"{auction_path}/trash_button.png"
auction_set_price = f"{auction_path}/set_price.png"
auction_prise_goal = f"{auction_path}/prise_goal.png"
auction_prise_goal_low = f"{auction_path}/prise_goal_low.png"

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
                button = pyautogui.locateCenterOnScreen(recipy["image"], confidence=confidence)
                if button:
                    if recipy["name"] not in collect:
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
    review = ", ".join(collect)
    while True:
        time.sleep(5)
        try:
            pyautogui.locateCenterOnScreen(auction_search_button, confidence=confidence)
            try:
                pyautogui.locateCenterOnScreen(auction_prise_goal, confidence=0.9, grayscale=False)
                pyautogui.locateCenterOnScreen(auction_prise_goal_low, confidence=0.7)
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
            continue
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




search_tasks(board_name)





