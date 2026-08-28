#!/usr/bin/env python3
"""Verify generated model configuration trees and their metadata."""

from __future__ import annotations

import sys
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(f"FAIL: {message}")


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def main() -> None:
    sys.path.insert(0, str(ROOT))
    from generate_ui import build_model_configuration_context, load_common_units, load_model_def

    context_template = read_text(ROOT / "templates" / "model_context.html")
    context_script = read_text(ROOT / "templates" / "model_context_script.html")
    require("lg:grid-cols-[minmax(220px,1fr)_3fr]" in context_template, "Context must use an approximate 1/4 and 3/4 desktop layout.")
    require("grid-cols-2" not in context_template and "md:grid-cols-4" not in context_template, "Context summary fields must be stacked vertically.")
    require('id="model-configuration-tree"' in context_template, "Context must include the configuration tree.")
    require('<details id="model-configuration-tree"' in context_template, "Configuration tree must be closed by default.")
    require('<details id="model-configuration-tree" class=' in context_template, "Configuration tree must not declare the open attribute.")
    for branch in ("Model Setup", "Current Design", "Geometric Options", "Construction Standards", "Geometric Parameters", "Units"):
        require(branch in context_script, f"Configuration tree must render {branch}.")
    require("max-h-32 overflow-y-auto" in context_script, "Long geometric selections must use a bounded scroll area.")

    common_units = load_common_units(str(ROOT))
    with (ROOT / "STHE" / "STHE_ui.yaml").open(encoding="utf-8") as handle:
        sthe_yaml = yaml.safe_load(handle)
    with (ROOT / "GPHE" / "GPHE_ui.yaml").open(encoding="utf-8") as handle:
        gphe_yaml = yaml.safe_load(handle)
    sthe = build_model_configuration_context(sthe_yaml, load_model_def("STHE"), common_units)
    gphe = build_model_configuration_context(gphe_yaml, load_model_def("GPHE"), common_units)
    require(sthe["display_name"] == "Shell & Tube", "STHE display metadata must be available.")
    require(gphe["display_name"] == "Plate Exchanger", "GPHE display metadata must be available.")
    require(any(item["key"] == "Shell_Method" for item in sthe["selections"]), "STHE select settings must be included.")
    require(any(item["key"] == "Ds" for item in sthe["geometric_options"]), "STHE geometry metadata must include Ds.")
    require(any(item["key"] == "Ntp" for item in gphe["geometric_options"]), "GPHE geometry metadata must include Ntp.")

    for model in ("STHE", "GPHE"):
        for page in ("problem_data.html", "results.html"):
            generated = read_text(ROOT / "output" / model / page)
            require('id="model-configuration-tree"' in generated, f"{model}/{page} must render the tree.")
            require("const MODEL_CONFIGURATION =" in generated, f"{model}/{page} must receive model metadata.")

    print("OK: expandable model configuration trees are generated for STHE and GPHE.")


if __name__ == "__main__":
    main()
