#!/usr/bin/env python3
"""generate_ui.py — Generates static HTML pages from model data + YAML UI metadata.

Reads:  Model_Def_{Model}.py  → structural metadata (variables, constraints, standard values)
        Examples_{Model}.py   → instance defaults (parameter values, discrete selections)
        {Model}_ui.yaml       → UI presentation metadata (labels, groupings, input types)

Output: output/{page}.html — rendered HTML pages using Jinja2 templates.
"""

import os
import sys
import importlib
import argparse
from pathlib import Path

import yaml
from jinja2 import Environment, FileSystemLoader, select_autoescape


# --- Color CSS class maps ---

PD_COLORS = {
    "red": {
        "bg": "bg-red-50/90", "border": "border-red-200",
        "title": "text-red-600", "label": "text-red-500", "input": "text-red-600",
    },
    "blue": {
        "bg": "bg-blue-50/90", "border": "border-blue-200",
        "title": "text-blue-600", "label": "text-blue-500", "input": "text-blue-600",
    },
    "yellow": {
        "bg": "bg-yellow-100/90", "border": "border-yellow-300",
        "title": "text-yellow-800", "label": "text-yellow-800", "input": "text-gray-800",
    },
    "gray": {
        "bg": "bg-gray-100/90", "border": "border-gray-300",
        "title": "text-gray-600", "label": "text-gray-600", "input": "text-gray-800",
    },
    "green": {
        "bg": "bg-green-50/90", "border": "border-green-200",
        "title": "text-green-600", "label": "text-green-600", "input": "text-green-600",
    },
    "pink": {
        "bg": "bg-pink-50/80", "border": "border-pink-200",
        "title": "text-gray-500", "label": "text-gray-500", "input": "text-gray-400",
    },
}

GO_COLORS = {
    "brown": {"panel": "bg-[#7a635a]", "text": "text-white"},
    "blue": {"panel": "bg-[#3b9df5]", "text": "text-white"},
    "yellow": {"panel": "bg-[#fbbd08]", "text": "text-black", "text_class": "!text-black"},
    "brown_dark": {"panel": "bg-[#3d2b24]", "text": "text-white"},
    "red_dark": {"panel": "bg-[#b91c1c]", "text": "text-white"},
    "green": {"panel": "bg-[#4caf50]", "text": "text-white"},
}


def setup_path():
    """Add OptiAppsCreator to sys.path so STHE/ modules are importable."""
    base_dir = os.path.dirname(os.path.abspath(__file__))
    if base_dir not in sys.path:
        sys.path.insert(0, base_dir)


def load_model_def(model_name):
    """Import Model_Def_{Model} and return the Model_{Model} dict."""
    module_path = f"{model_name}.Model.Model_Def_{model_name}"
    module = importlib.import_module(module_path)
    var_name = f"Model_{model_name}"
    return getattr(module, var_name)


def load_examples(model_name, example_name):
    """Import Examples_{Model} and return the Example dict."""
    module_path = f"{model_name}.Examples_{model_name}"
    module = importlib.import_module(module_path)
    return getattr(module, example_name)


def get_example_default(example, key_path, equipment=1):
    """Navigate the Example dict to get a default value.

    key_path examples:
        "Model_Parameters.Thi" → Equipment1.Model_Parameters.Thi
        "Model_Declarations.Selected_OF" → Equipment1.Model_Declarations.Selected_OF
    """
    eq = example[f"Equipment{equipment}"]
    parts = key_path.split(".", 1)
    if len(parts) == 2:
        section, key = parts
        return eq.get(section, {}).get(key, "")
    return ""


def build_problem_data_context(yaml_data, model_def, example):
    """Build resolved context for the problem_data page."""
    page_yaml = yaml_data["pages"]["problem_data"]
    sections_out = []

    for section_id, section in page_yaml["sections"].items():
        element = section.get("element", "form_group")
        title = section.get("title", "")
        color = section.get("color", "gray")
        source = section.get("source", "Model_Parameters")

        resolved = {"id": section_id, "element": element, "title": title}

        if element == "radio_group":
            source_key = section["source_key"]
            defaults = get_example_default(example, f"{source}.{source_key}")
            options = []
            if "options" in section:
                for opt in section["options"]:
                    options.append({
                        "value": opt["value"],
                        "label": opt["label"],
                        "checked": opt["value"] == defaults if isinstance(defaults, str) else opt["value"] == defaults[0],
                    })
            elif "option_labels" in section:
                # Options come from Model_Def objective function list
                of_data = model_def.get("Model_Info", {}).get("Objective_Function", {})
                eq_names = of_data.get("Equation_Name", [])
                labels = section.get("option_labels", {})
                for name in eq_names:
                    label = labels.get(name, name)
                    selected = defaults and defaults[0] == name
                    options.append({"value": name, "label": label, "checked": selected})
            resolved["options"] = options
            resolved["source_key"] = source_key
            resolved["color"] = {}  # radio groups use hardcoded classes in template

        elif element == "form_group":
            resolved["color"] = PD_COLORS.get(color, PD_COLORS["gray"])
            resolved["width_class"] = "w-56" if color in ("red", "blue") else "w-72" if color == "green" else "w-64"
            fields = []
            for key, field_meta in section.get("fields", {}).items():
                try:
                    default_val = get_example_default(example, f"{source}.{key}")
                    # Apply display conversions (e.g., int_rate stored as 0.1, displayed as 10%)
                    display_factor = field_meta.get("display_factor")
                    if display_factor is not None and isinstance(default_val, (int, float)):
                        default_val = default_val * float(display_factor)
                except Exception as e:
                    print(f"  ERROR section={section_id} source={source} key={key}: {e}")
                    raise
                field = {
                    "key": key,
                    "label": field_meta.get("label", key),
                    "unit": field_meta.get("unit"),
                    "default": default_val,
                    "element": field_meta.get("element", "text_input"),
                    "computed_hint": field_meta.get("computed_hint", False),
                    "options": field_meta.get("options"),
                }
                fields.append(field)
            resolved["fields"] = fields

        elif element == "limit_table":
            resolved["color"] = {}
            resolved["width_class"] = "w-64"
            rows = []
            for row in section.get("rows", []):
                lower_key = row["lower"]
                upper_key = row["upper"]
                lower_val = get_example_default(example, f"{source}.{lower_key}")
                upper_val = get_example_default(example, f"{source}.{upper_key}")
                rows.append({
                    "item": row["item"],
                    "unit": row.get("unit"),
                    "lower": lower_val,
                    "upper": upper_val,
                })
            resolved["rows"] = rows

        elif element == "computed_display":
            resolved["color"] = PD_COLORS.get("pink")
            resolved["rows"] = section.get("rows", [])

        sections_out.append(resolved)

    return sections_out


def build_geometric_options_context(yaml_data, model_def, example):
    """Build resolved context for the geometric_options page."""
    page_yaml = yaml_data["pages"]["geometric_options"]
    sections_out = []

    # Get variable definitions from Model_Def
    list_of_vars = model_def["Model_Info"]["List_of_Variables"]
    std_values = model_def["Model_Info"]["Standard_Variables_Values"]
    discrete_vals = example["Equipment1"]["Model_Declarations"]["Discrete_Values_of_Variables"]

    # Build a lookup: variable_name → (index, selected_values)
    var_selection = {}
    for idx, var_name in enumerate(list_of_vars):
        var_selection[var_name] = {
            "index": idx,
            "selected": discrete_vals[idx] if idx < len(discrete_vals) else [],
            "standard": std_values.get(var_name, []),
        }

    for section_id, section in page_yaml["sections"].items():
        element = section.get("element", "checkbox_grid")
        title = section.get("title", "")
        color = section.get("color", "brown")
        resolved = {"id": section_id, "element": element, "title": title}

        if element == "checkbox_grid":
            go_color = GO_COLORS.get(color, GO_COLORS["brown"])
            resolved["color"] = go_color
            # Handle title with line breaks for narrow columns
            resolved["title_nobreak"] = title.replace(" ", "&nbsp;")

            if section.get("static"):
                items = []
                for item in section.get("items", []):
                    items.append({
                        "label": str(item.get("label", item["value"])),
                        "value": item["value"],
                        "checked": True,  # Static items default to checked
                    })
                resolved["grid_items"] = items
            else:
                var_name = section.get("variable")
                if var_name and var_name in var_selection:
                    var_info = var_selection[var_name]
                    label_map = section.get("value_labels", {})
                    items = []
                    # Use standard values as the full option list
                    options = var_info["standard"]
                    selected_set = set(var_info["selected"])
                    for val in options:
                        label = label_map.get(val, str(val))
                        items.append({
                            "label": label,
                            "value": val,
                            "checked": val in selected_set,
                        })
                resolved["grid_items"] = items

        elif element == "form_group":
            go_color = GO_COLORS.get(color, GO_COLORS["brown_dark"])
            resolved["color"] = go_color
            source = section.get("source", "Model_Parameters")
            fields = []
            for key, field_meta in section.get("fields", {}).items():
                default_val = get_example_default(example, f"{source}.{key}")
                fields.append({
                    "key": key,
                    "label": field_meta.get("label", key),
                    "unit": field_meta.get("unit"),
                    "default": default_val,
                })
            resolved["fields"] = fields

        sections_out.append(resolved)

    return sections_out


def build_column_layout(sections, columns_spec):
    """Arrange resolved sections into columns based on the YAML column spec."""
    section_map = {s["id"]: s for s in sections}
    columns = []
    for col_spec in columns_spec:
        col_sections = []
        for sid in col_spec:
            if sid in section_map:
                col_sections.append(section_map[sid])
        if col_sections:
            columns.append(col_sections)
    return columns


def generate():
    parser = argparse.ArgumentParser(description="Generate HTML UI pages from model data + YAML")
    parser.add_argument("--model", default="STHE", help="Model name (default: STHE)")
    parser.add_argument("--example", default="Example1", help="Example name for defaults (default: Example1)")
    parser.add_argument("--output", default="output", help="Output directory (default: output)")
    args = parser.parse_args()

    setup_path()

    # Load data sources
    yaml_path = os.path.join(args.model, f"{args.model}_ui.yaml")
    with open(yaml_path, "r", encoding="utf-8") as f:
        yaml_data = yaml.safe_load(f)

    model_def = load_model_def(args.model)
    example = load_examples(args.model, args.example)

    # Set up Jinja2
    template_dir = os.path.join(os.path.dirname(__file__), "templates")
    env = Environment(
        loader=FileSystemLoader(template_dir),
        autoescape=select_autoescape(["html"]),
    )
    env.globals.update(zip=zip)  # needed for some template patterns

    output_dir = Path(args.output)
    output_dir.mkdir(parents=True, exist_ok=True)

    nav_pages = [
        {"label": "Problem Data", "file": "problem_data.html"},
        {"label": "Geometric Options", "file": "geometric_options.html"},
        {"label": "Results", "file": "results.html"},
    ]

    # --- Login page ---
    header_data = yaml_data.get("header", {
        "title": "OptiHexx",
        "subtitle": "Heat Exchanger Optimal Design Suite",
        "prototype": "Prototype P07",
    })
    login_context = {
        "header": header_data,
        "login": {"default_user": "|"},
    }
    template = env.get_template("login.html")
    html = template.render(**login_context)
    (output_dir / "login.html").write_text(html, encoding="utf-8")
    print(f"  ✓ output/login.html")

    # --- Main Menu page ---
    models_raw = yaml_data.get("available_models", [])
    models = []
    for m in models_raw:
        if m.get("active"):
            css = "bg-white text-[#4a6fa5]"
        else:
            css = "bg-[#a8c9a8] text-[#4a6fa5] opacity-60 cursor-not-allowed"
        models.append({
            "label": m["label"],
            "link": m.get("link", "#"),
            "css": css,
            "active": m.get("active", False),
        })
    menu_context = {
        "header": header_data,
        "models": models,
    }
    template = env.get_template("main_menu.html")
    html = template.render(**menu_context)
    (output_dir / "main_menu.html").write_text(html, encoding="utf-8")
    print(f"  ✓ output/main_menu.html")

    # --- Problem Data page ---
    nav_pd = [{"label": p["label"], "active": p["file"] == "problem_data.html"} for p in nav_pages]
    pd_sections = build_problem_data_context(yaml_data, model_def, example)
    pd_columns = build_column_layout(pd_sections, yaml_data["pages"]["problem_data"]["columns"])

    template = env.get_template("problem_data.html")
    html = template.render(
        page_title="Problem Data",
        nav_pages=nav_pd,
        columns=pd_columns,
    )
    (output_dir / "problem_data.html").write_text(html, encoding="utf-8")
    print(f"  ✓ output/problem_data.html")

    # --- Geometric Options page ---
    nav_go = [{"label": p["label"], "active": p["file"] == "geometric_options.html"} for p in nav_pages]
    go_sections = build_geometric_options_context(yaml_data, model_def, example)
    go_columns = build_column_layout(go_sections, yaml_data["pages"]["geometric_options"]["columns"])

    template = env.get_template("geometric_options.html")
    html = template.render(
        page_title="Geometric Options",
        nav_pages=nav_go,
        columns=go_columns,
    )
    (output_dir / "geometric_options.html").write_text(html, encoding="utf-8")
    print(f"  ✓ output/geometric_options.html")

    print(f"\nDone. Generated {args.model} UI for example '{args.example}' in '{output_dir}/'")


if __name__ == "__main__":
    generate()
