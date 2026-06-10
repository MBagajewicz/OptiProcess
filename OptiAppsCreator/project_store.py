#!/usr/bin/env python3
"""Project storage helpers for OptiAppsCreator.

Projects are Python files stored under {MODEL}/Projects/{ProjectName}.py and
must export a single variable named Project. The loader validates the AST before
execution and only allows data-oriented expressions used by project files.
"""

from __future__ import annotations

import ast
import copy
import pprint
import re
from pathlib import Path
from typing import Any

import numpy as np


SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_NAME_RE = re.compile(r"^[A-Za-z0-9_-]+$")
MODEL_NAME_RE = re.compile(r"^[A-Za-z0-9_]+$")


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


def projects_dir(model: str) -> Path:
    model = validate_model_name(model)
    path = SCRIPT_DIR / model / "Projects"
    path.mkdir(parents=True, exist_ok=True)
    return path


def project_path(model: str, project_name: str) -> Path:
    base = projects_dir(model).resolve()
    name = normalize_project_name(project_name)
    path = (base / f"{name}.py").resolve()
    if base != path.parent:
        raise ProjectError("Project path escapes Projects directory")
    return path


def list_projects(model: str) -> list[dict[str, Any]]:
    base = projects_dir(model)
    projects = []
    for path in sorted(base.glob("*.py"), key=lambda p: p.name.lower()):
        if path.name == "__init__.py":
            continue
        projects.append({"name": path.stem, "file": path.name})
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


def load_project(model: str, project_name: str) -> dict[str, Any]:
    path = project_path(model, project_name)
    if not path.exists():
        raise ProjectError(f"Project not found: {project_name}")
    return load_project_source(model, project_name, path.read_text(encoding="utf-8"))


def save_project(model: str, project_name: str, project: dict[str, Any]) -> Path:
    path = project_path(model, project_name)
    project_copy = json_safe(copy.deepcopy(project))
    text = "import numpy as np\n\nProject = " + pprint.pformat(project_copy, width=120, sort_dicts=False) + "\n"
    path.write_text(text, encoding="utf-8")
    return path


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
        "discrete_values": declarations.get("Discrete_Values_of_Variables", []),
        "selected_of": selected_of,
        "number_of_equipment": safe_project.get("Number_of_Equipment", 1),
    }


def ui_payload_to_project(model: str, payload: dict[str, Any], var_order: list[str]) -> dict[str, Any]:
    params = dict(payload.get("parameters") or {})
    try:
        ref = load_project(model, "Example1")
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
