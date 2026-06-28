# AGENTS.md — OptiProcess / OptiAppsCreator

## What this repo is

OptiProcess is a Python framework for heat exchanger design optimization using **Set Trimming** and **Enumeration** methods. `OptiAppsCreator/` is a sub-workspace that auto-generates web UIs from model directories (STHE implemented, others planned).

## Architecture

- **Root `Main.py`**: Entry point for running any model. Edit `Selected_Model` and `Selected_Example` at the top, then run it.
- **Model directory template** (e.g. `STHE/`, `Kettle/`, `GPHE/`):
  - `Examples_{Model}.py` — dictionaries with problem data and discrete variable options
  - `Model/Model_Def_{Model}.py` — solver configuration (Set Trimming mode, variables, constraint lists, OF definitions)
  - `Model/Parameters_Update_{Model}.py` — allocation and consistency check functions
  - `Model/Constraints_and_OF_{Model}.py` — constraint functions and objective functions
  - `Calculations/` — thermal-hydraulic model implementation modules
- **`OptiCode/`**: Shared optimization engine (dynamic imports, set trimming, enumeration, solvers).
- **`Common_Equations_HEX/`**: Shared LMTD, heat load, consistency checks.

### OptiAppsCreator web app (implemented)

The hybrid approach from `PLAN.md` is implemented for STHE and GPHE:

```
OptiAppsCreator/
├── common_ui.yaml                 ← Global UI metadata (header, login, available_models)
├── STHE/STHE_ui.yaml              ← Model-specific UI metadata (labels, units, layout)
├── GPHE/GPHE_ui.yaml              ← Model-specific UI metadata for GPHE
├── STHE/Projects/Default_Design.py← Developer-owned default design for new STHE designs
├── GPHE/Projects/Default_Design.py← Developer-owned default design for new GPHE designs
├── STHE/Model/Output_Info.py      ← Post-optimization calculations (STHE: 21 fields)
├── GPHE/Model/Output_Info.py      ← Post-optimization calculations (GPHE: 36 fields)
├── templates/                     ← Jinja2 HTML templates (5 files)
├── generate_ui.py                 ← HTML generator (reads common + model YAML → renders templates)
├── solver_runner.py               ← CLI solver (JSON in → JSON out, dynamic model imports)
├── solver_api.py                  ← FastAPI server (serves /ui/ + /api/optimize)
├── requirements.txt               ← Pinned dependencies
├── USER_MANUAL.md                 ← Full documentation
└── output/                        ← Generated HTML
    ├── login.html, main_menu.html ← Shared pages (generated once)
    ├── STHE/                      ← STHE model pages
    └── GPHE/                      ← GPHE model pages
```

**Launch:**
```bash
cd OptiAppsCreator
pip install -r requirements.txt
python generate_ui.py --all
uvicorn solver_api:app --host 127.0.0.1 --port 8000
# Open http://127.0.0.1:8000/ui/main_menu.html
```

**Data flow:** Browser form → sessionStorage → results.html JS → POST /api/optimize → solver_runner.py subprocess → returns JSON with optimal_variables + calculations (21 STHE / 36 GPHE fields).

### Projects / Designs architecture

`User Project` is a user-owned container. `Design` is the individual solvable case within a User Project. User Projects and Designs are persisted in SQLite (`user_projects`, `user_designs`) and Designs are stored as JSON payloads, not `.py` files.

Tutorials remain read-only legacy `.py` files under `{MODEL}/Projects/Example_Projects/` and are shown as **Design Tutorial Library**. `ExampleX.py` is displayed as `Tutorial X`.

Each model must have `{MODEL}/Projects/Default_Design.py`, exported as `Project = {...}` with the same project-file format. It is the source for UI defaults, `New Design`, and missing internal solver parameters. If it is missing, `project_store.ensure_default_design()` copies `{MODEL}/Projects/Example_Projects/Example1.py` as fallback. If both files are missing, generation/API calls fail with a clear `ProjectError` explaining which files are expected.

`generate_ui.py --example ...` is deprecated for defaults. The argument is still accepted for compatibility, but defaults now come from `Default_Design.py`.

Projects and Designs are server-owned data. Do not add UI flows to import/export individual Design `.py` files or local project directories. The supported local transfer mechanism is user backup/restore: `GET /api/user-backup` exports only the authenticated user's User Projects and Designs to JSON, and `POST /api/user-backup/restore` restores them under the authenticated user. Restore overwrites matching Project descriptions and matching Designs by default; IDs from backup files must not be trusted.

### Output_Info architecture (per-model)

Each model may have `Model/Output_Info.py` with `build_output_info(optimal_vars, params, objective)`. `solver_runner.py` imports it dynamically. If missing, `calculations` is `{}` (graceful fallback).

### OptiAppsCreator vs root

`OptiAppsCreator/` contains its own copies of `Main.py`, `OptiCode/`, `STHE/`, and `Common_Equations_HEX/`. It also has `ejemplos-interfaz-grafica-html-estatica/` (static HTML mockups, reference only) and `PLAN.md`. These copies are **not** symlinks — they are independent snapshots.

## Developer commands

```bash
cd OptiAppsCreator && python Main.py                    # Run STHE Example1 solver directly
cd OptiAppsCreator && python generate_ui.py             # Generate all HTML pages
cd OptiAppsCreator && uvicorn solver_api:app --port 8000 # Start API + UI server
```

There are no build/test/lint/typecheck commands configured. This is a pure Python research codebase. Dependencies are in `OptiAppsCreator/requirements.txt`.

## Gotchas

### Web UI: always use server URL, not file://
The browser blocks `fetch` from `file://` to `http://`. Always open `http://127.0.0.1:8000/ui/main_menu.html`. The solver_api serves static files at `/ui/`.

### Form data collection: data-key attributes
All form inputs use `data-key` attributes. The JS collectors read `input[data-key]` and `select[data-key]`. Do NOT rely on label text matching — use `data-key`. Numeric text inputs are filtered client-side with `data-numeric="true"`; backend validation in `solver_api.py` also rejects non-numeric parameter strings except known text parameters (`Shell_Method`, `Tube_Method`, `yfluid`, `_selected_of`).

### Flow Limits are editable numeric inputs
`limit_table` rows in Problem Data render editable numeric inputs for lower/upper bounds (for example `vtmin`, `vtmax`, `LBLD`, `UBLD`). These values are submitted like any other `data-key` input.

### Geometric options: data-var attributes
Checkbox grids use `data-var` attributes to identify which variable they belong to. The `saveAndOptimize()` JS iterates `[data-var]` panels. The generator must include `variable` in the resolved section context for each checkbox_grid.

### Cross-page scalar synchronization is YAML-driven
Do not hardcode model-specific scalar keys in shared JS. Use `{MODEL}_ui.yaml → model.sync_scalar_keys` for duplicated scalar fields that must stay synchronized between Problem Data and Geometric Options. Current setup: STHE syncs `LBLD`/`UBLD`; GPHE has `sync_scalar_keys: []`.

Geometric scalar form fields are discovered from `pages.geometric_options.sections[*].fields` and passed as `GEOMETRIC_SCALAR_KEYS` so loaded projects can populate Geometric Options without STHE-specific hardcoding.

### Pydantic drops extra fields
The `OptimizationResponse` model must have `model_config = {"extra": "allow"}` or explicitly declare all response fields (including `calculations`). Without this, the `calculations` key is silently removed from API responses.

### Intermediate calculations
`solver_runner.py` dynamically imports `{Model}/Model/Output_Info.py` to compute thermo/hydraulic/economics derived values post-optimization. Each model's `Output_Info.py` must export `build_output_info(optimal_vars, params, objective)`. If the file is missing, `calculations` is returned as `{}` (graceful fallback). STHE has 21 calc fields; GPHE has 36.

### `except NameError or KeyError:` is broken Python
In both `Main.py` files (root and OptiAppsCreator), lines like:
```python
except NameError or KeyError:
```
This evaluates as `except NameError:`. Use `except (NameError, KeyError):`.

### Dynamic imports require correct `sys.path`
`Main.py` appends `../` to `sys.path`. Always run scripts from their own directory.

### `.gitignore` typo in OptiAppsCreator
`OptiAppsCreator/.gitignore` has `*__pycache__/*` — double underscore. The root `.gitignore` is correct.

### Model directory naming convention
Each model must have a Python-package-compatible directory name. Must contain `__init__.py` at both the model root and `Model/` subdirectory levels.

### `Model_Def` naming convention for imports
`Import_Models.py` constructs the imported variable name as `Model_{model}` (e.g. `Model_STHE`). The `Model_Def_{Model}.py` file **must** export a variable with exactly that name.

### Results files are written to the model directory
`Main.py` creates `Results_{Model}_{Example}.txt` inside the model folder. These are git-tracked in this repo.

### Port 8000 cleanup
Lingering uvicorn processes from tests: `pkill -f uvicorn`

## Branch policy
Per `README.md`: don't work in `Development` or `main` branches.
