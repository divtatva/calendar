from astrology.domain.models.panchanga import Panchanga
from astrology.domain.models.panchanga_1 import HinduCalendarDay, Location, LunarCalendar, Muhurat, Sun, Tithi

class Transformer:
    def transform(oldPanchanga: Panchanga,
                    latitude: float,
                    longitude: float) -> HinduCalendarDay:
        """
        Transforms a Panchanga object into a HinduCalendarDay object.
        """
        # Transform the Panchanga object into a HinduCalendarDay object.
        hindu_calendar_day = HinduCalendarDay(
            date=oldPanchanga.date.strftime("%Y-%m-%d"),
            location=Location(
                city="Unknown",  # Assuming city is not available in Panchanga
                latitude=latitude,
                longitude=longitude,
                timezone="Unknown"  # Assuming timezone is not available in Panchanga
            ),
            sun=Sun(
                sunrise=oldPanchanga.sunrise.strftime("%I:%M:%S %p"),
                sunset=oldPanchanga.sunset.strftime("%I:%M:%S %p"),
                sun_icon_state="clear-day"
            ),
            lunar_calendar=LunarCalendar(
                tithi=Tithi(
                    name=oldPanchanga.tithi[0].name,
                    number=oldPanchanga.tithi[0].id,
                    paksha=oldPanchanga.paksha,
                    month=oldPanchanga.hindu_maasa.purnimanta,
                    ends_at=oldPanchanga.tithi[0].end_time.strftime("%I:%M:%S %p")
                )
            ),
            festivals=[
                
            ],
            muhurat=[
                Muhurat(
                    name="Abhijit Muhurat",
                    start=oldPanchanga.muhurta.abhijit_muhurta.start.strftime("%I:%M:%S %p"),
                    end=oldPanchanga.muhurta.abhijit_muhurta.end.strftime("%I:%M:%S %p"),
                    quality="Auspicious",
                    is_warning=False
                ) ,
                Muhurat(
                    name="Rahu Kaalam",
                    start=oldPanchanga.muhurta.rahu_kaalam.start.strftime("%I:%M:%S %p"),
                    end=oldPanchanga.muhurta.rahu_kaalam.end.strftime("%I:%M:%S %p"),
                    quality="Inauspicious",
                    is_warning=True
                ),
                Muhurat(
                    name="Gulika Kaalam",
                    start=oldPanchanga.muhurta.gulika_kaalam.start.strftime("%I:%M:%S %p"),
                    end=oldPanchanga.muhurta.gulika_kaalam.end.strftime("%I:%M:%S %p"),
                    quality="Inauspicious",
                    is_warning=True
                ),
                Muhurat(
                    name="Yamaganda Kaalam",
                    start=oldPanchanga.muhurta.yamaganda_kaalam.start.strftime("%I:%M:%S %p"),
                    end=oldPanchanga.muhurta.yamaganda_kaalam.end.strftime("%I:%M:%S %p"),
                    quality="Inauspicious",
                    is_warning=True
                ),
            ],
        )
        return hindu_calendar_day