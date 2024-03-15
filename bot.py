import asyncio
import logging
import os
from aiogram import Bot, Router, Dispatcher, types
from aiogram.filters import Command
from aiogram.handlers import MessageHandler
from config import BOT_TOKEN
from utils import process_message


# Инициализация бота
bot = Bot(token=BOT_TOKEN, parse_mode="Markdown")

# Инициализация роутера
router = Router()

# Инициализация диспетчера
dp = Dispatcher()
dp.bot = bot
dp.include_router(router)

# Путь к файлу с изображением (относительно текущего каталога)
image_path = os.path.join('images', 'Default_A_serene_cityscape_at_dawn_the_calm_before_the_storm_0.jpg')

# Создание экземпляра InputFile
photo = types.FSInputFile(image_path)

# Обработчик команды /start
@router.message(Command('start'))
async def send_welcome(message: types.Message):
    # Отправка изображения из локальной папки
    await bot.send_photo(
        chat_id=message.chat.id,
        photo=photo,
        caption="Привет👋, Я ИИ бот который может помочь тебе улучшить скилы и знания которые помогут выиграть дебаты🚀 Можешь начать разговор со мной и проверить как это работает😇 \n Удачи !",
        reply_markup=types.InlineKeyboardMarkup(
            inline_keyboard=[[
                types.InlineKeyboardButton(
                    text="Смотреть видео",
                    url="https://youtu.be/ph1EFkuCmyo?si=vLho92dJKMknhigx"
                )
            ]]
        )
    )


    # Через 1 минуту отправляем сообщение о возможности общения с ботом
    await asyncio.sleep(60)
    await bot.send_message(
        chat_id=message.chat.id,
        text=""
    )
# Обработчик всех остальных сообщений
@router.message()
async def handle_message(message: types.Message):
    # Обрабатываем входящее сообщение и получаем ответ от OpenAI API
       response = process_message(message)

    # Отправляем ответ пользователю
       await message.answer(response)

if __name__ == '__main__':
    from database import create_table
    create_table()

    # Запуск бота
    logging.basicConfig(level=logging.INFO)
    asyncio.run(dp.start_polling(bot))
