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
    require('class="flex min-w-0 flex-col gap-2"' in context_template, "Sidebar context blocks must be stacked vertically.")
    require("lg:grid-cols-[minmax(220px,1fr)_3fr]" not in context_template, "Legacy horizontal context layout must be removed.")
    require('id="model-configuration-tree"' in context_template, "Context must include the configuration tree.")
    require('<details id="model-configuration-tree"' in context_template, "Configuration tree must be closed by default.")
    require('<details id="model-configuration-tree" class=' in context_template, "Configuration tree must not declare the open attribute.")
    for branch in ("Model Setup", "Current Design", "Geometric Options", "Construction Standards", "Geometric Parameters", "Units"):
        require(branch in context_script, f"Configuration tree must render {branch}.")
    require("selected.length + ' selected'" in context_script, "Geometric selections must be summarized by count.")
    require("function toggleModelSidebar" in context_script, "Context script must control the mobile sidebar.")
    require('root.innerHTML = \'<div class="flex flex-col gap-2">\'' in context_script, "Configuration branches must use a compact single-column layout.")

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

    for shell_template in ("base.html", "results.html"):
        shell = read_text(ROOT / "templates" / shell_template)
        require("lg:grid-cols-[300px_minmax(0,1fr)]" in shell, f"{shell_template} must use the shared desktop sidebar layout.")
        require("lg:sticky" in shell and "lg:overflow-y-auto" in shell, f"{shell_template} sidebar must remain visible with its own scroll.")
        require('id="model-sidebar-toggle"' in shell and 'aria-expanded="false"' in shell, f"{shell_template} must provide a collapsed mobile toggle.")
        require('{% include "model_navigation.html" %}' in shell, f"{shell_template} must use shared model navigation.")

    for model in ("STHE", "GPHE"):
        for page in ("problem_data.html", "geometric_options.html", "units.html", "result_units.html", "results.html", "projects.html"):
            generated = read_text(ROOT / "output" / model / page)
            require('id="model-configuration-tree"' in generated, f"{model}/{page} must render the tree.")
            require("const MODEL_CONFIGURATION =" in generated, f"{model}/{page} must receive model metadata.")
            require('id="model-workspace"' in generated, f"{model}/{page} must render the shared workspace.")
            require(generated.index('aria-label="Current model context"') < generated.index('aria-label="Model pages"'), f"{model}/{page} sidebar must precede navigation.")

    print("OK: compact model context sidebars are generated for STHE and GPHE.")


if __name__ == "__main__":
    main()
