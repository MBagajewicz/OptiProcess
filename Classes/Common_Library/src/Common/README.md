# Common Library

> A modular Python library for chemical process simulation, providing thermodynamic streams, flowsheet frameworks, unit operations, heat-exchanger calculations, model consistency checks, and dynamic model loading.

---

## 📁 Package Structure

```
Common/
├── Stream/                              # Thermodynamic state representation
│   └── README.md
├── Process_Simulator/                   # Flowsheet framework & solvers
│   └── README.md
├── Unit_Operation/                      # Steady-state unit operations
│   └── README.md
├── HEX_Calculations/                    # Heat-exchanger sizing & thermal analysis
│   └── README.md
├── Calculations_Model_Consistency/      # Design-variable consistency checks
│   └── README.md
└── Utils/
    └── README.md                    # Dynamic model-definition loader
        
```

---

## 🚀 Quick Overview

| Module | What it does | Key Classes / Functions |
|--------|--------------|------------------------|
| **Stream** | Backend-agnostic thermodynamic state (CoolProp-backed) | `Stream`, `ThermoBackend` |
| **Process_Simulator** | Flowsheet topology, unit operations, sequential solver | `Flowsheet`, `UnitOperation`, `SequentialSolver`, `Port` |
| **Unit_Operation** | Ready-to-use equipment: compressor, mixer | `Compressor`, `Mixer` |
| **HEX_Calculations** | Heat-exchanger duty, LMTD, consistency, allocation, outlet temps | `HEX_heat_load`, `HEX_lmtd`, `HEX_Tho_Tco`, `allocation` |
| **Calculations_Model_Consistency** | Validate discrete design variables against model standards | `variables_bounds`, `variables_standard_values` |
| **Model_Loader** | Dynamically import equipment model definitions | `Model_Loader.load()` |

---

## 🔗 Module Dependencies

```
┌─────────────────────────────────────────────────────────────┐
│                      Common Library                          │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│   Stream  ◄──────────────────  Unit_Operation               │
│   (thermo)        │            (Compressor, Mixer)          │
│                   │                                         │
│                   └────────►  Process_Simulator             │
│                              (Flowsheet, Solver)            │
│                                                             │
│   HEX_Calculations  ◄──────  Stream (CoolProp)              │
│   (heat load, LMTD)                                         │
│                                                             │
│   Calculations_Model_Consistency  ◄──────  Model_Loader     │
│   (consistency checks)                    (dynamic import)  │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## 📖 Module Documentation

Click on any module below for detailed documentation.

### 1. [Stream](./Stream/README.md)

> A backend-agnostic thermodynamic state representation for process simulation.

- `Stream` class with CoolProp-backed properties
- `ThermoBackend` enum (HEOS, REFPROP, TTSE, BICUBIC)
- Automatic ideal-mixing fallback for unsupported mixtures
- Read-only property interface with state mutation via `set_PT()`, `update()`, etc.
- Serialization (`to_dict` / `from_dict`) and cloning
- Unit conversion utilities

**Key classes:** `Stream`, `ThermoBackend`, `StreamError`, `CompositionError`

---

### 2. [Process_Simulator](./Process_Simulator/README.md)

> A lightweight, modular Python framework for building and solving chemical process flowsheets.

- `Flowsheet` — topology manager (units, streams, connections)
- `UnitOperation` — abstract base class for all equipment
- `BaseEquipment` — common metadata, status, diagnostics
- `Port` / `PortDirection` — typed connection points
- `SequentialSolver` — topological sort (Kahn's algorithm) + sequential execution

**Key classes:** `Flowsheet`, `UnitOperation`, `SequentialSolver`, `Port`

---

### 3. [Unit_Operation](./Unit_Operation/README.md)

> Steady-state unit operations for the Process Simulator flowsheet engine.

- `Compressor` — isentropic compressor with real outlet temperature and power
- `Mixer` — adiabatic material mixer with component and energy balances

**Key classes:** `Compressor`, `Mixer`

---

### 4. [HEX_Calculations](./HEX_Calculations/README.md)

> Pure-math utilities for preliminary heat-exchanger (HEX) sizing and thermal analysis.

- `HEX_heat_load()` — sensible-heat duty calculation
- `HEX_lmtd()` — Log Mean Temperature Difference
- `HEX_Tho_Tco()` — outlet temperature solver (CoolProp or constant-$c_p$)
- `allocation()` — tube-side / shell-side fluid allocation
- Consistency verification suite (temperature checks, heat-load balance, flag validation)

**Key functions:** `HEX_heat_load`, `HEX_lmtd`, `HEX_Tho_Tco`, `allocation`

---

### 5. [Calculations_Model_Consistency](./Calculations_Model_Consistency/README.md)

> Consistency-checking module between discrete design-variable values and standard model values.

- `variables_bounds()` — checks that discrete values are within the standard range
- `variables_standard_values()` — checks exact match with catalogued standard values

**Key functions:** `variables_bounds`, `variables_standard_values`

---

### 6. [Utils / Model_Loader](./Utils/Model_Loader/README.md)

> Generic dynamic loader for equipment model definitions.

- `Model_Loader.load(model_name)` — dynamically imports `<Model>.Model.Model_Def_<Model>` and returns `Model_<Model>`
- Used by `Calculations_Model_Consistency` and other generic modules

**Key class:** `Model_Loader`

---

## 📄 License

*Under construction*

## 👤 Contact

*Add maintainer info here*
