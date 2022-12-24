import random
from telebot.async_telebot import AsyncTeleBot
from telebot import types
import asyncio
import numpy as np


TOKEN = '5788792002:AAG7KnVLSnErx8lIHIGbCyrRC8d_gXEfr1w' # указываем токен нашего бота (для этого надо создать бота в @BotFather)


bot = AsyncTeleBot(TOKEN)


@bot.message_handler(content_types=["new_chat_members"])
async def adding_new_member(message):
    global users_id
    await bot.send_message(message.chat.id, "Hello " + message.from_user.first_name)
    await bot.send_message(message.chat.id, "Ты тоже убеждён, что первая группа изоморфна, а вторая нет?")



photos = ['https://ic.pics.livejournal.com/hemiechinus/13541897/110721/110721_original.jpg',
          'https://mobimg.b-cdn.net/v3/fetch/ad/ad0002eaac3a960fb1dc8f591a49174a.jpeg',
          'https://klike.net/uploads/posts/2022-05/1653194085_3.jpg',
          'https://funart.pro/uploads/posts/2021-07/1627525173_21-funart-pro-p-milie-pingvini-zhivotnie-krasivo-foto-31.jpg']


@bot.message_handler(commands=['start'])
async def menu(message):
    markup = types.InlineKeyboardMarkup(row_width=1)
    button1 = types.InlineKeyboardButton(text="Мой любимый напиток", callback_data="coffee")
    button2 = types.InlineKeyboardButton(text="Кинь случайную фотку через минуту", callback_data="snd_photo")
    button3 = types.InlineKeyboardButton(text="Дай стату", callback_data="statistics")
    button4 = types.InlineKeyboardButton(text="Уйди отсюда😢", callback_data="leave")
    markup.add(button1, button2, button3, button4)
    await bot.send_message(message.chat.id, '<------menu------>', reply_markup=markup)\


@bot.callback_query_handler(func=lambda callback: len(callback.data) > 0)
async def actions(callback):
    if callback.data == "statistics":
        ch_memb = await bot.get_chat_member_count(callback.message.chat.id)
        admins_list = await bot.get_chat_administrators(callback.message.chat.id)
        await bot.send_message(callback.message.chat.id, "Chat members: " + str(ch_memb))
        await bot.send_message(callback.message.chat.id, "Admins: " + str(len(admins_list)))
        s = ""
        for i in admins_list:
            s += i.user.first_name + '\n'
        await bot.send_message(callback.message.chat.id, "They are(Admins):\n" + s)
        return

    if callback.data == "leave":
        await bot.send_message(callback.message.chat.id, "Bye:(")
        await bot.leave_chat(callback.message.chat.id)
        return

    if callback.data == "snd_photo":
        await asyncio.sleep(60)
        index = np.random.randint(0, len(photos))
        await bot.send_photo(callback.message.chat.id, photos[index])
        return

    if callback.data == "coffee":
        await bot.send_poll(callback.message.chat.id,'choose what you want',['coffee','coffee','coffee'])
        return


asyncio.run(bot.polling())


