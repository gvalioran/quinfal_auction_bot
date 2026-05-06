import threading
from app.overlay import start_overlay
from app.get_recepies import start_logic

def main():
    t_ui = threading.Thread(target=start_overlay, daemon=True)
    t_logic = threading.Thread(target=start_logic, daemon=True)

    t_ui.start()
    t_logic.start()

    t_ui.join()
    t_logic.join()

if __name__ == "__main__":
    main()
