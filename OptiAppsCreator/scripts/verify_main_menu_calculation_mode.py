#!/usr/bin/env python3
"""Verify the Calculation Mode selector on the Main Menu."""

from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]
EXPECTED_MODES = [
    ("optimal-design", "Optimal Design"),
    ("simulation", "Simulation"),
    ("rating", "Rating"),
    ("retrofit", "Retrofit"),
]


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(f"FAIL: {message}")


def main() -> None:
    with (ROOT / "common_ui.yaml").open(encoding="utf-8") as handle:
        common_ui = yaml.safe_load(handle)

    modes = common_ui.get("calculation_modes", [])
    configured_modes = [(mode.get("id"), mode.get("label")) for mode in modes]
    require(configured_modes == EXPECTED_MODES, "Calculation modes must be configured in the approved order.")
    require(sum(bool(mode.get("selected")) for mode in modes) == 1, "Exactly one calculation mode must be selected by default.")
    require(modes[0].get("selected") is True, "Optimal Design must be selected by default.")

    template = (ROOT / "templates" / "main_menu.html").read_text(encoding="utf-8")
    generated = (ROOT / "output" / "main_menu.html").read_text(encoding="utf-8")
    require('type="radio" name="calculation-mode"' in template, "Calculation Mode must allow only one selection.")
    require("optihexxCalculationMode" in template, "Calculation Mode selection must persist for the browser session.")
    require("Calculation Mode" in generated, "Generated Main Menu must contain the Calculation Mode block.")
    logo_markup = '<div class="optihexx-logo-frame optihexx-logo-frame--compact"'
    mode_markup = '<section class="calculation-mode-container"'
    menu_markup = '<div class="menu-box'
    require(generated.index(logo_markup) < generated.index(mode_markup) < generated.index(menu_markup), "Calculation Mode must appear between the logo and model selector.")
    for mode_id, label in EXPECTED_MODES:
        require(f'value="{mode_id}"' in generated and label in generated, f"Generated Main Menu must contain {label}.")
    require('value="optimal-design" checked' in generated, "Optimal Design must be checked in generated Main Menu.")

    print("OK: Main Menu includes the responsive Calculation Mode selector.")


if __name__ == "__main__":
    main()
