#!/usr/bin/env python3
"""Verify computed displays stay visual-only and backend-calculated."""

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


def verify_html_contract() -> None:
    html = read_text(ROOT / "output" / "STHE" / "problem_data.html")
    template = read_text(ROOT / "templates" / "problem_data.html")

    require(
        'data-display-key="LMTD"' in html,
        "LMTD computed display must render with data-display-key.",
    )
    require(
        'data-key="LMTD"' not in html,
        "LMTD computed display must not render with data-key.",
    )
    require(
        'input[data-display-key][data-computed-display="true"]' in template,
        "Problem Data JS must update computed displays by data-display-key.",
    )
    require(
        "delete data[input.dataset.displayKey]" in template,
        "Problem Data JS must remove computed display keys from saved problem data.",
    )


def verify_backend_contract() -> None:
    sys.path.insert(0, str(ROOT))
    from project_store import load_default_design
    from solver_api import build_calculated_inputs_response

    params = dict(load_default_design("STHE")["Equipment1"]["Model_Parameters"])
    result = build_calculated_inputs_response("STHE", params)
    calculated = result.get("parameters", {})

    require("Tco" in calculated, "Calculated inputs response must include Tco.")
    require("LMTD" in calculated, "Calculated inputs response must include LMTD.")
    require(isinstance(calculated["LMTD"], float), "LMTD must be a JSON-safe float.")
    json.dumps(result)


def main() -> int:
    try:
        verify_html_contract()
        verify_backend_contract()
    except AssertionError as exc:
        print(f"FAIL: {exc}")
        return 1

    print("OK: computed displays are visual-only and backend-calculated.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
