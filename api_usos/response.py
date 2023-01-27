class Response:
    def __init__(self, name, start_time, end_time, room_number, lecturer_ids, name_lecturer, number):
        if 'E-learning' in name['pl']:
            self.name = name['pl']
        else:
            self.name = name['pl'].split(' - ')[0]
        self.type_pl = name['pl'].split(' - ')[1]
        self.type_en = name['en'].split(' - ')[1]
        self.start_time = start_time
        self.end_time = end_time
        self.room_number = room_number
        self.lecturer_ids = lecturer_ids
        self.name_lecturer = name_lecturer
        self.number = number

    def get_repr(self):
        return {
            str(self.number): {
                "name": self.name,
                "name_pl": self.type_pl,
                "name_en": self.type_en,
                "start_time": self.start_time,
                "end_time": self.end_time,
                "room_number": self.room_number,
                "lecturer_ids": self.lecturer_ids,
                "name_lecturer": self.name_lecturer
            }
        }


class BotResponse():
    def __init__(self, name, name_pl, name_en, start_time, end_time, room_number, name_lecturer):
        self.name = name
        self.type_pl = name_pl
        self.type_en = name_en
        self.start_time = start_time
        self.end_time = end_time
        self.room_number = room_number
        self.name_lecturer = name_lecturer

    def __repr__(self):
        return f"""\n
            Nazwa przedmiotu: {self.name}\n
            Rodzaj: pl: {self.type_pl}, eu: {self.type_en}\n
            Czas rozpoczęcia: {self.start_time}\n
            Czas zakończenia: {self.end_time}\n
            Sala: {self.room_number}\n
            Prowadzący: {self.name_lecturer}\n
        """
