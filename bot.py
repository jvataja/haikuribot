#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This program is dedicated to the public domain under the CC0 license.
import requests
import logging
import random
import time
import json
import re
from haiku import tallenna
from io import BytesIO
from PIL import Image, ImageOps

from telegram import InputFile, ChatPermissions
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from telegram.ext.dispatcher import run_async

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)


# ryhmien id:t, joissa bot määritetty toimimaan
guiro_id = 1234
joonas_id = 1234
testi_id = 1234


def start(update, context):
    print(update.message.chat.id)
    """Send a message when the command /start is issued."""
    update.message.reply_text('Haiku komennolla /haiku. Toimii vain tietyissä ryhmissä.')


def help(update, context):
    print(update)
    """Send a message when the command /help is issued."""
    update.message.reply_text('Help!')


def vapaa(update, context):
    #print(update['message']['chat']['id'])
    if not update['message']['chat']['id'] in [guiro_id, joonas_id, testi_id]:
        return
    text = update['message']['text']
    if "bonk" in text.lower():
        return bonk(update, context)
    if "bail" in text.lower():
        return bail(update, context)
    peko(update, context)
    tallenna(text)

def bail(update, context):
    try:
        h_id = update.message.reply_to_message.from_user.id
    except:
        return
    with open("jailstats.csv", "a") as f:
        f.write("bonk,{},{},{}\n".format(update.message.reply_to_message.from_user.username, update.message.from_user.username, time.time()))
    context.bot.restrict_chat_member(update.message.chat.id, h_id,ChatPermissions(
    can_send_messages=True,
    can_send_media_messages=True,
    can_send_polls=True,
    can_send_other_messages=True,
    can_add_web_page_previews=True,
    can_change_info=True,
    can_invite_users=True,
    can_pin_messages=True
    ))


def bonk(update, context):
    try:
        h_id = update.message.reply_to_message.from_user.id
    except:
        return
    with open("jailstats.csv", "a") as f:
        f.write("bonk,{},{},{}\n".format(update.message.reply_to_message.from_user.username, update.message.from_user.username, time.time()))
    print(h_id)
    # dowload profile picture
    pp = context.bot.get_user_profile_photos(h_id)
    if int(h_id) == 1057924203:
        return context.bot.send_photo(update.message.chat.id, open('selfbonk.png', 'rb'))
    if len(pp.photos) == 0:
        context.bot.send_photo(update.message.chat.id, open('bonk.jpg', 'rb'))
    else:
        ppid = pp.photos[0][0]["file_id"]
        file = context.bot.get_file(ppid)
        path = file.file_path
        print(path)
        r = requests.get(path)
        open('pp.jpg', 'wb').write(r.content)

        # create composite
        img = Image.open('pp.jpg', 'r')
        mask = Image.open('mask.png').convert('L')
        img = ImageOps.fit(img, mask.size, centering=(0.5, 0.5))
        img.putalpha(mask)
        img_w, img_h = img.size
        background = Image.open('bonk.png', 'r')
        bg_w, bg_h = background.size
        offset = ((bg_w - img_w) // 2 + 170, (bg_h - img_h) // 2 + 120)
        background.alpha_composite(img.resize((img_w*2, img_h*2)), offset)
        bat = Image.open('bat.png', 'r')
        background.alpha_composite(bat)
        small = background.resize((bg_w//2, bg_h//2))

        arr = BytesIO()
        arr.name = "image.png"
        small.save(arr, format='PNG')
        arr.seek(0)
        context.bot.send_photo(update.message.chat.id, arr)
    context.bot.restrict_chat_member(update.message.chat.id, h_id,ChatPermissions(),int(time.time()+60))


def haiku(update, context):
    print(update.message.chat.id)
    par_l = update['message']['text'].split(" ")[1:]
    par_l = par_l + ["", "", ""]
    a, b, c, *d = par_l
    if not update['message']['chat']['id'] in [guiro_id, joonas_id, testi_id]:
        return
    s_7 = []
    with open("7.csv", "r") as f:
        for i in f:
            s_7.append(i)
    s_5 = []
    with open("5.csv", "r") as f:
        for i in f:
            s_5.append(i)
    eka = ""; toka = ""; kolmas = ""
    if a:
        random.shuffle(s_5)
        for el in s_5:
            if a in el:
                eka = el
                break
    if b:
        random.shuffle(s_7)
        for el in s_7:
            if b in el:
                toka = el
                break
    if c:
        random.shuffle(s_5)
        for el in s_5:
            if c in el:
                kolmas = el
                break
    if not eka:
        eka = random.choice(s_5)
    if not toka:
        toka = random.choice(s_7)
    if not kolmas:
        kolmas = random.choice(s_5)
    while kolmas == eka:
        kolmas = random.choice(s_5)
    context.bot.send_message(chat_id=update.message.chat_id, text=(eka.capitalize() + toka + kolmas[:-1] + "."))

def peko(update, context):

    text = update['message']['text']
    key = "1234"
    url = "https://api.cognitive.microsoft.com/bing/v7.0/images/search"

    s = text.lower()
    s = re.sub(r'[^\w\s]','',s)
    s = re.split('\s+', s)
    c = 0; pk = ""
    while c < len(s)-1:
        if s[c][0] == 'p' and s[c+1][0] == 'k':
            k = s[c+1].capitalize()
            pk = s[c].capitalize() + " " + k
            break
        c += 1
    if not pk:
        return

    print(pk)

    headers = {'Ocp-Apim-Subscription-Key': key}
    params = {'q': k, 'count': 6, 'mkt':'fi-FI', 'safeSearch': "Off"}
    params2 = {'q': pk, 'count': 6, 'mkt':'en-US', 'safeSearch': "Off"}

    a = requests.get(url,headers=headers,params=params2)
    #print(a.json())
    results_len = len(a.json()['value'])
    print(results_len)
    if results_len == 0:
        a = requests.get(url,headers=headers,params=params)
        results_len = len(a.json()['value'])
    if results_len == 0:
        return
    if results_len == 1:
        i = 0
    else:
        i = random.randint(0,results_len-1)
    print(i)
    #print(a.json())
    p_url = a.json()['value'][i]['contentUrl']
    p = requests.get(p_url)
    context.bot.set_chat_photo(update['message']['chat']['id'], InputFile(BytesIO(p.content)))
    context.bot.set_chat_title(update['message']['chat']['id'], pk)


def tanka(update, context):
    par_l = update['message']['text'].split(" ")[1:]
    par_l = par_l + ["", "", "", "", ""]
    a, b, c, d, e, *f = par_l
    if not update['message']['chat']['id'] in [guiro_id, joonas_id, testi_id]:
        return
    s_7 = []
    with open("7.csv", "r") as f:
        for i in f:
            s_7.append(i)
    s_5 = []
    with open("5.csv", "r") as f:
        for i in f:
            s_5.append(i)
    eka = ""; toka = ""; kolmas = ""; neljas = ""; viides = "";
    if a:
        random.shuffle(s_5)
        for el in s_5:
            if a in el:
                eka = el
                break
    if b:
        random.shuffle(s_7)
        for el in s_7:
            if b in el:
                toka = el
                break
    if c:
        random.shuffle(s_5)
        for el in s_5:
            if c in el:
                kolmas = el
                break
    if d:
        random.shuffle(s_7)
        for el in s_7:
            if d in el:
                kolmas = el
                break
    if e:
        random.shuffle(s_7)
        for el in s_7:
            if e in el:
                kolmas = el
                break
    if not eka:
        eka = random.choice(s_5)
    if not toka:
        toka = random.choice(s_7)
    if not kolmas:
        kolmas = random.choice(s_5)
    if not neljas:
        neljas = random.choice(s_7)
    if not viides:
        viides = random.choice(s_7)
    while kolmas == eka:
        kolmas = random.choice(s_5)
    while toka == neljas or toka == viides:
        toka = random.choice(s_7)
        neljas = random.choice(s_7)
        viides = random.choice(s_7)

    context.bot.send_message(chat_id=update.message.chat_id, text=(eka.capitalize() + toka + kolmas + neljas + viides[:-1] + "."))


def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', context.bot, update.error)


def main():
    """Start the context.bot."""
    # Create the Updater and pass it your context.bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    updater = Updater("1234", use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("haiku", haiku))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(CommandHandler("tanka", tanka))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, vapaa))
    #dp.add_handler(MessageHandler(Filters.text, peko))

    # on noncommand i.e message - echo the message on Telegram

    # log all errors
    dp.add_error_handler(error)

    # Start the context.bot
    updater.start_polling()

    # Run the context.bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the context.bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
