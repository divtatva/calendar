# src/astrology/domain/models/panchanga.py
import json
from dataclasses import asdict, dataclass, is_dataclass
from datetime import date, datetime, time
from typing import List


class CustomEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, time):
            return obj.strftime("%I:%M:%S %p")
        if isinstance(obj, datetime):
            return obj.strftime("%Y-%m-%d, %I:%M:%S %p")
        if isinstance(obj, date):
            return obj.isoformat()
        if is_dataclass(obj) and not isinstance(obj, type):
            return asdict(obj)
        return super().default(obj)


# Base class for elements with a start and end time.
@dataclass
class TimedEvent:
    id: int
    name: str
    start_time: datetime
    end_time: datetime

# Specific dataclasses for each of the five limbs (angas).
@dataclass
class TithiDetail(TimedEvent):
    pass #TODO: add deity

@dataclass
class NakshatraDetail(TimedEvent):
    pass #TODO: add deity

@dataclass
class YogaDetail(TimedEvent):
    pass

@dataclass
class KaranaDetail(TimedEvent):
    pass

@dataclass
class MuhurtaTime:
    start: datetime
    end: datetime

@dataclass
class Muhurta:
    abhijit_muhurta: MuhurtaTime
    rahu_kaalam: MuhurtaTime
    gulika_kaalam: MuhurtaTime
    yamaganda_kaalam: MuhurtaTime

@dataclass
class HinduMaasa:
    purnimanta: str
    amanta: str
    is_adhika_maasa: bool

@dataclass
class Samvat:
    year: int
    name: str

# The main Panchanga domain model, updated to represent the full JSON structure.
@dataclass
class Panchanga:
    """
    Represents the comprehensive panchanga details for a specific date,
    mapping directly to the provided JSON structure.
    """
    date: date
    day: str
    sunrise: datetime
    sunset: datetime
    moonrise: datetime
    moonset: datetime
    paksha: str
    ritu: str
    ayana: str
    
    # Use the detailed dataclasses for lists of events
    tithi: List[TithiDetail]
    nakshatra: List[NakshatraDetail]
    yoga: List[YogaDetail]
    karana: List[KaranaDetail]
    
    # Use the specific dataclasses for nested objects
    muhurta: Muhurta
    hindu_maasa: HinduMaasa
    vikram_samvat: Samvat
    shaka_samvat: Samvat