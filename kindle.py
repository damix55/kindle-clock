import subprocess
import picture
from pathlib import Path

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


def open_or_create(path, default):
    try:
        with open(path, 'r') as f:
            return f.read()

    except FileNotFoundError:
        Path(path).parent.mkdir(parents=True, exist_ok=True)

        with open(path, 'w') as f:
            f.write(default)

        return default


def get_mode():
    return open_or_create('tmp/mode', 'clock')


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
    clear_screen()
    eval(f'show_{mode}()')


def show_picture():
    set_mode('picture')
    show_image('tmp/picture.png', refresh=True, clear=True)


def get_clock_mode():
    return int(open_or_create('tmp/clock_mode', '0'))


def set_clock_mode(clock_mode):
    with open('tmp/clock_mode', 'w') as f:
        f.write(str(clock_mode))


def submode_back():
    submode_change('back')

def submode_up():
    submode_change('up')


def submode_change(direction):
    mode = get_mode()
    if mode == 'clock':
        total_clock_modes = 2       # hardcoded for now...
        submode = get_clock_mode()
        if direction == 'up':
            clock_mode = (submode+1)%total_clock_modes
        else:
            clock_mode = (submode-1)%total_clock_modes
        
        set_clock_mode(clock_mode)
        print('Changing to clock', clock_mode)

        refresh()


def update_clock():
    if get_mode == 'clock':
        show_clock()


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

    open_or_create('tmp/events.json', '[]')
    open_or_create('tmp/todos.json', '[]')

    picture.gen_clock(get_clock_mode())           
    show_image('tmp/clock.png', refresh=refresh, clear=clear)
    set_mode('clock')