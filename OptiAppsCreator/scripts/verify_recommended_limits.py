#!/usr/bin/env python3
"""Verify optional recommended limit metadata is rendered only when defined."""

import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def read_text(path: Path) -> str:
    require(path.exists(), f"Missing file: {path.relative_to(ROOT)}")
    return path.read_text(encoding="utf-8")


def verify_generated_html() -> None:
    sthe_problem = read_text(ROOT / "output" / "STHE" / "problem_data.html")
    sthe_model_options = read_text(ROOT / "output" / "STHE" / "model_options.html")
    sthe_geometric = read_text(ROOT / "output" / "STHE" / "geometric_options.html")
    gphe_problem = read_text(ROOT / "output" / "GPHE" / "problem_data.html")
    gphe_model_options = read_text(ROOT / "output" / "GPHE" / "model_options.html")
    gphe_geometric = read_text(ROOT / "output" / "GPHE" / "geometric_options.html")

    require(
        'data-key="mh"' in sthe_problem and 'data-recommended-min="10"' in sthe_problem and 'data-recommended-max="150"' in sthe_problem,
        "STHE mh must render recommended limits from Model_Info.",
    )
    require(
        'data-key="int_rate"' in sthe_model_options and 'data-recommended-min="5.0"' in sthe_model_options and 'data-recommended-max="20.0"' in sthe_model_options,
        "STHE int_rate recommended limits must use displayed percentage scale.",
    )
    require(
        'data-key="ktube"' in sthe_geometric and 'data-recommended-min="15"' in sthe_geometric and 'data-recommended-max="60"' in sthe_geometric,
        "STHE geometric form_group fields must render recommended limits.",
    )
    require(
        'data-recommended-min=' not in gphe_problem,
        "GPHE Problem Data must not render recommended limits when Model_Info has no key.",
    )
    require(
        'data-recommended-min=' not in gphe_model_options,
        "GPHE Model Options must not render recommended limits when Model_Info has no key.",
    )
    require(
        'data-recommended-min=' not in gphe_geometric,
        "GPHE Geometric Options must not render recommended limits when Model_Info has no key.",
    )


def verify_generator_contract() -> None:
    sys.path.insert(0, str(ROOT))
    from generate_ui import get_recommended_limit_parameters, load_model_def

    sthe_limits = get_recommended_limit_parameters(load_model_def("STHE"))
    gphe_limits = get_recommended_limit_parameters(load_model_def("GPHE"))

    require(isinstance(sthe_limits, dict) and "mh" in sthe_limits, "STHE must expose recommended limits.")
    require(gphe_limits == {}, "Missing Recomended_Limit_Parameters must be treated as no recommended limits.")
    require(
        get_recommended_limit_parameters({"Model_Info": {"Recomended_Limit_Parameters": None}}) == {},
        "Invalid recommended limits metadata must fall back to no limits.",
    )


def main() -> int:
    try:
        verify_generated_html()
        verify_generator_contract()
    except AssertionError as exc:
        print(f"FAIL: {exc}")
        return 1

    print("OK: recommended limits are optional and rendered when defined.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
