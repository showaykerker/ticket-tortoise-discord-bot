import datetime
import pytz
from typing import List, Dict, Union

# Set the timezone to +8
timezone = pytz.timezone('Asia/Taipei')

USER_MODEL = {
    "discord_id": int,
    "name": str,
    "create_date": datetime.datetime,
    "last_activate_date": datetime.datetime,
    "configs": Dict[str, Union[str, int, bool, List[str]]],
    "events_created": List[int]
}

EVENT_MODEL = {
    "name": str,
    "date": datetime.datetime,
    "url": str,
    "available_zones": List[str],
    "expired": bool,
    "required_by": List[int],
    "create_by": str,
    "create_date": datetime.datetime
}

EVENT_REQUIREMENT_MODEL = {
    "event_id": int,
    "user_id": int,
    "interested_zones": List[str],
    "create_date": datetime.datetime,
    "expired": bool
}

class ABC:
    def __init__(self, model: dict, **kwargs):
        self._model = model
        self.create_date = datetime.datetime.now(timezone) # Can be overwritten
        for key, value in kwargs.items():
            if key != "_id":
                assert key in self._model, f"Key {key} is not in model."
                assert value is None or isinstance(value, self._model[key]), \
                    f"Value {value} is not of type {self._model[key]} but {type(value)}."
            if key == "create_date":
                self.create_date = value or self.create_date
            else:
                setattr(self, key, value)
        for key, dtype_ in self._model.items():
            if key not in kwargs:
                try:
                    setattr(self, key, dtype_())
                except:
                    setattr(self, key, None)
        
    def to_dict(self) -> dict:
        return {key: getattr(self, key) for key in self._model.keys()}

    
class User(ABC):
    def __init__(self, **kwargs):
        super().__init__(USER_MODEL, **kwargs)
        assert "discord_id" in kwargs, "discord_id is required for User creation."
        assert "name" in kwargs, "name is required for User creation."

class Event(ABC):
    def __init__(self, **kwargs):
        super().__init__(EVENT_MODEL, **kwargs)
        

class EventRequirement(ABC):
    def __init__(self, **kwargs):
        super().__init__(EVENT_REQUIREMENT_MODEL, **kwargs)