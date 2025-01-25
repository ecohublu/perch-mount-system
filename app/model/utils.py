import enum
from datetime import datetime, date


class JsonAbleModel:
    def to_json(self):
        json = {}
        for c in self.__table__.columns:
            value = getattr(self, c.name)

            if type(value) == datetime or type(value) == date:
                value = value.isoformat()

            json[c.name] = value

        return json
