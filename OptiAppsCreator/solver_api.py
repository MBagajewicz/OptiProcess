#!/usr/bin/env python3
"""solver_api.py — FastAPI server that exposes the OptiProcess solver via REST API.

Start:    uvicorn solver_api:app --host 0.0.0.0 --port 8000
Endpoint: POST /api/optimize

Request body:
{
    "model": "STHE",
    "parameters": {
        "mh": 20, "roh": 750, "Cph": 2840, "mih": 0.002, "kh": 0.19, "Rfh": 0.0002, "DPhdisp": 100000.0,
        "mc": 60, "roc": 995, "Cpc": 4187, "mic": 0.0005, "kc": 0.6, "Rfc": 0.0007, "DPcdisp": 100000.0,
        "ktube": 50, "thk": 0.00165, "yfluid": "hot_stream",
        "Shell_Method": "Kern", "Tube_Method": "Dittus_Boelter",
        "Aexc": 11, "Tci": 47, "Tco": 56, "Thi": 120, "Tho": 80,
        "vsmax": 2, "vsmin": 0.5, "vtmax": 3, "vtmin": 1,
        "Retmin": 10000, "Resmin": 2000, "Retmax": 5000000, "Resmax": 100000,
        "LBLD": 3, "UBLD": 15, "Xp": 0.9, "F_min": 0.75,
        "Nss": 0, "plbmax1": 52, "plbmax2": 0.532,
        "par_a": 635.14, "par_b": 0.778, "pc": 0.15,
        "int_rate": 0.1, "n": 10, "eta": 0.6, "Nop": 7500
    },
    "discrete_variables": {
        "Ds": [0.7874, 0.8382, 0.889, 0.9398, 0.9906, 1.0668, 1.143, 1.2192, 1.3716, 1.524],
        "dte": [0.01905, 0.02540, 0.03175, 0.03810, 0.05080],
        "Npt": [1, 2, 4, 6],
        "rp": [1.25, 1.33, 1.50],
        "lay": [1, 2],
        "L": [1.2195, 1.8293, 2.4390, 3.0488, 3.6585, 4.8768, 6.0976],
        "Nb": [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20],
        "Bc": [0.25]
    },
    "selected_of": "TAC_OF",
    "number_of_equipment": 1
}
"""

import os
import sys
import json
import uuid
import subprocess
import shutil
import importlib
from pathlib import Path
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from project_store import (
    ProjectError,
    list_projects,
    load_project,
    project_to_ui_payload,
    save_project,
    ui_payload_to_project,
)


SCRIPT_DIR = Path(__file__).resolve().parent

# --- Pydantic models ---

class OptimizationRequest(BaseModel):
    model: str = "STHE"
    parameters: dict
    discrete_variables: dict
    selected_of: str = "TAC_OF"
    number_of_equipment: int = 1


class OptimizationResponse(BaseModel):
    model_config = {"extra": "allow"}
    status: str
    model: str | None = None
    objective: dict | None = None
    optimal_variables: dict | None = None
    number_of_solutions: int | None = None
    elapsed_seconds: float | None = None
    error: str | None = None


class ProjectSaveRequest(BaseModel):
    name: str | None = None
    parameters: dict
    discrete_variables: dict
    selected_of: str = "TAC_OF"
    number_of_equipment: int = 1


# --- App setup ---

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Ensure tmp directory exists on startup."""
    os.makedirs("/tmp/opencode", exist_ok=True)
    yield


app = FastAPI(title="OptiProcess Solver API", version="0.1.0", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve generated HTML from output/ at /ui path
output_dir = SCRIPT_DIR / "output"
if output_dir.exists():
    app.mount("/ui", StaticFiles(directory=str(output_dir), html=True), name="ui")


# --- Routes ---

def load_model_def(model_name: str) -> dict:
    module = importlib.import_module(f"{model_name}.Model.Model_Def_{model_name}")
    return getattr(module, f"Model_{model_name}")


def build_project_response(model: str, project_name: str) -> dict:
    model_def = load_model_def(model)
    var_order = model_def["Model_Info"]["List_of_Variables"]
    project = load_project(model, project_name)
    payload = project_to_ui_payload(model, project_name, project)
    discrete_values = payload.pop("discrete_values")
    payload["discrete_variables"] = {
        var: discrete_values[idx] if idx < len(discrete_values) else []
        for idx, var in enumerate(var_order)
    }
    payload["variable_order"] = var_order
    return payload

@app.get("/api/health")
async def health():
    return {"status": "ok", "service": "OptiProcess Solver API"}


@app.get("/api/projects/{model}")
async def api_list_projects(model: str):
    try:
        return {"model": model, "projects": list_projects(model)}
    except ProjectError as exc:
        raise HTTPException(status_code=400, detail=str(exc))


@app.get("/api/projects/{model}/{project_name}")
async def api_load_project(model: str, project_name: str):
    try:
        return build_project_response(model, project_name)
    except ProjectError as exc:
        raise HTTPException(status_code=400, detail=str(exc))
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))


@app.post("/api/projects/{model}")
async def api_save_project_as(model: str, req: ProjectSaveRequest):
    if not req.name:
        raise HTTPException(status_code=400, detail="Project name is required")
    try:
        model_def = load_model_def(model)
        var_order = model_def["Model_Info"]["List_of_Variables"]
        project = ui_payload_to_project(model, req.model_dump(), var_order)
        save_project(model, req.name, project)
        return build_project_response(model, req.name)
    except ProjectError as exc:
        raise HTTPException(status_code=400, detail=str(exc))
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))


@app.post("/api/projects/{model}/{project_name}")
async def api_save_project(model: str, project_name: str, req: ProjectSaveRequest):
    try:
        model_def = load_model_def(model)
        var_order = model_def["Model_Info"]["List_of_Variables"]
        project = ui_payload_to_project(model, req.model_dump(), var_order)
        save_project(model, project_name, project)
        return build_project_response(model, project_name)
    except ProjectError as exc:
        raise HTTPException(status_code=400, detail=str(exc))
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))


@app.post("/api/optimize", response_model=OptimizationResponse)
async def optimize(req: OptimizationRequest):
    """Run a heat exchanger design optimization with the submitted parameters."""
    job_id = uuid.uuid4().hex[:8]
    input_path = f"/tmp/opencode/input_{job_id}.json"
    output_path = f"/tmp/opencode/output_{job_id}.json"

    # Write input JSON
    input_data = {
        "model": req.model,
        "parameters": req.parameters,
        "discrete_variables": req.discrete_variables,
        "selected_of": req.selected_of,
        "number_of_equipment": req.number_of_equipment,
    }
    with open(input_path, "w", encoding="utf-8") as f:
        json.dump(input_data, f)

    # Locate solver_runner.py
    runner = SCRIPT_DIR / "solver_runner.py"

    try:
        result = subprocess.run(
            [sys.executable, str(runner), "--model", req.model, "--input", input_path, "--output", output_path],
            cwd=str(SCRIPT_DIR),
            capture_output=True,
            text=True,
            timeout=120,
        )
    except subprocess.TimeoutExpired:
        raise HTTPException(status_code=504, detail="Solver timed out after 120 seconds")

    if result.returncode != 0:
        raise HTTPException(
            status_code=500,
            detail=f"Solver exited with code {result.returncode}\nstdout: {result.stdout}\nstderr: {result.stderr}",
        )

    # Read output JSON
    if not os.path.exists(output_path):
        raise HTTPException(status_code=500, detail=f"Solver did not produce output file: {output_path}")

    with open(output_path, "r", encoding="utf-8") as f:
        output_data = json.load(f)

    # Clean up temp files
    for p in [input_path, output_path]:
        try:
            os.remove(p)
        except OSError:
            pass

    return OptimizationResponse(**output_data)


# --- Main ---
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("solver_api:app", host="0.0.0.0", port=8000, reload=True)
