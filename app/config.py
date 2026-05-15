import os

# --- Confidence levels ---
HIGH_CONFIDENCE = 0.9
CONFIDENCE = 0.7

# --- Base paths ---
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

# --- Task board paths ---
BOARD_PATH = os.path.join(BASE_DIR, "knowledge_base", "task_board")
BOARD_TASKS = os.path.join(BOARD_PATH, "base_locators")
BOARD_NAME = os.path.join(BOARD_TASKS, "task_board.png")

# --- Auction paths ---
AUCTION_PATH = os.path.join(BASE_DIR, "knowledge_base", "auction_locators")

AUCTION_BOARD = os.path.join(AUCTION_PATH, "auction_board.png")
AUCTION_SEARCH_BUTTON = os.path.join(AUCTION_PATH, "search_button.png")
AUCTION_TRASH_BUTTON = os.path.join(AUCTION_PATH, "trash_button.png")
AUCTION_SET_PRICE = os.path.join(AUCTION_PATH, "set_price.png")
AUCTION_PRICE_GOAL = os.path.join(AUCTION_PATH, "prise_goal.png")
AUCTION_PRICE_GOAL_LOW = os.path.join(AUCTION_PATH, "prise_goal_low.png")
AUCTION_MAIN_PANEL = os.path.join(AUCTION_PATH, "auction_main_panel.png")
AUCTION_MAIN_PANEL_UNACTIVE = os.path.join(AUCTION_PATH, "auction_main_panel_unactive.png")
EVERYTHING_ITEMS = os.path.join(AUCTION_PATH, "auction_everything_items.png")
EVERYTHING_ITEMS_UNACTIVE = os.path.join(AUCTION_PATH, "auction_everything_items_unactive.png")
AUCTION_SEARCH_ITEMS = os.path.join(AUCTION_PATH, "auction_search_items.png")
BUY_BUTTON = os.path.join(AUCTION_PATH, "buy_button.png")
AUCTION_COUNT = os.path.join(AUCTION_PATH, "count.png")
