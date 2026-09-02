# Tube Standards and Utilities

## Overview

`Tube.py` provides the common tube-handling logic used by the STHE
framework.

Its purpose is to separate **tube standard data** from the logic that
accesses and selects tubes.

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

The TEMA table contains the available tube outside diameters, BWG
values, and corresponding wall thicknesses. The current D7M table stores
these dimensions in millimetres.

------------------------------------------------------------------------

## Architecture

### `TEMA.py`

Contains the actual standard data.

The current structure is:

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
            'Tube_Outside_Diameter': {
                ...
            }
        }
    }
}
```

The table is the **source of truth** for standard tube dimensions.

### `Tube.py`

Contains the common logic to:

1.  Access a tube standard.
2.  Obtain properties for a specific OD/BWG combination.
3.  Select the minimum standard wall thickness satisfying a required
    minimum thickness.
4.  Generate a self-descriptive `Tube_ID`.
5.  Recover OD, BWG, and wall thickness directly from the `Tube_ID`.

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
    tube_outside_diameter,
    tube_bwg
)
```

Retrieves the wall thickness associated with a specific OD/BWG
combination.

Example:

``` python
tube_properties = Common_Tube.get_tube_properties(
    tube_source='TEMA',
    tube_standard='D7M',
    tube_outside_diameter=19.05,
    tube_bwg=18
)
```

Result:

``` python
{
    'Tube_Outside_Diameter': 19.05,
    'Tube_BWG': 18,
    'Tube_Wall_Thickness': 1.245
}
```

The method validates both the outside diameter and the BWG available for
that diameter.

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

For each outside diameter it:

1.  Reads the available BWG/thickness combinations.
2.  Discards thicknesses below the required minimum.
3.  Selects the **smallest standard wall thickness that satisfies the
    requirement**.
4.  Generates one `Tube_ID`.
5.  Does not return thicker alternatives for the same OD.

Therefore, the result contains **at most one tube per outside
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

The selected tube is:

``` text
D7M_OD19.05_BWG18_t1.245
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

> Use every outside diameter available in the selected standard.

For a required thickness of `1.12 mm`, the current D7M table produces
one candidate for each OD that has a valid standard thickness.

------------------------------------------------------------------------

# `Tube_ID`

The selected tube is represented by a self-descriptive string:

``` text
<STANDARD>_OD<OUTSIDE_DIAMETER>_BWG<BWG>_t<WALL_THICKNESS>
```

Example:

``` text
D7M_OD19.05_BWG18_t1.245
```

This avoids artificial identifiers such as:

``` text
tube1
tube2
tube3
```

The identifier itself contains the relevant dimensional information.

------------------------------------------------------------------------

# `get_tube_values()`

``` python
Common_Tube.get_tube_values(tube)
```

Extracts the tube values directly from a `Tube_ID`.

Example:

``` python
dte, bwg, thk = Common_Tube.get_tube_values(
    'D7M_OD19.05_BWG18_t1.245'
)
```

Returns:

``` text
dte = 19.05
bwg = 18
thk = 1.245
```

This method does not need to query `TEMA.py`, because the `Tube_ID`
already contains the selected dimensions.

This is particularly useful during repeated STHE model evaluations.

------------------------------------------------------------------------

# Overall Workflow

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
             required thickness
                    │
                    ▼
                 Tube_ID
                    │
                    ▼
          get_tube_values()
                    │
             ┌──────┼──────┐
             ▼      ▼      ▼
            dte    bwg    thk
```

The conceptual flow is:

``` text
TEMA standard
      ↓
tube selection
      ↓
Tube_ID
      ↓
tube dimensions
```

------------------------------------------------------------------------

# Separation of Responsibilities

`Tube.py` is responsible only for **tube standards and tube
interpretation**.

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

------------------------------------------------------------------------

# Current Scope

The current implementation supports:

-   TEMA as the tube data source.
-   TEMA D7M as the current tube standard.
-   Outside diameter.
-   BWG.
-   Wall thickness.
-   Selection based on minimum required wall thickness.
-   One selected standard tube per outside diameter.
-   Self-descriptive `Tube_ID` values.
-   Direct extraction of OD, BWG, and wall thickness from `Tube_ID`.

The current D7M table contains the standard OD/BWG/wall-thickness
combinations used by this implementation.

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

The key principle is:

> **Standard data remain separated from common tube-handling logic.**

As the framework evolves, `Consistency` can use `Common_Tube` to
construct the tube portion of the optimization search space, while the
engineering constraint layer remains responsible for feasibility
calculations.
