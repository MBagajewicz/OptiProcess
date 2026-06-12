# Consistency Check Process

This document describes how the current consistency check process works in `OptiAppsCreator`, how data adjustments are propagated between tests, and which issues should be reviewed before extending the process with configurable `Deactive`, `Soft (Warnings)`, and `Hard (Estrict)` modes.

## Current Flow

The consistency check is executed before the initial set is prepared and before the solver runs.

For the direct command-line flow, `Main.py` calls:

```python
Calculations_Consistency_Check.Consistency_Check(Active_Example, Active_Models, save_result)
```

For the web/API flow, `solver_runner.py` currently calls the same organizer inside `run_solver()`:

```python
Calculations_Consistency_Check.Consistency_Check(active_example, active_models, save_result)
```

The organizer then inspects each active equipment, reads the model type, imports the corresponding `Parameters_Update_{MODEL}.py` module, and calls the functions listed in the model definition:

```python
Consistency_Funcions = equipment_def['Model_Info'].setdefault('Consistency_Check_Functions', [])
for function in Consistency_Funcions:
    getattr(Parameters_Update_Module, function)(model_declarations, model_parameters, save_result)
```

For both implemented models, the model definition contains:

```python
'Consistency_Check_Functions': ['consistency']
```

Therefore the model-specific entry points are:

```text
STHE/Model/Parameters_Update_STHE.py::consistency()
GPHE/Model/Parameters_Update_GPHE.py::consistency()
```

## Modules Involved

### `OptiCode/Calculations_Consistency_Check.py`

This module is the organizer. It does not implement the actual tests. Its responsibilities are:

- iterate first-level equipments;
- iterate next-level equipments when present;
- identify each equipment model;
- read `Consistency_Check_Functions` from the model definition;
- dynamically call each listed function from the corresponding `Parameters_Update_{MODEL}.py` module.

### `{MODEL}/Model/Parameters_Update_{MODEL}.py`

This module owns the model-specific consistency entry point. The current implemented entry point is named `consistency()`.

Inside `consistency()`, each model calls common heat exchanger tests and model-specific tests in a fixed sequence.

### `Common_Equations_HEX/Calculations_HEX_Consistency.py`

This module contains common heat exchanger consistency functions used by STHE and GPHE:

- `verification_positive_variables()`
- `verification_DeltaTmin()`
- `verification_heatload()`
- `verification_Thi_Tho()`
- `verification_Tco_Tci()`
- `verification_Tco_Thi()`
- `verification_Tci_Tho()`

Some of these functions only validate data. Others mutate the input dictionary or abort the process with `sys.exit()`.

## How Data Adjustments Are Propagated

The consistency process relies on the fact that `m_p` and `m_d` are mutable Python dictionaries.

When a function receives `m_p` or `m_d`, it receives a reference to the same object used by the caller. Therefore, if a test modifies the dictionary, the change is visible to all later tests and to the solver.

Example from `verification_DeltaTmin()`:

```python
if 'DeltaT_min' not in m_p:
    m_p['DeltaT_min'] = 5
```

Later tests can then read:

```python
deltaTmin = m_p['DeltaT_min']
```

without receiving a new dictionary explicitly.

The same applies to `m_d`. In STHE, `verification_Tco_Thi_STHE()` can modify the discrete options:

```python
m_d['Discrete_Values_of_Variables'][2] = [1]
```

Since index `2` corresponds to `Npt`, this removes multipass alternatives when the temperature conditions do not allow them.

Although each function usually returns `m_p` or `m_d`, the current code stores those return values in variables named `verif1`, `verif2`, etc. and does not use them later. The effective propagation mechanism is mutation of the shared dictionary, not the return value.

## Current Tests

### Common Tests

#### `verification_positive_variables(m_p, save_result)`

Checks every numeric value in `m_p`. If a numeric value is negative, it writes a message through `save_result()` and aborts with `sys.exit()`.

Purpose: avoid physically invalid negative parameters such as flows, densities, heat capacities, viscosities, costs, and limits.

#### `verification_DeltaTmin(m_p, save_result)`

Checks whether `DeltaT_min` exists in `m_p`.

If it is missing, it mutates `m_p` by inserting:

```python
m_p['DeltaT_min'] = 5
```

and writes a message through `save_result()`.

Purpose: guarantee that later temperature-approach tests can use `DeltaT_min`.

#### `verification_heatload(m_p, save_result)`

Computes hot-side and cold-side heat loads:

```python
Qh = mh * Cph * (Thi - Tho)
Qc = mc * Cpc * (Tco - Tci)
```

The function compares the relative difference using `eps = 1e-4`. In the current code, if the relative difference is greater than `eps`, the function does nothing. If the relative difference is less than or equal to `eps`, it recalculates `Tco` from the hot-side heat load:

```python
m_p['Tco'] = Qh / (m_p['mc'] * m_p['Cpc']) + m_p['Tci']
```

and writes a message saying that the heat load is inconsistent.

Purpose: intended to enforce energy balance between hot and cold streams, but the exact current logic should be reviewed because the condition and the message appear ambiguous.

#### `verification_Thi_Tho(m_p, save_result)`

Checks:

```python
Thi > Tho
```

If it fails, it writes `Error data consistency: Tho > Thi` and aborts with `sys.exit()`.

Purpose: ensure that the hot stream cools down.

#### `verification_Tco_Tci(m_p, save_result)`

Checks:

```python
Tco > Tci
```

If it fails, it writes `Error data consistency: Tci > Tco` and aborts with `sys.exit()`.

Purpose: ensure that the cold stream heats up.

#### `verification_Tco_Thi(m_p, save_result)`

Checks:

```python
Tco < Thi - DeltaT_min
```

If it fails, it writes `Error data consistency: Tco > Thi - deltaTmin` and aborts with `sys.exit()`.

Purpose: ensure a minimum temperature approach between cold outlet and hot inlet.

This common function is currently not used by STHE or GPHE in the active `consistency()` implementations. STHE uses a model-specific version instead.

#### `verification_Tci_Tho(m_p, save_result)`

Checks:

```python
Tci < Tho - DeltaT_min
```

If it fails, it writes `Error data consistency: Tci > Tho - deltaTmin` and aborts with `sys.exit()`.

Purpose: ensure a minimum temperature approach between cold inlet and hot outlet.

### STHE-Specific Tests

#### `verification_Tco_Thi_STHE(m_p, m_d)`

This test is defined inside `STHE/Model/Parameters_Update_STHE.py::consistency()`.

First it checks:

```python
Tco < Thi - DeltaT_min
```

If it fails, it writes `Error data consistency: Tco > Thi - DeltaTmin` and aborts with `sys.exit()`.

If the first condition is valid, it then checks whether multipass tube configurations are compatible with the temperature levels. If:

```python
Tco > Tho - DeltaT_min
```

then it writes a message and mutates `m_d`:

```python
m_d['Discrete_Values_of_Variables'][2] = [1]
```

Purpose: remove multipass alternatives by forcing `Npt = [1]` when temperature conditions make multipass designs invalid.

#### `variables_bounds(m_d)`

Checks that each selected discrete value is within the min/max range of the corresponding standard value list in `Model_STHE['Model_Info']['Standard_Variables_Values']`.

If values are out of range, it writes warnings but does not abort.

Purpose: warn when selected design-variable values are outside the standard domain known by the model.

#### `variables_standard_values(m_d)`

Checks that each selected discrete value matches one of the values listed in `Standard_Variables_Values`.

This is stricter than `variables_bounds()`: a value can be inside the min/max range and still fail this test if it is not one of the standard catalog values.

If values do not match, it writes warnings but does not abort.

Purpose: warn when selected values are not catalog/standard options.

### GPHE-Specific Tests

GPHE defines the same two model-specific discrete-variable tests inside `GPHE/Model/Parameters_Update_GPHE.py::consistency()`:

- `variables_bounds(m_d)`
- `variables_standard_values(m_d)`

They serve the same purpose as the STHE versions but use `Model_GPHE['Model_Info']['Standard_Variables_Values']`.

## Current STHE Sequence

STHE currently executes:

```python
verif1 = Calculations_HEX_Consistency.verification_positive_variables(m_p, save_result)
verif2 = Calculations_HEX_Consistency.verification_DeltaTmin(m_p, save_result)
verif3 = Calculations_HEX_Consistency.verification_heatload(m_p, save_result)
verif4 = Calculations_HEX_Consistency.verification_Thi_Tho(m_p, save_result)
verif5 = Calculations_HEX_Consistency.verification_Tco_Tci(m_p, save_result)
verif6 = verification_Tco_Thi_STHE(m_p, m_d)
verif7 = Calculations_HEX_Consistency.verification_Tci_Tho(m_p, save_result)
verif8 = variables_bounds(m_d)
verif9 = variables_standard_values(m_d)
```

The order matters because later tests depend on modifications made by earlier tests. For example, `verification_Tco_Thi_STHE()` and `verification_Tci_Tho()` read `DeltaT_min`, which may have been inserted by `verification_DeltaTmin()`.

## Current GPHE Sequence

GPHE currently executes:

```python
verif1 = Calculations_HEX_Consistency.verification_positive_variables(m_p, save_result)
verif2 = Calculations_HEX_Consistency.verification_DeltaTmin(m_p, save_result)
verif3 = Calculations_HEX_Consistency.verification_heatload(m_p, save_result)
verif4 = Calculations_HEX_Consistency.verification_Thi_Tho(m_p, save_result)
verif5 = Calculations_HEX_Consistency.verification_Tco_Tci(m_p, save_result)
verif6 = Calculations_HEX_Consistency.verification_Tci_Tho(m_p, save_result)
verif7 = variables_bounds(m_d)
verif8 = variables_standard_values(m_d)
```

## Console Flow Through `Main.py`

When `Main.py` is executed from the command line, there is no browser session and no UI-selected consistency policy.

The expected default behavior is:

- all tests are treated as hard;
- any hard consistency failure prevents the solver from running;
- messages are written through `save_result()` to the normal results output;
- `Main.py` does not read or persist web consistency settings.

This preserves the current intent of the command-line workflow.

## Web Flow Through `solver_runner.py`

The web workflow can pass a temporary consistency configuration from the browser session to the API request. This configuration should not be saved in project files.

Expected browser-only state:

```text
sessionStorage['optihex_{MODEL}_consistency_checks']
```

Expected request-only payload:

```json
{
  "consistency_checks": {
    "positive_variables": "hard",
    "delta_t_min": "soft",
    "heatload": "deactive"
  }
}
```

If no configuration is provided, every test should default to `hard`.

## Notes For Future `Deactive` / `Soft` / `Hard` Modes

The desired behavior is:

- `Deactive`: do not execute the selected test;
- `Soft (Warnings)`: execute the test, report a warning if it fails, and continue to the solver;
- `Hard (Estrict)`: execute the test, report an error if it fails, and do not run the solver.

The current implementation has no explicit policy layer. Some tests already abort with `sys.exit()` while others only write warning messages. This should be normalized by wrapping each test call with policy-aware execution while keeping the test definitions inside `consistency()`.

## Issues To Review

### Exact Intent Of `verification_heatload()`

The function appears intended to validate or enforce energy balance between hot and cold streams.

However, the current condition is ambiguous:

```python
if abs((Qh - Qc)/Qh) > eps:
    pass
else:
    m_p['Tco'] = Qh/(m_p['mc']*m_p['Cpc']) + m_p['Tci']
    save_result("Error data consistency: heat load is inconsistent ...")
```

The function adjusts `Tco` when the relative difference is within tolerance, while the message says the heat load is inconsistent. This should be reviewed to confirm whether the condition is inverted, whether the message is wrong, or whether the adjustment is intended as a normalization step.

### Tests That Abort vs Tests That Only Warn

Some tests call `sys.exit()` on failure:

- `verification_positive_variables()`
- `verification_Thi_Tho()`
- `verification_Tco_Tci()`
- `verification_Tco_Thi()`
- `verification_Tci_Tho()`
- `verification_Tco_Thi_STHE()` in one branch

Other tests only write warning messages and continue:

- `variables_bounds()`
- `variables_standard_values()`
- the multipass branch inside `verification_Tco_Thi_STHE()`
- `verification_DeltaTmin()` when it inserts a default value
- `verification_heatload()` when it adjusts `Tco`

This behavior may duplicate or conflict with the planned `Soft` and `Hard` indicators. The policy should be defined explicitly by the selected mode instead of being implicitly determined by whether a test currently calls `sys.exit()`.

### Return Values Stored But Not Used

The current code stores each return value:

```python
verif1 = ...
verif2 = ...
```

but those variables are not used later. The real effect comes from mutating `m_p` and `m_d` in place.

This should be cleaned up or documented clearly. A future refactor could either remove the unused variables or reassign explicitly:

```python
m_p = verification_DeltaTmin(m_p, save_result)
```

### Dependency On Test Order

Some tests depend on earlier tests. For example, temperature-approach checks read `DeltaT_min`, which may be inserted by `verification_DeltaTmin()`.

If `verification_DeltaTmin()` is set to `Deactive` and the project does not define `DeltaT_min`, later tests may fail with `KeyError`. The configurable implementation should either document this dependency or protect dependent tests with a clear error message.

### Tests With Side Effects

Some tests are not pure validations. They modify input data:

- `verification_DeltaTmin()` adds `DeltaT_min`;
- `verification_heatload()` can modify `Tco`;
- `verification_Tco_Thi_STHE()` can force `Npt = [1]`.

When such tests are set to `Deactive`, their corrective side effects are also disabled. When they are `Soft` or `Hard`, the implementation should preserve the current side effects unless a future model decision changes that behavior.

### Possible Mislabeling Of STHE Tube Options

The STHE UI currently labels `LBLD` and `UBLD` as tube-length limits:

```yaml
LBLD: {label: "Minimum Tube Length", unit: "m"}
UBLD: {label: "Maximum Tube Length", unit: "m"}
```

However, in the solver these parameters are used as limits for the dimensionless ratio `L / Ds`, not as absolute tube-length limits.

In `STHE/Model/Constraints_and_OF_STHE.py`:

```python
def LD_lb(Ds, dte, Npt, rp, lay, L, Nb, Bc, m_p):
    fun_val = m_p['LBLD'] - L / Ds
    return fun_val

def LD_ub(Ds, dte, Npt, rp, lay, L, Nb, Bc, m_p):
    fun_val = L / Ds - m_p['UBLD']
    return fun_val
```

Therefore the effective hard solver restriction is:

```text
LBLD <= L / Ds <= UBLD
```

These checks are not part of the configurable consistency process. They are primordial set-trimming constraints listed in `Model_Def_STHE.py`:

```python
'Primordial_Set_Trimming_Constraints_List': ['LD_lb', 'LD_ub', 'lbc_lb', 'lbc_ub']
```

As a consequence, setting `UBLD = 5` in the UI imposes `L / Ds <= 5` as a hard solver constraint regardless of the selected mode for:

- `variables_bounds`
- `variables_standard_values`

This can make a case infeasible even when the discrete-variable consistency checks are set to `Soft (Warnings)`.

The UI labels should be reviewed. More accurate labels would be:

```yaml
LBLD: {label: "Minimum L/D ratio", unit: "-"}
UBLD: {label: "Maximum L/D ratio", unit: "-"}
```

If these restrictions need to become optional, soft, or user-configurable, that should be handled by a separate solver-constraint policy. It should not be mixed with the data-consistency test policy unless the conceptual scope of the consistency system is deliberately expanded.
