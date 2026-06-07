import json
import time
import os

import cv2
import dxcam
import numpy as np
import pyautogui
import pydirectinput
import pyperclip

from app.config import *
from app.message_sender import send_text
from pyautogui import ImageNotFoundException


# ============================================================
# DXCAM: DXGI → WINRT fallback
# ============================================================

def init_camera():
    for attempt in range(5):
        try:
            cam = dxcam.create(output_idx=0, backend="dxgi")
            cam.start(target_fps=30)
            time.sleep(0.2)
            if cam.get_latest_frame() is not None:
                print(f"[DXCAM] DXGI успешно (попытка {attempt+1})")
                return cam
        except Exception as e:
            print(f"[DXCAM] DXGI ошибка: {e}")
            time.sleep(0.2)

    print("[DXCAM] DXGI недоступен, переключаюсь на WINRT")

    for attempt in range(10):
        try:
            cam = dxcam.create(output_idx=0, backend="winrt")
            cam.start(target_fps=30)
            time.sleep(0.2)
            if cam.get_latest_frame() is not None:
                print(f"[DXCAM] WINRT успешно (попытка {attempt+1})")
                return cam
        except Exception as e:
            print(f"[DXCAM] WINRT ошибка: {e}")
            time.sleep(0.3)

    raise RuntimeError("DXCAM не удалось инициализировать")


camera = init_camera()


def get_frame():
    global camera
    try:
        frame = camera.get_latest_frame()
        if frame is None:
            raise Exception("DXCAM вернул None")
        return frame.copy()
    except Exception as e:
        print(f"[DXCAM] Ошибка получения кадра: {e}")
        print("[DXCAM] Перезапуск DXCAM...")
        camera = init_camera()
        frame = camera.get_latest_frame()
        return frame.copy() if frame is not None else None


# ============================================================
# locate_center_on_screen: аналог pyautogui.locateCenterOnScreen
# ============================================================

def locate_center_on_screen(path, confidence=0.8, grayscale=True, debug_name=None):
    """
    Полный аналог pyautogui.locateCenterOnScreen, но через DXCAM+OpenCV:
    - если не найдено → ImageNotFoundException
    - если найдено → (x, y) центра
    """
    frame = get_frame()
    if frame is None:
        raise ImageNotFoundException("DXCAM не дал кадр")

    if grayscale:
        template = cv2.imread(path, 0)
    else:
        template = cv2.imread(path, cv2.IMREAD_COLOR)

    if template is None:
        raise ImageNotFoundException(f"PNG не найден: {path}")

    img_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    tmpl_gray = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY) if not grayscale else template

    res = cv2.matchTemplate(img_gray, tmpl_gray, cv2.TM_CCOEFF_NORMED)
    _, max_val, _, max_loc = cv2.minMaxLoc(res)

    if debug_name:
        print(f"[MATCH] {debug_name}: {max_val:.3f}")

    if max_val < confidence:
        raise ImageNotFoundException(f"Шаблон не найден: {path}")

    h, w = tmpl_gray.shape[:2]
    x, y = max_loc
    return (x + w // 2, y + h // 2)


# ============================================================
# Фаза 1: поиск задач
# ============================================================

def search_tasks():
    collect = []
    while True:
        time.sleep(5)
        try:
            locate_center_on_screen(BOARD_NAME, confidence=CONFIDENCE, grayscale=True,
                                    debug_name="BOARD_NAME")
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
        recipes_path = f"{BOARD_PATH}/recipes.json"
        with open(recipes_path, "r", encoding="utf-8") as f:
            recipes = json.load(f)

        for recipy in recipes:
            try:
                recipy_text_path = os.path.join(BASE_DIR, recipy["image"])
                recipy_image_path = os.path.join(BASE_DIR, recipy["image_board"])

                recipy_text = locate_center_on_screen(
                    recipy_text_path,
                    confidence=CONFIDENCE,
                    grayscale=True,
                    debug_name=f"{recipy['name']}_text"
                )
                recipy_image = locate_center_on_screen(
                    recipy_image_path,
                    confidence=CONFIDENCE,
                    grayscale=True,
                    debug_name=f"{recipy['name']}_icon"
                )

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


# ============================================================
# Фаза 2: поиск аукциона и настройка
# ============================================================

def find_auction(collect):
    review = ", ".join(collect)
    send_text(f"Фаза 2\n Иди на аукцион\n Корзина сформирована\n {review}")
    while True:
        time.sleep(5)
        try:
            locate_center_on_screen(AUCTION_BOARD, confidence=CONFIDENCE, grayscale=True,
                                    debug_name="AUCTION_BOARD")
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
        try:
            try:
                locate_center_on_screen(AUCTION_MAIN_PANEL, confidence=CONFIDENCE, grayscale=True,
                                        debug_name="AUCTION_MAIN_PANEL")
            except ImageNotFoundException:
                main_panel = locate_center_on_screen(AUCTION_MAIN_PANEL_UNACTIVE, confidence=CONFIDENCE,
                                                     grayscale=True,
                                                     debug_name="AUCTION_MAIN_PANEL_UNACTIVE")
                pyautogui.click(main_panel)
                continue
            except Exception as err:
                print("Неожиданная ошибка:", err)
                continue

            try:
                locate_center_on_screen(EVERYTHING_ITEMS, confidence=CONFIDENCE, grayscale=True,
                                        debug_name="EVERYTHING_ITEMS")
            except ImageNotFoundException:
                unactive_items = locate_center_on_screen(EVERYTHING_ITEMS_UNACTIVE, confidence=CONFIDENCE,
                                                         grayscale=True,
                                                         debug_name="EVERYTHING_ITEMS_UNACTIVE")
                pyautogui.click(unactive_items)
                continue
            except Exception as err:
                print("Неожиданная ошибка:", err)
                continue

            locate_center_on_screen(AUCTION_SEARCH_ITEMS, confidence=CONFIDENCE, grayscale=True,
                                    debug_name="AUCTION_SEARCH_ITEMS")

            try:
                locate_center_on_screen(AUCTION_PRICE_GOAL, confidence=HIGH_CONFIDENCE,
                                        grayscale=False,
                                        debug_name="AUCTION_PRICE_GOAL")
                locate_center_on_screen(AUCTION_PRICE_GOAL_LOW, confidence=CONFIDENCE,
                                        grayscale=True,
                                        debug_name="AUCTION_PRICE_GOAL_LOW")
            except ImageNotFoundException:
                try:
                    price_set = locate_center_on_screen(AUCTION_SET_PRICE, confidence=CONFIDENCE,
                                                        grayscale=True,
                                                        debug_name="AUCTION_SET_PRICE")
                    pyautogui.click(price_set)
                except ImageNotFoundException:
                    continue
                continue
            except Exception as err:
                print("Неожиданная ошибка:", err)
                continue

            locate_center_on_screen(AUCTION_SEARCH_BUTTON, confidence=CONFIDENCE, grayscale=True,
                                    debug_name="AUCTION_SEARCH_BUTTON")
            buying_items(collect)

        except ImageNotFoundException:
            try:
                trash = locate_center_on_screen(AUCTION_TRASH_BUTTON, confidence=CONFIDENCE,
                                                grayscale=True,
                                                debug_name="AUCTION_TRASH_BUTTON")
                pyautogui.click(trash)
                continue
            except ImageNotFoundException:
                continue
        except Exception as err:
            print("Неожиданная ошибка:", err)
            continue


# ============================================================
# Фаза 3: покупка предметов
# ============================================================

def buying_items(collect):
    review = ", ".join(collect)
    while True:
        time.sleep(5)
        try:
            locate_center_on_screen(AUCTION_MAIN_PANEL, confidence=CONFIDENCE, grayscale=True,
                                    debug_name="AUCTION_MAIN_PANEL")
            send_text(f"Фаза 3\n Покупка предметов\n Аукцион готов\n {review} ...")

            recipes_path = f"{BOARD_PATH}/recipes.json"
            with open(recipes_path, "r", encoding="utf-8") as f:
                recipes = json.load(f)

            for recipy in recipes:
                if recipy["name"] == collect[0]:
                    remainder = recipy["amount"]
                    while remainder != 0:
                        send_text(f"Фаза 3\n Покупка предметов\n Покупаю\n {recipy['name']}\n {review}")
                        remainder = buy_item(recipy, remainder)
                    collect.pop(0)
                    review = ", ".join(collect)
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
        locate_center_on_screen(AUCTION_SEARCH_BUTTON, confidence=CONFIDENCE, grayscale=True,
                                debug_name="AUCTION_SEARCH_BUTTON")
    except ImageNotFoundException:
        trash = locate_center_on_screen(AUCTION_TRASH_BUTTON, confidence=CONFIDENCE,
                                        grayscale=True,
                                        debug_name="AUCTION_TRASH_BUTTON")
        pyautogui.click(trash)

    search_items = locate_center_on_screen(AUCTION_SEARCH_ITEMS, confidence=CONFIDENCE,
                                           grayscale=True,
                                           debug_name="AUCTION_SEARCH_ITEMS")
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

    search_button = locate_center_on_screen(AUCTION_SEARCH_BUTTON, confidence=CONFIDENCE,
                                            grayscale=True,
                                            debug_name="AUCTION_SEARCH_BUTTON")
    pyautogui.click(search_button)
    time.sleep(1)

    find_item = locate_center_on_screen(os.path.join(BASE_DIR, item["auction_image"]),
                                        confidence=CONFIDENCE,
                                        grayscale=True,
                                        debug_name=f"{item['name']}_auction_image")
    x, y = find_item
    pyautogui.click(x + 120, y)

    remainder = 0
    if item_count == 1:
        pass
    else:
        count = locate_center_on_screen(AUCTION_COUNT, confidence=HIGH_CONFIDENCE,
                                        grayscale=True,
                                        debug_name="AUCTION_COUNT")
        pyautogui.click(count)
        for _ in range(item_count - 1):
            pydirectinput.press('right')
        for num in range(item_count):
            try:
                amount = os.path.join(AUCTION_PATH, "count", f"{num + 1}.png")
                locate_center_on_screen(amount, confidence=HIGH_CONFIDENCE,
                                        grayscale=True,
                                        debug_name=f"COUNT_{num+1}")
                real_count = num + 1
                remainder = item_count - real_count
                break
            except ImageNotFoundException:
                continue
            except Exception:
                continue

    buy = locate_center_on_screen(BUY_BUTTON, confidence=CONFIDENCE,
                                  grayscale=True,
                                  debug_name="BUY_BUTTON")
    if buy:
        pyautogui.click(buy)
        return remainder
    else:
        return False


# ============================================================
# Старт
# ============================================================

def start_logic():
    search_tasks()
