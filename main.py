from aiogram import Bot, Dispatcher, executor, types  # импорт библиотеки для создания ботов
from settings import *  # импортируем переменные из файоа настроек
from time import sleep  # импорт функции паузы
import json  # библиотека для упрощенной работы со словарями
import pickledb  # библиотека для простых баз данных

bot = Bot(token=token)  # создаем клиент бота
dp = Dispatcher(bot)  # "диспетчер" бота (для запуска и обозначения функций)


@dp.message_handler(commands=["start", "help"])  # при командах /start или /help запускаем функцию
async def start(message):  # функция вызываемая при /start или /help
	try:  # при ошибке в блоке try вызываем except
		if message.from_user.id == message.chat.id:  # если id пользователя = id чата (пользователь в лс с ботом) то
			await bot.send_message(message.chat.id, rf"""Привет @{message.from_user.username}! Я бот модератор от @voobrazimo и @vAPGSv!

Я нужен для того что бы в чате никто не шалил, не оскорблял никого и не вытворял всякую дичь)

(ну и еще удаляю запрещённые стикеры ¯\_(ツ)_/¯)

Что бы проверить бан за стикер/слово/предложение отправь его в лс, если удалю то значит в чате за него получишь BAN!

А если стикер/слово/предложение не соответствует правилам чата то отправь его @vAPGSv или @Hurricane999, мы его быстро добавим в наш банлист 😉!
(Так же напишите если наоборот - бан за нормальное слово/предложение)!""")  # отправляем сообщение в лс пользователю
	except Exception as ex:  # при ошибке в блоке try мы записываем её в перемнную ex и выполняем код внутри except
		print(ex)  # пишем ошибку
		sleep(0.1)  # засыпание программы на 1/10 секунды


@dp.message_handler(commands=["top"])  # при команде /top выполняем функцию
async def top(message):  # при команде /top выполняем функцию
	try:  # при ошибке в блоке try вызываем except
		with open(f"{message.chat.id}.txt", "r") as f:  # открываем файл с id чата на чтение
			text = json.loads(f.read())  # с помощью json преобразовываем текст в словарь
			text = sorted(text.items(), key=lambda x: x[1])[::-1]  # сортируем и разворачиваем список с топами по собщениям
			text = dict(text)  # превращаем список в словарь
			top = []  # создаем список

			for user, i in zip(text.items(), [i for i in range(1, int(users_in_top)+1)]):  # берем пользователя (имя и число сообщений) и число от 1 до ограничения указанного в файле настроек (ограничение и место)
				top.append(f"{i}. {user[0]} - {user[1]}")  # добавляем в список top место, имя и кол-во сообщений
				
			await message.reply("\n".join(top))  # отвечаем на сообщение нашим списком, предварительно соеденив элементы пропусками строк
	except Exception as ex:  # при ошибке в блоке try мы записываем её в перемнную ex и выполняем код внутри except
		print(ex)  # пишем ошибку
		sleep(0.1)  # засыпание программы на 1/10 секунды


@dp.message_handler(content_types=["sticker", "text"])  # функция срабатывает на текст и стикеры
async def main(message):  # функция срабатывает на текст и стикеры
	
		bmessage = json.dumps(dict(message), indent=4, sort_keys=True, ensure_ascii=False)  # делаем красивый словарь из компонентов сообщения (чат, пользователь, текст или стикер и прочие значения)
		
		if "sticker" in bmessage:  # примитивная проверка на то является ли стикером сообщение
			if message.sticker.file_unique_id in dangerstickers:  # если id стикера в бан-листе то
			
				db = pickledb.load(f"{message.chat.id}BAN.txt", True)  # подгружаем базу данных (по id чата и слову BAN после)
				value = db.get(str(message.from_user.id))  # получаем кол-во предупреждений (по умолчанию их 0)
				db.set(str(message.from_user.id), value+1)  # ставим на одно предупреждение больше
				
				await message.reply(f"@{message.from_user.username} если будете правила, то будете забанены (предупреждение {str(int(value))}/{nums2ban})!")  # пишем что пользователь будет забанен
				await message.delete()  # удаляем сообщение
				
				if value > int(nums2ban)-1:
					db.set(str(message.from_user.id), 1)
			
					await bot.send_message(message.chat.id, f"@{message.from_user.username} забанен за использование запрещённого стикера!")  # пишем что забанили пользователя
					await message.delete()  # удаляем сообщение
				
					await bot.ban_chat_member(message.chat.id, message.from_user.id)  # баним пользователя
			
			elif message.from_user.id == message.chat.id:  # проверка на то пишем ли мы в лс боту
				await message.reply(f"Уникальный ID стикера {message.sticker.file_unique_id}!")  # если мы в отправили стикер в лс боту он пишет его уникальный id
				
		else:  # если сообщение не стикер то
			for word in dangertext:  # перебор слов из бан-листа
				if word in message.text.lower():  # если слово есть в сообщении (.lower() делает все сообщение с малых букв, это для упрощения проверки)
					block = 1  # записываем True в переменную block (она влияет будем ли банить пользователя, если будет False то нет)
					for acceptword in accept:  # перебор разрешенных слов
						if word in acceptword and acceptword in message.text.lower():  # если плохое слово в разрешенном слове и разрешенное слово в сообщении то
							block = False  # меняем переменную бана на False (банить не будет)
							break  # завершаем цикл
					if block:  # если блок остался True то
						db = pickledb.load(f"{str(message.chat.id)}BAN.txt", True)  # подгружаем базу данных (по id чата и слову BAN после)
						value = db.get(str(message.from_user.id))  # получаем кол-во предупреждений (по умолчанию их 0)
						db.set(str(message.from_user.id), value+1)  # ставим на одно предупреждение больше
						
						await message.reply(f"@{message.from_user.username} если будете правила, то будете забанены (предупреждение {str(int(value))}/{nums2ban})!")  # пишем что пользователь будет забанен
						await message.delete()  # удаляем сообщение
						
						if value > int(nums2ban)-1:
							db.set(str(message.from_user.id), 1)
						
							await bot.send_message(message.chat.id, f"@{message.from_user.username} забанен за использование запрещённого слова!")  # пишем что забанили пользователя
							await message.delete()  # удаляем сообщение
							await bot.ban_chat_member(message.chat.id, message.from_user.id)  # баним пользователя

			db = pickledb.load(f"{message.chat.id}.txt", True)  # загружаем бд чата (по id)
			value = db.get(message.from_user.username)+1  # прибавляем к числу сообщений 1 (если их не было то просто пишем 1)
			db.set(message.from_user.username, value)  # записываем число сообщений к нику пользователя
	


@dp.message_handler(content_types=['new_chat_members'])  # запуск функции если сообщение про подключение пользователю к чату
async def new_members(message):  # запуск функции если сообщение про подключение пользователю к чату
	try:  # если ошибки в блоке try то запускаем except
		bmessage = json.dumps(dict(message), indent=4, sort_keys=True, ensure_ascii=False)  # делаем красивый словарь из компонентов сообщения (чат, пользователь, текст или стикер и прочие значения)
		await message.delete()  # удаляем сообщение о том что пользователь подключился
		await bot.send_message(message.chat.id, rf"""👋 Привет @{message.new_chat_members[0].username} 👋
 🔥Правила чата:🔥 
1) Ваши сообщения только текстом. 
2) Никаких оскорблений. 
3) Общение только по существу. 
4) Стикеры 18+ БАН навсегда 
5) Сторонние ссылки (реклама) 
 ❗️Любое нарушение - бан❗️""")  # пишем сообщение с приветствием и правилами
	except Exception as ex:  # при ошибке в блоке try мы записываем её в перемнную ex и выполняем код внутри except
		print(ex)  # пишем ошибку
		sleep(0.1)  # засыпание программы на 1/10 секунды
		
executor.start_polling(dp, skip_updates=True)  # запуск бота
