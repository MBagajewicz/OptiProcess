#!/usr/bin/env python3
"""Verify model base units, UI unit metadata, and parameter_units persistence."""

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def read_text(path: Path) -> str:
    require(path.exists(), f"Missing file: {path.relative_to(ROOT)}")
    return path.read_text(encoding="utf-8")


def verify_model_definitions() -> None:
    sys.path.insert(0, str(ROOT))
    from generate_ui import build_unit_options, load_common_units, load_model_def

    common_units = load_common_units(ROOT)
    unit_options = build_unit_options(common_units)
    require(unit_options["kg/s"] == ["kg/s", "kg/h", "lb/h"], "Mass flow unit options must be available.")

    sthe_units = load_model_def("STHE")["Model_Info"]["Base_Units"]
    gphe_units = load_model_def("GPHE")["Model_Info"]["Base_Units"]
    require(sthe_units["Model_Parameters"]["mh"] == "kg/s", "STHE mh base unit must be kg/s.")
    require(sthe_units["Discrete_Variables"]["Ds"] == "m", "STHE Ds base unit must be m.")
    require(gphe_units["Model_Parameters"]["bp"] == "m", "GPHE bp base unit must be m.")


def verify_generated_html() -> None:
    sthe_problem = read_text(ROOT / "output" / "STHE" / "problem_data.html")
    sthe_geometric = read_text(ROOT / "output" / "STHE" / "geometric_options.html")
    sthe_results = read_text(ROOT / "output" / "STHE" / "results.html")
    sthe_units = read_text(ROOT / "output" / "STHE" / "units.html")

    require('data-key="mh"' in sthe_problem and 'data-base-unit="kg/s"' in sthe_problem, "STHE mh input must expose base unit metadata.")
    require('data-unit-label-for="mh"' in sthe_problem, "STHE mh label must expose dynamic unit metadata.")
    require('data-unit-label-for="Thi"' in sthe_problem, "STHE Thi label must expose dynamic unit metadata.")
    require('data-unit-for=' not in sthe_problem, "Problem Data must not render inline unit selectors.")
    require('data-unit-for=' not in sthe_geometric, "Geometric Options must not render inline unit selectors.")
    require('data-key="ktube"' in sthe_geometric and 'data-base-unit="W/m/K"' in sthe_geometric, "STHE ktube must expose base unit metadata.")
    require('data-unit-label-for="thk"' in sthe_geometric, "STHE thk label must expose dynamic unit metadata.")
    require('Configurations' in sthe_problem and 'units.html' in sthe_problem, "Navbar must expose Configurations -> Units Configuration.")
    require('Units Configuration' in sthe_units, "STHE units.html must be generated.")
    require('data-unit-config-key="mh"' in sthe_units, "STHE units.html must allow selecting mh display unit.")
    require('data-unit-config-key="Thi"' in sthe_units, "STHE units.html must allow selecting Thi display unit.")
    require('data-unit-config-key="thk"' in sthe_units, "STHE units.html must allow selecting thk display unit.")
    require('data-unit-config-key="Ds"' in sthe_units, "STHE units.html must allow selecting Ds display unit.")
    require('data-unit-config-key="dte"' in sthe_units, "STHE units.html must allow selecting dte display unit.")
    require('data-var="Ds" data-base-unit="m"' in sthe_geometric, "STHE Ds checkbox grid must expose base unit metadata.")
    require('data-option-label-for="Ds"' in sthe_geometric, "STHE Ds checkbox options must expose convertible display labels.")
    require('data-unit-label-for="Ds"' in sthe_geometric, "STHE Ds checkbox title must expose dynamic unit metadata.")
    require('data-unit-label-for="dte"' in sthe_geometric, "STHE dte checkbox title must expose dynamic unit metadata.")
    require('data-unit-label-for="L"' in sthe_geometric, "STHE L checkbox title must expose dynamic unit metadata.")
    require("parameter_units" in sthe_problem, "Problem Data must include parameter_units persistence hooks.")
    require("parameter_units" in sthe_results, "Results must preserve parameter_units when saving designs.")


def verify_persistence() -> None:
    sys.path.insert(0, str(ROOT))
    from project_store import _design_payload_to_json

    payload = {"parameters": {"mh": 20}, "parameter_units": {"mh": "kg/h"}}
    data = json.loads(_design_payload_to_json("STHE", "UnitTest", payload))
    require(data["parameters"] == {"mh": 20}, "Parameters must be persisted in base units.")
    require(data["parameter_units"] == {"mh": "kg/h"}, "parameter_units must be persisted as visual metadata.")


def main() -> int:
    try:
        verify_model_definitions()
        verify_generated_html()
        verify_persistence()
    except AssertionError as exc:
        print(f"FAIL: {exc}")
        return 1
    print("OK: unit metadata and parameter_units persistence are wired.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
