from aiogram import Bot, Dispatcher, executor, types  # импорт библиотеки для создания ботов
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton  # импорт кнопок
from settings import *  # импортируем переменные из файоа настроек
from time import sleep  # импорт функции паузы
import json  # библиотека для упрощенной работы со словарями
import pickledb  # библиотека для простых баз данных
import re  # регулярки
from datetime import datetime, timedelta  # библиотека для работы с временем
import os  # библиотека для работы с системой (тут она просто для удаления файлов с жб)


def main(token, chat_id, rules, start_message, doban, report_sleep, nums2ban, users_in_top):
    global bantext, delete_text, dangerstickers, bot, dp, databan, hour, time
    if not doban:
        bantext = delete_text = dangerstickers = []

    bot = Bot(token=token)  # создаем клиент бота
    dp = Dispatcher(bot)  # "диспетчер" бота (для запуска и обозначения функций)

    databan = {}  # данные о репортах

    hour = 60 * 60  # час

    time = datetime.now() - timedelta(seconds=int(report_sleep))  # время по умолчанию (для таймингов репорта)

    @dp.message_handler(commands=["start", "help"])  # при командах /start или /help запускаем функцию
    async def start(message):  # функция вызываемая при /start или /help
        try:  # при ошибке в блоке try вызываем except
            if message.from_user.id == message.chat.id:  # если id пользователя = id чата (пользователь в лс с ботом) то
                await bot.send_message(message.chat.id,
                                       f"Привет @{message.from_user.username}!\n{start_message}")  # отправляем сообщение в лс пользователю
        except Exception as ex:  # при ошибке в блоке try мы записываем её в перемнную ex и выполняем код внутри except
            print(ex)  # пишем ошибку
            sleep(0.1)  # засыпание программы на 1/10 секунды

    @dp.message_handler(commands=["report"])  # при комманде /report выполнятся функция
    async def report(message):  # при комманде /report выполнятся функция
        global databan, time  # подключаем переменную databan к функции (даем право изменять её)

        if message.reply_to_message is None or str(
                message.chat.id) != chat_id:  # если сообщение не ответ или не в нужном чате – то...
            return  # закрываем функцию

        if datetime.now() < time:  # если нынешнее время меньше чем надо то
            await bot.send_message(chat_id=chat_id,
                                   text=f"@{message.from_user.username} репорт уже отправлен, пожалуйста подожди {str((time.minute - datetime.now().minute) * 60 + time.second - datetime.now().second)} секунд до следующего!")  # пишем что репорт отправлен
            await message.delete()  # удаляем сообщение
            return  # закрываем функцию

        time = datetime.now() + timedelta(seconds=int(report_sleep))  # время с задержкой

        databan[
            "user"] = message.reply_to_message.from_user.id  # добавляем переменную с id пользователя на которого пожаловались в словарь
        databan[
            "userwarn"] = message.from_user.id  # добавляем переменную с id пользователя, который отправил жб в словарь
        databan["msgid"] = message.reply_to_message.message_id  # добавляем id сообщения в словарь

        ##############################################################################################################################################################################################

        with open(f"{message.from_user.id}on{message.reply_to_message.from_user.id}", "w") as f:
            f.write(
                f"'user': {message.reply_to_message.from_user.id}, 'userwarn': {message.from_user.id}, 'msgid': {message.reply_to_message.message_id}")

        Bwarn = InlineKeyboardButton("Предупреждение",
                                     callback_data=f"warn {message.from_user.id}on{message.reply_to_message.from_user.id}")
        Bwarn_rep = InlineKeyboardButton("Предупреждение отправителю",
                                         callback_data=f"warn_rep {message.from_user.id}on{message.reply_to_message.from_user.id}")
        Bban = InlineKeyboardButton("Бан",
                                    callback_data=f"ban {message.from_user.id}on{message.reply_to_message.from_user.id}")
        Bban_rep = InlineKeyboardButton("Бан отправителю",
                                        callback_data=f"ban_rep {message.from_user.id}on{message.reply_to_message.from_user.id}")
        Bdelete = InlineKeyboardButton("Удалить сообщение",
                                       callback_data=f"delete {message.from_user.id}on{message.reply_to_message.from_user.id}")

        # все от Bwarn до Bdelete это создание кнопок

        commands = InlineKeyboardMarkup(row_width=1, column_width=2).add(Bwarn, Bban, Bwarn_rep, Bban_rep,
                                                                         Bdelete)  # добавляем кнопки к шаблону, который позже добавим к сообщению

        admins = list(await bot.get_chat_administrators(chat_id))  # список админов в чате

        await message.delete()  # удаляем сообщение репорта

        for i in admins:  # перебор админов
            try:
                await bot.send_message(i.user.id, f"""
    🆘 Получена жалоба в группе {message.chat.title}
    
    {message.from_user.first_name} (@{message.from_user.username}) пожаловался на 
    {message.reply_to_message.from_user.first_name} (@{message.reply_to_message.from_user.username})
    
    <a href="https://t.me/c/{str(message.chat.id)[4:]}/{message.reply_to_message.message_id}">Сообщение</a> будет ниже
    """, reply_markup=commands, parse_mode="HTML")  # шаблон сообщения которое прийдет к админам

                if not message.reply_to_message.sticker is None:  # проверка является ли сообщение стикером
                    await bot.send_sticker(i.user.id,
                                           f'{message.reply_to_message.sticker.file_id}')  # отправляем стикер

                elif not message.reply_to_message.video is None:  # проверка является ли сообщение видео
                    await bot.send_video(i.user.id, f'{message.reply_to_message.video.file_id}')  # отправляем видео

                elif not message.reply_to_message.voice is None:  # проверка является ли сообщение голосовым
                    await bot.send_audio(i.user.id, f'{message.reply_to_message.voice.file_id}')  # отправляем гс

                elif not message.reply_to_message.photo is None:  # проверка является ли сообщение изображением
                    try:  # проверка на наличие ошибок
                        await bot.send_photo(i.user.id,
                                             f'{message.reply_to_message.photo[0].file_id}')  # отправляем изображение
                    except:  # вызываем то что внутри except
                        await bot.send_message(i.user.id, f'{message.reply_to_message.text}')  # отправляем сообщение
                        continue  # сразу переходим к следующему админу

                else:  # если сообщение не гс, фото, видео или стикер – то отправляем текстовое сообщение
                    await bot.send_message(i.user.id, f'{message.reply_to_message.text}')  # отправляем сообщение
            except Exception as ex:  # при ошибке в блоке try мы записываем её в перемнную ex и выполняем код внутри except
                print(ex)
                sleep(0.01)

    @dp.callback_query_handler()  # если мы нажали на кнопку то
    async def button(callback):
        # global databan  # подключаем переменную databan к функции
        with open(callback.data.split(" ")[1], "r") as f:
            databan = json.loads(f"{{{f.read()}}}".replace("'", '"'))
        btype = callback.data.split(" ")[0]
        print(btype)
        print(databan)

        if btype == 'warn':
            os.remove(callback.data.split(" ")[1])

            nn = await bot.get_chat(
                databan['user'])  # записываем в переменную nn (nickname) данные о пользователе на которого пожаловались
            nn = nn.username  # достаем юзернейм из nn

            db = pickledb.load(f"warn.txt", True)  # подгружаем базу данных (по id чата и слову BAN после)
            value = db.get(str(databan["user"]))  # получаем кол-во предупреждений (по умолчанию их 0)
            db.set(str(databan["user"]), value + 1)  # ставим на одно предупреждение больше

            await bot.send_message(chat_id,
                                   f"@{nn} если будете нарушать правила, то будете забанены (предупреждение {str(int(value))}/{nums2ban} и оно выдано администрацией)!")  # пишем что пользователь будет забанен

            if value > int(nums2ban) - 1:  # если кол-во предупреждений больше чем задано в файле настроек то
                db.set(str(databan["user"]), 1)  # сбрасываем количество предупреждений

                db = pickledb.load(f"BANS.txt", True)  # подгружаем базу данных
                value = db.get(str(databan["user"]))  # получем значение: бан или кол-во часов на мут

                if not value:  # если значение пустое то
                    db.set(str(databan["user"]), "6")  # ставим что мут на 6 часов
                    await bot.restrict_chat_member(chat_id=chat_id, user_id=databan["user"],
                                                   until_date=datetime.now() + timedelta(
                                                       seconds=hour))  # мут пользователя на час
                    await bot.send_message(chat_id=chat_id,
                                           text=f"@{nn} забанен на час!")  # пишем что забанили пользователя на час
                elif value == "ban":  # если значение равно ban то
                    db.set(str(databan["user"]), False)  # делаем значение бана как false
                    await bot.ban_chat_member(chat_id, databan['user'])  # баним пользователя
                    await bot.send_message(chat_id=chat_id, text=f"@{nn} забанен!")  # пишем что забанили пользователя
                else:  # если значение не пустое и не равно ban то
                    if value == "6":  # если значение равно 6 то
                        db.set(str(databan["user"]), "12")  # ставим что мут на 12 часов
                        await bot.restrict_chat_member(chat_id=chat_id, user_id=databan["user"],
                                                       until_date=datetime.now() + timedelta(
                                                           seconds=hour * 6))  # мут пользователя на 6 часов
                        await bot.send_message(chat_id=chat_id,
                                               text=f"@{nn} забанен на 6 часов!")  # пишем что забанили пользователя на 6 часов
                    if value == "12":  # если значение равно 12 то
                        db.set(str(databan["user"]), "24")  # ставим что мут на сутки
                        await bot.restrict_chat_member(chat_id=chat_id, user_id=databan["user"],
                                                       until_date=datetime.now() + timedelta(
                                                           seconds=hour * 12))  # мут пользователя на 12 часов
                        await bot.send_message(chat_id=chat_id,
                                               text=f"@{nn} забанен на 12 часов!")  # пишем что забанили пользователя на 12 часов
                    if value == "24":  # если значение равно 24 то
                        db.set(str(databan["user"]), "ban")  # ставим что дальше бан
                        await bot.restrict_chat_member(chat_id=chat_id, user_id=databan["user"],
                                                       until_date=datetime.now() + timedelta(
                                                           seconds=hour * 24))  # мут пользователя на сутки
                        await bot.send_message(chat_id=chat_id,
                                               text=f"@{nn} забанен на 24 часа!")  # пишем что забанили пользователя на сутки

            await bot.delete_message(chat_id, databan["msgid"])  # удаляем сообщение

        if btype == 'warn_rep':
            os.remove(callback.data.split(" ")[1])

            nn = await bot.get_chat(
                databan['userwarn'])  # записываем в переменную nn (nickname) данные о пользователе который отправил жб
            nn = nn.username  # достаем юзернейм из nn

            db = pickledb.load(f"BAN.txt", True)  # подгружаем базу данных (по id чата и слову BAN после)
            value = db.get(str(databan["userwarn"]))  # получаем кол-во предупреждений (по умолчанию их 0)
            db.set(str(databan["userwarn"]), value + 1)  # ставим на одно предупреждение больше

            await bot.send_message(chat_id,
                                   f"@{nn} если будете кидать репорты без причины, то будете забанены (предупреждение {str(int(value))}/{nums2ban} и оно выдано администрацией)!")  # пишем что пользователь будет забанен

            if value > int(nums2ban) - 1:  # если кол-во предупреждений больше чем задано в файле настроек то
                db.set(str(databan["userwarn"]), 1)  # сбрасываем количество предупреждений

                db = pickledb.load(f"BANS.txt", True)  # подгружаем базу данных
                value = db.get(str(databan["userwarn"]))  # получем значение: бан или кол-во часов на мут

                if not value:  # если значение пустое то
                    db.set(str(databan["userwarn"]), "6")  # ставим что мут на 6 часов
                    await bot.restrict_chat_member(chat_id=chat_id, user_id=databan["userwarn"],
                                                   until_date=datetime.now() + timedelta(
                                                       seconds=hour))  # мут пользователя на час
                    await bot.send_message(chat_id=chat_id,
                                           text=f"@{nn} забанен на час!")  # пишем что забанили пользователя на час
                elif value == "ban":  # если значение равно ban то
                    db.set(str(databan["userwarn"]), False)  # делаем значение бана как false
                    await bot.ban_chat_member(chat_id, databan['userwarn'])  # баним пользователя
                    await bot.send_message(chat_id=chat_id, text=f"@{nn} забанен!")  # пишем что забанили пользователя
                else:  # если значение не пустое и не равно ban то
                    if value == "6":  # если значение равно 6 то
                        db.set(str(databan["userwarn"]), "12")  # ставим что мут на 12 часов
                        await bot.restrict_chat_member(chat_id=chat_id, user_id=databan["userwarn"],
                                                       until_date=datetime.now() + timedelta(
                                                           seconds=hour * 6))  # мут пользователя на 6 часов
                        await bot.send_message(chat_id=chat_id,
                                               text=f"@{nn} забанен на 6 часов!")  # пишем что забанили пользователя на 6 часов
                    if value == "12":  # если значение равно 12 то
                        db.set(str(databan["userwarn"]), "24")  # ставим что мут на сутки
                        await bot.restrict_chat_member(chat_id=chat_id, user_id=databan["userwarn"],
                                                       until_date=datetime.now() + timedelta(
                                                           seconds=hour * 12))  # мут пользователя на 12 часов
                        await bot.send_message(chat_id=chat_id,
                                               text=f"@{nn} забанен на 12 часов!")  # пишем что забанили пользователя на 12 часов
                    if value == "24":  # если значение равно 24 то
                        db.set(str(databan["userwarn"]), "ban")  # ставим что дальше бан
                        await bot.restrict_chat_member(chat_id=chat_id, user_id=databan["userwarn"],
                                                       until_date=datetime.now() + timedelta(
                                                           seconds=hour * 24))  # мут пользователя на сутки
                        await bot.send_message(chat_id=chat_id,
                                               text=f"@{nn} забанен на 24 часа!")  # пишем что забанили пользователя на сутки

        if btype == 'ban':
            os.remove(callback.data.split(" ")[1])

            nn = await bot.get_chat(
                databan['user'])  # записываем в переменную nn (nickname) данные о пользователе на которого пожаловались
            nn = nn.username  # достаем юзернейм из nn

            db = pickledb.load(f"BANS.txt", True)  # подгружаем базу данных
            value = db.get(str(databan["user"]))  # получем значение: бан или кол-во часов на мут

            if not value:  # если значение пустое то
                db.set(str(databan["user"]), "6")  # ставим что мут на 6 часов
                await bot.restrict_chat_member(chat_id=chat_id, user_id=databan["user"],
                                               until_date=datetime.now() + timedelta(
                                                   seconds=hour))  # мут пользователя на час
                await bot.send_message(chat_id=chat_id,
                                       text=f"@{nn} забанен на час!")  # пишем что забанили пользователя на час
            elif value == "ban":  # если значение равно ban то
                db.set(str(databan["user"]), False)  # делаем значение бана как false
                await bot.ban_chat_member(chat_id, databan['user'])  # баним пользователя
                await bot.send_message(chat_id=chat_id, text=f"@{nn} забанен!")  # пишем что забанили пользователя
            else:  # если значение не пустое и не равно ban то
                if value == "6":  # если значение равно 6 то
                    db.set(str(databan["user"]), "12")  # ставим что мут на 12 часов
                    await bot.restrict_chat_member(chat_id=chat_id, user_id=databan["user"],
                                                   until_date=datetime.now() + timedelta(
                                                       seconds=hour * 6))  # мут пользователя на 6 часов
                    await bot.send_message(chat_id=chat_id,
                                           text=f"@{nn} забанен на 6 часов!")  # пишем что забанили пользователя на 6 часов
                if value == "12":  # если значение равно 12 то
                    db.set(str(databan["user"]), "24")  # ставим что мут на сутки
                    await bot.restrict_chat_member(chat_id=chat_id, user_id=databan["user"],
                                                   until_date=datetime.now() + timedelta(
                                                       seconds=hour * 12))  # мут пользователя на 12 часов
                    await bot.send_message(chat_id=chat_id,
                                           text=f"@{nn} забанен на 12 часов!")  # пишем что забанили пользователя на 12 часов
                if value == "24":  # если значение равно 24 то
                    db.set(str(databan["user"]), "ban")  # ставим что дальше бан
                    await bot.restrict_chat_member(chat_id=chat_id, user_id=databan["user"],
                                                   until_date=datetime.now() + timedelta(
                                                       seconds=hour * 24))  # мут пользователя на сутки
                    await bot.send_message(chat_id=chat_id,
                                           text=f"@{nn} забанен на 24 часа!")  # пишем что забанили пользователя на сутки

            await bot.delete_message(chat_id, databan["msgid"])  # удаляем сообщение

        if btype == 'ban_rep':
            os.remove(callback.data.split(" ")[1])

            nn = await bot.get_chat(databan[
                                        'userwarn'])  # записываем в переменную nn (nickname) данные о пользователе на которого пожаловались
            nn = nn.username  # достаем юзернейм из nn

            db = pickledb.load(f"BANS.txt", True)  # подгружаем базу данных
            value = db.get(str(databan["userwarn"]))  # получем значение: бан или кол-во часов на мут

            if not value:  # если значение пустое то
                db.set(str(databan["userwarn"]), "6")  # ставим что мут на 6 часов
                await bot.restrict_chat_member(chat_id=chat_id, user_id=databan["userwarn"],
                                               until_date=datetime.now() + timedelta(
                                                   seconds=hour))  # мут пользователя на час
                await bot.send_message(chat_id=chat_id,
                                       text=f"@{nn} забанен на час!")  # пишем что забанили пользователя на час
            elif value == "ban":  # если значение равно ban то
                db.set(str(databan["userwarn"]), False)  # делаем значение бана как false
                await bot.ban_chat_member(chat_id, databan['userwarn'])  # баним пользователя
                await bot.send_message(chat_id=chat_id, text=f"@{nn} забанен!")  # пишем что забанили пользователя
            else:  # если значение не пустое и не равно ban то
                if value == "6":  # если значение равно 6 то
                    db.set(str(databan["userwarn"]), "12")  # ставим что мут на 12 часов
                    await bot.restrict_chat_member(chat_id=chat_id, user_id=databan["userwarn"],
                                                   until_date=datetime.now() + timedelta(
                                                       seconds=hour * 6))  # мут пользователя на 6 часов
                    await bot.send_message(chat_id=chat_id,
                                           text=f"@{nn} забанен на 6 часов!")  # пишем что забанили пользователя на 6 часов
                if value == "12":  # если значение равно 12 то
                    db.set(str(databan["userwarn"]), "24")  # ставим что мут на сутки
                    await bot.restrict_chat_member(chat_id=chat_id, user_id=databan["userwarn"],
                                                   until_date=datetime.now() + timedelta(
                                                       seconds=hour * 12))  # мут пользователя на 12 часов
                    await bot.send_message(chat_id=chat_id,
                                           text=f"@{nn} забанен на 12 часов!")  # пишем что забанили пользователя на 12 часов
                if value == "24":  # если значение равно 24 то
                    db.set(str(databan["userwarn"]), "ban")  # ставим что дальше бан
                    await bot.restrict_chat_member(chat_id=chat_id, user_id=databan["userwarn"],
                                                   until_date=datetime.now() + timedelta(
                                                       seconds=hour * 24))  # мут пользователя на сутки
                    await bot.send_message(chat_id=chat_id,
                                           text=f"@{nn} забанен на 24 часа!")  # пишем что забанили пользователя на сутки

        if btype == 'delete':
            os.remove(callback.data.split(" ")[1])

            nn = await bot.get_chat(databan[
                                        'userwarn'])  # записываем в переменную nn (nickname) данные о пользователе на которого пожаловались
            nn = nn.username  # достаем юзернейм из nn

            await bot.delete_message(chat_id, databan["msgid"])  # удаляем сообщение

        databan = {}  # сбрасываем данные о репорте

    @dp.message_handler(commands=["top"])  # при команде /top выполняем функцию
    async def top(message):  # при команде /top выполняем функцию
        if str(message.chat.id) != chat_id:  # если сообщение не в нужном чате – то...
            return  # закрываем функцию

        try:  # при ошибке в блоке try вызываем except
            with open(f"TOP.txt", "r") as f:  # открываем файл с id чата на чтение
                text = json.loads(f.read())  # с помощью json преобразовываем текст в словарь
                text = sorted(text.items(), key=lambda x: x[1])[
                       ::-1]  # сортируем и разворачиваем список с топами по собщениям
                text = dict(text)  # превращаем список в словарь
                top = []  # создаем список

                for i, user in enumerate(
                        text.items()):  # берем пользователя (имя и число сообщений) и число от 1 до ограничения указанного в файле настроек (ограничение и место)
                    if i == users_in_top:
                        break
                    top.append(
                        f"{i + 1}. @{user[0]} - {user[1]}")  # добавляем в список top место, имя и кол-во сообщений

                await message.reply("\n".join(
                    top))  # отвечаем на сообщение нашим списком, предварительно соеденив элементы пропусками строк
        except Exception as ex:  # при ошибке в блоке try мы записываем её в перемнную ex и выполняем код внутри except
            print(ex)  # пишем ошибку
            sleep(0.1)  # засыпание программы на 1/10 секунды

    @dp.message_handler(content_types=["sticker", "text"])  # функция срабатывает на текст и стикеры
    async def main(message):  # функция срабатывает на текст и стикеры
        if str(message.chat.id) != chat_id:  # если сообщение не в нужном чате – то...
            return  # закрываем функцию

        await standart_ban(message)  # функция проверки на бан

        db = pickledb.load(f"TOP.txt", True)  # загружаем бд чата (по id)
        value = db.get(
            message.from_user.username) + 1  # прибавляем к числу сообщений 1 (если их не было то просто пишем 1)
        db.set(message.from_user.username, value)  # записываем число сообщений к нику пользователя

    async def standart_ban(message):  # функция для проверки надо ли банить пользователя
        if message.sticker is not None:  # примитивная проверка на то является ли стикером сообщение
            if message.sticker.file_unique_id in dangerstickers:  # если id стикера в бан-листе то

                db = pickledb.load(f"BAN.txt", True)  # подгружаем базу данных (по id чата и слову BAN после)
                value = db.get(str(message.from_user.id))  # получаем кол-во предупреждений (по умолчанию их 0)
                db.set(str(message.from_user.id), value + 1)  # ставим на одно предупреждение больше

                await message.reply(
                    f"@{message.from_user.username} если будете нарушать правила, то будете забанены (предупреждение {str(int(value))}/{nums2ban})!")  # пишем что пользователь будет забанен
                await message.delete()  # удаляем сообщение

                if value > int(nums2ban) - 1:  # если предупреждений больше чем указано в файле настроек то
                    db.set(str(message.from_user.id), 1)  # сбрасываем кол-во предупреждений

                    await bot.send_message(chat_id,
                                           f"@{message.from_user.username} забанен за использование запрещённого стикера!")  # пишем что забанили пользователя

                    await bot.ban_chat_member(chat_id, message.from_user.id)  # баним пользователя

            elif message.from_user.id == message.chat.id:  # проверка на то пишем ли мы в лс боту
                print(
                    message.sticker.file_unique_id)  # если мы отправили стикер в лс боту, то нам напишет его уникальный ID

        else:  # если сообщение не стикер то
            for word in bantext:  # перебор слов бан-листа
                if re.search(word, "".join(message.text.lower().split(
                        ' '))):  # если слово есть в сообщении (.lower() делает все сообщение с малых букв, это для упрощения проверки)
                    block = 1  # записываем True в переменную block (она влияет банить ли пользователя, если будет False то нет)
                    for acceptword in accept:  # перебор разрешенных слов
                        if re.search(word,
                                     acceptword) and acceptword in message.text.lower():  # если плохое слово в разрешенном слове и разрешенное слово в сообщении то
                            block = False  # меняем переменную бана на False (банить не будет)
                            break  # завершаем цикл

                    if block:  # если блок остался True то
                        db = pickledb.load(f"BAN.txt", True)  # подгружаем базу данных (по id чата и слову BAN после)
                        value = db.get(str(message.from_user.id))  # получаем кол-во предупреждений (по умолчанию их 0)
                        db.set(str(message.from_user.id), value + 1)  # ставим на одно предупреждение больше

                        await message.reply(
                            f"@{message.from_user.username} если будете нарушать правила, то будете забанены (предупреждение {str(int(value))}/{nums2ban})!")  # пишем что пользователь будет забанен
                        await message.delete()  # удаляем сообщение

                        if value > int(nums2ban) - 1:  # если предупреждений больше чем указано в файле настроек то
                            db.set(str(message.from_user.id), 1)  # сбрасываем кол-во предупреждений

                            await bot.send_message(chat_id,
                                                   f"@{message.from_user.username} забанен за использование запрещённого слова!")  # пишем что забанили пользователя

                            await bot.ban_chat_member(chat_id, message.from_user.id)  # баним пользователя

            for word in bantext:  # перебор слов бан-листа
                if re.search(word, "".join(message.text.lower().split(
                        ' '))):  # если слово есть в сообщении (.lower() делает все сообщение с малых букв, это для упрощения проверки)
                    block = 1  # записываем True в переменную block (она влияет банить ли пользователя, если будет False то нет)
                    for acceptword in accept:  # перебор разрешенных слов
                        if re.search(word,
                                     acceptword) and acceptword in message.text.lower():  # если плохое слово в разрешенном слове и разрешенное слово в сообщении то
                            block = False  # меняем переменную бана на False (банить не будет)
                            break  # завершаем цикл

                    if block:  # если блок остался True то
                        await message.delete()  # удаляем сообщение

    @dp.message_handler(
        content_types=['new_chat_members'])  # запуск функции если сообщение про подключение пользователю к чату
    async def new_members(message):  # запуск функции если сообщение про подключение пользователю к чату
        if str(message.chat.id) != chat_id:  # если сообщение не в нужном чате – то...
            return  # закрываем функцию

        try:  # если ошибки в блоке try, то запускаем except
            await message.delete()  # удаляем сообщение о том что пользователь подключился
            await bot.send_message(message.chat.id, rf"""👋 Привет @{message.new_chat_members[0].username} 👋
    {rules}
     😁 Будем благодарны если вы будете жаловаться на нарушителей
    (/report как ответ на сообщение)""")  # пишем сообщение с приветствием и правилами
        except Exception as ex:  # при ошибке в блоке try мы записываем её в перемнную ex и выполняем код внутри except
            print(ex)  # пишем ошибку
            sleep(0.1)  # засыпание программы на 1/10 секунды

    executor.start_polling(dp, skip_updates=True)  # запуск бота
