# src/calibre/application/use_cases/get_panchanga_for_date.py
from datetime import datetime
from astrology.domain.models.panchanga import Panchanga
from astrology.domain.services.astrology_engine import AstrologyEngine
class GetPanchangaForDate:
    """
    This class orchestrates the process of generating a Panchanga.
    It uses the ports to fetch external data and the domain engine to perform calculations.
    """

    def __init__(self, astrology_engine: AstrologyEngine):
        self.astrology_engine = astrology_engine

    def execute(self, 
                date: datetime,
                latitude: float,
                longitude: float) -> Panchanga:

        print("Use Case: Handing off to the astrology engine for calculation...")
        panchanga = self.astrology_engine.calculate_panchanga(
            date=date,
            latitude=latitude,
            longitude=longitude
        )

        return panchanga
