#!/usr/bin/env python3
"""Verify generated model configuration summaries and their metadata."""

from __future__ import annotations

import sys
from copy import deepcopy
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
    require('id="model-context-panel"' in context_template, "Project and configuration details must share one panel.")
    require('id="model-configuration-summary-content"' in context_template, "Context panel must include the configured summary.")
    require("<details" not in context_template, "Configured summary must remain visible without an inner dropdown.")
    require('text-[8px]' in context_template and 'text-[10px]' in context_template, "Context panel must use compact readable typography.")
    require('leading-[1.1]' in context_template, "Context panel must use compact readable line spacing.")
    require("model-context-drag-handle" not in context_template, "Fixed context panel must not expose a drag handle.")
    require("model-context-reset-position" not in context_template, "Fixed context panel must not expose position controls.")
    require("function renderModelConfigurationSummary" in context_script, "Context script must render the configured summary.")
    require("MODEL_CONFIGURATION.configuration_summary" in context_script, "Context script must use only YAML-configured fields.")
    require("item.kind === 'selection_count'" in context_script, "Geometric selections must be summarized by count.")
    require("function toggleModelSidebar" in context_script, "Context script must control the mobile sidebar.")
    for drag_marker in ("initializeModelContextDrag", "context_panel_position", "setPointerCapture", "setModelContextPosition", "resetModelContextPosition"):
        require(drag_marker not in context_script, f"Fixed context panel must not include {drag_marker}.")
    for legacy_branch in ("Model Setup", "Construction Standards", "Geometric Parameters", "Input display units"):
        require(legacy_branch not in context_script, f"Compact summary must not render legacy branch {legacy_branch}.")

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
    require([item["key"] for item in sthe["configuration_summary"]] == ["Selected_OF", "yfluid", "Shell_Method", "Npt", "lay", "Ds"], "STHE summary must follow its YAML configuration.")
    require([item["key"] for item in gphe["configuration_summary"]] == ["Selected_OF", "Ntp", "Pl", "Sa", "Nph", "Npc"], "GPHE summary must follow its YAML configuration.")

    invalid_yaml = deepcopy(sthe_yaml)
    invalid_yaml["model"]["configuration_summary"].append({"key": "unknown_key"})
    try:
        build_model_configuration_context(invalid_yaml, load_model_def("STHE"), common_units)
    except ValueError as exc:
        require("unknown_key" in str(exc), "Unknown summary key error must identify the invalid key.")
    else:
        require(False, "Unknown configuration_summary keys must be rejected.")

    sidebar = read_text(ROOT / "templates" / "model_sidebar.html")
    require("lg:sticky" in sidebar and "lg:overflow-y-auto" in sidebar, "Sidebar must remain visible with its own desktop scroll.")
    require("lg:absolute" not in sidebar, "Sidebar must not use movable absolute positioning.")
    require('id="model-sidebar-toggle"' in sidebar and 'aria-expanded="false"' in sidebar, "Sidebar must provide a collapsed mobile toggle.")
    for shell_template in ("base.html", "results.html"):
        shell = read_text(ROOT / "templates" / shell_template)
        require("lg:grid-cols-[220px_minmax(0,1fr)]" in shell, f"{shell_template} must use a fixed 220px sidebar column.")
        require("lg:pl-[228px]" not in shell, f"{shell_template} must not reserve empty space with padding.")
        require('{% include "model_sidebar.html" %}' in shell, f"{shell_template} must use the shared sidebar.")
        require('{% include "model_navigation.html" %}' in shell, f"{shell_template} must use shared model navigation.")
        require(shell.index('{% include "model_navigation.html" %}') < shell.index('id="model-workspace"'), f"{shell_template} navigation must span the page above the workspace.")

    for model in ("STHE", "GPHE"):
        for page in ("model_options.html", "problem_data.html", "geometric_options.html", "units.html", "result_units.html", "results.html", "projects.html"):
            generated = read_text(ROOT / "output" / model / page)
            require('id="model-context-panel"' in generated, f"{model}/{page} must render the unified context panel.")
            require('id="model-configuration-summary-content"' in generated, f"{model}/{page} must render the configured summary.")
            require("const MODEL_CONFIGURATION =" in generated, f"{model}/{page} must receive model metadata.")
            require('id="model-workspace"' in generated, f"{model}/{page} must render the shared workspace.")
            require(generated.index('aria-label="Model pages"') < generated.index('aria-label="Current model context"'), f"{model}/{page} navigation must precede the sidebar.")

    print("OK: compact YAML-configured context panels are generated for STHE and GPHE.")


if __name__ == "__main__":
    main()
