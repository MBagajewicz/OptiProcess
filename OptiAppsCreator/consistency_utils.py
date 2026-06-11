#!/usr/bin/env python3
"""Shared helpers for configurable consistency checks in OptiAppsCreator."""

from __future__ import annotations

from typing import Callable, Any


MODES = {"deactive", "soft", "hard"}

CONSISTENCY_TESTS = {
    "STHE": [
        {"id": "positive_variables", "label": "Positive numeric variables"},
        {"id": "delta_t_min", "label": "Minimum temperature difference"},
        {"id": "heatload", "label": "Heat load balance"},
        {"id": "thi_tho", "label": "Hot stream cools down (Thi > Tho)"},
        {"id": "tco_tci", "label": "Cold stream heats up (Tco > Tci)"},
        {"id": "tco_thi_sthe", "label": "STHE cold outlet vs hot inlet approach"},
        {"id": "tci_tho", "label": "Cold inlet vs hot outlet approach"},
        {"id": "variables_bounds", "label": "Discrete variables inside standard bounds"},
        {"id": "variables_standard_values", "label": "Discrete variables match standard values"},
    ],
    "GPHE": [
        {"id": "positive_variables", "label": "Positive numeric variables"},
        {"id": "delta_t_min", "label": "Minimum temperature difference"},
        {"id": "heatload", "label": "Heat load balance"},
        {"id": "thi_tho", "label": "Hot stream cools down (Thi > Tho)"},
        {"id": "tco_tci", "label": "Cold stream heats up (Tco > Tci)"},
        {"id": "tci_tho", "label": "Cold inlet vs hot outlet approach"},
        {"id": "variables_bounds", "label": "Discrete variables inside standard bounds"},
        {"id": "variables_standard_values", "label": "Discrete variables match standard values"},
    ],
}


class ConsistencyHardError(RuntimeError):
    """Raised by the web/API flow when a hard consistency test fails."""


def get_tests(model: str) -> list[dict[str, str]]:
    return CONSISTENCY_TESTS.get(model, [])


def default_config(model: str) -> dict[str, str]:
    return {test["id"]: "hard" for test in get_tests(model)}


def normalize_config(model: str, config: dict[str, str] | None) -> dict[str, str]:
    normalized = default_config(model)
    for test_id, mode in (config or {}).items():
        mode_value = str(mode).strip().lower()
        if mode_value in MODES and test_id in normalized:
            normalized[test_id] = mode_value
    return normalized


def new_report() -> dict[str, list[dict[str, str]]]:
    return {"warnings": [], "errors": [], "applied": []}


def _format_messages(messages: list[str]) -> str:
    return "".join(messages).strip()


def _message_is_failure(messages: list[str]) -> bool:
    text = _format_messages(messages).lower()
    return "warning" in text or "error data consistency" in text or "error" in text


def run_test(
    *,
    model: str,
    test_id: str,
    label: str,
    config: dict[str, str],
    report: dict[str, list[dict[str, str]]] | None,
    save_result: Callable[..., Any],
    call: Callable[[Callable[..., Any]], Any],
) -> Any:
    """Run one consistency test under deactive/soft/hard policy.

    The `call` callback receives the save function to use for that test. This lets
    each model keep its tests inside `consistency()` while the wrapper captures
    messages and SystemExit failures for the web flow.
    """
    mode = config.get(test_id, "hard")
    if mode == "deactive":
        if report is not None:
            report["applied"].append({"id": test_id, "label": label, "mode": mode, "status": "skipped"})
        return None

    messages: list[str] = []

    def capture_save_result(*texts: Any) -> None:
        text = "".join(str(t) for t in texts)
        messages.append(text)
        save_result(*texts)

    failed = False
    result = None
    try:
        result = call(capture_save_result)
    except SystemExit as exc:
        failed = True
        if not messages:
            messages.append(str(exc) or f"{label} failed.")

    if _message_is_failure(messages):
        failed = True

    message = _format_messages(messages) or f"{label} failed."
    status = "failed" if failed else "passed"
    if report is not None:
        report["applied"].append({"id": test_id, "label": label, "mode": mode, "status": status})

    if failed:
        item = {"id": test_id, "label": label, "mode": mode, "message": message}
        if mode == "soft":
            if report is not None:
                report["warnings"].append(item)
            else:
                save_result(f"WARNING: {label}: {message}\n")
        else:
            if report is not None:
                report["errors"].append(item)
                raise ConsistencyHardError(f"{label}: {message}")
            raise SystemExit(message)

    return result
