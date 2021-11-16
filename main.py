from ui import init_ui
from core.config import global_event_loop


if __name__ == '__main__':
    app = init_ui()

    with global_event_loop:
        global_event_loop.run_forever()
