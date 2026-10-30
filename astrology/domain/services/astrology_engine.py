import re
from datetime import datetime, timedelta
from typing import List
from jhora.panchanga import drik
from jhora.horoscope.chart import charts 
from jhora import utils, const
import os

from astrology.domain.models.chart import PlanetaryPosition
from ..models.panchanga import (
    HinduMaasa,
    KaranaDetail,
    Muhurta,
    MuhurtaTime,
    NakshatraDetail,
    Panchanga,
    Samvat,
    TithiDetail,
    YogaDetail
)

def parse_time_with_offset(time_str, base_date):
    
    match = re.match(r"(\d{2}:\d{2}:\d{2})(?:\s*\(([-+]?\d+)\))?", time_str)
    if match:
        time_part = match.group(1)
        offset = int(match.group(2)) if match.group(2) else 0
        dt = datetime.combine(base_date + timedelta(days=offset), datetime.strptime(time_part, "%H:%M:%S").time())
        return dt
    else:
        raise ValueError(f"Invalid time string format {time_str} {base_date}")

def parse_time_with_offset_new(time_str, base_date):
    
    match = re.match(r"([-]*\d{0,2}):([-]*\d{0,2}):([-]*\d{0,2})(?:\s*\(([-+]?\d+)\))?", time_str)
    if match:
        hh = int(match.group(1))
        mm = int(match.group(2))
        ss = int(match.group(3))
        offset = int(match.group(4)) if match.group(4) else 0
        dt = base_date + timedelta(hours=hh, minutes=mm, seconds=ss, days=offset)
        return dt
    else:
        raise ValueError(f"Invalid time string format {time_str} {base_date}")



class AstrologyEngine:
    RITU_LIST = ['Vasanta', 'Greeshma', 'Varsha', 'Sharath', 'Hemantha', 'Shishira']

    def calculate_panchanga(
            self,
            date: datetime,
            latitude: float,
            longitude: float,
            ) -> Panchanga:
        
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        const_en_path = os.path.join(base_dir, "lang", "const_en.txt")
        resources = utils.get_resource_lists(const_en_path)
        # Get the julian date for the given date
        jd = utils.gregorian_to_jd(drik.Date(date.year, date.month, date.day))

        # Create the Place object with the given latitude and longitude
        place = drik.Place("Unknown", latitude, longitude, +5.5)
        sunrise = drik.sunrise(jd, place)

        sunrise_time = parse_time_with_offset_new(sunrise[1],date)

        sunset = drik.sunset(jd, place)
        sunset_time = parse_time_with_offset_new(sunset[1], date)


        moonrise = drik.moonrise(jd, place)
        moonrise_time = parse_time_with_offset_new(moonrise[1],date)
        moonset = drik.moonset(jd, place)
        moonset_time = parse_time_with_offset_new(moonset[1],date)

        # 23-07-2025 [28, -16.946667113174463, 4.673331385436752, 29, 4.673331385436752, 4.678873628572271]
        # 24-07-2025 [29, -19.449615701851975, 2.4949134051276065, 30, 2.4949134051276065, 2.4973320272333006]
        # TITHI CALCULATION START
        _tithi_returned = drik.tithi(jd, place, True)
        first_tithi_id = _tithi_returned[0]
        first_tithi_name = utils.TITHI_LIST[_tithi_returned[0]-1]
        first_tithi_start_time = parse_time_with_offset_new(utils.to_dms(_tithi_returned[1]), date)
        first_tithi_end_time = parse_time_with_offset_new(utils.to_dms(_tithi_returned[2]), date)

        tithis = []
        first_tithi_detail = TithiDetail(
            id=first_tithi_id,
            name=first_tithi_name,
            start_time=first_tithi_start_time,
            end_time=first_tithi_end_time
        )
        tithis.append(first_tithi_detail)

        if len(_tithi_returned) > 3:
            second_tithi_name = utils.TITHI_LIST[_tithi_returned[3]-1]
            second_tithi_id = _tithi_returned[3]
            second_tithi_start_time = parse_time_with_offset_new(utils.to_dms(_tithi_returned[4]), date)
            second_tithi_end_time = parse_time_with_offset_new(utils.to_dms(_tithi_returned[5]), date)

            second_tithi_detail = TithiDetail(
                id=second_tithi_id,
                name=second_tithi_name,
                start_time=second_tithi_start_time,
                end_time=second_tithi_end_time
            )
            tithis.append(second_tithi_detail)

        # TITHI CALCULATION END
        
        # PAKSHA CALCULATION START
        _paksha = 0 if _tithi_returned[0]<=15 else 1
        paksha = utils.PAKSHA_LIST[_paksha]
        # PAKSHA CALCULATION END
        # RITU CALCULATION START
        lmd = drik.lunar_month_date(jd, place, use_purnimanta_system=True)
        _ritu_num = drik.ritu(lmd[0])
        ritu = utils.SEASON_NAMES[_ritu_num] if _ritu_num > 0 else None
        # RITU CALCULATION END

        # AYANA CALCULATION START
        _ayana = const._DEFAULT_AYANAMSA_MODE
        # AYANA CALCULATION END

        # NAKSHATRA CALCULATION START
        nakshatras = drik.nakshatra_new(jd, place)
        _first_nakshatra_id = nakshatras[0]
        _first_nakshatra_name = utils.NAKSHATRA_LIST[_first_nakshatra_id-1]
        first_nakshatra_start_time = parse_time_with_offset_new(utils.to_dms(nakshatras[2]), date)
        first_nakshatra_end_time =  parse_time_with_offset_new(utils.to_dms(nakshatras[3]), date)
        first_nakshatra_detail = NakshatraDetail(
            id=_first_nakshatra_id,
            name=_first_nakshatra_name,
            start_time=first_nakshatra_start_time,
            end_time=first_nakshatra_end_time
        )
        nakshatras_list = [first_nakshatra_detail]
        if len(nakshatras) > 4:
            _second_nakshatra_id = nakshatras[4]
            _second_nakshatra_name = utils.NAKSHATRA_LIST[_second_nakshatra_id-1]
            second_nakshatra_start_time = parse_time_with_offset_new(utils.to_dms(nakshatras[6]), date)
            second_nakshatra_end_time = parse_time_with_offset_new(utils.to_dms(nakshatras[7]), date)
            second_nakshatra_detail = NakshatraDetail(
                id=_second_nakshatra_id,
                name=_second_nakshatra_name,
                start_time=second_nakshatra_start_time,
                end_time=second_nakshatra_end_time
            )
            nakshatras_list.append(second_nakshatra_detail)
        # NAKSHATRA CALCULATION END

        # YOGA CALCULATION START
        # Placeholder for Yoga calculation logic
        # For now, we will return an empty list as Yoga details are not yet implemented
        yogas = drik.yogam(jd, place)
        _first_yoga_id = yogas[0]
        _first_yoga_name = utils.YOGAM_LIST[_first_yoga_id-1]
        first_yoga_start_time = parse_time_with_offset_new(utils.to_dms(yogas[1]), date)
        first_yoga_end_time = parse_time_with_offset_new(utils.to_dms(yogas[2]), date)
        first_yoga_detail = YogaDetail(
            id=_first_yoga_id,
            name=_first_yoga_name,
            start_time=first_yoga_start_time,
            end_time=first_yoga_end_time
        )
        yogas_list = [first_yoga_detail]
        if len(yogas) > 4:
            _second_yoga_id = yogas[4]
            _second_yoga_name = utils.YOGAM_LIST[_second_yoga_id-1]
            second_yoga_start_time = parse_time_with_offset_new(utils.to_dms(yogas[5]), date)
            second_yoga_end_time = parse_time_with_offset_new(utils.to_dms(yogas[6]), date)
            second_yoga_detail = YogaDetail(
                id=_second_yoga_id,
                name=_second_yoga_name,
                start_time=second_yoga_start_time,
                end_time=second_yoga_end_time
            )
            yogas_list.append(second_yoga_detail)
        # YOGA CALCULATION END

        # KARANA CALCULATION START
        karanas = drik.karana(jd, place)
        karana_id = karanas[0]
        karana_name = utils.KARANA_LIST[karana_id-1]
        karana_start_time = parse_time_with_offset_new(utils.to_dms(karanas[1]), date)
        karana_end_time = parse_time_with_offset_new(utils.to_dms(karanas[2]), date)
        karana_detail = KaranaDetail(
            id=karana_id,
            name=karana_name,
            start_time=karana_start_time,
            end_time=karana_end_time
        )
        # KARANA CALCULATION END
        
        # MUHURTA CALCULATION START
        ## Abhijit Muhurta
        abhijit_muhurat = drik.abhijit_muhurta(jd, place)
        raahu_kaalam = drik.raahu_kaalam(jd, place)
        yamaganda_kaalam =  drik.yamaganda_kaalam(jd, place)
        gulikai_kaalam = drik.gulikai_kaalam(jd, place)
        
        muhurta = Muhurta(
            abhijit_muhurta=MuhurtaTime(
                start=parse_time_with_offset_new(abhijit_muhurat[0], date),
                end=parse_time_with_offset_new(abhijit_muhurat[1], date)
            ),
            rahu_kaalam=MuhurtaTime(
                start=parse_time_with_offset_new(raahu_kaalam[0], date),
                end=parse_time_with_offset_new(raahu_kaalam[1], date)  # Assuming same
            ),  
            gulika_kaalam=MuhurtaTime(
                start=parse_time_with_offset_new(gulikai_kaalam[0], date),
                end=parse_time_with_offset_new(gulikai_kaalam[1], date)  # Assuming same
            ),  
            yamaganda_kaalam=MuhurtaTime(
                start=parse_time_with_offset_new(yamaganda_kaalam[0], date),
                end=parse_time_with_offset_new(yamaganda_kaalam[1], date)  # Assuming same
            )  
        )
        # MUHURTA CALCULATION END

        # MAASA CALCULATION START
        # Placeholder for Hindu Maasa calculation logic
        p_lmd = drik.lunar_month_date(jd, place, use_purnimanta_system=True)
        a_lmd = drik.lunar_month_date(jd, place, use_purnimanta_system=False)
        
        hindu_maasa = HinduMaasa(
            amanta=utils.MONTH_LIST[a_lmd[0]-1],
            purnimanta=utils.MONTH_LIST[p_lmd[0]-1],
            is_adhika_maasa=p_lmd[3] 
        )  # Not implemented yet
        # MAASA CALCULATION END

        # VIKRAM SAMVAT CALCULATION START
        maas_no = drik.lunar_month(jd, place)
        [kali_year, vikrama_year,saka_year] = drik.elapsed_year(jd,maas_no[0])
        
        return Panchanga(
            date=date,
            day = date.strftime("%A"),
            sunrise = sunrise_time,
            sunset = sunset_time,
            moonrise= moonrise_time,
            moonset = moonset_time,
            paksha = paksha,
            ritu = ritu,
            ayana = _ayana,
            
            # Use the detailed dataclasses for lists of events
            tithi = tithis,
            nakshatra = nakshatras_list,
            yoga = yogas_list,
            karana = [karana_detail],
            
            # Use the specific dataclasses for nested objects
            muhurta = muhurta,
            hindu_maasa = hindu_maasa,
            vikram_samvat = Samvat(year=vikrama_year, name="Vikrama"),
            shaka_samvat = Samvat(year=saka_year, name="Shaka")
            
    )

    def calculate_rasi_chart(self, date: datetime, latitude: float, longitude: float) -> List[PlanetaryPosition]:
        # Create Place Object
        place = drik.Place('Unknown',longitude=longitude, latitude=latitude, timezone=+5.5)

        # Get the Julian date for the given date
        dob = (date.year, date.month, date.day)
        tob = (date.hour,date.minute,date.second)

        chart = charts.rasi_chart(utils.julian_day_number(dob, tob), place)

        result = []
        for entry in chart:
            p, (r, deg) = entry
            planetary_position = PlanetaryPosition(
                planet=p,
                rasi=r,
                degree=deg
            )
            result.append(planetary_position)
        return result
