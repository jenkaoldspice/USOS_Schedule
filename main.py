import time
import json
from aiogram import Bot, Dispatcher, types, executor
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from core.settings import API_TOKEN, DATA_FILE
from api_usos import api
from api_usos.response import BotResponse

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)


def load_data():
    try:
        with open(DATA_FILE, "r") as file:
            data = file.read()
            if not data:
                return {}
            return json.loads(data)
    except FileNotFoundError:
        with open(DATA_FILE, "a") as file:
            return


def save_data(data):
    with open(DATA_FILE, "w") as file:
        json.dump(data, file, indent=4)


user_data = load_data()


def get_main_menu_keyboard():
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(KeyboardButton("/schedule"), KeyboardButton("/change"))
    return keyboard


@dp.message_handler(commands=["start"])
async def start_handler(message: types.Message):
    user_id = str(message.from_user.id)
    if user_id not in user_data:
        await message.reply("Cześć! Wprowadź swój login:")
    else:
        await message.reply("Cześć, już mamy twoje dane do logowania\n"
                            "Wprowadż jedną z dostępnych komend:\n"
                            "/schedule - Wysyłka aktualnego harmonogramu(maksymalnie 7 dni)\n"
                            "/change - Zmień login, hasło lub oba")


@dp.message_handler(commands=["help"])
async def help_handler(message: types.Message):
    help_text = (
        "Dostępne komendy:\n"
        "/start - Rozpocznij interakcję z botem\n"
        "/schedule - Wysyłka aktualnego harmonogramu(maksymalnie 7 dni)\n"
        "/change - Zmień login, hasło lub oba"
    )
    await message.reply(help_text)


@dp.message_handler(commands=["change"])
async def change_credentials(message: types.Message):
    user_id = str(message.from_user.id)
    if user_id not in user_data or "login" not in user_data[user_id] or "password" not in user_data[user_id]:
        await message.reply("Nie wprowadziłeś jeszcze loginu lub hasła. Wprowadź je przed użyciem tego polecenia.")
        return
    else:
        keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        keyboard.add(KeyboardButton("Zmień login"), KeyboardButton("Zmień hasło"),
                     KeyboardButton("Zmień login i hasło"))
        await message.reply("Wybierz opcję zmiany:", reply_markup=keyboard)


@dp.message_handler(lambda message: message.text in ["Zmień login", "Zmień hasło", "Zmień login i hasło"])
async def handle_change_option(message: types.Message):
    global user_data
    user_id = str(message.from_user.id)
    option = message.text
    if option == "Zmień login":
        user_data[user_id].pop("login", None)
        save_data(user_data)
        await message.reply("Twój login został usunięty. Wprowadź nowy login:",
                            reply_markup=types.ReplyKeyboardRemove())
    elif option == "Zmień hasło":
        user_data[user_id].pop("password", None)
        save_data(user_data)
        await message.reply("Twoje hasło zostało usunięte. Wprowadź nowe hasło:",
                            reply_markup=types.ReplyKeyboardRemove())
    elif option == "Zmień login i hasło":
        user_data.pop(user_id, None)
        save_data(user_data)
        await message.reply("Twoje dane zostały usunięte. Wprowadź nowy login:",
                            reply_markup=types.ReplyKeyboardRemove())


@dp.message_handler(lambda message: message.text not in ["/schedule", "1", "2", "3," "4", "5", "6", "7"])
async def save_login(message: types.Message):
    global user_data
    user_id = str(message.from_user.id)
    if user_id not in user_data:
        user_data[user_id] = {}
    if "login" not in user_data[user_id]:
        user_data[user_id]["login"] = message.text
        if "password" not in user_data[user_id]:
            await message.reply("Login zapisany! Teraz wprowadź swoje hasło:")

        else:
            save_data(user_data)
            await message.reply("Login zapisany! Teraz dostępne jest polecenie /schedule")
    elif "password" not in user_data[user_id]:
        user_data[user_id]["password"] = message.text
        save_data(user_data)
        await message.reply(f"Twój login i hasło zostały zapisane!\nTeraz dostępne jest polecenie /schedule.",
                            reply_markup=get_main_menu_keyboard())


@dp.message_handler(commands=["schedule"])
async def schedule_handler(message: types.Message):
    user_id = str(message.from_user.id)
    if user_id not in user_data or "login" not in user_data[user_id] or "password" not in user_data[user_id]:
        await message.reply("Nie wprowadziłeś jeszcze loginu lub hasła. Wprowadź je przed użyciem tego polecenia.")
        return

    keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    buttons = [KeyboardButton(str(i)) for i in range(1, 8)]
    keyboard.add(*buttons)
    await message.reply("Wybierz liczbę dni (1-7):", reply_markup=keyboard)


@dp.message_handler(lambda message: message.text in [str(i) for i in range(1, 8)])
async def days_handler(message: types.Message):
    global response
    user_id = str(message.from_user.id)
    await message.reply(f"Wybrałeś {message.text} dni dla harmonogramu.", reply_markup=types.ReplyKeyboardRemove())
    schedule = api.take_plan(time.strftime('%Y-%m-%d'), message.text, user_data[user_id]['login'],
                             user_data[user_id]['password'])
    if schedule == "You have no classes in this period":
        await message.reply("W tym okresie nie masz żadnych zajęć")
        return
    elif schedule == "Login or password is wrong":
        await message.answer("Login lub hasło nie poprawne, zmień za pomocą komendy /change")
    else:
        response = ""
        for key in schedule:
            one_response = BotResponse(schedule[key]['name'],
                                       schedule[key]['name_pl'],
                                       schedule[key]['name_en'],
                                       schedule[key]['start_time'],
                                       schedule[key]['end_time'],
                                       schedule[key]['room_number'],
                                       schedule[key]['name_lecturer'])
            response = response + f'{one_response}\n'
        await message.answer(response, reply_markup=get_main_menu_keyboard())


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
