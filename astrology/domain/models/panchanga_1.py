from dataclasses import dataclass


@dataclass
class Location:
    city: str
    latitude: float
    longitude: float
    timezone: str


@dataclass
class Sun:
    sunrise: str
    sunset: str
    sun_icon_state: str


@dataclass
class Tithi:
    name: str
    number: int
    paksha: str
    month: str
    ends_at: str


@dataclass
class LunarCalendar:
    tithi: Tithi


@dataclass
class Festival:
    name: str
    significance: str


@dataclass
class Muhurat:
    name: str
    start: str
    end: str
    quality: str
    is_warning: bool | None = None


@dataclass
class HinduCalendarDay:
    date: str
    location: Location
    sun: Sun
    lunar_calendar: LunarCalendar
    festivals: list[Festival]
    muhurat: list[Muhurat]
