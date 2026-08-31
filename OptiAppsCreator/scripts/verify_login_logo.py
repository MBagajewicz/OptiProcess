#!/usr/bin/env python3
"""Verify the responsive OptiHexx logo used on the Login page."""

from __future__ import annotations

from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(f"FAIL: {message}")


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def main() -> None:
    with (ROOT / "common_ui.yaml").open(encoding="utf-8") as handle:
        common_ui = yaml.safe_load(handle)
    logo = common_ui.get("login", {}).get("logo", {})
    production = common_ui.get("login", {}).get("production", {})
    require(logo.get("name") == "OptiHex", "Login logo name must be configured in common_ui.yaml.")
    require(logo.get("suffix") == "x", "Login logo suffix must be configured separately.")
    require(logo.get("subtitle") == "Heat Exchanger Suite", "Login logo subtitle must match the approved prototype.")
    require(logo.get("prototype") == "Prototype 0.1", "Login logo prototype label must match the approved prototype.")
    require(production.get("text") == "Web Production: OK-Solutions", "Login production text must be configured in common_ui.yaml.")

    template = read_text(ROOT / "templates" / "login.html")
    component = read_text(ROOT / "templates" / "optihexx_logo.html")
    styles = read_text(ROOT / "templates" / "optihexx_logo_styles.html")
    generated = read_text(ROOT / "output" / "login.html")
    require('include "optihexx_logo.html"' in template, "Login must use the shared logo component.")
    require('include "optihexx_logo_styles.html"' in template, "Login must use the shared logo styles.")
    for marker in ("optihexx-logo-frame", "optihexx-logo-panel", "optihexx-logo-name-suffix"):
        require(marker in component and marker in generated, f"Login logo must include {marker}.")
    require("width: min(760px, calc(100vw - 32px))" in styles, "Login logo must adapt to the viewport width.")
    require("clamp(" in styles, "Login logo typography and spacing must scale responsively.")
    require("Heat Exchanger Suite" in generated and "Prototype 0.1" in generated, "Generated Login must contain the approved logo text.")
    require("login-production-panel" in template and "login-production-panel" in generated, "Login must include the OK-Solutions production panel.")
    require("width: min(456px, calc(100vw - 32px))" in template, "Production panel must use 60% of the original maximum width.")
    require("white-space: nowrap" in template, "Production text must remain on one line.")
    require("linear-gradient(180deg, #d4f5e8 0%, #b8ede0 100%)" in template, "Production panel must use the approved mint gradient.")
    require("border: 3px solid #1a3a52" in template, "Production panel must use the approved navy border.")
    require("color: #e63946" in template, "Production text must use the approved red color.")
    require("Web Production: OK-Solutions" in generated, "Generated Login must show OK-Solutions production text.")
    for legacy_text in (
        "Guarantees global optimality",
        "Diego. G. Oliva",
        "Miguel. J. Bagajewicz",
        "Instituto de Desarrollo y Diseño",
        "Universidade Federal do Rio de Janeiro",
    ):
        require(legacy_text not in template and legacy_text not in generated, f"Legacy Login text must be removed: {legacy_text}")
    require('from-[#fff400] to-[#e8a689]' not in template, "Legacy Login banner must be removed.")
    require("support.js" not in template and "imagen.png" not in template, "Login logo must not depend on prototype runtime or raster assets.")

    print("OK: Login uses the responsive OptiHexx HTML/CSS logo.")


if __name__ == "__main__":
    main()
