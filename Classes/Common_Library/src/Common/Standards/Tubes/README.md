# Tube Standards and Utilities

## Overview

`Tube.py` provides the common tube-handling logic used by the STHE
framework.

Its purpose is to separate **tube standard data** from the logic that
accesses, validates, selects, and interprets standard tubes.

The current implementation works with the TEMA D7M standard stored in:

``` text
Common/
└── Standards/
    └── Tubes/
        ├── Tables/
        │   └── TEMA.py
        │
        └── Tube.py
```

`Tube.py` imports the TEMA table directly:

``` python
from Common.Standards.Tubes.Tables.TEMA import TEMA
```

The TEMA table contains the available tube outside diameters, BWG values,
and corresponding wall thicknesses. The current D7M table stores these
dimensions in millimetres.

`Tube.py` converts outside diameter and wall thickness from millimetres
to metres when returning values through `get_tube_values()`.

------------------------------------------------------------------------

## Architecture

### `TEMA.py`

Contains the actual standard data.

The current structure uses a numeric `Tube_Index`:

``` python
TEMA = {
    'Source': {
        'Organization': 'TEMA',
        'Description': 'Tubing Standards'
    },
    'Standards': {
        'D7M': {
            'Units': {
                'Tube_Outside_Diameter': 'mm',
                'Tube_Wall_Thickness': 'mm'
            },
            'Tube_Index': {
                0: {
                    'Tube_Outside_Diameter': 6.35,
                    'Tube_BWG': 22,
                    'Tube_Wall_Thickness': 0.711
                },
                ...
            }
        }
    }
}
```

The table is the **source of truth** for standard tube dimensions.

The numeric `Tube_Index` identifies one specific standard
OD/BWG/wall-thickness combination.

### `Tube.py`

Contains the common logic to:

1. Access a tube standard.
2. Obtain properties for a specific `Tube_Index`.
3. Select the minimum standard wall thickness satisfying a required
   minimum thickness for a specified outside diameter.
4. Return the selected `Tube_Index` values.
5. Recover outside diameter, BWG, and wall thickness from one or more
   numeric `Tube_Index` values.
6. Support both scalar and NumPy-array tube evaluations.

This logic is implemented in `Common_Tube`.

------------------------------------------------------------------------

# `Common_Tube`

## 1. `get_tube_standard()`

``` python
Common_Tube.get_tube_standard(
    tube_source,
    tube_standard
)
```

Verifies that the requested source and standard exist and returns the
corresponding standard dictionary.

Example:

``` python
standard = Common_Tube.get_tube_standard(
    tube_source='TEMA',
    tube_standard='D7M'
)
```

Invalid sources or standards raise a `ValueError`.

------------------------------------------------------------------------

## 2. `get_tube_properties()`

``` python
Common_Tube.get_tube_properties(
    tube_source,
    tube_standard,
    tube_index
)
```

Retrieves the standard tube properties associated with a numeric
`Tube_Index`.

Example:

``` python
tube_properties = Common_Tube.get_tube_properties(
    tube_source='TEMA',
    tube_standard='D7M',
    tube_index=29
)
```

For the current D7M table, `Tube_Index = 29` corresponds to:

``` python
{
    'Tube_Outside_Diameter': 19.05,
    'Tube_BWG': 18,
    'Tube_Wall_Thickness': 1.245
}
```

The returned dimensional values are in the units used by the selected
standard table, which for the current D7M implementation are millimetres.

The method validates that the supplied `Tube_Index` exists in the selected
standard.

------------------------------------------------------------------------

## 3. `select_standard_tubes()`

``` python
Common_Tube.select_standard_tubes(
    tube_source,
    tube_standard,
    tube_outside_diameter=[],
    minimum_wall_thickness=0.0
)
```

This is the main tube-selection method.

For each requested outside diameter it:

1. Reads the available standard tube combinations.
2. Discards wall thicknesses below the required minimum.
3. Selects the **smallest standard wall thickness that satisfies the
   requirement**.
4. Returns the corresponding numeric `Tube_Index`.
5. Does not return thicker alternatives for the same outside diameter.

Therefore, the result contains **at most one `Tube_Index` per outside
diameter**.

### Example

For:

``` text
OD = 19.05 mm
Required wall thickness = 1.12 mm
```

the relevant D7M choices include:

``` text
BWG 20 → 0.889 mm   not sufficient
BWG 18 → 1.245 mm   selected
BWG 17 → 1.473 mm   thicker alternative
BWG 16 → 1.651 mm   thicker alternative
```

The selected result is the corresponding numeric index:

``` text
Tube_Index = 29
```

### Specific outside diameters

``` python
tube_outside_diameter=[19.05]
```

selects only that OD.

Multiple ODs can be supplied:

``` python
tube_outside_diameter=[19.05, 25.40, 31.75]
```

### All available outside diameters

An empty list:

``` python
tube_outside_diameter=[]
```

means:

``` text
Use every outside diameter available in the selected standard.
```

For each OD, the method selects the thinnest standard tube whose wall
thickness is greater than or equal to `minimum_wall_thickness`.

If no standard tube satisfies the minimum thickness for an OD, that OD
does not generate a candidate.

------------------------------------------------------------------------

# `Tube_Index`

The current implementation intentionally uses a **numeric index** instead
of a self-descriptive string such as:

``` text
D7M_OD19.05_BWG18_t1.245
```

A `Tube_Index` is simply the key of an entry in:

``` python
TEMA['Standards']['D7M']['Tube_Index']
```

For example:

``` python
Tube_Index = 29
```

maps to one specific standard tube:

``` text
OD  = 19.05 mm
BWG = 18
t   = 1.245 mm
```

This design keeps the optimization variable numeric and therefore
compatible with NumPy-based candidate-space generation.

The dimensional properties remain in the standard table rather than being
encoded into the optimization variable itself.

------------------------------------------------------------------------

# `get_tube_values()`

``` python
Common_Tube.get_tube_values(
    tube,
    tube_source='TEMA',
    tube_standard='D7M'
)
```

Converts one or more numeric `Tube_Index` values into the corresponding
tube properties:

``` text
dte → tube outside diameter
bwg → tube BWG
thk → tube wall thickness
```

The method supports two input modes.

## Scalar `Tube_Index`

Example:

``` python
dte, bwg, thk = Common_Tube.get_tube_values(
    29
)
```

For the current D7M table:

``` text
dte = 0.01905 m
bwg = 18
thk = 0.001245 m
```

Outside diameter and wall thickness are converted from millimetres to
metres.

## NumPy array of `Tube_Index`

The method also accepts a NumPy array:

``` python
tube = np.array([29, 49, 59, 71])

dte, bwg, thk = Common_Tube.get_tube_values(
    tube
)
```

The returned values are NumPy arrays:

``` text
dte = [0.01905 0.02540 0.03175 0.06350] m
bwg = [18 18 18 14]
thk = [0.001245 0.001245 0.001245 0.002108] m
```

The expected data types are:

``` text
dte → float64
bwg → int64
thk → float64
```

The vectorized implementation evaluates unique `Tube_Index` values and
then maps the results back to the original array positions.

This allows repeated tube indices to be handled without evaluating the
same table entry more than once.

## Empty NumPy array

If an empty NumPy array is supplied, the method returns empty arrays with
the appropriate data types:

``` text
dte → float array
bwg → int array
thk → float array
```

## Invalid indices

If a supplied `Tube_Index` does not exist in the selected standard, the
method raises a `ValueError`.

For scalar inputs, non-numeric values also raise a `ValueError`.

------------------------------------------------------------------------

# Units

The current D7M source table stores dimensions in millimetres:

``` text
Tube_Outside_Diameter → mm
Tube_Wall_Thickness   → mm
```

`get_tube_properties()` returns these values in the source-table units.

`get_tube_values()` converts dimensional values to SI metres:

``` text
dte → m
thk → m
bwg → dimensionless integer
```

This distinction is important because tube-selection calculations operate
on the units of the standard table, while the STHE model uses `dte` and
`thk` in metres.

------------------------------------------------------------------------

# Overall Workflow

The current tube-handling workflow is:

``` text
                  TEMA.py
                     │
                     ▼
             Standard tube data
                     │
                     ▼
          get_tube_standard()
                     │
                     ▼
        select_standard_tubes()
                     │
                     ▼
               Tube_Index
                     │
                     ▼
             get_tube_values()
                     │
              ┌──────┼──────┐
              ▼      ▼      ▼
             dte    bwg    thk
              │      │      │
              └──────┴──────┘
                     ▼
                 STHE Model
```

The conceptual flow is:

``` text
TEMA standard
      ↓
tube selection
      ↓
numeric Tube_Index
      ↓
tube properties
      ↓
STHE calculations
```

The important separation is that `Tube_Index` is the optimization-space
representation, while `dte`, `bwg`, and `thk` are the interpreted tube
properties used by engineering calculations.

------------------------------------------------------------------------

# Integration with the STHE Framework

The tube variable in the optimization problem is represented by the
numeric `Tube_Index`.

For example:

``` python
'Tube': 29
```

does not directly contain the tube dimensions.

When the STHE model requires the actual tube dimensions, the common
utility resolves the index:

``` python
dte, bwg, thk = Common_Tube.get_tube_values(Tube)
```

For vectorized model evaluations, the same method can receive a NumPy
array of indices and return NumPy arrays.

This keeps the optimization variable numeric and avoids introducing
strings or mixed-type objects into the NumPy candidate space.

------------------------------------------------------------------------

# Separation of Responsibilities

`Tube.py` is responsible only for **tube standards, tube selection, and
tube interpretation**.

It does not perform STHE optimization constraints.

The intended framework separation is:

``` text
TEMA.py
   ↓
Standard data

Common_Tube
   ↓
Access / selection / interpretation

Consistency
   ↓
Builds and validates the search space

Constraints
   ↓
Restricts the search space using engineering equations
```

The fundamental distinction is:

> **Consistency builds/validates the search space; Constraints restrict
> it according to the problem equations.**

`Common_Tube` provides the interface needed by both layers without moving
engineering constraint logic into the tube-standard utility.

------------------------------------------------------------------------

# Current Scope

The current implementation supports:

- TEMA as the tube data source.
- TEMA D7M as the current tube standard.
- Numeric `Tube_Index` values.
- Tube outside diameter.
- Tube BWG.
- Tube wall thickness.
- Selection based on a required minimum wall thickness.
- One selected standard tube per outside diameter.
- Scalar tube-property retrieval.
- NumPy-array tube-property retrieval.
- Conversion of outside diameter and wall thickness from mm to m in
  `get_tube_values()`.
- Validation of tube sources, standards, and indices.

The current D7M table contains the standard OD/BWG/wall-thickness
combinations used by this implementation.

------------------------------------------------------------------------

# Important Design Principle

The tube dimensions are **not duplicated inside the optimization
variable**.

The optimization variable contains only:

``` text
Tube_Index
```

The standard table contains:

``` text
Tube_Index
      ↓
Outside Diameter
BWG
Wall Thickness
```

This provides a single source of truth for standard tube dimensions and
allows the same interpretation logic to be used consistently throughout
the STHE framework.

------------------------------------------------------------------------

# Future Extensions

The structure is intended to allow additional tube sources and standards
to be added without changing the general tube-handling concept.

For example:

``` text
TEMA
 ├── D7
 └── D7M

Commercial
 ├── Supplier_A
 ├── Supplier_B
 └── Supplier_C
```

The common interface can continue to expose:

``` text
source
standard
Tube_Index
      ↓
tube properties
```

The key principle is:

> **Standard data remain separated from common tube-handling logic.**

As the framework evolves, `Consistency` can use `Common_Tube` to construct
the tube portion of the optimization search space, while the engineering
constraint layer remains responsible for feasibility calculations.

------------------------------------------------------------------------

# Summary of Public Methods

| Method | Purpose | Main Input | Output |
|---|---|---|---|
| `get_tube_standard()` | Validate and access a standard | source, standard | standard dictionary |
| `get_tube_properties()` | Retrieve table data for one tube | `Tube_Index` | OD, BWG, thickness in table units |
| `select_standard_tubes()` | Select standard tubes satisfying minimum thickness | OD(s), minimum thickness | numeric `Tube_Index` list |
| `get_tube_values()` | Interpret tube index for STHE calculations | scalar/array `Tube_Index` | `dte`, `bwg`, `thk` |

