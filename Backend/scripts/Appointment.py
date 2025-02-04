import datetime
from datetime import date, timedelta
import logging
import json

logger = logging.getLogger('FIS')


# noinspection PyRedundantParentheses
class Appointment_Abstract:
    def __new__(cls, *args, **kwargs):
        return super().__new__(cls)

    def __init__(self, id: int, name: str, description: str, startTime: datetime.time, endTime: datetime.time, lecturer: int,
                 room: int, dateSpan: int):
        self.groups = None
        self.id = id
        self.name = name
        self.description = description
        self.startTime = startTime
        self.endTime = endTime
        self.lecturer = lecturer
        self.room = room
        self.dateSpan = dateSpan

    def resolveTargetGroups(self, database):
        self.groups = database.GetIntrestedGroups(self.id)

    def resolveToAppointment_Where(self, database, DateCondition):
        today = date.today()
        start, end, repeat = database.FetchRepeateInfo(self.dateSpan)
        self.resolveTargetGroups(database)
        if (repeat == 0 and DateCondition(start, today)):
            return [Appointment(self, start)]
        # In this case We need to get all futer Events
        Appointments = []

        event = start
        while (event < end):
            event += timedelta(days=repeat)
            if (DateCondition(event, today)):
                Appointments.append(Appointment(self, event, database))
        return Appointments

    def resolveToAppointment(self, database):
        start, end, repeate = database.FetchRepeateInfo(self.dateSpan)
        self.resolveTargetGroups(database)
        if (repeate == 0):
            return [Appointment(self, start)]
        # In this case We need to get all futer Events
        Appointments = []
        today = date.today()
        event = start
        while (event < end):
            event += timedelta(days=repeate)
            if (event >= today):
                Appointments.append(Appointment(self, event, database))
        return Appointments

    def toJson(self):
        return {"id": self.id,
                "name": self.name,
                "description": self.description,
                "start": self.startTime.strftime("%H:%M"),
                "end": self.endTime.strftime("%H:%M"),
                "lecturer": self.lecturer,
                "room": self.room,
                "dateSpan": self.dateSpan,
                "groups": self.groups
                }


class Appointment:
    def __new__(cls, *args, **kwargs):
        return super().__new__(cls)

    def __init__(self, abstractApp: Appointment_Abstract, date: date, Database):
        self.id = abstractApp.id
        self.name = abstractApp.name
        self.description = abstractApp.description
        self.startTime = abstractApp.startTime
        self.endTime = abstractApp.endTime

        self.canceled = Database.IsAppointmentCanceld(date, self.id)
        self.groups = abstractApp.groups

        self.lecturer = abstractApp.lecturer
        self.room = abstractApp.room
        self.roomName = Database.GetRoomName(self.room)

        self.date = date

    def toJson(self):
        return {"id": self.id, "name": self.name, "description": self.description,
                "start": self.startTime.strftime("%H:%M"),
                "end": self.endTime.strftime("%H:%M"), "lecturer": self.lecturer,
                "date": self.date.strftime("%d.%m.%Y"),
                "canceld": self.canceled, "groups": self.groups, "room": self.roomName}
