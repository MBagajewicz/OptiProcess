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
import importlib
import copy
from pathlib import Path
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException, Query, Request, Response, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from auth_db import (
    create_session,
    get_session_user,
    get_user_by_username,
    init_db,
    record_login,
    revoke_session,
    verify_password,
)

from project_store import (
    ProjectError,
    create_user_project,
    export_user_backup,
    list_user_designs,
    list_user_projects,
    list_projects,
    load_default_design,
    load_project,
    load_user_design,
    project_to_ui_payload,
    save_user_design,
    restore_user_backup,
)


SCRIPT_DIR = Path(__file__).resolve().parent
SESSION_COOKIE_NAME = os.getenv("SESSION_COOKIE_NAME", "optihex_session")
SESSION_HOURS = int(os.getenv("SESSION_HOURS", "8"))
SESSION_COOKIE_SECURE = os.getenv("SESSION_COOKIE_SECURE", "false").lower() in {"1", "true", "yes", "on"}

# --- Pydantic models ---

class OptimizationRequest(BaseModel):
    model: str = "STHE"
    parameters: dict
    parameter_units: dict | None = None
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
    design_name: str | None = None
    user_project_id: int | None = None
    user_project_name: str | None = None
    parameters: dict
    parameter_units: dict | None = None
    result_units: dict | None = None
    geometric_standards: dict | None = None
    discrete_variables: dict
    selected_of: str = "TAC_OF"
    number_of_equipment: int = 1


class CalculatedInputsRequest(BaseModel):
    parameters: dict


class UserProjectCreateRequest(BaseModel):
    name: str
    description: str | None = None


class BackupRestoreRequest(BaseModel):
    backup: dict
    overwrite: bool = True


TEXT_PARAMETER_KEYS = {"Shell_Method", "Tube_Method", "yfluid", "_selected_of"}


def validate_numeric_parameters(parameters: dict) -> None:
    for key, value in parameters.items():
        if key in TEXT_PARAMETER_KEYS or value is None:
            continue
        if isinstance(value, bool):
            raise HTTPException(status_code=400, detail=f"Parameter '{key}' must be numeric")
        if isinstance(value, (int, float)):
            continue
        if isinstance(value, str):
            try:
                float(value.strip())
            except ValueError:
                raise HTTPException(status_code=400, detail=f"Parameter '{key}' must be numeric")
            continue
        raise HTTPException(status_code=400, detail=f"Parameter '{key}' must be numeric")


def normalize_numeric_parameters(parameters: dict) -> dict:
    normalized = {}
    for key, value in parameters.items():
        if key in TEXT_PARAMETER_KEYS or value is None:
            normalized[key] = value
        elif isinstance(value, str):
            normalized[key] = float(value.strip())
        else:
            normalized[key] = value
    return normalized


class LoginRequest(BaseModel):
    username: str
    password: str


# --- App setup ---

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Ensure tmp directory exists on startup."""
    os.makedirs("/tmp/opencode", exist_ok=True)
    init_db()
    yield


app = FastAPI(title="OptiProcess Solver API", version="0.1.0", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.middleware("http")
async def protect_ui_pages(request: Request, call_next):
    path = request.url.path
    public_ui = {"/ui/login.html"}
    protected = path == "/ui/main_menu.html" or path.startswith("/ui/STHE/") or path.startswith("/ui/GPHE/")
    if protected and path not in public_ui and not get_session_user(request.cookies.get(SESSION_COOKIE_NAME)):
        return RedirectResponse(url="/ui/login.html", status_code=303)
    return await call_next(request)

# Serve generated HTML from output/ at /ui path
output_dir = SCRIPT_DIR / "output"
if output_dir.exists():
    app.mount("/ui", StaticFiles(directory=str(output_dir), html=True), name="ui")


# --- Routes ---

def client_ip(request: Request) -> str:
    forwarded = request.headers.get("x-forwarded-for")
    if forwarded:
        return forwarded.split(",", 1)[0].strip()
    return request.client.host if request.client else "unknown"


def require_session(request: Request) -> dict:
    user = get_session_user(request.cookies.get(SESSION_COOKIE_NAME))
    if not user:
        raise HTTPException(status_code=401, detail="Authentication required")
    return user

def load_model_def(model_name: str) -> dict:
    module = importlib.import_module(f"{model_name}.Model.Model_Def_{model_name}")
    return getattr(module, f"Model_{model_name}")


def build_project_response(model: str, project_name: str, scope: str = "users", user_id: int | None = None, user_project_id: int | None = None) -> dict:
    model_def = load_model_def(model)
    var_order = model_def["Model_Info"]["List_of_Variables"]
    if scope == "users":
        if user_id is None:
            raise ProjectError("Authentication required")
        payload = load_user_design(user_id, model, project_name, project_id=user_project_id)
        payload["variable_order"] = var_order
        return payload
    project = load_project(model, project_name, scope=scope)
    payload = project_to_ui_payload(model, project_name, project)
    discrete_values = payload.pop("discrete_values")
    payload["discrete_variables"] = {
        var: discrete_values[idx] if idx < len(discrete_values) else []
        for idx, var in enumerate(var_order)
    }
    payload["variable_order"] = var_order
    payload["scope"] = scope
    return payload


def build_default_design_response(model: str) -> dict:
    model_def = load_model_def(model)
    var_order = model_def["Model_Info"]["List_of_Variables"]
    project = load_default_design(model)
    payload = project_to_ui_payload(model, "Default_Design", project)
    discrete_values = payload.pop("discrete_values")
    payload["discrete_variables"] = {
        var: discrete_values[idx] if idx < len(discrete_values) else []
        for idx, var in enumerate(var_order)
    }
    payload["variable_order"] = var_order
    payload["scope"] = "default"
    return payload


def update_energy_balance_calculated_parameters(parameters: dict) -> dict:
    from Common_Equations_HEX import Calculations_HEX_LMTD

    calculated = {}
    try:
        mh = float(parameters["mh"])
        cph = float(parameters["Cph"])
        thi = float(parameters["Thi"])
        tho = float(parameters["Tho"])
        mc = float(parameters["mc"])
        cpc = float(parameters["Cpc"])
        tci = float(parameters["Tci"])
        if mc != 0 and cpc != 0:
            parameters["Tco"] = tci + mh * cph * (thi - tho) / (mc * cpc)
            calculated["Tco"] = parameters["Tco"]
            try:
                calculated["LMTD"] = float(Calculations_HEX_LMTD.HEX_lmtd(thi, tho, tci, parameters["Tco"]))
            except Exception:
                pass
    except (KeyError, TypeError, ValueError):
        pass
    return calculated


def build_calculated_inputs_response(model: str, parameters: dict) -> dict:
    from OptiCode import Calculations_Consistency_Check, Import_Functions, Import_Models

    validate_numeric_parameters(parameters)
    model = model.strip()
    normalized_parameters = normalize_numeric_parameters(parameters)
    project = copy.deepcopy(load_default_design(model))
    equipment = project["Equipment1"]
    equipment["Model_Parameters"].update({k: v for k, v in normalized_parameters.items() if k != "_selected_of"})
    if normalized_parameters.get("_selected_of"):
        equipment["Model_Declarations"]["Selected_OF"] = [normalized_parameters["_selected_of"]]

    active_models_list = [model, equipment["Model_Declarations"].get("Type_Equipment", model)]
    active_models_list = list(set(active_models_list))
    active_models = {
        "Models_Def": Import_Models.Import_Models(active_models_list, "Model_Def_"),
        "Constraints_and_OF": Import_Functions.Import_Functions(active_models_list, "Constraints_and_OF_"),
        "Parameters_Update": Import_Functions.Import_Functions(active_models_list, "Parameters_Update_"),
    }
    messages = []

    def save_result(*texts):
        messages.append(" ".join(str(text) for text in texts))

    consistency_report = Calculations_Consistency_Check.Consistency_Check(project, active_models, save_result)
    model_parameters = equipment["Model_Parameters"]
    calculated = update_energy_balance_calculated_parameters(model_parameters)
    return {
        "status": "ok",
        "model": model,
        "parameters": calculated,
        "consistency": consistency_report,
        "messages": messages[-20:],
    }

@app.get("/api/health")
async def health():
    return {"status": "ok", "service": "OptiProcess Solver API"}


@app.post("/api/auth/login")
async def auth_login(req: LoginRequest, request: Request, response: Response):
    username = req.username.strip()
    ip_address = client_ip(request)
    user = get_user_by_username(username)
    if not user:
        record_login(None, username, ip_address, False, "unknown_user")
        raise HTTPException(status_code=401, detail="Invalid username or password")
    if not user.get("is_active"):
        record_login(user["id"], username, ip_address, False, "inactive_user")
        raise HTTPException(status_code=401, detail="Invalid username or password")
    if not verify_password(req.password, user.get("password_hash")):
        record_login(user["id"], username, ip_address, False, "bad_password")
        raise HTTPException(status_code=401, detail="Invalid username or password")

    record_login(user["id"], username, ip_address, True, None)

    session_token = create_session(
        user["id"], ip_address, request.headers.get("user-agent"), SESSION_HOURS
    )
    response.set_cookie(
        SESSION_COOKIE_NAME,
        session_token,
        httponly=True,
        secure=SESSION_COOKIE_SECURE,
        samesite="lax",
        max_age=SESSION_HOURS * 3600,
    )
    return {"status": "ok", "username": user["username"], "email": user["email"]}


@app.post("/api/auth/logout")
async def auth_logout(request: Request, response: Response):
    revoke_session(request.cookies.get(SESSION_COOKIE_NAME))
    response.delete_cookie(SESSION_COOKIE_NAME, secure=SESSION_COOKIE_SECURE, samesite="lax")
    return {"status": "ok"}


@app.get("/api/auth/me")
async def auth_me(user: dict = Depends(require_session)):
    return {"status": "ok", "username": user["username"], "email": user["email"]}


@app.get("/api/user-projects")
async def api_list_user_projects(user: dict = Depends(require_session)):
    return {"projects": list_user_projects(user["id"])}


@app.post("/api/user-projects")
async def api_create_user_project(req: UserProjectCreateRequest, user: dict = Depends(require_session)):
    try:
        return create_user_project(user["id"], req.name, req.description)
    except ProjectError as exc:
        raise HTTPException(status_code=400, detail=str(exc))


@app.get("/api/user-projects/{project_id}/designs")
async def api_list_user_project_designs(project_id: int, model: str | None = None, user: dict = Depends(require_session)):
    try:
        return {"project_id": project_id, "designs": list_user_designs(user["id"], model=model, project_id=project_id)}
    except ProjectError as exc:
        raise HTTPException(status_code=400, detail=str(exc))


@app.get("/api/user-backup")
async def api_export_user_backup(user: dict = Depends(require_session)):
    try:
        return export_user_backup(user["id"])
    except ProjectError as exc:
        raise HTTPException(status_code=400, detail=str(exc))
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))


@app.post("/api/user-backup/restore")
async def api_restore_user_backup(req: BackupRestoreRequest, user: dict = Depends(require_session)):
    try:
        return restore_user_backup(user["id"], req.backup, overwrite=req.overwrite)
    except ProjectError as exc:
        raise HTTPException(status_code=400, detail=str(exc))
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))


@app.get("/api/projects/{model}")
async def api_list_projects(model: str, scope: str = Query("users"), user: dict = Depends(require_session)):
    try:
        if scope == "users":
            return {"model": model, "scope": scope, "projects": list_user_designs(user["id"], model=model)}
        return {"model": model, "scope": scope, "projects": list_projects(model, scope=scope)}
    except ProjectError as exc:
        raise HTTPException(status_code=400, detail=str(exc))


@app.get("/api/projects/{model}/default-design")
async def api_default_design(model: str, user: dict = Depends(require_session)):
    try:
        return build_default_design_response(model)
    except ProjectError as exc:
        raise HTTPException(status_code=400, detail=str(exc))
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))


@app.post("/api/models/{model}/calculated-inputs")
async def api_calculated_inputs(model: str, req: CalculatedInputsRequest, user: dict = Depends(require_session)):
    try:
        return build_calculated_inputs_response(model, req.parameters)
    except ProjectError as exc:
        raise HTTPException(status_code=400, detail=str(exc))
    except HTTPException:
        raise
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))


@app.get("/api/projects/{model}/{project_name}")
async def api_load_project(model: str, project_name: str, scope: str = Query("users"), user_project_id: int | None = None, user: dict = Depends(require_session)):
    try:
        return build_project_response(model, project_name, scope=scope, user_id=user["id"], user_project_id=user_project_id)
    except ProjectError as exc:
        raise HTTPException(status_code=400, detail=str(exc))
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))


@app.post("/api/projects/{model}")
async def api_save_project_as(model: str, req: ProjectSaveRequest, user: dict = Depends(require_session)):
    design_name = req.design_name or req.name
    if not design_name:
        raise HTTPException(status_code=400, detail="Project name is required")
    try:
        validate_numeric_parameters(req.parameters)
        model_def = load_model_def(model)
        var_order = model_def["Model_Info"]["List_of_Variables"]
        payload = req.model_dump()
        payload["parameters"] = normalize_numeric_parameters(payload["parameters"])
        saved = save_user_design(user["id"], model, design_name, payload, project_id=req.user_project_id, user_project_name=req.user_project_name)
        saved["variable_order"] = var_order
        return saved
    except ProjectError as exc:
        raise HTTPException(status_code=400, detail=str(exc))
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))


@app.post("/api/projects/{model}/{project_name}")
async def api_save_project(model: str, project_name: str, req: ProjectSaveRequest, user: dict = Depends(require_session)):
    try:
        validate_numeric_parameters(req.parameters)
        model_def = load_model_def(model)
        var_order = model_def["Model_Info"]["List_of_Variables"]
        payload = req.model_dump()
        payload["parameters"] = normalize_numeric_parameters(payload["parameters"])
        saved = save_user_design(user["id"], model, project_name, payload, project_id=req.user_project_id, user_project_name=req.user_project_name)
        saved["variable_order"] = var_order
        return saved
    except ProjectError as exc:
        raise HTTPException(status_code=400, detail=str(exc))
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))


@app.post("/api/optimize", response_model=OptimizationResponse)
async def optimize(req: OptimizationRequest, user: dict = Depends(require_session)):
    """Run a heat exchanger design optimization with the submitted parameters."""
    validate_numeric_parameters(req.parameters)
    job_id = uuid.uuid4().hex[:8]
    input_path = f"/tmp/opencode/input_{job_id}.json"
    output_path = f"/tmp/opencode/output_{job_id}.json"

    # Write input JSON
    input_data = {
        "model": req.model,
        "parameters": normalize_numeric_parameters(req.parameters),
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
