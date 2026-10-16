from dataclasses import dataclass
from datetime import date


@dataclass
class Cruise:
    cruise_name: str
    ship_name: str
    departure_port: str
    departure_date: date
    return_date: date
    trip_total: float

    @property
    def nights(self):
        return (self.return_date - self.departure_date).days