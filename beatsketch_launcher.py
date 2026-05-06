#!/usr/bin/env python3

from gui import close_window, create_launcher_app
import colorama

if __name__ == "__main__":
    print(colorama.Fore.BLUE + colorama.Style.BRIGHT + """
 ___               _   ___   _           _         _
(  _ \\            ( )_(  _ \\( )         ( )_      ( )
| (_) )  __    _ _|  _) (_(_) |/ )   __ |  _)  ___| |__
|  _ ( / __ \\/ _  ) |  \\__ \\|   (  / __ \\ |  / ___)  _  \\
| (_) )  ___/ (_| | |_( )_) | |\\ \\(  ___/ |_( (___| | | |
(____/ \\____)\\__ _)\\__)\\____)_) (_)\\____)\\__)\\____)_) (_)

                        LAUNCHER
    """ + colorama.Style.RESET_ALL)
    app, window = create_launcher_app()
    try:
        window.show()
        app.exec()
    except KeyboardInterrupt:
        close_window(app)
        exit(130)
