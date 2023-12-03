import time

from api_usos import api
from api_usos.response import BotResponse


def schedule():
    return api.take_plan(time.strftime('%Y-%m-%d'), '7')


def main():
    today_schedule = schedule()
    if today_schedule == "You have no classes in this period":
        print(today_schedule)
    else:
        for key in today_schedule:
            response = BotResponse(today_schedule[key]['name'],
                                   today_schedule[key]['name_pl'],
                                   today_schedule[key]['name_en'],
                                   today_schedule[key]['start_time'],
                                   today_schedule[key]['end_time'],
                                   today_schedule[key]['room_number'],
                                   today_schedule[key]['name_lecturer'])
            print(response)

main()