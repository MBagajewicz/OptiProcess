# USER MANUAL — OptiHexx / OptiAppsCreator

**OptiHexx** is a web application for Shell & Tube Heat Exchanger design optimization. It uses **Set Trimming** and **Smart Enumeration** to guarantee global optimality. The UI is auto-generated from Python model definitions + a lightweight YAML metadata file.

---

## 1. Architecture

```
OptiAppsCreator/
├── STHE/                          ← Model directory (one per heat exchanger type)
│   ├── STHE_ui.yaml               ← UI presentation metadata (labels, groups, layout)
│   ├── Examples_STHE.py           ← Problem instances (Example1..Example13)
│   ├── Model/
│   │   ├── Model_Def_STHE.py      ← Structural metadata (variables, constraints, OF)
│   │   ├── Parameters_Update_STHE.py
│   │   └── Constraints_and_OF_STHE.py
│   └── Calculations/              ← Thermal-hydraulic model
├── OptiCode/                      ← Shared optimization engine
├── Common_Equations_HEX/          ← Shared LMTD, heat load
├── templates/                     ← Jinja2 HTML templates
│   ├── base.html                  ← Shared header, nav, Tailwind CDN
│   ├── login.html
│   ├── main_menu.html
│   ├── problem_data.html
│   ├── geometric_options.html
│   └── results.html
├── generate_ui.py                 ← HTML generator (reads YAML + .py → renders templates)
├── solver_runner.py               ← CLI solver runner (JSON in → JSON out)
├── solver_api.py                  ← FastAPI REST server (POST /api/optimize)
└── output/                        ← Generated HTML files (5 pages)
```

**Data flow for UI generation:**

```
Model_Def_STHE.py ──┐
Examples_STHE.py  ──┼──► generate_ui.py ──► output/*.html
STHE_ui.yaml ───────┘
```

**Data flow at runtime:**

```
Browser (problem_data.html)
    │ sessionStorage
    ▼
Browser (geometric_options.html)
    │ sessionStorage
    ▼
Browser (results.html) ──► POST /api/optimize ──► solver_runner.py ──► Main.py pipeline ──► JSON results
```

---

## 2. Prerequisites

| Dependency | Purpose |
|-----------|---------|
| Python ≥ 3.10 | Runtime |
| numpy, scipy | Solver engine |
| pyyaml | YAML parsing |
| jinja2 | HTML template rendering |
| fastapi, uvicorn | API server (only for runtime) |
| Tailwind CSS | Loaded from CDN (no install needed) |

Install everything:

```bash
pip install numpy scipy pyyaml jinja2 fastapi uvicorn
```

---

## 3. Quick Start

### 3.1 Install dependencies

```bash
pip install -r requirements.txt
```

### 3.2 Generate the UI pages

```bash
cd OptiAppsCreator
python generate_ui.py --model STHE --example Example1
```

This produces 5 files in `output/`:

```
output/login.html
output/main_menu.html
output/problem_data.html       ← pre-filled with Example1 defaults
output/geometric_options.html  ← pre-checked with Example1 discrete values
output/results.html            ← empty tables, populated at runtime by JS
```

### 3.3 Start the server

```bash
cd OptiAppsCreator
uvicorn solver_api:app --host 127.0.0.1 --port 8000
```

A single process serves:
- **Web UI** at `/ui/` (static HTML, CSS, JS)
- **REST API** at `/api/` (POST /api/optimize)

### 3.4 Open the application

Open **http://127.0.0.1:8000/ui/main_menu.html** in your browser.

> **Do not** open the `.html` files directly from disk (`file://`). The browser blocks cross-origin `fetch` calls to `http://127.0.0.1:8000`. Always use the server URL.

### 3.5 User flow

1. **Main Menu** → click **Shell & Tube**
2. **Problem Data** → review/edit pre-filled parameters → click **Next: Geometric Options →**
3. **Geometric Options** → check/uncheck discrete variable ranges → click **Run Optimization →**
4. **Results** → page auto-calls the API and populates all tables (streams, geometry, thermo, pressure, economics)
5. Click **Download Results** to save as `.txt`

---

## 4. User Flow (Browser)

### Page 1: Login
Credits and branding. Login form is decorative (no backend auth).

### Page 2: Main Menu
Select an equipment type. Only **Shell & Tube** is active; others are greyed out.

### Page 3: Problem Data
Fill in process conditions and economic parameters. Sections:

| Panel | Fields |
|-------|--------|
| **OPTIMIZATION TARGET** | Radio: TAC / CAPEX / AREA |
| **FLUID ALLOCATION** | Radio: Autoselect / Cold in Tubes / Hot in Tubes |
| **HOT STREAM** | 9 fields: temps, flow, density, Cp, viscosity, k, fouling, ΔP |
| **COLD STREAM** | 9 fields (same structure) |
| **FLOW LIMITS** | Table: tube/shell velocity, Reynolds, L/D bounds |
| **LMTD SETTINGS** | Xp limit, F min |
| **OTHER OPTIONS** | Excess area, pump efficiency, shell method, tube method |
| **ECONOMIC PARAMETERS** | Amortization, energy cost, hours/year, interest, cost params |

Click **Next: Geometric Options →** to save data and proceed.

### Page 4: Geometric Options
Select which discrete design values the optimizer may consider. Each panel is a checkbox grid:

| Panel | Variable | Source |
|-------|----------|--------|
| Configurations Available | — (static UI) | Series/Parallel combos |
| Number of Shells Available | — (static UI) | 1–8 |
| Number of Tube Passes | Npt | Standard_Variables_Values |
| Layouts Available | lay | 1=Square, 2=Triangle, 3=Rotated Square |
| Pitch Ratio | rp | 1.25, 1.33, 1.50 |
| Shell Diameter [m] | Ds | TEMA standard list |
| Outer Tube Diameter [m] | dte | BWG sizes |
| Tube Length [m] | L | Standard lengths |
| Baffle cut | Bc | 0.15–0.45 |
| Tube Options | ktube, thk, LBLD, UBLD | Text inputs |
| Number of Baffles | Nb | 1–20 |
| Bell Method Parameters | Nss, plbmax1, plbmax2 | Text inputs |

Click **Run Optimization →** to save selections and navigate to results.

### Page 5: Results
On load, the page:
1. Reads saved data from sessionStorage
2. Sends `POST /api/optimize`
3. Populates all tables:

| Panel | Fields displayed |
|-------|-----------------|
| **HOT STREAM** | Echoed input parameters (mass flow, temps, density, viscosity, Cp, k, fouling) |
| **COLD STREAM** | Echoed input parameters |
| *(Summary)* | Heat load [kW], LMTD [°C] |
| **UNIT GEOMETRY** | Optimal Ds, dte, Npt, rp, lay (layout), L, Nb, Bc; tube count (Nt), heat transfer area, correction factor F, area ratio A/A_req |
| **THERMO PROPERTIES** | Tube & shell velocities, Reynolds numbers, convective heat transfer coefficients, overall HTC (dirty & clean) |
| **PRESSURE DROP** | Tube & shell ΔP [kPa] |
| **OPTIMIZATION** | Objective function value, CAPEX, tube/shell/total OPEX, TAC |

Click **Download Results** to save as text file.

---

## 5. API Reference

### `GET /api/health`

Health check.

**Response:**
```json
{"status": "ok", "service": "OptiProcess Solver API"}
```

### `POST /api/optimize`

Run a full optimization.

**Request body:**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `model` | string | yes | Model name (currently only `"STHE"`) |
| `parameters` | object | yes | All Model_Parameters key-value pairs (43 required — see below) |
| `discrete_variables` | object | yes | `{"Ds": [...], "dte": [...], ...}` — 8 arrays, each must have ≥1 value |
| `selected_of` | string | no | `"TAC_OF"`, `"CAPEX_OF"`, or `"AREA_OF"` (default: `"TAC_OF"`) |
| `number_of_equipment` | int | no | Number of units (default: 1) |

**Required `parameters` keys:**

```
mh, roh, Cph, mih, kh, Rfh, DPhdisp,     # Hot stream
mc, roc, Cpc, mic, kc, Rfc, DPcdisp,     # Cold stream
ktube, thk, yfluid,                        # HEX config
Shell_Method, Tube_Method,                 # Correlation methods
Aexc, Tci, Tco, Thi, Tho,                 # Problem temps
vsmax, vsmin, vtmax, vtmin,               # Velocity bounds
Retmin, Resmin, Retmax, Resmax,            # Reynolds bounds
LBLD, UBLD, Xp, F_min,                    # Geometric/LMTD bounds
par_a, par_b, pc, int_rate, n, eta, Nop   # Economics
```

For Bell method, also include: `Nss`, `plbmax1`, `plbmax2`.

**Response (200 OK):**

```json
{
    "status": "ok",
    "model": "STHE",
    "objective": {
        "function": "TAC_OF",
        "variable": "TAC",
        "value": 8247.52,
        "unit": "$/year"
    },
    "optimal_variables": {
        "Ds": 0.7874, "dte": 0.0254, "Npt": 6, "rp": 1.5,
        "lay": 1, "L": 6.0976, "Nb": 13, "Bc": 0.25,
        "yfluid": "hot_stream"
    },
    "calculations": {
        "vt": 1.38, "vs": 0.53,
        "Ret": 11446, "Res": 49721,
        "ht": 967.6, "hs": 2648.5,
        "U": 395.2, "Uc": 624.7,
        "DPt": 48.1, "DPs": 7.3,
        "CAPEX": 30825.6,
        "OPEX_t": 2406.6, "OPEX_s": 824.2, "OPEX_total": 3230.8,
        "TAC": 8247.5, "Q": 2272.0,
        "Nt": 302, "F": 0.971, "A_total": 146.9, "A_ratio": 1.16
    },
    "number_of_solutions": 1,
    "elapsed_seconds": 0.19
}
```

| Field | Type | Description |
|-------|------|-------------|
| `status` | string | `"ok"` or `"error"` |
| `model` | string | Model name |
| `objective` | object | OF equation name, variable name, optimal value, unit |
| `optimal_variables` | object | Optimal discrete variable values (+ `yfluid`) |
| `calculations` | object | 21 intermediate results: velocities, Reynolds, HTCs, pressure drops, economics |
| `number_of_solutions` | int | Number of equally-optimal candidates |
| `elapsed_seconds` | number | Solver execution time |

**Response (200 — error):**

```json
{
    "status": "error",
    "error": "description of what went wrong",
    "elapsed_seconds": 0.0
}
```

Validation errors return 200 with `"status": "error"` and a descriptive message. Infrastructure errors (Python crash, timeout) return HTTP 500.

### cURL example

```bash
curl -s -X POST http://127.0.0.1:8000/api/optimize \
  -H 'Content-Type: application/json' \
  -d '{
    "model": "STHE",
    "selected_of": "TAC_OF",
    "parameters": {
        "mh": 20, "roh": 750, "Cph": 2840, "mih": 0.002, "kh": 0.19,
        "Rfh": 0.0002, "DPhdisp": 100000,
        "mc": 60, "roc": 995, "Cpc": 4187, "mic": 0.0005, "kc": 0.6,
        "Rfc": 0.0007, "DPcdisp": 100000,
        "ktube": 50, "thk": 0.00165, "yfluid": "hot_stream",
        "Shell_Method": "Kern", "Tube_Method": "Dittus_Boelter",
        "Aexc": 11, "Tci": 47, "Tco": 56, "Thi": 120, "Tho": 80,
        "vsmax": 2, "vsmin": 0.5, "vtmax": 3, "vtmin": 1,
        "Retmin": 10000, "Resmin": 2000, "Retmax": 5000000, "Resmax": 100000,
        "LBLD": 3, "UBLD": 15, "Xp": 0.9, "F_min": 0.75,
        "par_a": 635.14, "par_b": 0.778, "pc": 0.15,
        "int_rate": 0.1, "n": 10, "eta": 0.6, "Nop": 7500
    },
    "discrete_variables": {
        "Ds": [0.7874,0.8382,0.889,0.9398,0.9906,1.0668,1.143,1.2192,1.3716,1.524],
        "dte": [0.01905,0.02540,0.03175,0.03810,0.05080],
        "Npt": [1,2,4,6],
        "rp": [1.25,1.33,1.50],
        "lay": [1,2],
        "L": [1.2195,1.8293,2.4390,3.0488,3.6585,4.8768,6.0976],
        "Nb": [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20],
        "Bc": [0.25]
    }
}' | python3 -m json.tool
```

---

## 6. YAML Schema Reference (`STHE_ui.yaml`)

The YAML file contains **only** UI presentation metadata. Structural data comes from `Model_Def_STHE.py` and `Examples_STHE.py`.

### Top-level

```yaml
header:
  title: "OptiHexx"
  subtitle: "Heat Exchanger Optimal Design Suite"
  prototype: "Prototype P07"

available_models:
  - {id: "STHE", label: "Shell & Tube", active: true, link: "problem_data.html"}
  - {id: "GPHE", label: "Plate Exchangers", active: false, link: "#"}
  # ... more models

model:
  display_name: "Shell & Tube"
  icon: "fa-industry"
```

### Pages → `problem_data`

```yaml
pages:
  problem_data:
    title: "Problem Data"
    columns:                     # each column is a list of section IDs
      - [optimization_target, fluid_allocation]
      - [hot_stream, cold_stream, lmtd_display]
      - [flow_limits, lmtd_settings, other_options]
      - [economic]
    sections:
      optimization_target:
        title: "OPTIMIZATION TARGET"
        element: radio_group
        source: "Model_Declarations"
        source_key: "Selected_OF"
        option_labels: {TAC_OF: "TAC", CAPEX_OF: "CAPEX", AREA_OF: "AREA"}

      hot_stream:
        title: "HOT STREAM"
        element: form_group       # renders labeled text inputs
        color: red                # red, blue, yellow, gray, green, pink
        source: "Model_Parameters"
        fields:
          Thi: {label: "Inlet Temperature", unit: "°C"}
          Tho: {label: "Outlet Temperature", unit: "°C"}
          # ...

      flow_limits:
        title: "FLOW LIMITS"
        element: limit_table      # special 3-column table: lower | item | upper
        rows:
          - {item: "Tube velocity", unit: "m/s", lower: vtmin, upper: vtmax}
          # ...

      shell_method:
        # Use element: select for dropdowns
        fields:
          Shell_Method:
            label: "Shell Method"
            element: select
            options: ["Kern", "Bell"]
```

**Supported `element` types for problem_data:**

| element | Renders as |
|---------|-----------|
| `radio_group` | Radio button group |
| `form_group` | Labeled text inputs (or selects) |
| `limit_table` | Three-column min/item/max table |
| `computed_display` | Read-only display field |

**Field modifiers:**
- `unit: "°C"` — appended to label
- `display_factor: 100` — multiply stored value for display (e.g., 0.1 → 10%)
- `computed_hint: true` — shows field as disabled (calculated)
- `element: select` — renders `<select>` dropdown instead of `<input>`

### Pages → `geometric_options`

```yaml
  geometric_options:
    title: "Geometric Options"
    columns:
      - [configurations, shell_count]
      - [tube_passes, layouts, pitch_ratio]
      - [shell_diameter]
      # ...
    sections:
      tube_passes:
        title: "Number of Tube Passes"
        element: checkbox_grid
        color: blue               # brown, blue, yellow, brown_dark, red_dark, green
        variable: "Npt"           # must match List_of_Variables from Model_Def

      layouts:
        variable: "lay"
        value_labels: {1: "Square (90°)", 2: "Triangle (30°)", 3: "Rotated Square (45°)"}

      configurations:
        element: checkbox_grid
        static: true              # not tied to a model variable
        items:
          - {value: "series", label: "Series"}
          - {value: "parallel", label: "Parallel"}

      tube_options:
        element: form_group       # text inputs within geometric-options page
        color: brown_dark
        source: "Model_Parameters"
        fields:
          ktube: {label: "Thermal Conductivity", unit: "W/(m K)"}
```

**color values for geometric_options:** `brown`, `blue`, `yellow`, `brown_dark`, `red_dark`, `green`

### Pages → `results`

```yaml
  results:
    title: "Results"
    columns:
      - [hot_stream_results, cold_stream_results, summary_data]
      - [unit_geometry]
      - [thermo_properties, pressure_drop]
      - [optimization_results]
    sections:
      hot_stream_results:
        title: "HOT STREAM"
        element: data_table
        color: green_display      # green_display, blue_display, yellow_display, red_display
        rows:
          - {label: "Mass flow rate", key: "mh", unit: "kg/s"}
          # ...

      thermo_properties:
        title: "THERMO PROPERTIES"
        color: yellow_display
        subsections:              # nested sub-tables with their own headers
          - title: "TUBE SIDE"
            rows:
              - {label: "Velocity flow", key: "vt", unit: "m/s", computed: true}
          - title: "SHELL SIDE"
            rows: [...]
        footer_rows:              # rows below all subsections
          - {label: "Overall HTC (dirty)", key: "U", unit: "W/(m² K)", computed: true}

      optimization_results:
        subsections:
          - title: ""
            rows:
              - {label: "Objective function", key: "OF_value", highlight: true}
          - title: "ECONOMICS"
            rows:
              - {label: "Capital cost", key: "CAPEX", unit: "$"}
```

**Row modifiers for results:**
- `computed: true` — value comes from solver (or is derived by JS)
- `highlight: true` — bold text
- `result_var: true` — value is an optimal discrete variable
- `display_factor: 1000` — for unit conversion in display (e.g., Pa·s → mPa·s)

---

## 7. Adding a New Model

To add a new heat exchanger type (e.g., GPHE / Plate Exchanger):

### Step 1: Create model directory structure

```
GPHE/
├── GPHE_ui.yaml
├── Examples_GPHE.py
├── Model/
│   ├── Model_Def_GPHE.py
│   ├── Parameters_Update_GPHE.py
│   └── Constraints_and_OF_GPHE.py
├── Calculations/
│   └── (thermal-hydraulic model)
└── __init__.py
```

### Step 2: Write the YAML metadata (`GPHE_ui.yaml`)

Follow the same schema as `STHE_ui.yaml` (see Section 6). The YAML references variable names, parameter keys, and objective function names as defined in your `Model_Def_GPHE.py`.

### Step 3: Add model to the main menu

In `GPHE_ui.yaml`, include the `available_models` list, or add the new model to the shared list:

```yaml
available_models:
  - {id: "GPHE", label: "Plate Exchangers", active: true, link: "problem_data.html"}
```

### Step 4: Generate and test

```bash
python generate_ui.py --model GPHE --example Example1
uvicorn solver_api:app --host 127.0.0.1 --port 8000
```

**Requirements for the model to work with the generator:**
- `Model_Def_{Model}.py` must export `Model_{Model}` dict with:
  - `Model_Info.List_of_Variables` — ordered list of discrete variable names
  - `Model_Info.Standard_Variables_Values` — dict with full option lists per variable
  - `Model_Info.Objective_Function` — dict with `Equation_Name`, `Optimization_Variables_Names`, `Unit_OF`
- `Examples_{Model}.py` must export one or more example dicts with:
  - `Number_of_Equipment`
  - `Equipment1.Model_Declarations`: `Type_Equipment`, `Discrete_Values_of_Variables`, `Selected_OF`
  - `Equipment1.Model_Parameters`: all parameter key-value pairs

---

## 8. CLI Reference

### `generate_ui.py`

```bash
python generate_ui.py [--model STHE] [--example Example1] [--output output]
```

| Option | Default | Description |
|--------|---------|-------------|
| `--model` | `STHE` | Model name (must have `{Model}_ui.yaml`) |
| `--example` | `Example1` | Example name for default values |
| `--output` | `output` | Output directory for generated HTML |

### `solver_runner.py`

```bash
python solver_runner.py --model STHE --input /tmp/in.json --output /tmp/out.json
```

Used internally by the API. Can also be used standalone for batch processing.

### `solver_api.py`

```bash
uvicorn solver_api:app --host 0.0.0.0 --port 8000
```

| Option | Default | Description |
|--------|---------|-------------|
| `--host` | `127.0.0.1` | Bind address (`0.0.0.0` for network access) |
| `--port` | `8000` | Port number |
| `--reload` | off | Auto-restart on code changes (dev only) |

---

## 9. Troubleshooting

**All result cells show "—" (dashes)**
- The API call failed. Check that the server is running: `curl http://127.0.0.1:8000/api/health`
- Ensure you opened the page via `http://127.0.0.1:8000/ui/...` (not `file://`).
- Open the browser console (F12) and look for errors.

**"Optimization failed: Missing required parameters: [...]"**
- The browser JS failed to collect some form fields. Refresh the page, refill, and try again. If persistent, the generated HTML may need regeneration: `python generate_ui.py`

**"Optimization failed: No feasible design found" (or "variables_survivor_names")**
- The discrete variable ranges are too restrictive — no geometric combination satisfies the Primordial constraints (L/D between 3-15, baffle spacing limits). Widen the ranges for Shell Diameter (Ds), Tube Length (L), and Number of Baffles (Nb).

**"500 Internal Server Error" on POST /api/optimize**
- The solver subprocess crashed. Check the server console for a Python traceback. Common causes: missing required parameters, empty discrete variable arrays, or invalid data types.

**"No input data found" on results page**
- You navigated directly to results.html without filling the previous pages. Start from the Main Menu: Shell & Tube → Problem Data → Next → Geometric Options → Run Optimization.

**"Is the API server running?" error**
- Start the server: `uvicorn solver_api:app --host 127.0.0.1 --port 8000`
- Verify: `curl http://127.0.0.1:8000/api/health`

**Solver returns `number_of_solutions: 0`**
- No feasible design found with the selected discrete variable ranges. Widen the search space or relax constraints.

**Import errors when running from a different directory**
- Always run scripts from the `OptiAppsCreator/` directory. The code relies on relative imports and `sys.path`.

**Generator warns about display_factor on non-numeric field**
- A `display_factor` was set on a field whose value is a string. Remove the factor or ensure the source field is numeric.

**"Module STHE not found"**
- Run from the `OptiAppsCreator/` directory. The `generate_ui.py` script adds it to `sys.path` automatically.

**Port 8000 already in use**
- A previous server instance is still running: `pkill -f uvicorn` then restart.
