from aiogram import types
from aiogram.utils import executor
import time

from api_usos import api
from api_usos.response import BotResponse
from core.settings import dp


def schedule():
    return api.take_plan(time.strftime('%Y-%m-%d'), '7')


@dp.message_handler()
async def echo_send(message: types.Message):
    today_schedule = schedule()
    if today_schedule == "You have no classes in this period":
        await message.answer(today_schedule)
    else:
        for key in today_schedule:
            response = BotResponse(today_schedule[key]['name'],
                                   today_schedule[key]['name_pl'],
                                   today_schedule[key]['name_en'],
                                   today_schedule[key]['start_time'],
                                   today_schedule[key]['end_time'],
                                   today_schedule[key]['room_number'],
                                   today_schedule[key]['name_lecturer'])
            await message.answer(response)


executor.start_polling(dp, skip_updates=True)
