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
    from standard_values import flatten_standard_values, grouped_standard_options

    common_units = load_common_units(ROOT)
    unit_options = build_unit_options(common_units)
    require(unit_options["kg/s"] == ["kg/s", "kg/h", "lb/h"], "Mass flow unit options must be available.")

    sthe_model_info = load_model_def("STHE")["Model_Info"]
    gphe_model_info = load_model_def("GPHE")["Model_Info"]
    sthe_units = sthe_model_info["Base_Units"]
    sthe_standard_values = sthe_model_info["Standard_Variables_Values"]
    gphe_units = gphe_model_info["Base_Units"]
    require(sthe_units["Model_Parameters"]["mh"] == "kg/s", "STHE mh base unit must be kg/s.")
    require(sthe_units["Discrete_Variables"]["Ds"] == "m", "STHE Ds base unit must be m.")
    require(gphe_units["Model_Parameters"]["bp"] == "m", "GPHE bp base unit must be m.")
    require("TEMA" in grouped_standard_options(sthe_standard_values["Ds"]), "STHE Ds standards must include TEMA.")
    require(0.2032 in flatten_standard_values(sthe_standard_values["Ds"]), "Grouped STHE Ds values must flatten for validation.")
    require(grouped_standard_options(sthe_standard_values["dte"]) is None, "STHE dte must remain a flat standard list.")
    require("temperatures" in sthe_model_info.get("Input_Unit_Groups", {}), "STHE input unit groups must be defined in Model_Def.")
    require("plate_dimensions" in gphe_model_info.get("Input_Unit_Groups", {}), "GPHE input unit groups must be defined in Model_Def.")


def verify_generated_html() -> None:
    sthe_problem = read_text(ROOT / "output" / "STHE" / "problem_data.html")
    sthe_geometric = read_text(ROOT / "output" / "STHE" / "geometric_options.html")
    sthe_results = read_text(ROOT / "output" / "STHE" / "results.html")
    sthe_units = read_text(ROOT / "output" / "STHE" / "units.html")
    sthe_result_units = read_text(ROOT / "output" / "STHE" / "result_units.html")
    sthe_yaml = read_text(ROOT / "STHE" / "STHE_ui.yaml")
    gphe_yaml = read_text(ROOT / "GPHE" / "GPHE_ui.yaml")

    require('data-key="mh"' in sthe_problem and 'data-base-unit="kg/s"' in sthe_problem, "STHE mh input must expose base unit metadata.")
    require('data-unit-label-for="mh"' in sthe_problem, "STHE mh label must expose dynamic unit metadata.")
    require('data-unit-label-for="Thi"' in sthe_problem, "STHE Thi label must expose dynamic unit metadata.")
    require('data-unit-for=' not in sthe_problem, "Problem Data must not render inline unit selectors.")
    require('data-unit-for=' not in sthe_geometric, "Geometric Options must not render inline unit selectors.")
    require('data-key="ktube"' in sthe_geometric and 'data-base-unit="W/m/K"' in sthe_geometric, "STHE ktube must expose base unit metadata.")
    require('data-unit-label-for="thk"' in sthe_geometric, "STHE thk label must expose dynamic unit metadata.")
    navigation = (ROOT / "templates" / "model_navigation.html").read_text(encoding="utf-8")
    require('Units <i class="fas fa-caret-down' in navigation, "Navbar must expose the Units menu.")
    require('id="units-menu"' in navigation, "Navbar must use the consolidated Units dropdown.")
    require('>Input</button>' in navigation and 'openUnitsConfiguration()' in navigation, "Units menu must expose Input configuration.")
    require('>Output</button>' in navigation and 'openResultsUnitsConfiguration()' in navigation, "Units menu must expose Output configuration.")
    require('units.html' in sthe_problem and 'result_units.html' in sthe_problem, "Generated navbar must retain both unit configuration routes.")
    require('Units Configuration' in sthe_units, "STHE units.html must be generated.")
    require('Results Units Configuration' in sthe_result_units, "STHE result_units.html must be generated.")
    require('data-unit-group-id="temperatures"' in sthe_units, "STHE units.html must allow selecting the temperatures group display unit.")
    require('data-unit-group-id="flow_rates"' in sthe_units, "STHE units.html must allow selecting the flow rates group display unit.")
    require('data-unit-group-id="diameters"' in sthe_units, "STHE units.html must allow selecting the diameters group display unit.")
    require('data-unit-group-id="tube_length"' in sthe_units, "STHE units.html must allow selecting tube length display unit separately.")
    require('data-unit-config-key="Thi"' not in sthe_units, "Grouped STHE temperatures must not be duplicated as individual unit rows.")
    require('data-unit-config-key="Ds"' not in sthe_units, "Grouped STHE diameters must not be duplicated as individual unit rows.")
    require('data-unit-config-key="plbmax2"' in sthe_units, "Ungrouped STHE length parameters must remain individually configurable.")
    require('Model Options' in sthe_units, "Moved parameter units must identify Model Options as their source page.")
    require("input_unit_groups" not in sthe_yaml, "STHE input unit groups must not be defined in YAML.")
    require("input_unit_groups" not in gphe_yaml, "GPHE input unit groups must not be defined in YAML.")
    require('data-var="Ds" data-base-unit="m"' in sthe_geometric, "STHE Ds checkbox grid must expose base unit metadata.")
    require('data-option-label-for="Ds"' in sthe_geometric, "STHE Ds checkbox options must expose convertible display labels.")
    require('data-unit-label-for="Ds"' in sthe_geometric, "STHE Ds checkbox title must expose dynamic unit metadata.")
    require('data-standard-for="Ds"' in sthe_geometric, "STHE Ds checkbox grid must expose a standard selector.")
    require('data-standard="TEMA"' in sthe_geometric, "STHE grouped geometric options must identify TEMA values.")
    require('data-unit-label-for="dte"' in sthe_geometric, "STHE dte checkbox title must expose dynamic unit metadata.")
    require('data-unit-label-for="L"' in sthe_geometric, "STHE L checkbox title must expose dynamic unit metadata.")
    require("parameter_units" in sthe_problem, "Problem Data must include parameter_units persistence hooks.")
    require("parameter_units" in sthe_results, "Results must preserve parameter_units when saving designs.")
    require("result_units" in sthe_results, "Results must preserve result_units when saving designs.")
    require('data-result-unit-config-key="Q"' in sthe_result_units, "STHE result_units.html must allow selecting Q display unit.")
    require('data-result-unit-config-key="DPt"' in sthe_result_units, "STHE result_units.html must allow selecting pressure drop display unit.")
    require('STORAGE_KEY_RESULT_UNITS' in sthe_results, "Results page must read stored result unit preferences.")
    require('RESULT_BASE_UNITS' in sthe_results, "Results page must include result base unit metadata.")
    require("geometric_standards" in sthe_results, "Results must preserve geometric_standards when saving designs.")


def verify_persistence() -> None:
    sys.path.insert(0, str(ROOT))
    from project_store import _design_payload_to_json

    payload = {"parameters": {"mh": 20}, "parameter_units": {"mh": "kg/h"}, "result_units": {"Q": "MW"}, "geometric_standards": {"Ds": "TEMA"}}
    data = json.loads(_design_payload_to_json("STHE", "UnitTest", payload))
    require(data["parameters"] == {"mh": 20}, "Parameters must be persisted in base units.")
    require(data["parameter_units"] == {"mh": "kg/h"}, "parameter_units must be persisted as visual metadata.")
    require(data["result_units"] == {"Q": "MW"}, "result_units must be persisted as visual metadata.")
    require(data["geometric_standards"] == {"Ds": "TEMA"}, "geometric_standards must be persisted as visual metadata.")


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
