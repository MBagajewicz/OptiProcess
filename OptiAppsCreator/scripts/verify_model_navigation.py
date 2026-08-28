#!/usr/bin/env python3
"""Verify model-page buttons, context details, and automatic Results execution."""

from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(f"FAIL: {message}")


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def verify_navigation(path: Path) -> None:
    text = read_text(path)
    require('<button type="button" onclick="navigateModelPage' in text, f"{path.name} must use model-page buttons.")
    require('aria-current="page"' in text, f"{path.name} must identify the active model-page button.")
    require('{% include "model_context.html" %}' in text, f"{path.name} must include the shared model context.")
    for removed_id in ("nav-back-btn", "nav-next-btn", "nav-run-btn", "project-indicator"):
        require(removed_id not in text, f"{path.name} must not include legacy {removed_id}.")
    require("function updateCalculationStatus" in text, f"{path.name} must update calculation status.")


def main() -> None:
    base = ROOT / "templates" / "base.html"
    results = ROOT / "templates" / "results.html"
    verify_navigation(base)
    verify_navigation(results)

    context_text = read_text(ROOT / "templates" / "model_context.html")
    for context_id in ("context-model", "context-project", "context-design", "context-calculation-status"):
        require(f'id="{context_id}"' in context_text, f"Shared model context must include {context_id}.")

    results_text = read_text(results)
    require("if (hasOptimizationChanges())" in results_text, "Results must optimize when inputs changed.")
    require("runOptimization().then" in results_text, "Results must start optimization automatically.")
    require("STORAGE_KEY_LAST_OPT_RESULT" in results_text, "Results must retain cached optimization results.")
    require("Press RUN" not in results_text, "Results must not instruct users to press RUN.")
    require("shouldRun" not in results_text and "?run=1" not in results_text, "Results must not depend on the legacy run query parameter.")

    print("OK: model navigation uses buttons and Results optimizes automatically when needed.")


if __name__ == "__main__":
    main()
