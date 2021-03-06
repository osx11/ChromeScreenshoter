import keyboard
import os
from datetime import datetime
from time import sleep

from PIL import ImageGrab
import pywinauto
from plyer import notification

date = datetime.now().strftime('%d.%m.%Y')
root_path = os.path.expanduser('~/Documents/ChromeScreenshoter')
date_path = root_path + '/' + str(date)
w_handle = None

screen_width = 3840
screen_height = 2160

welcome = '''
Программа готова к использованию.
Управление:
    Скриншот :: CTRL + ALT
    Сброс :: ALT + X
    Выход :: CTRL + Q
'''


def alert(msg):
    notification.notify(title='ChromeScreenshoter', message=msg, app_name='ChromeScreenshoter')


def chrome_init():
    alert('Ожидание соединения с Chrome')
    global w_handle
    w_handle = None
    while not w_handle:
        print('Ожидание Chrome. Откройте ОДНУ пустую вкладку.')
        find = pywinauto.findwindows.find_windows(title_re=u'Новая вкладка')
        w_handle = find[0] if find.__len__() == 1 else None
        sleep(0.1)
    print(welcome)
    alert('Программа готова к использованию')


def first_startup():
    #  ######################################## creating directories ###################################################
    os.mkdir(root_path) if not os.path.exists(root_path) else None
    os.mkdir(date_path) if not os.path.exists(date_path) else None
    # ##################################################################################################################


def screenshot():
    coordinates = coords(w_handle)
    if not coordinates:
        return

    if coordinates['left'] < 0 or coordinates['right'] > screen_width or coordinates['top'] < 0 or coordinates['bottom'] > screen_height:
        print('Ошибка: поместите Chrome в пределы экрана.')
        return

    filename = os.listdir(date_path).__len__() + 1

    img = ImageGrab.grab((coordinates['left'] + 10, coordinates['top'], coordinates['right'] - 10, coordinates['bottom'] - 10))
    img.save(date_path + '/%d.png' % filename, 'PNG')
    print('Скриншот сохранен как %s' % date_path + '/%d.png' % filename)
    alert('Скриншот сохранен как %s' % date_path + '/%d.png' % filename)


def coords(handle):
    try:
        window = pywinauto.Application().connect(handle=handle).top_window()
        window.set_focus()
        sleep(0.5)
        rect = window.rectangle()
        return {'left': rect.left, 'right': rect.right, 'top': rect.top, 'bottom': rect.bottom, 'width': rect.width(), 'height': rect.height()}
    except RuntimeError:
        alert('Потеряна связь с Chrome')
        chrome_init()
        return


if __name__ == '__main__':
    first_startup()
    chrome_init()

    keyboard.add_hotkey("Ctrl + Alt", lambda: screenshot())
    keyboard.add_hotkey("Alt + X", chrome_init)
    keyboard.wait('Ctrl + Q')
