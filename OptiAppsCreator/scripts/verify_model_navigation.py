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
    require('{% include "model_navigation.html" %}' in text, f"{path.name} must use shared model navigation.")
    require('{% include "model_sidebar.html" %}' in text, f"{path.name} must include the shared model sidebar.")
    for removed_id in ("nav-back-btn", "nav-next-btn", "nav-run-btn", "project-indicator"):
        require(removed_id not in text, f"{path.name} must not include legacy {removed_id}.")
    require("function updateCalculationStatus" in text, f"{path.name} must update calculation status.")


def main() -> None:
    base = ROOT / "templates" / "base.html"
    results = ROOT / "templates" / "results.html"
    verify_navigation(base)
    verify_navigation(results)

    navigation = read_text(ROOT / "templates" / "model_navigation.html")
    require('<button type="button" onclick="navigateModelPage' in navigation, "Shared navigation must use model-page buttons.")
    require('aria-current="page"' in navigation, "Shared navigation must identify the active model-page button.")
    require('id="file-menu"' in navigation and 'onclick="toggleFileMenu()"' in navigation, "Navigation must begin with the File dropdown.")
    require('id="units-menu"' in navigation and 'onclick="toggleUnitsMenu()"' in navigation, "Units must be the second navigation control.")
    for action in ("Open Tutorial Library", "Save Design", "Save Design As...", "Reset", "Project Management"):
        require(action in navigation, f"File menu must contain {action}.")
    require("Open User Projects" not in navigation, "File menu must not duplicate Project Management with Open User Projects.")

    generated_problem = read_text(ROOT / "output" / "STHE" / "problem_data.html")
    ordered_markers = [
        'onclick="toggleFileMenu()"',
        'onclick="toggleUnitsMenu()"',
        "navigateModelPage(event, 'model_options.html')",
        "navigateModelPage(event, 'problem_data.html')",
        "navigateModelPage(event, 'geometric_options.html')",
        "navigateModelPage(event, 'results.html')",
    ]
    positions = [generated_problem.index(marker) for marker in ordered_markers]
    require(positions == sorted(positions), "Navigation controls must follow File, Units, Model Options, Problem Data, Geometric Options, Results.")
    require("projects.html?scope=users" in generated_problem, "Project Management must open the existing Projects page.")
    require("navigateModelPage(event, 'projects.html')" not in generated_problem, "Projects must not remain a standalone page button.")
    require(generated_problem.index("navigateModelPage(event, 'results.html')") < generated_problem.index("/ui/main_menu.html") < generated_problem.index('onclick="logout()"'), "Main Menu and Logout must remain at the right end.")

    generated_projects = read_text(ROOT / "output" / "STHE" / "projects.html")
    require('onclick="toggleFileMenu()" aria-current="page"' in generated_projects, "File must be active on Project Management.")
    generated_units = read_text(ROOT / "output" / "STHE" / "units.html")
    require('onclick="toggleUnitsMenu()" aria-current="page"' in generated_units, "Units must be active on Input configuration.")
    generated_model_options = read_text(ROOT / "output" / "STHE" / "model_options.html")
    require("navigateModelPage(event, 'model_options.html')" in generated_model_options and 'aria-current="page"' in generated_model_options, "Model Options must be generated and active.")

    for template_path in (base, results, ROOT / "templates" / "model_navigation.html"):
        text = read_text(template_path)
        for legacy_marker in ("toggleSaveMenu", "toggleLoadMenu", "toggleConfigMenu", "load-menu", "save-menu", "config-menu", "loadUserProjects"):
            require(legacy_marker not in text, f"{template_path.name} must not retain legacy navigation marker {legacy_marker}.")

    context_text = read_text(ROOT / "templates" / "model_context.html")
    for context_id in ("context-model", "context-project", "context-design", "context-calculation-status"):
        require(f'id="{context_id}"' in context_text, f"Shared model context must include {context_id}.")

    results_text = read_text(results)
    require("if (hasOptimizationChanges())" in results_text, "Results must optimize when inputs changed.")
    require("runOptimization().then" in results_text, "Results must start optimization automatically.")
    require("STORAGE_KEY_LAST_OPT_RESULT" in results_text, "Results must retain cached optimization results.")
    require("Press RUN" not in results_text, "Results must not instruct users to press RUN.")
    require("shouldRun" not in results_text and "?run=1" not in results_text, "Results must not depend on the legacy run query parameter.")

    print("OK: model navigation uses File and Units menus in the approved order, and Results optimizes automatically.")


if __name__ == "__main__":
    main()
