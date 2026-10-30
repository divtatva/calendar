from datetime import datetime
from typing import List, Dict
from dataclasses import dataclass

@dataclass
class PlanetaryPosition:
    """
    Represents a planetary position in the Rasi chart.
    """
    planet: int # Planet index (0-8 for Sun to Ketu)
    rasi: int  # Rasi index (0-11)
    degree: float
    is_lagna: bool = False  # True if this is the Lagna (Ascendant)
