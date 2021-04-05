import schedule
import kindle

from threading import Thread
from struct import unpack
from time import sleep
from bot import start_bot
from cal import get_events
from todos import get_todos


def main():
    # Disable screensaver and stop framework
    kindle.run('lipc-set-prop -i com.lab126.powerd preventScreenSaver 1')
    print('Screensaver disabled')
    kindle.run('/etc/init.d/framework stop')
    print('Framework stopped')

    # Monitor keypress
    Thread(target=get_keypress_1).start()
    Thread(target=get_keypress_2).start()

    # Start the telegram bot
    Thread(target=start_bot).start()

    # Schedule the clock update every minute at 58 seconds, since it takes
    # approximately 2 seconds to generate the picture
    schedule.every().minute.at(':58').do(run_threaded, kindle.show_clock)

    # Check for updates of events and todos every 15 minutes
    schedule.every(15).minutes.do(run_threaded, get_events)
    schedule.every(1).hours.do(run_threaded, get_todos)

    schedule.every(6).hours.do(run_threaded, clear_log)

    # Check for updates of events and todos
    run_threaded(get_events)
    run_threaded(get_todos)
    kindle.refresh()

    while True:
        schedule.run_pending()
        sleep(1)


def get_keypress_1():
    f = open('/dev/input/event0', 'rb')
    while True:
        data = f.read(24)
        upk = unpack('12H', data)
        if upk[2] == 1:
            code = upk[1]
            map_key(code)


def get_keypress_2():
    f = open('/dev/input/event1', 'rb')
    while True:
        data = f.read(16)
        upk = unpack('8H', data)
        if upk[6] == 1:
            code = upk[5]
            map_key(code)


def map_key(code):
    print(f'Key code: {code}')

    # when a key is pressed, run the corresponding function
    keys = {
        193: None,                  # F23          left side down
        104: None,                  # PageUp       left side up
        191: None,                  # F21          right side down
        109: None,                  # PageDown     right side up
        158: kindle.refresh,        # Back
        29:  kindle.show_picture,   # LeftControl
        139: kindle.show_clock,     # Menu
        102: None,                  # Home
        105: None,                  # Left
        108: None,                  # Down
        106: None,                  # Right
        103: None,                  # Up
        194: None,                  # F24          center button
    }

    action = keys[code]
    if action is not None:
        action()


def run_threaded(job_func, args=()):
    job_thread = Thread(target=job_func, args=args)
    job_thread.start()


def clear_log():
    print('Clearing log')
    kindle.run('rm screenlog.0')


if __name__ == '__main__':
    main()
