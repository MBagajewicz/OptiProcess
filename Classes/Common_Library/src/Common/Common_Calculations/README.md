# Calculations_Model_Consistency

> Consistency-checking module between discrete design-variable values and the standard values defined in the equipment model.  
> Ensures that optimization/sizing variables respect range limits and match the model's standard values.  
> Supports `Calculated_*` markers for discrete sets that are generated later by a dedicated calculated-values resolver.

---

## 📁 File

| File | Functions | Purpose |
|------|-----------|---------|
| `Calculations_Model_Consistency.py` | `variables_bounds()`, `variables_standard_values()` | Verifies that discrete variable values are within the allowed range and match the model's standard values. |

---

## Dependencies

```python
from Common.Utils.Model_Loader import Model_Loader
```

- `Model_Loader.load()` loads the equipment model information (`Model_Info`) based on the type specified in `m_d['Type_Equipment']`.
- The loaded model must contain:
  - `List_of_Variables`: list with the names of the design variables.
  - `Standard_Variables_Values`: dictionary `{variable_name: [standard_values]}`.

---

## 1. `variables_bounds(m_d, save_result)`

Verifies that **all discrete values** of each design variable fall within the range defined by the **minimum and maximum** of the model's standard values.

### Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `m_d` | `dict` | Design model dictionary. Must contain `Type_Equipment` and `Discrete_Values_of_Variables`. |
| `save_result` | `callable` | Callback function to log warnings (e.g. `print`, logger, or text accumulator). |

### Expected `m_d` structure

```python
m_d = {
    'Type_Equipment': 'Shell_and_Tube',          # Equipment type (used by Model_Loader)
    'Discrete_Values_of_Variables': [
        [0.0127, 0.01905, 0.0254],               # Discrete values for variable 0
        [1, 2, 4, 6],                             # Discrete values for variable 1
        # ... one list per variable
    ]
}
```

### Expected loaded model structure (`m_i`)

```python
m_i = {
    'List_of_Variables': ['Do', 'Npt', 'L', 'B', ...],
    'Standard_Variables_Values': {
        'Do': [0.0127, 0.01905, 0.0254],
        'Npt': [1, 2, 4, 6],
        # ...
    }
}
```

### Behavior

1. Loads the model corresponding to `m_d['Type_Equipment']`.
2. Iterates over each variable and its discrete values.
3. For each variable, obtains the `[min, max]` range from its standard values.
4. If any discrete value falls outside the range `± tol` (where `tol = 0.001`), a warning is logged.
5. If there are no issues, no message is emitted.
6. If a variable's discrete-value entry is a string starting with `Calculated_`, it is treated as a calculation marker rather than as an actual discrete-value list and is skipped by this validation. The marker is resolved later by the calculated-values resolver.

### Returns

| Type | Description |
|------|-------------|
| `dict` | The same `m_d` dictionary (possibly unmodified). |

### Usage example

```python
from Common.Calculations_Model_Consistency import variables_bounds

def save_result(msg):
    print(msg)

m_d = {
    'Type_Equipment': 'Shell_and_Tube',
    'Discrete_Values_of_Variables': [
        [0.0127, 0.01905, 0.0300],  # 0.0300 is outside the standard range
        [1, 2, 8],                   # 8 may be outside the range
    ]
}

m_d = variables_bounds(m_d, save_result)
# → WARNING: Variables out of range:
# →  - Do: Invalid values [0.03]
# →  - Npt: Invalid values [8]
```

### Notes

- The tolerance `tol = 0.001` allows small numerical deviations without generating false positives.
- Only checks **range limits** (minimum/maximum); it does not require exact match with individual values.
- Variables without defined standard values are silently ignored.

---

## 2. `variables_standard_values(m_d, save_result)`

Verifies that **each discrete value** of each design variable **matches exactly** (within a tolerance) at least one of the model's standard values.

### Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `m_d` | `dict` | Design model dictionary. Must contain `Type_Equipment` and `Discrete_Values_of_Variables`. |
| `save_result` | `callable` | Callback function to log warnings. |

### Behavior

1. Loads the model corresponding to `m_d['Type_Equipment']`.
2. Iterates over each variable and its discrete values.
3. For each discrete value, checks whether there exists a standard value such that `|v - std_val| <= tol`.
4. If a discrete value does not match any standard value, it is flagged as invalid.
5. If there are no issues, no message is emitted.

### Returns

| Type | Description |
|------|-------------|
| `dict` | The same `m_d` dictionary (possibly unmodified). |

### Usage example

```python
from Common.Calculations_Model_Consistency import variables_standard_values

def save_result(msg):
    print(msg)

m_d = {
    'Type_Equipment': 'Shell_and_Tube',
    'Discrete_Values_of_Variables': [
        [0.0127, 0.01905, 0.0200],  # 0.0200 is not a standard value
        [1, 2, 4],                   # All are standard values
    ]
}

m_d = variables_standard_values(m_d, save_result)
# → WARNING: Variables do not match standard values
# →  - Do: Invalid values [0.02]
```

### Notes

- The tolerance `tol = 0.001` allows small rounding differences.
- Unlike `variables_bounds()`, this function requires **point-wise matching** with catalogued values, not just being within a range.
- Useful for validating that optimization variables only take commercial or manufacturable values.
- `Calculated_*` entries are intentionally skipped here because they are placeholders for discrete sets that have not yet been generated.
- Once the calculated marker has been resolved into actual discrete values, those generated values can be checked normally.

---

## 🔗 Difference between the two functions

| Aspect | `variables_bounds()` | `variables_standard_values()` |
|--------|----------------------|-------------------------------|
| **What it checks** | Range (min/max) of standard values | Exact match with standard values |
| **Tolerance** | `±0.001` relative to the limit | `±0.001` relative to each standard value |
| **Example of failure** | Value 0.0300 when the maximum standard is 0.0254 | Value 0.0200 when standards are [0.0127, 0.01905, 0.0254] |
| **Typical use** | Detect extreme values outside the catalog | Ensure only commercial/manufacturable values are used |

---

## 🧪 Suggested Tests

| Test | What to check |
|------|---------------|
| Correct range | Values within the standard range do not trigger warnings. |
| Range exceeded | Values above the maximum or below the minimum trigger `WARNING: Variables out of range`. |
| Exact match | Values that match a standard value do not trigger warnings. |
| Intermediate value | A value within the range but not matching any standard triggers `WARNING: Variables do not match standard values`. |
| Tolerance | Values with deviation `< 0.001` from a standard should be accepted. |
| Variables without standard | Variables not present in `Standard_Variables_Values` should be silently ignored. |
| Calculated discrete marker | A value such as `'Calculated_from_TEMA'` should be recognized as a calculation marker and should not trigger a standard-value warning. |
| Resolved calculated values | After the marker is replaced by actual discrete values, those values should be subject to the normal standard-value validation. |
| Non-existent model | Unregistered `Type_Equipment` should be handled by `Model_Loader` (typically with an exception). |

---

## 📄 License

*Under construction*
