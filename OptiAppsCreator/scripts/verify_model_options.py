#!/usr/bin/env python3
"""Verify YAML-driven Model Options pages for every implemented model."""

from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(f"FAIL: {message}")


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def main() -> None:
    for model in ("STHE", "GPHE"):
        with (ROOT / model / f"{model}_ui.yaml").open(encoding="utf-8") as handle:
            config = yaml.safe_load(handle)
        problem_sections = config["pages"]["problem_data"]["sections"]
        option_sections = config["pages"]["model_options"]["sections"]
        require("other_options" not in problem_sections and "economic" not in problem_sections, f"{model} must move parameter blocks out of Problem Data.")
        require("other_options" in option_sections and "economic" in option_sections, f"{model} Model Options must contain moved parameter blocks.")

        thermal = option_sections.get("thermal_model", {})
        require(thermal.get("default") == "LMTD", f"{model} must default to the LMTD model.")
        thermal_options = {item["value"]: item for item in thermal.get("options", [])}
        require("LMTD" in thermal_options, f"{model} must expose LMTD Model.")
        require(thermal_options.get("Distributed", {}).get("disabled") is True, f"{model} Distributed Model must remain disabled.")

        generated_problem = read_text(ROOT / "output" / model / "problem_data.html")
        generated_options = read_text(ROOT / "output" / model / "model_options.html")
        require('data-section-id="other_options"' not in generated_problem, f"{model} Problem Data must not render Other Options.")
        require('data-section-id="economic"' not in generated_problem, f"{model} Problem Data must not render Economic Parameters.")
        require('data-section-id="other_options"' in generated_options, f"{model} Model Options must render Other Options.")
        require('data-section-id="economic"' in generated_options, f"{model} Model Options must render Economic Parameters.")
        require('name="Thermal_Model" value="LMTD" checked' in generated_options, f"{model} generated page must select LMTD Model.")
        distributed_input = next((line for line in generated_options.splitlines() if 'name="Thermal_Model" value="Distributed"' in line), "")
        require('disabled aria-disabled="true"' in distributed_input, f"{model} generated page must disable Distributed Model.")
        require('data-key="Thermal_Model"' not in generated_options, f"{model} thermal UI choice must not enter solver parameters.")
        require("window.collectProblemData = collectProblemData" in generated_options, f"{model} moved fields must synchronize before navigation.")

    sthe_options = read_text(ROOT / "output" / "STHE" / "model_options.html")
    require('data-section-id="bell_params"' in sthe_options, "STHE Bell Method Parameters must move with Shell Method.")
    require('data-visible-key="Shell_Method" data-visible-equals="Bell"' in sthe_options, "STHE Bell parameters must retain conditional visibility.")

    template = read_text(ROOT / "templates" / "model_options.html")
    require("collectProblemData" in template and "problemStorageKey()" in template, "Model Options must share persisted model parameters.")
    require("Thermal_Model" not in template, "Thermal model must remain YAML-driven.")

    print("OK: YAML-driven Model Options pages move parameter blocks and expose LMTD safely.")


if __name__ == "__main__":
    main()
