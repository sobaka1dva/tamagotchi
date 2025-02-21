from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram import types
from models import session, Tamagotchi
from utils import *


class Handlers:
    def __init__(self, bot):
        self.bot = bot

    async def send_welcome(self, message):
        user_id = message.from_user.id
        tamagotchi = session.query(Tamagotchi).filter_by(id=user_id).first()
        if not tamagotchi:
            tamagotchi = Tamagotchi(id=user_id)
            session.add(tamagotchi)
            session.commit()

        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton("+ Плюс", callback_data="health_up"))
        markup.add(InlineKeyboardButton("- Минус", callback_data="health_down"))
        markup.add(InlineKeyboardButton("Обновить имя", callback_data="update_name"))

        await message.answer_photo(
            photo=open(get_image_path(tamagotchi.current_health), 'rb'),
            caption=f'Имя: {tamagotchi.name}\nЗдоровье: {get_health(tamagotchi.current_health)}',
            reply_markup=markup
        )

    async def process_callback_health_up(self, callback_query):
        user_id = callback_query.from_user.id
        tamagotchi = session.query(Tamagotchi).filter_by(id=user_id).first()
        if tamagotchi.current_health < 20:
            tamagotchi.current_health += 1
            session.commit()
        await self.bot.answer_callback_query(callback_query.id)
        await self.update_message(callback_query.message, tamagotchi)

    async def process_callback_health_down(self, callback_query):
        user_id = callback_query.from_user.id
        tamagotchi = session.query(Tamagotchi).filter_by(id=user_id).first()
        if tamagotchi.current_health > 0:
            tamagotchi.current_health -= 1
            session.commit()
        await self.bot.answer_callback_query(callback_query.id)
        await self.update_message(callback_query.message, tamagotchi)

    async def process_callback_update_name(self, callback_query):
        await self.bot.answer_callback_query(callback_query.id)
        await self.bot.send_message(callback_query.from_user.id, "Введите новое имя:")

    async def update_name(self, message):
        user_id = message.from_user.id
        tamagotchi = session.query(Tamagotchi).filter_by(id=user_id).first()
        tamagotchi.name = message.text
        session.commit()
        await message.answer(f'Имя изменено на {tamagotchi.name}')
        await self.send_welcome(message)

    def create_markup(self):
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton("+ Плюс", callback_data="health_up"))
        markup.add(InlineKeyboardButton("- Минус", callback_data="health_down"))
        markup.add(InlineKeyboardButton("Обновить имя", callback_data="update_name"))
        return markup

    async def update_message(self, message, tamagotchi: Tamagotchi):
        media = types.InputMediaPhoto(
            media=open(get_image_path(tamagotchi.current_health), 'rb'),
            caption=f'Имя: {tamagotchi.name}\nЗдоровье: {get_health(tamagotchi.current_health)}'
        )
        await message.edit_media(media, reply_markup=self.create_markup())
