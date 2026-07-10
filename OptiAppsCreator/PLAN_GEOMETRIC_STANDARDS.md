# Plan: Geometric Options By Construction Standard

## Objective

Allow geometric discrete variables to expose alternative construction-standard value sets in the UI, while keeping the solver-facing payload unchanged.

Example target format:

```python
'Standard_Variables_Values': {
    'Ds': {
        'TEMA': [0.2032, 0.254, 0.3048],
        'DIN': [0.8, 0.9, 1.0],
    },
    'dte': [0.01905, 0.02540, 0.03175],
}
```

Existing flat-list format must remain valid:

```python
'dte': [0.01905, 0.02540, 0.03175]
```

## Important Finding

`STHE/Model/Parameters_Update_STHE.py` and `GPHE/Model/Parameters_Update_GPHE.py` currently assume each `Standard_Variables_Values[var]` is a flat list.

If a variable like `Ds` changes to a dict of standards, existing consistency checks can break because they call operations like `min(standard_values_verif)` and iterate directly over `standard_values_verif`.

Therefore, grouped standards need normalization before consistency validation.

## Recommended Format

Use a dictionary keyed by standard name:

```python
'Ds': {
    'TEMA': [...],
    'DIN': [...],
}
```

Do not use tuple lists unless there is a specific reason. Dicts are clearer, easier to validate, and easier to extend later with metadata.

## Solver Contract

The solver should continue receiving only selected values:

```json
"discrete_variables": {
  "Ds": [0.2032, 0.254]
}
```

Construction-standard metadata should not be sent to `solver_runner.py`.

## UI Behavior

For variables with grouped standards, `geometric_options.html` should render a standard selector inside the corresponding `checkbox_grid` block.

Example:

```text
Shell Diameter [m]
Standard: [TEMA v]
[ ] 0.2032
[ ] 0.254
[ ] 0.3048
```

When the user changes the standard:

```text
Standard: [DIN v]
[ ] 0.8
[ ] 0.9
[ ] 1.0
```

Variables without grouped standards should keep the current checkbox-grid behavior and should not show a selector.

## Persistence

Selected geometric values remain in the existing geometric data storage:

```json
{
  "Ds": [0.2032, 0.254],
  "dte": [0.01905]
}
```

Selected standards should be stored separately as metadata:

```json
{
  "Ds": "TEMA"
}
```

Recommended session storage key:

```text
optihex_{MODEL}_geometric_standards
```

Recommended persisted design field:

```json
"geometric_standards": {
  "Ds": "TEMA"
}
```

## Implementation Steps

1. Add standard-value normalization.

   Flat list stays unchanged.

   Dict of standards is flattened for solver and consistency validation.

   Dict also exposes grouped options for UI rendering.

2. Update `generate_ui.py`.

   Detect grouped standards for each checkbox variable.

   For grouped variables, pass `standards` and `default_standard` to `geometric_options.html`.

   Keep `grid_items` compatible for non-grouped variables.

3. Update `templates/geometric_options.html`.

   Add a standard selector only when a variable has grouped standards.

   Render grouped options with `data-standard`.

   Show only the active standard's options.

   When switching standard, update visible options and collect data again.

4. Persist selected standards as metadata.

   Add a storage helper in `templates/base.html`.

   Save selected standards separately from geometric selected values.

   Do not include standards metadata in solver payload.

5. Update `project_store.py` and `solver_api.py`.

   Accept optional `geometric_standards` in project save requests.

   Return `geometric_standards` when loading user designs.

   Preserve `geometric_standards` in user backup and restore.

6. Update `templates/results.html`.

   Preserve `geometric_standards` when saving from Results.

   Keep optimization payload unchanged.

7. Update consistency checks.

   Use flattened standard values in `Parameters_Update_STHE.py`.

   Use flattened standard values in `Parameters_Update_GPHE.py`.

8. Add or extend verification scripts.

   Check that grouped variables generate a standard selector.

   Check that non-grouped variables still render normally.

   Check that saved project payload includes `geometric_standards`.

   Check that solver payload does not include `geometric_standards`.

## Compatibility Requirements

The following format must continue to work:

```python
'Ds': [0.2032, 0.254, 0.3048]
```

The new grouped format must also work:

```python
'Ds': {
    'TEMA': [0.2032, 0.254, 0.3048],
    'DIN': [0.8, 0.9, 1.0],
}
```

If no grouped standards are defined for a variable, no standard selector should be shown.

## Open Decision

Confirm the final grouped format before implementation.

Recommended final format:

```python
'Standard_Variables_Values': {
    'Ds': {
        'TEMA': [...],
        'DIN': [...],
    },
    'dte': [0.01905, 0.02540, 0.03175],
}
```
