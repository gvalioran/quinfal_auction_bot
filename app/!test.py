import json
import time
import pyautogui
from message_sender import send_text
from pyautogui import ImageNotFoundException

confidence = 0.7
board_path = r'../knowledge_base/task_board'
board_tasks = f"{board_path}/base_locators"
board_name = f"{board_tasks}/task_board.png"

time.sleep(5)
recipes = f"{board_path}/recipes.json"
with open(recipes, "r", encoding="utf-8") as f:
    recipes = json.load(f)
for recipy in recipes:
    button = pyautogui.locateCenterOnScreen(recipy["image"], confidence=confidence)
