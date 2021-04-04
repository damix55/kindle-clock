import subprocess
import picture
import os

from datetime import datetime


def run(script, *args, **kwargs):
    out = subprocess.run(script, shell=True, stdout=subprocess.PIPE, *args, **kwargs).stdout
    if out is not None:
        return out.decode('utf-8')[:-1]


def clear_screen():
    run('eips -c')
    print('Clearing screen')


def show_image(pic, refresh=False, clear=False):
    if clear:
        clear_screen()

    if refresh:
        run(f'eips -f -g {pic}')
        print('Setting picture and refreshing screen')
    else:
        run(f'eips -g {pic}')
        print('Setting picture')


def get_mode():
    try:
        with open('tmp/mode', 'r') as f:
            return f.read()

    except FileNotFoundError:
        if not os.path.exists('tmp'):
            os.mkdir('tmp')

        with open('tmp/mode', 'w') as f:
            f.write('clock')

        return 'clock'


def set_mode(mode):
    with open('tmp/mode', 'w') as f:
        f.write(mode)


def get_battery_level():
    return int(run('gasgauge-info -s').replace('%', ''))


def is_battery_charging():
    load = run('gasgauge-info -l')
    return load[0] != '-'


def refresh():
    mode = get_mode()
    eval(f'show_{mode}()')


def show_picture():
    set_mode('picture')
    show_image('tmp/picture.png', refresh=True, clear=True)


def show_clock():
    s = int(datetime.now().strftime('%S'))
    m = int(datetime.now().strftime('%M'))
    if s >= 58:
        m = (m + 1) % 60

    if m == 0 or m == 30 or get_mode() != 'clock':
        refresh = True
        clear = True
    else:
        refresh = False
        clear = False

    picture.gen_clock()           
    show_image('tmp/clock.png', refresh=refresh, clear=clear)
    set_mode('clock')