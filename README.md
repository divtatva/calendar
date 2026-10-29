# Divtatva Calendar CLI

Generate a date-indexed JSON file at `api/v1/<year>/<month>/<day>.json`. The
`data` object is an empty placeholder for the calendar content generator.

## Usage

Run from the repository root:

```sh
python -m calendar_cli \
  --date 2026-03-04 \
  --city Pune \
  --latitude 18.5204 \
  --longitude 73.8567
```

The command creates missing directories and replaces the file if it already
exists. Use `--output-dir` to choose another output root; it defaults to `api`.
After installing the project, the same command is available as `calendar-json`.

The GitHub Actions workflow generates Pune's JSON daily using the local Pune
date, and deploys the `api` directory to GitHub Pages. For a repository named
`calendar`, files are served at
`https://divtatva.github.io/calendar/api/v1/<year>/<month>/<day>.json`.
