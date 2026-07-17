#!/usr/bin/env python3
"""Project storage helpers for OptiAppsCreator.

Projects are Python files stored under {MODEL}/Projects/{scope}/{ProjectName}.py and
must export a single variable named Project. The loader validates the AST before
execution and only allows data-oriented expressions used by project files.
"""

from __future__ import annotations

import ast
import copy
import json
import pprint
import re
import shutil
from pathlib import Path
from typing import Any

import numpy as np

from auth_db import connect, init_db, utc_iso


SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_NAME_RE = re.compile(r"^[A-Za-z0-9_-]+$")
MODEL_NAME_RE = re.compile(r"^[A-Za-z0-9_]+$")
PROJECT_SCOPES = {
    "examples": "Example_Projects",
    "users": "User_Projects",
}


class ProjectError(ValueError):
    """Raised when a project path, file, or payload is invalid."""


def json_safe(obj: Any) -> Any:
    """Convert numpy/scalar objects to JSON-serializable Python objects."""
    if isinstance(obj, np.ndarray):
        return obj.tolist()
    if isinstance(obj, np.generic):
        return obj.item()
    if isinstance(obj, dict):
        return {k: json_safe(v) for k, v in obj.items()}
    if isinstance(obj, (list, tuple)):
        return [json_safe(v) for v in obj]
    return obj


def validate_model_name(model: str) -> str:
    if not MODEL_NAME_RE.fullmatch(model or ""):
        raise ProjectError("Invalid model name")
    model_dir = SCRIPT_DIR / model
    if not model_dir.is_dir():
        raise ProjectError(f"Unknown model: {model}")
    return model


def normalize_project_name(project_name: str) -> str:
    name = (project_name or "").strip()
    if name.endswith(".py"):
        name = name[:-3]
    if not PROJECT_NAME_RE.fullmatch(name):
        raise ProjectError("Invalid project name. Use letters, numbers, '_' or '-'.")
    return name


def normalize_scope(scope: str | None) -> str:
    scope = scope or "users"
    if scope not in PROJECT_SCOPES:
        raise ProjectError("Invalid project scope. Use 'examples' or 'users'.")
    return scope


def projects_dir(model: str) -> Path:
    model = validate_model_name(model)
    path = SCRIPT_DIR / model / "Projects"
    path.mkdir(parents=True, exist_ok=True)
    return path


def project_scope_dir(model: str, scope: str | None = "users") -> Path:
    scope = normalize_scope(scope)
    path = projects_dir(model) / PROJECT_SCOPES[scope]
    path.mkdir(parents=True, exist_ok=True)
    return path


def project_path(model: str, project_name: str, scope: str | None = "users") -> Path:
    base = project_scope_dir(model, scope).resolve()
    name = normalize_project_name(project_name)
    path = (base / f"{name}.py").resolve()
    if base != path.parent:
        raise ProjectError("Project path escapes Projects directory")
    return path


def list_projects(model: str, scope: str | None = "users") -> list[dict[str, Any]]:
    scope = normalize_scope(scope)
    base = project_scope_dir(model, scope)
    projects = []
    for path in sorted(base.glob("*.py"), key=lambda p: p.name.lower()):
        if path.name == "__init__.py":
            continue
        projects.append({"name": path.stem, "file": path.name, "scope": scope})
    return projects


class _ProjectAstValidator(ast.NodeVisitor):
    """Validate that a project file contains only safe data expressions."""

    def __init__(self) -> None:
        self.project_assignments = 0

    def visit_Module(self, node: ast.Module) -> Any:
        for stmt in node.body:
            if isinstance(stmt, ast.Import):
                self.visit(stmt)
            elif isinstance(stmt, ast.Assign):
                self.visit(stmt)
            elif isinstance(stmt, ast.Expr) and isinstance(stmt.value, ast.Constant) and isinstance(stmt.value.value, str):
                continue
            else:
                raise ProjectError(f"Unsupported statement in project file: {type(stmt).__name__}")

    def visit_Import(self, node: ast.Import) -> Any:
        if len(node.names) != 1:
            raise ProjectError("Only 'import numpy as np' is allowed")
        alias = node.names[0]
        if alias.name != "numpy" or alias.asname != "np":
            raise ProjectError("Only 'import numpy as np' is allowed")

    def visit_Assign(self, node: ast.Assign) -> Any:
        if len(node.targets) != 1 or not isinstance(node.targets[0], ast.Name) or node.targets[0].id != "Project":
            raise ProjectError("Project files must assign only the 'Project' variable")
        self.project_assignments += 1
        self.visit(node.value)

    def visit_Call(self, node: ast.Call) -> Any:
        if isinstance(node.func, ast.Name):
            if node.func.id not in {"list", "range"}:
                raise ProjectError(f"Function call not allowed: {node.func.id}")
        elif isinstance(node.func, ast.Attribute):
            if not (isinstance(node.func.value, ast.Name) and node.func.value.id == "np" and node.func.attr == "array"):
                raise ProjectError("Only np.array(...) attribute calls are allowed")
        else:
            raise ProjectError("Unsupported function call")
        for arg in node.args:
            self.visit(arg)
        for keyword in node.keywords:
            self.visit(keyword.value)

    def visit_Attribute(self, node: ast.Attribute) -> Any:
        if not (isinstance(node.value, ast.Name) and node.value.id == "np" and node.attr == "array"):
            raise ProjectError("Only np.array is allowed as an attribute")

    def visit_Name(self, node: ast.Name) -> Any:
        if node.id.startswith("__"):
            raise ProjectError("Dunder names are not allowed")

    def visit_Constant(self, node: ast.Constant) -> Any:
        return None

    def visit_Dict(self, node: ast.Dict) -> Any:
        for key in node.keys:
            if key is not None:
                self.visit(key)
        for value in node.values:
            self.visit(value)

    def visit_List(self, node: ast.List) -> Any:
        for elt in node.elts:
            self.visit(elt)

    def visit_Tuple(self, node: ast.Tuple) -> Any:
        for elt in node.elts:
            self.visit(elt)

    def visit_UnaryOp(self, node: ast.UnaryOp) -> Any:
        if not isinstance(node.op, (ast.UAdd, ast.USub)):
            raise ProjectError("Only unary +/- are allowed")
        self.visit(node.operand)

    def visit_BinOp(self, node: ast.BinOp) -> Any:
        if not isinstance(node.op, (ast.Add, ast.Sub, ast.Mult, ast.Div, ast.FloorDiv, ast.Mod, ast.Pow)):
            raise ProjectError("Unsupported binary operation")
        self.visit(node.left)
        self.visit(node.right)

    def visit_ListComp(self, node: ast.ListComp) -> Any:
        self.visit(node.elt)
        for gen in node.generators:
            self.visit(gen)

    def visit_comprehension(self, node: ast.comprehension) -> Any:
        if node.is_async:
            raise ProjectError("Async comprehensions are not allowed")
        self.visit(node.target)
        self.visit(node.iter)
        for condition in node.ifs:
            self.visit(condition)

    def visit_Compare(self, node: ast.Compare) -> Any:
        self.visit(node.left)
        for comparator in node.comparators:
            self.visit(comparator)

    def generic_visit(self, node: ast.AST) -> Any:
        allowed = (
            ast.Load, ast.Store, ast.Add, ast.Sub, ast.Mult, ast.Div, ast.FloorDiv,
            ast.Mod, ast.Pow, ast.UAdd, ast.USub, ast.Eq, ast.NotEq, ast.Lt,
            ast.LtE, ast.Gt, ast.GtE,
        )
        if isinstance(node, allowed):
            return None
        super().generic_visit(node)


def load_project_source(model: str, project_name: str, source: str) -> dict[str, Any]:
    """Load a project from source text without writing it to disk."""
    validate_model_name(model)
    name = normalize_project_name(project_name)
    tree = ast.parse(source, filename=f"{name}.py")
    validator = _ProjectAstValidator()
    validator.visit(tree)
    if validator.project_assignments != 1:
        raise ProjectError("Project file must assign Project exactly once")

    def safe_import(name, globals=None, locals=None, fromlist=(), level=0):
        if name == "numpy" and level == 0:
            return np
        raise ProjectError("Only numpy can be imported by project files")

    env: dict[str, Any] = {
        "__builtins__": {"range": range, "list": list, "__import__": safe_import},
        "np": np,
        "numpy": np,
    }
    local_env: dict[str, Any] = {}
    exec(compile(tree, f"{name}.py", "exec"), env, local_env)
    project = local_env.get("Project")
    if not isinstance(project, dict):
        raise ProjectError("Project must be a dictionary")
    return project


def load_project(model: str, project_name: str, scope: str | None = "users") -> dict[str, Any]:
    path = project_path(model, project_name, scope)
    if not path.exists():
        raise ProjectError(f"Project not found: {project_name}")
    return load_project_source(model, project_name, path.read_text(encoding="utf-8"))


def default_design_path(model: str) -> Path:
    return projects_dir(model) / "Default_Design.py"


def fallback_default_design_path(model: str) -> Path:
    return project_scope_dir(model, "examples") / "Example1.py"


def ensure_default_design(model: str) -> Path:
    model = validate_model_name(model)
    default_path = default_design_path(model)
    if default_path.exists():
        return default_path

    fallback_path = fallback_default_design_path(model)
    if fallback_path.exists():
        shutil.copyfile(fallback_path, default_path)
        return default_path

    raise ProjectError(
        f"Default design not found for model {model}. "
        f"Expected {default_path.relative_to(SCRIPT_DIR)}. "
        f"Fallback {fallback_path.relative_to(SCRIPT_DIR)} also does not exist. "
        "Create Default_Design.py or restore Example1.py."
    )


def load_default_design(model: str) -> dict[str, Any]:
    path = ensure_default_design(model)
    return load_project_source(model, "Default_Design", path.read_text(encoding="utf-8"))


def save_project(model: str, project_name: str, project: dict[str, Any], scope: str | None = "users") -> Path:
    scope = normalize_scope(scope)
    if scope == "examples":
        raise ProjectError("Example projects are read-only")
    path = project_path(model, project_name, scope)
    project_copy = json_safe(copy.deepcopy(project))
    text = "import numpy as np\n\nProject = " + pprint.pformat(project_copy, width=120, sort_dicts=False) + "\n"
    path.write_text(text, encoding="utf-8")
    return path


def list_user_projects(user_id: int) -> list[dict[str, Any]]:
    init_db()
    with connect() as conn:
        rows = conn.execute(
            """
            SELECT p.*, COUNT(d.id) AS design_count
            FROM user_projects p
            LEFT JOIN user_designs d ON d.project_id = p.id
            WHERE p.user_id = ?
            GROUP BY p.id
            ORDER BY p.name COLLATE NOCASE
            """,
            (user_id,),
        ).fetchall()
    return [dict(row) for row in rows]


def get_user_project(user_id: int, project_id: int) -> dict[str, Any]:
    init_db()
    with connect() as conn:
        row = conn.execute(
            "SELECT * FROM user_projects WHERE id = ? AND user_id = ?",
            (project_id, user_id),
        ).fetchone()
    if not row:
        raise ProjectError("User project not found")
    return dict(row)


def get_or_create_user_project(user_id: int, name: str | None = None) -> dict[str, Any]:
    project_name = normalize_project_name(name or "My_Designs")
    init_db()
    now = utc_iso()
    with connect() as conn:
        row = conn.execute(
            "SELECT * FROM user_projects WHERE user_id = ? AND name = ?",
            (user_id, project_name),
        ).fetchone()
        if row:
            return dict(row)
        cursor = conn.execute(
            """
            INSERT INTO user_projects (user_id, name, description, created_at, updated_at)
            VALUES (?, ?, NULL, ?, ?)
            """,
            (user_id, project_name, now, now),
        )
        project_id = cursor.lastrowid
        row = conn.execute("SELECT * FROM user_projects WHERE id = ?", (project_id,)).fetchone()
    return dict(row)


def create_user_project(user_id: int, name: str, description: str | None = None) -> dict[str, Any]:
    project_name = normalize_project_name(name)
    init_db()
    now = utc_iso()
    try:
        with connect() as conn:
            cursor = conn.execute(
                """
                INSERT INTO user_projects (user_id, name, description, created_at, updated_at)
                VALUES (?, ?, ?, ?, ?)
                """,
                (user_id, project_name, description, now, now),
            )
            row = conn.execute("SELECT * FROM user_projects WHERE id = ?", (cursor.lastrowid,)).fetchone()
        return dict(row)
    except Exception as exc:
        raise ProjectError(f"Could not create user project: {exc}")


def list_user_designs(user_id: int, model: str | None = None, project_id: int | None = None) -> list[dict[str, Any]]:
    init_db()
    filters = ["p.user_id = ?"]
    params: list[Any] = [user_id]
    if model:
        filters.append("d.model = ?")
        params.append(validate_model_name(model))
    if project_id:
        filters.append("p.id = ?")
        params.append(project_id)
    where = " AND ".join(filters)
    with connect() as conn:
        rows = conn.execute(
            f"""
            SELECT d.id, d.project_id, d.model, d.name, d.created_at, d.updated_at,
                   p.name AS user_project_name
            FROM user_designs d
            JOIN user_projects p ON p.id = d.project_id
            WHERE {where}
            ORDER BY p.name COLLATE NOCASE, d.model COLLATE NOCASE, d.name COLLATE NOCASE
            """,
            params,
        ).fetchall()
    return [dict(row) for row in rows]


def _design_payload_to_json(model: str, name: str, payload: dict[str, Any]) -> str:
    design = {
        "model": model,
        "name": normalize_project_name(name),
        "parameters": json_safe(payload.get("parameters") or {}),
        "parameter_units": json_safe(payload.get("parameter_units") or {}),
        "geometric_standards": json_safe(payload.get("geometric_standards") or {}),
        "discrete_variables": json_safe(payload.get("discrete_variables") or {}),
        "selected_of": payload.get("selected_of") or "TAC_OF",
        "number_of_equipment": int(payload.get("number_of_equipment") or 1),
    }
    return json.dumps(design, ensure_ascii=False, sort_keys=True)


def save_user_design(
    user_id: int,
    model: str,
    name: str,
    payload: dict[str, Any],
    project_id: int | None = None,
    user_project_name: str | None = None,
) -> dict[str, Any]:
    model = validate_model_name(model)
    design_name = normalize_project_name(name)
    if project_id:
        user_project = get_user_project(user_id, int(project_id))
    else:
        user_project = get_or_create_user_project(user_id, user_project_name)
    now = utc_iso()
    design_json = _design_payload_to_json(model, design_name, payload)
    with connect() as conn:
        existing = conn.execute(
            "SELECT id FROM user_designs WHERE project_id = ? AND model = ? AND name = ?",
            (user_project["id"], model, design_name),
        ).fetchone()
        if existing:
            conn.execute(
                "UPDATE user_designs SET design_json = ?, updated_at = ? WHERE id = ?",
                (design_json, now, existing["id"]),
            )
            design_id = existing["id"]
        else:
            cursor = conn.execute(
                """
                INSERT INTO user_designs (project_id, model, name, design_json, created_at, updated_at)
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (user_project["id"], model, design_name, design_json, now, now),
            )
            design_id = cursor.lastrowid
        conn.execute("UPDATE user_projects SET updated_at = ? WHERE id = ?", (now, user_project["id"]))
        row = conn.execute(
            """
            SELECT d.id, d.project_id, d.model, d.name, d.design_json, d.created_at, d.updated_at,
                   p.name AS user_project_name
            FROM user_designs d
            JOIN user_projects p ON p.id = d.project_id
            WHERE d.id = ?
            """,
            (design_id,),
        ).fetchone()
    return _design_row_to_ui_payload(row)


def load_user_design(user_id: int, model: str, name: str, project_id: int | None = None) -> dict[str, Any]:
    model = validate_model_name(model)
    design_name = normalize_project_name(name)
    filters = ["p.user_id = ?", "d.model = ?", "d.name = ?"]
    params: list[Any] = [user_id, model, design_name]
    if project_id:
        filters.append("p.id = ?")
        params.append(project_id)
    where = " AND ".join(filters)
    with connect() as conn:
        row = conn.execute(
            f"""
            SELECT d.id, d.project_id, d.model, d.name, d.design_json, d.created_at, d.updated_at,
                   p.name AS user_project_name
            FROM user_designs d
            JOIN user_projects p ON p.id = d.project_id
            WHERE {where}
            ORDER BY d.updated_at DESC
            LIMIT 1
            """,
            params,
        ).fetchone()
    if not row:
        raise ProjectError("Design not found")
    return _design_row_to_ui_payload(row)


def export_user_backup(user_id: int) -> dict[str, Any]:
    init_db()
    with connect() as conn:
        project_rows = conn.execute(
            """
            SELECT id, name, description
            FROM user_projects
            WHERE user_id = ?
            ORDER BY name COLLATE NOCASE
            """,
            (user_id,),
        ).fetchall()
        projects = []
        for project in project_rows:
            design_rows = conn.execute(
                """
                SELECT model, name, design_json
                FROM user_designs
                WHERE project_id = ?
                ORDER BY model COLLATE NOCASE, name COLLATE NOCASE
                """,
                (project["id"],),
            ).fetchall()
            designs = []
            for design in design_rows:
                data = json.loads(design["design_json"])
                designs.append({
                    "model": design["model"],
                    "name": design["name"],
                    "parameters": data.get("parameters", {}),
                    "parameter_units": data.get("parameter_units", {}),
                    "geometric_standards": data.get("geometric_standards", {}),
                    "discrete_variables": data.get("discrete_variables", {}),
                    "selected_of": data.get("selected_of", "TAC_OF"),
                    "number_of_equipment": data.get("number_of_equipment", 1),
                })
            projects.append({
                "name": project["name"],
                "description": project["description"],
                "designs": designs,
            })
    return {
        "format": "optiapps_user_backup",
        "version": 1,
        "created_at": utc_iso(),
        "projects": projects,
    }


def restore_user_backup(user_id: int, backup: dict[str, Any], overwrite: bool = True) -> dict[str, int]:
    if not isinstance(backup, dict):
        raise ProjectError("Backup payload must be a JSON object")
    if backup.get("format") != "optiapps_user_backup" or backup.get("version") != 1:
        raise ProjectError("Invalid backup format or version")
    projects = backup.get("projects")
    if not isinstance(projects, list):
        raise ProjectError("Backup must contain a projects list")

    summary = {
        "projects_created": 0,
        "projects_updated": 0,
        "designs_created": 0,
        "designs_overwritten": 0,
        "designs_skipped": 0,
    }
    init_db()
    now = utc_iso()
    with connect() as conn:
        for project in projects:
            if not isinstance(project, dict):
                raise ProjectError("Each project in the backup must be an object")
            project_name = normalize_project_name(project.get("name"))
            description = project.get("description")
            if description is not None:
                description = str(description)
            row = conn.execute(
                "SELECT * FROM user_projects WHERE user_id = ? AND name = ?",
                (user_id, project_name),
            ).fetchone()
            if row:
                project_id = row["id"]
                conn.execute(
                    "UPDATE user_projects SET description = ?, updated_at = ? WHERE id = ?",
                    (description, now, project_id),
                )
                summary["projects_updated"] += 1
            else:
                cursor = conn.execute(
                    """
                    INSERT INTO user_projects (user_id, name, description, created_at, updated_at)
                    VALUES (?, ?, ?, ?, ?)
                    """,
                    (user_id, project_name, description, now, now),
                )
                project_id = cursor.lastrowid
                summary["projects_created"] += 1

            designs = project.get("designs") or []
            if not isinstance(designs, list):
                raise ProjectError(f"Project '{project_name}' designs must be a list")
            for design in designs:
                if not isinstance(design, dict):
                    raise ProjectError(f"Design in project '{project_name}' must be an object")
                model = validate_model_name(design.get("model"))
                design_name = normalize_project_name(design.get("name"))
                design_json = _design_payload_to_json(model, design_name, design)
                existing = conn.execute(
                    "SELECT id FROM user_designs WHERE project_id = ? AND model = ? AND name = ?",
                    (project_id, model, design_name),
                ).fetchone()
                if existing:
                    if not overwrite:
                        summary["designs_skipped"] += 1
                        continue
                    conn.execute(
                        "UPDATE user_designs SET design_json = ?, updated_at = ? WHERE id = ?",
                        (design_json, now, existing["id"]),
                    )
                    summary["designs_overwritten"] += 1
                else:
                    conn.execute(
                        """
                        INSERT INTO user_designs (project_id, model, name, design_json, created_at, updated_at)
                        VALUES (?, ?, ?, ?, ?, ?)
                        """,
                        (project_id, model, design_name, design_json, now, now),
                    )
                    summary["designs_created"] += 1
            conn.execute("UPDATE user_projects SET updated_at = ? WHERE id = ?", (now, project_id))
    return summary


def _design_row_to_ui_payload(row: Any) -> dict[str, Any]:
    data = json.loads(row["design_json"])
    return {
        "id": row["id"],
        "project_id": row["project_id"],
        "user_project_id": row["project_id"],
        "user_project_name": row["user_project_name"],
        "name": row["name"],
        "model": row["model"],
        "parameters": data.get("parameters", {}),
        "parameter_units": data.get("parameter_units", {}),
        "geometric_standards": data.get("geometric_standards", {}),
        "discrete_variables": data.get("discrete_variables", {}),
        "selected_of": data.get("selected_of", "TAC_OF"),
        "number_of_equipment": data.get("number_of_equipment", 1),
        "scope": "users",
    }


def project_to_ui_payload(model: str, project_name: str, project: dict[str, Any]) -> dict[str, Any]:
    safe_project = json_safe(project)
    eq = safe_project.get("Equipment1", {})
    declarations = eq.get("Model_Declarations", {})
    params = eq.get("Model_Parameters", {})
    selected = declarations.get("Selected_OF", ["TAC_OF"])
    if isinstance(selected, list):
        selected_of = selected[0] if selected else "TAC_OF"
    else:
        selected_of = selected
    return {
        "name": normalize_project_name(project_name),
        "model": model,
        "project": safe_project,
        "parameters": params,
        "parameter_units": {},
        "geometric_standards": {},
        "discrete_values": declarations.get("Discrete_Values_of_Variables", []),
        "selected_of": selected_of,
        "number_of_equipment": safe_project.get("Number_of_Equipment", 1),
    }


def ui_payload_to_project(model: str, payload: dict[str, Any], var_order: list[str]) -> dict[str, Any]:
    params = dict(payload.get("parameters") or {})
    try:
        ref = load_project(model, "Example1", scope="examples")
        ref_params = json_safe(ref.get("Equipment1", {}).get("Model_Parameters", {}))
        ref_params.update(params)
        params = ref_params
    except Exception:
        pass
    selected_of = payload.get("selected_of") or params.pop("_selected_of", "TAC_OF")
    discrete = payload.get("discrete_variables") or {}
    discrete_values = []
    for var in var_order:
        vals = discrete.get(var, [])
        discrete_values.append(vals)
    return {
        "Number_of_Equipment": int(payload.get("number_of_equipment") or 1),
        "Equipment1": {
            "Model_Declarations": {
                "Type_Equipment": model,
                "Discrete_Values_of_Variables": discrete_values,
                "Selected_OF": [selected_of],
            },
            "Model_Parameters": params,
        },
    }
