#!/usr/bin/env python3

from util import config

try:
    from sys import argv
    from gui import close_window, create_launcher_app
    from gui.elements import dialog
    import colorama
    import multiprocessing as mp
except ModuleNotFoundError as e:
    print("--> ERROR: Required python modules are not installed.")
    print(e)
    inp = input("Pring stack trace? (y/N) ")
    if inp.lower() == "y":
        raise e
    print("Aborting.")
    exit(1)

if __name__ == "__main__":
    mp.freeze_support()
    # The above needs to exist due to multiprocessing being frozen
    # https://github.com/pyinstaller/pyinstaller/wiki/Recipe-Multiprocessing
    print(colorama.Fore.BLUE + colorama.Style.BRIGHT + """
 ___               _   ___   _           _         _
(  _ \\            ( )_(  _ \\( )         ( )_      ( )
| (_) )  __    _ _|  _) (_(_) |/ )   __ |  _)  ___| |__
|  _ ( / __ \\/ _  ) |  \\__ \\|   (  / __ \\ |  / ___)  _  \\
| (_) )  ___/ (_| | |_( )_) | |\\ \\(  ___/ |_( (___| | | |
(____/ \\____)\\__ _)\\__)\\____)_) (_)\\____)\\__)\\____)_) (_)

                        LAUNCHER
    """ + colorama.Style.RESET_ALL)
    testing = False
    debug = False
    dev = False
    for arg in argv:
        if arg == "testing":
            testing = True
        elif arg == "debug":
            debug = True
        elif arg == "dev":
            dev = True

    app, window = create_launcher_app(
        testing_mode=testing, vr_debug=debug, dev_mode=dev
    )
    try:
        window.show()
        if not config.load_and_validate_config("./config.yml")[0]:
            dialog.open_msg_dialog(
                "Your configuration is invalid. A default config has been loaded",
                title="Invalid configuration",
            )
        app.exec()
    except KeyboardInterrupt:
        close_window(app)
        exit(130)
