from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
from handlers import Handlers


class TamagotchiBot:
    def __init__(self, token):
        self.bot = Bot(token=token)
        self.dp = Dispatcher(self.bot)
        self.handlers = Handlers(self.bot)
        self.register_handlers()

    def register_handlers(self):
        self.dp.register_message_handler(self.handlers.send_welcome, commands=['start'])
        self.dp.register_message_handler(self.handlers.update_name)
        self.dp.register_callback_query_handler(self.handlers.process_callback_health_up,
                                                lambda x: x.data == 'health_up')
        self.dp.register_callback_query_handler(self.handlers.process_callback_health_down,
                                                lambda x: x.data == 'health_down')
        self.dp.register_callback_query_handler(self.handlers.process_callback_update_name,
                                                lambda x: x.data == 'update_name')

    def start(self):
        executor.start_polling(self.dp, skip_updates=True)
