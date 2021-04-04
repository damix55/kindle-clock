from PIL import Image, ImageDraw, ImageFont, ImageEnhance
import os
from datetime import datetime, timedelta
import math
import json
import re


def gen_clock():
    colors = {
        'dark_grey': '#464646',
        'grey': '#969696',
        'light_grey': '#C4C4C4'
    }

    size_x = 800
    size_y = 600

    image = Image.new(mode='L', size=(size_x, size_y), color='white')
    font_regular = 'fonts/Coolvetica.ttf'
    font_condensed = 'fonts/CoolveticaCondensed.ttf'
    font_symbols = 'fonts/icomoon.ttf'

    clock_font = ImageFont.truetype(font_regular, 260)
    date_font = ImageFont.truetype(font_condensed, 80)
    event_title_font = ImageFont.truetype(font_condensed, 48)
    event_title_time = ImageFont.truetype(font_condensed, 36)
    todo_checkbox = ImageFont.truetype(font_symbols, 36)

    draw = ImageDraw.Draw(image)

    now = datetime.now()
    s = int(now.strftime('%S'))
    if s >= 58:
        now = now + timedelta(minutes=1)

    hours = now.strftime('%H')
    minutes = now.strftime('%M')
    day = re.sub(r'\b0', '', now.strftime('%d'))
    week_day = now.strftime('%a')
    month = now.strftime('%b')

    print(f'Generating clock ({hours}:{minutes})')

    with open('tmp/events.json') as f:
        events = json.load(f)

    with open('tmp/todos.json') as f:
        todos = json.load(f)


    margin_y = 0
    margin_x = 50


    ### Clock
    hours_width, _ = draw.textsize(hours, font=clock_font)

    draw.text(
        (margin_x, margin_y),
        hours,
        font=clock_font,
        fill=colors['grey'],
        anchor='la'
    )
    draw.text(
        (margin_x + hours_width + 2, margin_y),
        minutes,
        font=clock_font,
        fill='black',
        anchor='la'
    )

    ### Date
    draw.text(
        (size_x - margin_x, margin_y + 78),
        week_day.upper(),
        font=date_font,
        fill=colors['grey'],
        anchor='ra'
    )

    draw.text(
        (size_x - margin_x, margin_y + 148),
        f'{day} {month.upper()}',
        font=date_font,
        fill='black',
        anchor='ra'
    )


    ### Events
    margin_y = margin_y + 320
    margin_x = margin_x - 3

    margin_y_ev = margin_y

    # fix colors and crop events

    for event in events[:2]:
        draw.rectangle([
            margin_x,
            margin_y_ev + 10,
            margin_x + 10,
            margin_y_ev + 90],
            fill=colors['light_grey']
        )

        draw.text(
            (margin_x + 27, margin_y_ev),
            event['title'],
            font=event_title_font,
            fill=colors['dark_grey'],
            anchor='la'
        )

        draw.text(
            (margin_x + 27, margin_y_ev + 49),
            event['start'] + ' | ' + event['end'],
            font=event_title_time,
            fill=colors['grey'],
            anchor='la'
        )

        margin_y_ev = margin_y_ev + 105


    ### Todos
    
    for todo in todos[:4]:
        draw.text(
            (margin_x + 400, margin_y + 15),
            '\U0000E901',
            font=todo_checkbox,
            fill=colors['dark_grey'],
            anchor='la'
        )

        # if completed

        draw.text(
            (margin_x + 440, margin_y),
            todo['title'][:20],
            font=event_title_font,
            fill=colors['dark_grey'],
            anchor='la'
        )

        margin_y = margin_y + 58


    image = image.rotate(90, expand=True)
    image.save("tmp/clock.png", bits=4)

    #image.show()



def convert_pic(filename, target, contrast=1, brightness=1, angle=90):
    print('Converting picture')
    image = Image.open(filename).convert('L')
    width, height = image.size

    if width/8 > height/6:
        width = round(width*600/height)
        image = image.resize(size=(width, 600))
        margin = (width - 800)/2
        image = image.crop((math.floor(margin), 0, math.ceil(800+margin), 600))

    else:
        height = round(height*800/width)
        image = image.resize(size=(800, height))
        margin = (height - 600)/2
        image = image.crop((0, math.floor(margin), 800, math.ceil(600+margin)))

    image = image.rotate(angle, expand=True)

    enhancer = ImageEnhance.Brightness(image)
    image = enhancer.enhance(brightness)

    enhancer = ImageEnhance.Contrast(image)
    image = enhancer.enhance(contrast)

    image.save(target, bits=4)


if __name__ == "__main__":
    gen_clock()