#!/usr/bin/env python3
"""Verify the compact shared OptiHexx logo used on the Main Menu."""

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(f"FAIL: {message}")


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def main() -> None:
    template = read_text(ROOT / "templates" / "main_menu.html")
    styles = read_text(ROOT / "templates" / "optihexx_logo_styles.html")
    generated = read_text(ROOT / "output" / "main_menu.html")

    require('include "optihexx_logo.html"' in template, "Main Menu must use the shared logo component.")
    require('include "optihexx_logo_styles.html"' in template, "Main Menu must use the shared logo styles.")
    require("logo_compact = true" in template, "Main Menu must select the compact logo variant.")
    require("width: min(600px, calc(100vw - 32px))" in styles, "Compact logo must align with the menu width.")
    require('aria-label="OptiHexx"' in generated, "Generated Main Menu logo must say only OptiHexx.")
    require("optihexx-logo-frame--compact" in generated, "Generated Main Menu must contain the compact logo.")
    for removed_text in ("Heat Exchanger Optimal Design Suite", "Prototype P07", "MAIN MENU"):
        require(removed_text not in generated, f"Main Menu must not show {removed_text}.")
    require("header-box" not in template and "header-font" not in template, "Legacy Main Menu banner styles must be removed.")

    print("OK: Main Menu uses the compact OptiHexx-only shared logo.")


if __name__ == "__main__":
    main()
