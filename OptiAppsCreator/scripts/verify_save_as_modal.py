#!/usr/bin/env python3
"""Verify Save Design As modal safeguards in generated templates."""

from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(f"FAIL: {message}")


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def verify_template(path: Path) -> None:
    text = read_text(path)
    require("function escapeAttr(value)" in text, f"{path.name} must escape option attributes.")
    require("function escapeText(value)" in text, f"{path.name} must escape option labels.")
    require("save-as-modal-error" in text, f"{path.name} must show modal-local Save As errors.")
    require("Could not load designs for this project" in text, f"{path.name} must report design-list loading errors.")
    require("designSelect.value !== '__new__'" in text, f"{path.name} must detect existing design selections.")
    require("This will overwrite the existing design" in text, f"{path.name} must confirm overwrites.")
    require("document.getElementById('save-as-design-input').value = '';" in text, f"{path.name} must clear the name when New Design is selected.")
    require("confirmButton.textContent = 'Saving...'" in text, f"{path.name} must show save progress.")
    require("overlay.remove();\n                    setCurrentProject" in text or "overlay.remove();\n                setCurrentProject" in text, f"{path.name} must close the modal after a successful save.")


def main() -> None:
    verify_template(ROOT / "templates" / "base.html")
    verify_template(ROOT / "templates" / "results.html")
    print("OK: Save Design As modal safeguards are present.")


if __name__ == "__main__":
    main()
