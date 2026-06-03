import json
import sys
from pathlib import Path

import pandas as pd

BASE_DIR = Path(__file__).resolve().parents[1]
sys.path.append(str(BASE_DIR))

from pipeline.calculation import (
    calculate_remote_sensing_indices,
    summarize_calculated_indices,
)


BASE_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = BASE_DIR / "field_data"

INPUT_FILE = DATA_DIR / "mirpur_unified_environmental_data_clean.csv"
OUTPUT_FILE = DATA_DIR / "mirpur_calculated_environmental_indices.csv"
SUMMARY_JSON = DATA_DIR / "mirpur_calculation_summary.json"
SUMMARY_MD = DATA_DIR / "mirpur_calculation_summary.md"


def write_markdown_summary(summary: dict) -> None:
    lines = [
        "# Mirpur Calculation Summary",
        "",
        "Generated from `data/mirpur_unified_environmental_data_clean.csv`.",
        "",
        "## Output",
        "",
        "- `data/mirpur_calculated_environmental_indices.csv`",
        "- `data/mirpur_calculation_summary.json`",
        "",
        "## Calculated Columns",
        "",
        "- `Red`: estimated red-band reflectance from surface type and weather context.",
        "- `NIR`: estimated near-infrared reflectance from surface type and weather context.",
        "- `NDVI`: `(NIR - Red) / (NIR + Red)`.",
        "- `Calculated_NDVI`: verification copy recalculated from `NIR` and `Red`.",
        "- `LST_C`: estimated land surface temperature in Celsius.",
        "- `Temperature`: alias of `LST_C` for the existing pipeline, plotting, and ML modules.",
        "",
        "These are calculation-stage estimates from ground/weather data. Replace `Red`, `NIR`, and `LST_C` with true satellite-derived values when Landsat/Sentinel bands are available.",
        "",
        "## Dataset Summary",
        "",
        f"- Rows: `{summary['rows']}`",
        f"- Average LST: `{summary['avg_lst_c']}` C",
        f"- Average NDVI: `{summary['avg_ndvi']}`",
        f"- NDVI range: `{summary['min_ndvi']}` to `{summary['max_ndvi']}`",
        "",
        "## Hotspot",
        "",
        f"- Location: `{summary['peak_hotspot']['name']}`",
        f"- LST: `{summary['peak_hotspot']['lst_c']}` C",
        f"- Coordinate: `{summary['peak_hotspot']['lat']}, {summary['peak_hotspot']['lng']}`",
        "",
        "## Coolspot",
        "",
        f"- Location: `{summary['peak_coolspot']['name']}`",
        f"- LST: `{summary['peak_coolspot']['lst_c']}` C",
        f"- Coordinate: `{summary['peak_coolspot']['lat']}, {summary['peak_coolspot']['lng']}`",
        "",
    ]
    SUMMARY_MD.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    df = pd.read_csv(INPUT_FILE)
    calculated = calculate_remote_sensing_indices(df)

    calculated.to_csv(OUTPUT_FILE, index=False)

    summary = summarize_calculated_indices(calculated)
    SUMMARY_JSON.write_text(json.dumps(summary, indent=2), encoding="utf-8")
    write_markdown_summary(summary)

    print(f"Wrote {OUTPUT_FILE} ({len(calculated)} rows)")
    print(f"Wrote {SUMMARY_JSON}")
    print(f"Wrote {SUMMARY_MD}")


if __name__ == "__main__":
    main()
