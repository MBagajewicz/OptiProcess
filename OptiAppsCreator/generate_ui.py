#!/usr/bin/env python3
"""generate_ui.py — Generates static HTML pages from model data + YAML UI metadata.

Reads:  Model_Def_{Model}.py  → structural metadata (variables, constraints, standard values)
        {Model}/Projects/*.py → project defaults (parameter values, discrete selections)
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

from project_store import load_project


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

RS_COLORS = {
    "green_display": {"border": "border-[6px] border-[#b5d5c5]", "bg": "bg-[#dcf0e3]", "title": "text-red-500"},
    "blue_display": {"border": "border-[6px] border-[#a5cbf0]", "bg": "bg-[#dbeafe]", "title": "text-gray-800"},
    "yellow_display": {"border": "border-[6px] border-[#fce4a1]", "bg": "bg-[#fef9c3]", "title": "text-gray-800"},
    "red_display": {"border": "border-[6px] border-[#f0a8a8]", "bg": "bg-[#fee2e2]", "title": "text-gray-800"},
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


def load_project_defaults(model_name, project_name):
    """Load a project dict from {Model}/Projects/{Project}.py."""
    return load_project(model_name, project_name, scope="examples")


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
            opts = section.get("options")
            if not opts:
                raise ValueError(f"radio_group section '{section_id}' has no 'options' list in YAML")
            for opt in opts:
                options.append({
                    "value": opt["value"],
                    "label": opt["label"],
                    "checked": opt["value"] == defaults if isinstance(defaults, str) else opt["value"] == defaults[0],
                })
            resolved["options"] = options
            resolved["source_key"] = source_key
            resolved["width_class"] = "w-56"
            resolved["color"] = {}  # radio groups use hardcoded classes in template

        elif element == "form_group":
            resolved["color"] = PD_COLORS.get(color, PD_COLORS["gray"])
            resolved["width_class"] = "w-56" if color in ("red", "blue") else "w-72" if color == "green" else "w-64"
            fields = []
            for key, field_meta in section.get("fields", {}).items():
                try:
                    default_val = get_example_default(example, f"{source}.{key}")
                    # Use YAML default as fallback when not in the example
                    if isinstance(default_val, str) and default_val == "" and "default" in field_meta:
                        default_val = field_meta["default"]
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
                    "lower_key": lower_key,
                    "upper_key": upper_key,
                })
            resolved["rows"] = rows

        elif element == "computed_display":
            resolved["color"] = PD_COLORS.get("pink")
            resolved["width_class"] = "w-56"
            resolved["rows"] = section.get("rows", [])

        sections_out.append(resolved)

    return sections_out


def build_geometric_options_context(yaml_data, model_def, example, sort_numeric=True):
    """Build resolved context for the geometric_options page.
    
    sort_numeric: if True, sort purely-numeric option lists before rendering checkbox grids.
    """
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
            resolved["width_class"] = "w-44"
            resolved["variable"] = section.get("variable", "")
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
                    # Sort purely-numeric lists when the flag is enabled
                    if (sort_numeric and isinstance(options, list)
                            and options
                            and all(isinstance(v, (int, float)) and not isinstance(v, bool) for v in options)):
                        options = sorted(options)
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
            resolved["width_class"] = "w-56"
            source = section.get("source", "Model_Parameters")
            fields = []
            for key, field_meta in section.get("fields", {}).items():
                default_val = get_example_default(example, f"{source}.{key}")
                # Use YAML default as fallback when not in the example
                if isinstance(default_val, str) and default_val == "" and "default" in field_meta:
                    default_val = field_meta["default"]
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


_WC_MAP = {"w-44": 44, "w-56": 56, "w-64": 64, "w-72": 72}


def _width_value(width_class):
    return _WC_MAP.get(width_class, 0)


def uniformize_column_widths(columns):
    """Make all sections in each column share the widest width_class in that column."""
    for col in columns:
        if not col:
            continue
        max_w = max((_width_value(s.get("width_class", "")) for s in col), default=0)
        if max_w > 0:
            classname = f"w-{max_w}"
            for s in col:
                s["width_class"] = classname
    return columns


def build_results_context(yaml_data, model_def):
    """Build resolved context for the results page (structure + metadata, values come from JS)."""
    page_yaml = yaml_data["pages"]["results"]
    sections_out = []
    all_rows_flat = []

    for section_id, section in page_yaml["sections"].items():
        color = section.get("color", "blue_display")
        resolved = {
            "id": section_id,
            "element": section.get("element", "data_table"),
            "title": section.get("title", ""),
            "color": RS_COLORS.get(color, RS_COLORS["blue_display"]),
            "full_height": section_id == "unit_geometry",
        }

        # Handle subsections (thermo_properties, optimization_results)
        if section.get("subsections"):
            resolved["subsections"] = []
            for sub in section["subsections"]:
                sub_rows = []
                for row in sub.get("rows", []):
                    sub_rows.append({
                        "label": row["label"],
                        "key": row["key"],
                        "unit": row.get("unit", ""),
                        "highlight": row.get("highlight", False),
                    })
                resolved["subsections"].append({"title": sub.get("title", ""), "rows": sub_rows})
                all_rows_flat.extend([r["key"] for r in sub_rows])

        if section.get("rows"):
            resolved["rows"] = []
            for row in section["rows"]:
                resolved["rows"].append({
                    "label": row["label"],
                    "key": row["key"],
                    "unit": row.get("unit", ""),
                    "highlight": row.get("highlight", False),
                    "display_factor": row.get("display_factor", 1),
                })
                all_rows_flat.append(row["key"])

        if section.get("footer_rows"):
            resolved["footer_rows"] = []
            for row in section["footer_rows"]:
                resolved["footer_rows"].append({
                    "label": row["label"],
                    "key": row["key"],
                    "unit": row.get("unit", ""),
                })
                all_rows_flat.append(row["key"])

        sections_out.append(resolved)

    return sections_out, all_rows_flat


def flatten_section_rows(sections):
    """Extract all rows with their display metadata for JS data mapping."""
    flat = []
    for s in sections:
        for r in s.get("rows", []):
            flat.append(r)
        for sub in s.get("subsections", []):
            for r in sub.get("rows", []):
                flat.append(r)
        for r in s.get("footer_rows", []):
            flat.append(r)
    return flat


def build_results_js_context(yaml_data):
    """Build dynamic JS variables for the results page: result_var_keys, value_labels, var_units."""
    results = yaml_data["pages"]["results"]
    geo = yaml_data["pages"]["geometric_options"]

    # Collect all result_var keys from results page
    var_keys = []
    var_units = {}
    for section in results["sections"].values():
        for row in section.get("rows", []):
            if row.get("result_var"):
                var_keys.append(row["key"])
                if row.get("unit"):
                    var_units[row["key"]] = row["unit"]

    # Collect value labels from geometric_options sections
    var_labels = {}
    for section in geo["sections"].values():
        var_name = section.get("variable", "")
        if var_name and section.get("value_labels"):
            var_labels[var_name] = section["value_labels"]

    return var_keys, var_labels, var_units


def generate():
    parser = argparse.ArgumentParser(description="Generate HTML UI pages from model data + YAML")
    parser.add_argument(
        "--model", nargs="*", default=["STHE"],
        help="Model names to generate (default: STHE). Ignored when --all is passed.",
    )
    parser.add_argument(
        "--all", action="store_true",
        help="Generate pages for every active model listed in common_ui.yaml",
    )
    parser.add_argument("--example", default="Example1", help="Project name for defaults (default: Example1)")
    parser.add_argument("--output", default="output", help="Output directory (default: output)")
    parser.add_argument(
        "--no-sort-numeric-options",
        action="store_false",
        dest="sort_numeric_options",
        default=True,
        help="Disable automatic sorting of numeric geometric option lists in the UI (enabled by default)",
    )
    args = parser.parse_args()

    setup_path()

    script_dir = os.path.dirname(os.path.abspath(__file__))

    # Load common UI metadata (header, login, available_models)
    common_yaml_path = os.path.join(script_dir, "common_ui.yaml")
    with open(common_yaml_path, "r", encoding="utf-8") as f:
        common_ui = yaml.safe_load(f)

    # Determine which models to generate
    if args.all:
        model_list = [m["id"] for m in common_ui.get("available_models", []) if m.get("active")]
        if not model_list:
            print("No active models found in common_ui.yaml. Nothing to generate.")
            return
    else:
        model_list = args.model

    # Set up Jinja2 (shared across all models)
    template_dir = os.path.join(script_dir, "templates")
    env = Environment(
        loader=FileSystemLoader(template_dir),
        autoescape=select_autoescape(["html"]),
    )
    env.globals.update(zip=zip)

    output_dir = Path(args.output)
    output_dir.mkdir(parents=True, exist_ok=True)

    # Common header for all pages
    header_data = common_ui.get("header", {
        "title": "OptiHexx",
        "subtitle": "Heat Exchanger Optimal Design Suite",
        "prototype": "Prototype P07",
    })

    nav_pages = [
        {"label": "Problem Data", "file": "problem_data.html"},
        {"label": "Geometric Options", "file": "geometric_options.html"},
        {"label": "Results", "file": "results.html"},
        {"label": "Projects", "file": "projects.html"},
    ]

    # --- Login page (once, in output/) ---
    login_context = {
        "header": header_data,
        "login": common_ui.get("login", {"default_user": "|"}),
    }
    template = env.get_template("login.html")
    html = template.render(**login_context)
    (output_dir / "login.html").write_text(html, encoding="utf-8")
    print(f"  ✓ output/login.html")

    # --- Main Menu page (once, in output/) ---
    models_raw = common_ui.get("available_models", [])
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

    # --- Model-specific pages (each model in output/{model}/) ---
    for model_name in model_list:
        model_yaml_path = os.path.join(script_dir, model_name, f"{model_name}_ui.yaml")
        with open(model_yaml_path, "r", encoding="utf-8") as f:
            model_ui = yaml.safe_load(f)

        model_def = load_model_def(model_name)
        example = load_project_defaults(model_name, args.example)

        model_output_dir = output_dir / model_name
        model_output_dir.mkdir(parents=True, exist_ok=True)

        # Problem Data page
        nav_pd = [{"label": p["label"], "active": p["file"] == "problem_data.html", "file": p["file"]} for p in nav_pages]
        pd_sections = build_problem_data_context(model_ui, model_def, example)
        pd_columns = build_column_layout(pd_sections, model_ui["pages"]["problem_data"]["columns"])
        pd_columns = uniformize_column_widths(pd_columns)

        template = env.get_template("problem_data.html")
        html = template.render(
            page_title="Problem Data",
            nav_pages=nav_pd,
            columns=pd_columns,
            all_sections=pd_sections,
            header=header_data,
            model_name=model_name,
        )
        (model_output_dir / "problem_data.html").write_text(html, encoding="utf-8")
        print(f"  ✓ output/{model_name}/problem_data.html")

        # Geometric Options page
        nav_go = [{"label": p["label"], "active": p["file"] == "geometric_options.html", "file": p["file"]} for p in nav_pages]
        go_sections = build_geometric_options_context(model_ui, model_def, example, args.sort_numeric_options)
        go_columns = build_column_layout(go_sections, model_ui["pages"]["geometric_options"]["columns"])
        go_columns = uniformize_column_widths(go_columns)

        template = env.get_template("geometric_options.html")
        html = template.render(
            page_title="Geometric Options",
            nav_pages=nav_go,
            columns=go_columns,
            all_sections=go_sections,
            header=header_data,
            model_name=model_name,
        )
        (model_output_dir / "geometric_options.html").write_text(html, encoding="utf-8")
        print(f"  ✓ output/{model_name}/geometric_options.html")

        # Results page
        nav_rs = [{"label": p["label"], "active": p["file"] == "results.html", "file": p["file"]} for p in nav_pages]
        rs_sections, rs_keys = build_results_context(model_ui, model_def)
        rs_columns = build_column_layout(rs_sections, model_ui["pages"]["results"]["columns"])
        rs_all_rows = flatten_section_rows(rs_sections)
        rs_var_keys, rs_var_labels, rs_var_units = build_results_js_context(model_ui)

        template = env.get_template("results.html")
        html = template.render(
            page_title="Results",
            nav_pages=nav_rs,
            columns=rs_columns,
            header=header_data,
            model_name=model_name,
            all_sections=rs_sections,
            zip=zip,
            var_keys=rs_var_keys,
            var_labels=rs_var_labels,
            var_units=rs_var_units,
        )
        (model_output_dir / "results.html").write_text(html, encoding="utf-8")
        print(f"  ✓ output/{model_name}/results.html")

        # Projects page
        nav_pr = [{"label": p["label"], "active": p["file"] == "projects.html", "file": p["file"]} for p in nav_pages]
        template = env.get_template("projects.html")
        html = template.render(
            page_title="Projects",
            nav_pages=nav_pr,
            header=header_data,
            model_name=model_name,
        )
        (model_output_dir / "projects.html").write_text(html, encoding="utf-8")
        print(f"  ✓ output/{model_name}/projects.html")




if __name__ == "__main__":
    generate()
