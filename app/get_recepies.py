import json
import time
import pyautogui
from message_sender import send_text
from pyautogui import ImageNotFoundException

confidence = 0.7
board_path = r'../knowledge_base/task_board'
board_tasks = f"{board_path}/base_locators"
board_name = f"{board_tasks}/task_board.png"

def search_tasks(task):
    while True:
        time.sleep(5)
        try:
            pyautogui.locateCenterOnScreen(task, confidence=confidence)
            send_text("Фаза 1\n Доска задач обнаружена\n Ищём задачи")
            search_tasks_names()
        except ImageNotFoundException:
            send_text("Фаза 1\n подойди к доске задач\n Доска задач не найдена ...")
            continue
        except Exception as err:
            print("Неожиданная ошибка:", err)
            continue


def search_tasks_names():
    while True:
        time.sleep(5)
        recipes = f"{board_path}/recipes.json"
        with open(recipes, "r", encoding="utf-8") as f:
            recipes = json.load(f)
        collect = []
        try:
            for recipy in recipes:
                button = pyautogui.locateCenterOnScreen(recipy["image"], confidence=confidence)
                if button:
                    collect.append(recipy["name"])
                    review = ", ".join(collect)
                    send_text(f"Фаза 1\n Доска задач обнаружена\n {review}")
        except ImageNotFoundException:
            continue
        except Exception as err:
            print("Неожиданная ошибка:", err)
            continue



search_tasks(board_name)





