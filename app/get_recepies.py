import time

import pyautogui
from message_sender import send_text
board_path = r'../knowledge_base/task_board'
board_cooking = f"{board_path}/base_locators"
confidence = 0.7
recipy_temp = f"{board_cooking}/task_board.png"


def search_tasks(recipy):
    while True:
        time.sleep(5)
        try:
            button = pyautogui.locateCenterOnScreen(recipy, confidence=confidence)
        except Exception as err:
            button = False
            print("Доска задач не обнаружена:", err)
        if button:
            return "Фаза 1\n Доска задач обнаружена\n Ищём задачи"
    #return "Фаза 1\n подойди к доске задач\n Доска задач не найдена"


send_text(search_tasks(recipy_temp))






