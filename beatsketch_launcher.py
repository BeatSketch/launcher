#!/usr/bin/env python3

from gui import close_window, create_launcher_app

if __name__ == "__main__":
    app, window = create_launcher_app()
    try:
        window.show()
        app.exec()
    except KeyboardInterrupt:
        close_window(app)
        exit(130)
