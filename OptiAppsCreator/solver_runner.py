#!/usr/bin/env python3
"""solver_runner.py — Receives problem data as JSON, runs the OptiProcess solver, outputs results JSON.

Usage:
    python solver_runner.py --model STHE --input /tmp/input.json --output /tmp/output.json

Input JSON schema:
{
    "model": "STHE",
    "parameters": {                          // Model_Parameters dict
        "mh": 20, "roh": 750, "Cph": 2840, ...,
        "yfluid": "hot_stream",
        "Shell_Method": "Kern",
        "Tube_Method": "Dittus_Boelter",
        ...
    },
    "discrete_variables": {                  // Discrete_Values_of_Variables (by name)
        "Ds": [0.7874, 0.8382, ...],
        "dte": [0.01905, 0.02540, ...],
        ...
    },
    "selected_of": "TAC_OF",                // Selected objective function
    "number_of_equipment": 1
}

Output JSON:
{
    "status": "ok",
    "objective": {"name": "TAC", "value": 8247.52, "unit": "$/year"},
    "optimal_variables": {"Ds": 0.7874, "dte": 0.0254, ...},
    "number_of_solutions": 1,
    "equipment": "STHE",
    "elapsed_seconds": 0.01
}
"""

import os
import sys
import json
import time
import argparse
import importlib
import numpy as np

from project_store import load_project
from consistency_utils import ConsistencyHardError, new_report

# Ensure OptiAppsCreator is on sys.path for imports
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
if SCRIPT_DIR not in sys.path:
    sys.path.insert(0, SCRIPT_DIR)


def json_safe(obj):
    """Recursively convert numpy types to native Python for JSON serialization."""
    if isinstance(obj, (np.integer,)):
        return int(obj)
    if isinstance(obj, (np.floating,)):
        return float(obj)
    if isinstance(obj, np.ndarray):
        return obj.tolist()
    if isinstance(obj, dict):
        return {k: json_safe(v) for k, v in obj.items()}
    if isinstance(obj, (list, tuple)):
        return [json_safe(v) for v in obj]
    return obj


def load_model_def(model_name):
    """Import Model_Def_{Model} and return the Model_{Model} dict."""
    module_path = f"{model_name}.Model.Model_Def_{model_name}"
    module = importlib.import_module(module_path)
    var_name = f"Model_{model_name}"
    return getattr(module, var_name)


def load_project_defaults(model_name, project_name):
    """Load a project dict from {Model}/Projects/{Project}.py."""
    return load_project(model_name, project_name, scope="examples")


def compute_output_info(optimal_vars, params, model_name, objective=None):
    """Import and call model-specific Output_Info.build_output_info() if available."""
    try:
        module = importlib.import_module(f"{model_name}.Model.Output_Info")
        return module.build_output_info(optimal_vars, params, objective)
    except ModuleNotFoundError:
        return {"calculations": {}, "objective": objective or {}}
    except Exception:
        return {"calculations": {}, "objective": objective or {}}


def build_example_dict(input_data):
    """Convert user-submitted JSON into a project/example dict matching solver expectations."""
    params = input_data["parameters"]
    discrete = input_data["discrete_variables"]
    selected_of = input_data.get("selected_of", "TAC_OF")
    n_equip = input_data.get("number_of_equipment", 1)
    model_name = input_data.get("model", "STHE")

    # Read variable order from Model_Def_{Model}.py
    model_def = load_model_def(model_name)
    var_order = model_def["Model_Info"]["List_of_Variables"]

    discrete_values = []
    for v in var_order:
        vals = discrete.get(v, [])
        if not vals:
            raise ValueError(
                f"Discrete variable '{v}' is empty or missing. "
                f"Expected {len(var_order)} variables: {var_order}. "
                f"Received keys: {sorted(discrete.keys())}"
            )
        discrete_values.append(vals)

    # Merge user-submitted params with Example1 defaults (fills missing internal params)
    try:
        example_ref = load_project_defaults(model_name, "Example1")
        ref_params = dict(example_ref["Equipment1"]["Model_Parameters"])
        # Convert numpy arrays to lists for JSON compatibility, then merge
        for k in list(ref_params.keys()):
            if hasattr(ref_params[k], 'tolist'):
                ref_params[k] = ref_params[k].tolist()
        ref_params.update(params)
        params = ref_params
    except Exception:
        pass  # if no reference example, use params as-is

    # Convert list parameters to numpy arrays if the original model expects them
    array_params = ["ppLp", "ppLw", "ppDp"]
    for key in array_params:
        if key in params and isinstance(params[key], list):
            params[key] = np.array(params[key])

    example = {
        "Number_of_Equipment": n_equip,
        "Equipment1": {
            "Model_Declarations": {
                "Type_Equipment": model_name,
                "Discrete_Values_of_Variables": discrete_values,
                "Selected_OF": [selected_of],
            },
            "Model_Parameters": params,
        },
    }
    return example


def run_solver(model_name, example_name, example_dict, consistency_config=None, consistency_report=None):
    """Run the full OptiProcess pipeline for the given model and example. Returns (Sol_Dict, active_example, active_models)."""
    from OptiCode import (
        Calculations_Prep_Organizer,
        Calculations_Solver_Selection,
        Calculations_Consistency_Check,
        Import_Functions,
        Import_Models,
    )

    active_example = example_dict

    # Collect model list
    active_models_list = [model_name]
    for i in range(1, active_example.get("Number_of_Equipment", 1) + 1):
        eq = active_example.get(f"Equipment{i}", {})
        active_models_list.append(eq.get("Model_Declarations", {}).get("Type_Equipment", model_name))
    active_models_list = list(set(active_models_list))

    # Import model definitions, constraints, and parameter update functions
    active_models = {}
    active_models["Models_Def"] = Import_Models.Import_Models(active_models_list, "Model_Def_")
    active_models["Constraints_and_OF"] = Import_Functions.Import_Functions(active_models_list, "Constraints_and_OF_")
    active_models["Parameters_Update"] = Import_Functions.Import_Functions(active_models_list, "Parameters_Update_")

    # Dummy save_result to suppress console output
    def save_result(*texts):
        pass

    # Consistency check + initial set up
    Calculations_Consistency_Check.Consistency_Check(
        active_example, active_models, save_result, consistency_config, consistency_report
    )
    Calculations_Prep_Organizer.Prep_Organizer(active_example, active_models, model_name, example_name, save_result)

    # Run solver
    solution = Calculations_Solver_Selection.Solver_Selection(
        active_example, active_models, model_name, example_name, save_result
    )
    return solution, active_example, active_models


def extract_results(sol_dict, active_models, model_name):
    """Convert raw Sol_Dict into a clean JSON-serializable results dict."""
    model_def = active_models["Models_Def"][model_name]
    of_info = model_def["Model_Info"]["Objective_Function"]
    var_list = model_def["Model_Info"]["List_of_Variables"]

    # Extract Equipment1 solution
    eq_sol = sol_dict.get("Equipment1", {})
    total_of = sol_dict.get("total_solution", None)

    # Find which OF was used
    of_eq_name = None
    of_var = None
    of_unit = None
    for eq_name in of_info.get("Equation_Name", []):
        if eq_name in eq_sol:
            of_eq_name = eq_name
            of_data = eq_sol[eq_name]
            of_var = list(of_data.keys())[0] if of_data else None
            of_unit = of_info["Unit_OF"][of_info["Equation_Name"].index(eq_name)]
            break

    if of_eq_name is None and eq_sol:
        # Try to find any OF key
        for key in eq_sol:
            if "_OF" in key:
                of_eq_name = key
                break

    # Build optimal variables dict
    optimal_vars = {}
    for var in var_list:
        if var in eq_sol:
            optimal_vars[var] = eq_sol[var]

    # Include yfluid if present (recursive trimming)
    if "yfluid" in eq_sol:
        optimal_vars["yfluid"] = eq_sol["yfluid"]

    # Get OF value
    of_value = total_of
    if of_eq_name and of_eq_name in eq_sol:
        of_inner = eq_sol[of_eq_name]
        if isinstance(of_inner, dict) and of_var:
            of_value = of_inner.get(of_var, of_value)
    num_solutions = eq_sol.get(of_eq_name, {}).get("Number_of_solutions", 0) if of_eq_name else 0
    
    # For the case where OF is in the dict but not as a dedicated function key
    if isinstance(num_solutions, np.integer):
        num_solutions = int(num_solutions)
    if of_value is not None and isinstance(of_value, np.floating):
        of_value = float(of_value)

    return {
        "objective": {
            "function": of_eq_name or "unknown",
            "variable": of_var or "unknown",
            "value": of_value,
            "unit": of_unit or "unknown",
        },
        "optimal_variables": json_safe(optimal_vars),
        "number_of_solutions": json_safe(num_solutions),
    }


def main():
    parser = argparse.ArgumentParser(description="OptiProcess solver runner")
    parser.add_argument("--model", default="STHE", help="Model name")
    parser.add_argument("--input", required=True, help="Path to input JSON file")
    parser.add_argument("--output", required=True, help="Path to output JSON file")
    args = parser.parse_args()

    # Load input data
    with open(args.input, "r", encoding="utf-8") as f:
        input_data = json.load(f)

    model_name = input_data.get("model", args.model)
    example_name = "web"

    start = time.time()

    consistency_report = new_report()
    try:
        # Build example dict (validation errors are caught and returned gracefully)
        example_dict = build_example_dict(input_data)
        sol_dict, active_example, active_models = run_solver(
            model_name,
            example_name,
            example_dict,
            input_data.get("consistency_checks"),
            consistency_report,
        )
        results = extract_results(sol_dict, active_models, model_name)
        if not results.get("optimal_variables") or not results.get("number_of_solutions"):
            raise ValueError(
                "No feasible design found after applying the selected consistency policy. "
                "Review the consistency warnings and widen or correct the selected geometric options."
            )
        # Compute model-specific output info (thermo/hydraulic/economics)
        params = example_dict.get("Equipment1", {}).get("Model_Parameters", input_data.get("parameters", {}))
        optimal = results.get("optimal_variables", {})
        objective = results.get("objective")
        if optimal:
            output_info = compute_output_info(optimal, params, model_name, objective)
            results["calculations"] = json_safe(output_info.get("calculations", {}))
            results["objective"] = output_info.get("objective", objective)
        results["status"] = "ok"
        results["model"] = model_name
        results["consistency"] = consistency_report
        results["elapsed_seconds"] = round(time.time() - start, 4)
    except ConsistencyHardError as e:
        results = {
            "status": "error",
            "error": "Consistency check failed. The solver was not executed.",
            "details": str(e),
            "consistency": consistency_report,
            "model": model_name,
            "elapsed_seconds": round(time.time() - start, 4),
        }
    except Exception as e:
        error_msg = str(e)
        # Translate cryptic solver errors into user-friendly messages
        if "variables_survivor_names" in error_msg:
            error_msg = (
                "No feasible design found with the selected geometric options. "
                "Try widening the ranges of Shell Diameter (Ds), Tube Length (L), "
                "and Number of Baffles (Nb) so that L/Ds is between 3 and 15."
            )
        elif "allocation" in error_msg or "yfluid" in error_msg:
            error_msg = "Invalid or missing fluid allocation. Select Cold in Tubes or Hot in Tubes."
        elif "Missing required parameters" in error_msg:
            pass  # already descriptive
        results = {
            "status": "error",
            "error": error_msg,
            "consistency": consistency_report,
            "model": model_name,
            "elapsed_seconds": round(time.time() - start, 4),
        }

    # Write output
    output = json_safe(results)
    with open(args.output, "w", encoding="utf-8") as f:
        json.dump(output, f, indent=2, ensure_ascii=False)

    # Also print summary to stdout
    if results.get("status") == "ok":
        of = results.get("objective", {})
        print(f"OK | {of.get('variable','?')}={of.get('value','?')} {of.get('unit','')} | {results['elapsed_seconds']}s")
    else:
        print(f"ERROR | {results.get('error', 'unknown')} | {results['elapsed_seconds']}s")


if __name__ == "__main__":
    main()
