import json
import tempfile
import unittest
from pathlib import Path

from calendar_cli.cli import main


class CalendarCliTests(unittest.TestCase):
    def test_generates_date_path_and_overwrites_existing_file(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            output_dir = Path(temporary_directory) / "api"
            output_file = output_dir / "v1" / "2026" / "03" / "04.json"
            output_file.parent.mkdir(parents=True)
            output_file.write_text("stale content", encoding="utf-8")

            result = main(
                [
                    "--date",
                    "2026-03-04",
                    "--city",
                    "Pune",
                    "--latitude",
                    "18.5204",
                    "--longitude",
                    "73.8567",
                    "--output-dir",
                    str(output_dir),
                ]
            )

            self.assertEqual(result, 0)
            self.assertEqual(
                json.loads(output_file.read_text(encoding="utf-8")),
                {
                    "date": "2026-03-04",
                    "city": "Pune",
                    "latitude": 18.5204,
                    "longitude": 73.8567,
                    "data": {},
                },
            )
