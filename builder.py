import os


def build_exe(debug_mode=False):
    if debug_mode == False:
        os.system('pyinstaller main.py --onefile --add-binary "./driver/chromedriver.exe;./driver" --add-data "./ui_files/login.ui;./ui_files" --add-data "./ui_files/editwindow.ui;./ui_files" --add-data "./ui_files/mainwindow_ex.ui;./ui_files" --add-data "./ui_files/naverlogin.ui;./ui_files" --icon="icon.ico"')
    else:
        os.system('pyinstaller main.py --onefile --add-binary --noconsole\
            "./driver/chromedriver.exe;./driver" --add-data \
                "./ui_files/login.ui;./ui_files" --add-data \
                    "./ui_files/editwindow.ui;./ui_files" \
                        --add-data "./ui_files/mainwindow_ex.ui;./ui_files" \
                            --add-data "./ui_files/naverlogin.ui;./ui_files" --icon="icon.ico"')


if __name__ == "__main__":
    build_exe()