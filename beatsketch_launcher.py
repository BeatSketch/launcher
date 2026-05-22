#!/usr/bin/env python3

try:
    from sys import argv
    from gui import close_window, create_launcher_app
    import colorama
except ModuleNotFoundError:
    print("--> ERROR: Required python modules are not installed.")
    print("Aborting.")
    exit(1)

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
    # TODO: Parse from CLI
    testing = False
    debug = False
    for arg in argv:
        if arg == "testing":
            testing = True
        elif arg == "debug":
            debug = True

    app, window = create_launcher_app(testing_mode=testing, vr_debug=debug)
    try:
        window.show()
        app.exec()
    except KeyboardInterrupt:
        close_window(app)
        exit(130)
