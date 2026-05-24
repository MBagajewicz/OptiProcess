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


def _scalar(val):
    """Extract scalar from numpy array or return as-is if already scalar."""
    if isinstance(val, np.ndarray):
        return val.item()
    return float(val) if isinstance(val, (np.floating, np.integer)) else val


def compute_intermediate_results(optimal_vars, params, model_name):
    """After optimization, compute thermo/hydraulic/economics details from optimal variables."""
    if model_name != "STHE":
        return {}

    # Wrap scalars as 1-element arrays — some calculation functions expect .shape
    Ds = np.atleast_1d(float(optimal_vars["Ds"]))
    dte = np.atleast_1d(float(optimal_vars["dte"]))
    Npt = np.atleast_1d(float(optimal_vars["Npt"]))
    rp = np.atleast_1d(float(optimal_vars["rp"]))
    lay = np.atleast_1d(float(optimal_vars["lay"]))
    L = np.atleast_1d(float(optimal_vars["L"]))
    Nb = np.atleast_1d(float(optimal_vars["Nb"]))
    Bc = np.atleast_1d(float(optimal_vars["Bc"]))

    from STHE.Model.Parameters_Update_STHE import allocation
    from STHE.Calculations import (
        Calculations_STHE_velocity_tubeside,
        Calculations_STHE_velocity_shellside,
        Calculations_STHE_Reynolds_tubeside,
        Calculations_STHE_Reynolds_shellside,
        Calculations_STHE_htubeside,
        Calculations_STHE_hshellside,
        Calculations_STHE_U,
        Calculations_STHE_DeltaPtubeside,
        Calculations_STHE_DeltaPshellside,
        Calculations_STHE_area,
        Calculations_STHE_correction_factor,
    )
    from Common_Equations_HEX import Calculations_HEX_heatload, Calculations_HEX_LMTD

    m_p = allocation(dict(params))

    # Velocities
    vt = Calculations_STHE_velocity_tubeside.STHE_tubeside_velocity(
        m_p["mt"], m_p["rot"], m_p["thk"], Ds, dte, Npt, rp, lay, m_p)
    vs = Calculations_STHE_velocity_shellside.STHE_shellside_velocity(
        m_p["ms"], m_p["ros"], Ds, rp, L, Nb, dte, lay, m_p)

    # Reynolds numbers
    Ret = Calculations_STHE_Reynolds_tubeside.STHE_Reynolds_tubeside(
        m_p["mt"], m_p["rot"], m_p["mit"], m_p["thk"], Ds, dte, Npt, rp, lay, m_p)
    Res = Calculations_STHE_Reynolds_shellside.STHE_Reynolds_shellside(
        m_p["ms"], m_p["ros"], m_p["mis"], Ds, dte, rp, lay, L, Nb, m_p)

    # Heat transfer coefficients
    ht = Calculations_STHE_htubeside.STHE_h_tubeside(
        m_p["mt"], m_p["rot"], m_p["Cpt"], m_p["mit"], m_p["kt"], m_p["thk"],
        m_p["yfluid"], Ds, dte, Npt, rp, lay, L, m_p)
    hs = Calculations_STHE_hshellside.STHE_h_shellside(
        m_p["ms"], m_p["ros"], m_p["Cps"], m_p["mis"], m_p["ks"],
        Ds, dte, Npt, rp, lay, L, Nb, Bc, m_p)

    # Overall HTC
    U_dirty = Calculations_STHE_U.STHE_overall_coefficient(
        m_p["mt"], m_p["rot"], m_p["Cpt"], m_p["mit"], m_p["kt"], m_p["Rft"],
        m_p["ms"], m_p["ros"], m_p["Cps"], m_p["mis"], m_p["ks"], m_p["Rfs"],
        m_p["thk"], params.get("ktube", 50), m_p["yfluid"],
        Ds, dte, Npt, rp, lay, L, Nb, Bc, m_p)

    # Clean HTC (without fouling)
    U_clean = Calculations_STHE_U.STHE_overall_coefficient(
        m_p["mt"], m_p["rot"], m_p["Cpt"], m_p["mit"], m_p["kt"], 0.0,
        m_p["ms"], m_p["ros"], m_p["Cps"], m_p["mis"], m_p["ks"], 0.0,
        m_p["thk"], params.get("ktube", 50), m_p["yfluid"],
        Ds, dte, Npt, rp, lay, L, Nb, Bc, m_p)

    # Pressure drops (Pa → kPa for display)
    DPt = Calculations_STHE_DeltaPtubeside.STHE_tubeside_DeltaP(
        m_p["mt"], m_p["rot"], m_p["mit"], m_p["thk"], Ds, dte, Npt, rp, lay, L, m_p) / 1000.0
    DPs = Calculations_STHE_DeltaPshellside.STHE_shellside_DeltaP(
        m_p["ms"], m_p["ros"], m_p["mis"], Ds, dte, Npt, rp, lay, L, Nb, Bc, m_p) / 1000.0

    # Area
    A_total = Calculations_STHE_area.STHE_area(Ds, dte, Npt, rp, lay, L, m_p)

    # Correction factor F
    F = Calculations_STHE_correction_factor.STHE_correction_factor(
        params["Thi"], params["Tho"], params["Tci"], params["Tco"], Npt, params["Xp"])

    # CAPEX
    par_a = params.get("par_a", 0)
    par_b = params.get("par_b", 1)
    CAPEX = par_a * A_total ** par_b

    # OPEX
    pc = params.get("pc", 0)
    Nop = params.get("Nop", 0)
    eta = params.get("eta", 1)
    # Note: DPt and DPs are in kPa here, convert back to Pa for power calculation
    DPt_Pa = DPt * 1000
    DPs_Pa = DPs * 1000
    Cop_t = Nop * (pc / 1000) * (DPt_Pa * m_p["mt"] / (eta * m_p["rot"]))
    Cop_s = Nop * (pc / 1000) * (DPs_Pa * m_p["ms"] / (eta * m_p["ros"]))
    OPEX_total = Cop_t + Cop_s

    # Amortization factor
    int_rate = params.get("int_rate", 0.1)
    n_years = params.get("n", 10)
    r = (int_rate * (1 + int_rate) ** n_years) / ((1 + int_rate) ** n_years - 1) if int_rate > 0 else 1.0 / n_years
    TAC = r * CAPEX + OPEX_total

    # Heat load
    Q = Calculations_HEX_heatload.HEX_heat_load(params["mh"], params["Cph"], params["Thi"], params["Tho"])
    Q_kW = Q / 1000.0

    # Nt approximate (from counting table: Nt = A / (pi * dte * L))
    denom = np.pi * _scalar(dte) * _scalar(L)
    Nt = int(round(_scalar(A_total) / denom)) if denom > 0 else 0

    # Required area ratio (actual / required)
    LMTD = Calculations_HEX_LMTD.HEX_lmtd(
        params["Thi"], params["Tho"], params["Tci"], params["Tco"])
    A_req = Q / (_scalar(U_dirty) * _scalar(LMTD) * _scalar(F)) if _scalar(U_dirty) > 0 and _scalar(F) > 0 else 0
    A_ratio = _scalar(A_total) / A_req if A_req > 0 else 0

    return {
        "vt": _scalar(vt), "vs": _scalar(vs),
        "Ret": _scalar(Ret), "Res": _scalar(Res),
        "ht": _scalar(ht), "hs": _scalar(hs),
        "U": _scalar(U_dirty), "Uc": _scalar(U_clean),
        "DPt": _scalar(DPt), "DPs": _scalar(DPs),
        "CAPEX": _scalar(CAPEX), "OPEX_t": _scalar(Cop_t),
        "OPEX_s": _scalar(Cop_s), "OPEX_total": _scalar(OPEX_total),
        "TAC": _scalar(TAC), "Q": _scalar(Q_kW),
        "Nt": Nt, "A_total": _scalar(A_total),
        "F": _scalar(F), "A_shell": _scalar(A_total), "A_ratio": _scalar(A_ratio),
    }


def build_example_dict(input_data):
    """Convert user-submitted JSON into an Example dict matching Examples_STHE.py structure."""
    params = input_data["parameters"]
    discrete = input_data["discrete_variables"]
    selected_of = input_data.get("selected_of", "TAC_OF")
    n_equip = input_data.get("number_of_equipment", 1)

    # The variable order must match List_of_Variables from Model_Def_STHE.py:
    # ['Ds', 'dte', 'Npt', 'rp', 'lay', 'L', 'Nb', 'Bc']
    var_order = ["Ds", "dte", "Npt", "rp", "lay", "L", "Nb", "Bc"]
    discrete_values = []
    for v in var_order:
        vals = discrete.get(v, [])
        if not vals:
            raise ValueError(
                f"Discrete variable '{v}' is empty or missing. "
                f"All 8 variables (Ds, dte, Npt, rp, lay, L, Nb, Bc) must have at least one option. "
                f"Received keys: {sorted(discrete.keys())}"
            )
        discrete_values.append(vals)

    # Validate required model parameters
    required_params = [
        "mh", "roh", "Cph", "mih", "kh", "Rfh", "DPhdisp",
        "mc", "roc", "Cpc", "mic", "kc", "Rfc", "DPcdisp",
        "ktube", "thk", "yfluid",
        "Shell_Method", "Tube_Method",
        "Aexc", "Tci", "Tco", "Thi", "Tho",
        "vsmax", "vsmin", "vtmax", "vtmin",
        "Retmin", "Resmin", "Retmax", "Resmax",
        "LBLD", "UBLD", "Xp", "F_min",
        "par_a", "par_b", "pc", "int_rate", "n", "eta", "Nop",
    ]
    missing = [p for p in required_params if p not in params]
    if missing:
        raise ValueError(f"Missing required parameters: {missing}")

    example = {
        "Number_of_Equipment": n_equip,
        "Equipment1": {
            "Model_Declarations": {
                "Type_Equipment": input_data.get("model", "STHE"),
                "Discrete_Values_of_Variables": discrete_values,
                "Selected_OF": [selected_of],
            },
            "Model_Parameters": params,
        },
    }
    return example


def inject_example(example_dict, model_name, example_name):
    """Inject an example dict into the Examples module at runtime via monkey-patching."""
    module = importlib.import_module(f"{model_name}.Examples_{model_name}")
    setattr(module, example_name, example_dict)
    return module


def run_solver(model_name, example_name, example_dict):
    """Run the full OptiProcess pipeline for the given model and example. Returns (Sol_Dict, active_example, active_models)."""
    from OptiCode import (
        Calculations_Prep_Organizer,
        Calculations_Solver_Selection,
        Calculations_Consistency_Check,
        Import_Example,
        Import_Functions,
        Import_Models,
    )

    # Inject the user-submitted example into the Examples module
    inject_example(example_dict, model_name, example_name)

    # Import example data using the existing infrastructure
    active_repo = Import_Example.Import_Example(model_name, "Examples_")
    active_example = getattr(active_repo, example_name)

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
    Calculations_Consistency_Check.Consistency_Check(active_example, active_models, save_result)
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

    try:
        # Build example dict (validation errors are caught and returned gracefully)
        example_dict = build_example_dict(input_data)
        sol_dict, active_example, active_models = run_solver(model_name, example_name, example_dict)
        results = extract_results(sol_dict, active_models, model_name)
        # Compute intermediate thermo/hydraulic/economics results
        params = input_data.get("parameters", {})
        optimal = results.get("optimal_variables", {})
        if optimal:
            intermediates = compute_intermediate_results(optimal, params, model_name)
            results["calculations"] = json_safe(intermediates)
        results["status"] = "ok"
        results["model"] = model_name
        results["elapsed_seconds"] = round(time.time() - start, 4)
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
