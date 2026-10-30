import argparse
import json
import math
from datetime import date, datetime, time
from pathlib import Path
from typing import Sequence
from astrology.application.use_cases.get_panchanga_for_date import GetPanchangaForDate
from astrology.domain.models.panchanga import CustomEncoder
from astrology.domain.models.transform import Transformer
from astrology.domain.services.astrology_engine import AstrologyEngine


def _coordinate(value: str, name: str, minimum: float, maximum: float) -> float:
    try:
        coordinate = float(value)
    except ValueError as error:
        raise argparse.ArgumentTypeError(f"{name} must be a number") from error

    if not math.isfinite(coordinate) or not minimum <= coordinate <= maximum:
        raise argparse.ArgumentTypeError(
            f"{name} must be between {minimum} and {maximum}"
        )
    return coordinate


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Generate a date-indexed calendar JSON file."
    )
    parser.add_argument("--date", required=True, help="Date in YYYY-MM-DD format")
    parser.add_argument("--city", required=True, help="City name")
    parser.add_argument(
        "--latitude",
        required=True,
        type=lambda value: _coordinate(value, "Latitude", -90, 90),
    )
    parser.add_argument(
        "--longitude",
        required=True,
        type=lambda value: _coordinate(value, "Longitude", -180, 180),
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("api"),
        help="Root output directory (default: api)",
    )
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    astrology_engine = AstrologyEngine()
    get_panchanga_use_case = GetPanchangaForDate(astrology_engine=astrology_engine)
    try:
        calendar_date = date.fromisoformat(args.date)
    except ValueError:
        parser.error("--date must be a valid date in YYYY-MM-DD format")
    if calendar_date.isoformat() != args.date:
        parser.error("--date must be in YYYY-MM-DD format")
    
    city = args.city.strip()
    if not city:
        parser.error("--city must not be empty")

    output_path = (
        args.output_dir
        / "v1"
        / f"{calendar_date.year:04d}"
        / f"{calendar_date.month:02d}"
        / f"{calendar_date.day:02d}.json"
    )
    output_path.parent.mkdir(parents=True, exist_ok=True)
    result = get_panchanga_use_case.execute(
        datetime.combine(calendar_date, time.min),
        args.latitude,
        args.longitude,
    )
    transformed_result = Transformer.transform(result, args.latitude, args.longitude)
    output_path.write_text(
        json.dumps(
            transformed_result,indent=4, cls=CustomEncoder
        )
        + "\n",
        encoding="utf-8",
    )
    print(output_path)
    return 0
