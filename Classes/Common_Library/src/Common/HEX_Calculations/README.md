# HEX_Calculations

> Pure-math utilities for preliminary heat-exchanger (HEX) sizing and thermal analysis.  
> These modules provide the fundamental equations required to size or rate a shell-and-tube, plate, or any other indirect heat exchanger: the energy balance (heat load), the driving-force calculation (LMTD), fluid allocation, outlet temperature determination, and data-consistency verification.

---

## 📁 Module Index

| File | Function(s) | Purpose |
|------|-------------|---------|
| `Calculations_HEX_heatload.py` | `HEX_heat_load()` | Computes the heat duty exchanged by a single fluid stream. |
| `Calculations_HEX_LMTD.py` | `HEX_lmtd()` | Computes the Log Mean Temperature Difference between two fluid streams. |
| `Calculations_HEX_Consistency.py` | Multiple verification functions | Checks the consistency of HEX model parameters, temperatures, heat-load data, and input flags. |
| `Calculations_HEX_Allocation.py` | `allocation()` | Allocates fluid properties to tube-side (`t`) and shell-side (`s`) variables based on the specified tube fluid. |
| `Calculations_HEX_Tho_Tco.py` | `HEX_Tho_Tco()` | Calculates the unspecified outlet temperature (Tho or Tco) using either CoolProp or user-defined properties. |

---

## 1. `Calculations_HEX_heatload.py` — Heat-Load Calculation

### `HEX_heat_load(mass_flow_rate, specific_heat, inlet_temperature, outlet_temperature)`

Computes the sensible-heat load transferred to or from a fluid stream using the classic first-law energy balance:

$$\dot{Q} = \dot{m} \cdot c_p \cdot (T_{in} - T_{out})$$

### Parameters

| Parameter | Type | Unit | Description |
|-----------|------|------|-------------|
| `mass_flow_rate` | `float` | kg·s⁻¹ | Mass flow rate of the fluid. |
| `specific_heat` | `float` | J·(kg·K)⁻¹ | Specific heat capacity at constant pressure ($c_p$). |
| `inlet_temperature` | `float` | K | Fluid inlet temperature. |
| `outlet_temperature` | `float` | K | Fluid outlet temperature. |

### Returns

| Type | Unit | Description |
|------|------|-------------|
| `float` | W | Heat load $\dot{Q}$. **Positive** when the fluid **cools down** ($T_{in} > T_{out}$), i.e. heat is rejected. **Negative** when the fluid **heats up** ($T_{in} < T_{out}$), i.e. heat is absorbed. |

### Usage example

```python
from Common.HEX_Calculations.Calculations_HEX_heatload import HEX_heat_load

# Hot stream cooling from 90 °C to 50 °C
Q_hot = HEX_heat_load(
    mass_flow_rate=2.0,       # kg/s
    specific_heat=4200,       # J/(kg·K)  (water-like)
    inlet_temperature=363.15, # K  (90 °C)
    outlet_temperature=323.15 # K  (50 °C)
)
print(f"Heat rejected by hot stream: {Q_hot/1000:.2f} kW")
# → Heat rejected by hot stream: 336.00 kW

# Cold stream heating from 20 °C to 80 °C (same magnitude, opposite sign)
Q_cold = HEX_heat_load(
    mass_flow_rate=2.0,
    specific_heat=4200,
    inlet_temperature=293.15,  # K (20 °C)
    outlet_temperature=353.15  # K (80 °C)
)
print(f"Heat absorbed by cold stream: {Q_cold/1000:.2f} kW")
# → Heat absorbed by cold stream: -504.00 kW
```

### Notes

- The function assumes **constant $c_p$** over the temperature range. For large temperature spans or phase changes, use an enthalpy-based balance instead.
- No phase change is handled; this is a **sensible-heat-only** calculation.
- When used for HEX design, the hot-stream and cold-stream heat loads must balance (accounting for heat losses):
  $$\dot{Q}_{hot} + \dot{Q}_{cold} = 0$$

---

## 2. `Calculations_HEX_LMTD.py` — Log Mean Temperature Difference

### `HEX_lmtd(Thi, Tho, Tci, Tco)`

Computes the Log Mean Temperature Difference (LMTD), the effective average driving force for heat transfer in a shell-and-tube, plate, or double-pipe heat exchanger:

$$\Delta T_{lm} = \frac{\Delta T_1 - \Delta T_2}{\ln(\Delta T_1 / \Delta T_2)}$$

where

- $\Delta T_1 = T_{h,in} - T_{c,out}$ (largest terminal temperature difference)
- $\Delta T_2 = T_{h,out} - T_{c,in}$ (smallest terminal temperature difference)

### Parameters

| Parameter | Type | Unit | Description |
|-----------|------|------|-------------|
| `Thi` | `float` | K | Hot fluid **inlet** temperature. |
| `Tho` | `float` | K | Hot fluid **outlet** temperature. |
| `Tci` | `float` | K | Cold fluid **inlet** temperature. |
| `Tco` | `float` | K | Cold fluid **outlet** temperature. |

### Returns

| Type | Unit | Description |
|------|------|-------------|
| `float` | K | Log Mean Temperature Difference. |

### Raises

| Exception | Condition |
|-----------|-----------|
| `ValueError` | If either terminal temperature difference is **zero or negative** ($\Delta T_1 \leq 0$ or $\Delta T_2 \leq 0$). This prevents physically impossible configurations (e.g., cold outlet hotter than hot inlet in a pure counter-current exchanger). |

### Usage example

```python
from Common.HEX_Calculations.Calculations_HEX_LMTD import HEX_lmtd

# Counter-current HEX
# Hot:  150 °C → 100 °C
# Cold:  30 °C →  80 °C
lmtd = HEX_lmtd(
    Thi=423.15,  # K (150 °C)
    Tho=373.15,  # K (100 °C)
    Tci=303.15,  # K ( 30 °C)
    Tco=353.15   # K ( 80 °C)
)
print(f"LMTD = {lmtd:.2f} K")
# → LMTD = 70.00 K
```

### Notes

- The formula above assumes a **counter-current** arrangement. For **co-current** flow, swap the cold-side temperatures ($T_{c,in}$ and $T_{c,out}$) in the arguments, or equivalently redefine $\Delta T_1$ and $\Delta T_2$.
- When $\Delta T_1 \approx \Delta T_2$ (balanced exchanger), the LMTD tends to $\Delta T_1$ (arithmetic mean). The implementation uses `numpy.log` for numerical stability.
- Once $\dot{Q}$ and $\Delta T_{lm}$ are known, the required heat-transfer area follows from:
  $$A = \frac{\dot{Q}}{U \cdot \Delta T_{lm}}$$
  where $U$ is the overall heat-transfer coefficient.

---

## 3. `Calculations_HEX_Consistency.py` — Data Consistency Verification

This module provides common consistency checks for heat-exchanger model parameters and operating data. It is intended to be shared by different HEX models so that basic data validation is handled in a common calculation layer.

### Main functions

| Function | Purpose |
|----------|---------|
| `verification_positive_variables(m_p, save_result)` | Verifies that all numerical model parameters are non-negative. Exits on failure. |
| `verification_DeltaTmin(m_p, save_result)` | Verifies the presence of `DeltaT_min`; assigns a default value of 5 °C when absent. |
| `verification_Thi_Tho(m_p, save_result)` | Checks that hot-stream inlet temperature is greater than outlet ($T_{h,i} > T_{h,o}$). |
| `verification_Tco_Tci(m_p, save_result)` | Checks that cold-stream outlet temperature is greater than inlet ($T_{c,o} > T_{c,i}$). |
| `verification_Tco_Thi(m_p, save_result)` | Checks the minimum temperature approach between cold outlet and hot inlet ($T_{c,o} < T_{h,i} - \Delta T_{min}$). |
| `verification_Tci_Tho(m_p, save_result)` | Checks the minimum temperature approach between cold inlet and hot outlet ($T_{c,i} < T_{h,o} - \Delta T_{min}$). |
| `verification_heatload(m_p, save_result)` | Verifies consistency between hot- and cold-side heat loads. If the relative error exceeds $10^{-4}$, it **corrects `Tco`** to close the energy balance and pauses for user confirmation. |
| `verification_Tco_Thi_STHE(m_p, m_d, save_result)` | **STHE-specific** check: if $T_{c,o} > T_{h,o} - \Delta T_{min}$, restricts the exchanger to single-pass ($N_{pt} = 1$). |
| `verify_flag_inputs(m_p)` | Validates input flags: `Property_Source` must be `'CoolProp'` or `'User'`; `Outlet_Temperature_Spec` must be `'cold'` or `'hot'`; and the corresponding outlet temperature must be present. |

### Notes

- The functions operate directly on the model-parameter dictionary `m_p`.
- `save_result` is a callback used to report warnings, corrections, and consistency errors.
- Temperature consistency checks use `DeltaT_min` as the minimum allowed temperature approach.
- `verification_heatload` now **automatically updates `Tco`** when the energy balance is outside tolerance and prompts the user to press ENTER before continuing.
- This module centralizes common HEX consistency logic and avoids duplicating these checks in individual equipment models.

### Usage example

```python
from Common.HEX_Calculations.Calculations_HEX_Consistency import (
    verification_positive_variables,
    verification_DeltaTmin,
    verification_Thi_Tho,
    verification_Tco_Tci,
    verification_Tco_Thi,
    verification_Tci_Tho,
    verification_heatload,
    verify_flag_inputs,
)

# Run checks in sequence
m_p = verification_positive_variables(m_p, save_result)
m_p = verification_DeltaTmin(m_p, save_result)
m_p = verification_Thi_Tho(m_p, save_result)
m_p = verification_Tco_Tci(m_p, save_result)
m_p = verification_Tco_Thi(m_p, save_result)
m_p = verification_Tci_Tho(m_p, save_result)
m_p = verification_heatload(m_p, save_result)
verify_flag_inputs(m_p)
```

---

## 4. `Calculations_HEX_Allocation.py` — Fluid Allocation (Tube / Shell Side)

### `allocation(m_p)`

Allocates fluid properties to **tube-side** (`t`) and **shell-side** (`s`) variables based on the value of `m_p['yfluid']`. This is essential for shell-and-tube heat-exchanger (STHE) calculations where the geometric correlations depend on which fluid runs inside the tubes.

### Behavior

| `yfluid` | Tube side (`t`) | Shell side (`s`) |
|----------|-----------------|------------------|
| `'cold_stream'` | Cold fluid ($\dot{m}_c$, $\rho_c$, $c_{p,c}$, $\mu_c$, $k_c$, $R_{f,c}$, $\Delta P_{c,disp}$) | Hot fluid ($\dot{m}_h$, $\rho_h$, $c_{p,h}$, $\mu_h$, $k_h$, $R_{f,h}$, $\Delta P_{h,disp}$) |
| `'hot_stream'` | Hot fluid ($\dot{m}_h$, $\rho_h$, $c_{p,h}$, $\mu_h$, $k_h$, $R_{f,h}$, $\Delta P_{h,disp}$) | Cold fluid ($\dot{m}_c$, $\rho_c$, $c_{p,c}$, $\mu_c$, $k_c$, $R_{f,c}$, $\Delta P_{c,disp}$) |

### Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `m_p` | `dict` | Model-parameter dictionary containing hot- and cold-stream properties. Must include the key `yfluid` (`'cold_stream'` or `'hot_stream'`). |

### Returns

| Type | Description |
|------|-------------|
| `dict` | The updated `m_p` dictionary with tube-side (`mt`, `rot`, `Cpt`, `mit`, `kt`, `Rft`, `DPtdisp`) and shell-side (`ms`, `ros`, `Cps`, `mis`, `ks`, `Rfs`, `DPsdisp`) variables. |

### Usage example

```python
from Common.HEX_Calculations.Calculations_HEX_Allocation import allocation

m_p['yfluid'] = 'cold_stream'  # Cold fluid inside tubes
m_p = allocation(m_p)

print(f"Tube-side mass flow:   {m_p['mt']:.3f} kg/s")
print(f"Shell-side mass flow:  {m_p['ms']:.3f} kg/s")
```

### Notes

- The function performs an **in-place mapping**; the original hot/cold keys (`mh`, `mc`, etc.) remain unchanged.
- This allocation must be performed **before** any tube-side or shell-side heat-transfer or pressure-drop correlations are evaluated.

---

## 5. `Calculations_HEX_Tho_Tco.py` — Outlet Temperature Calculation

### `HEX_Tho_Tco(m_p)`

Calculates the **unspecified outlet temperature** — either $T_{h,o}$ or $T_{c,o}$ — depending on `Outlet_Temperature_Spec`. The calculation can use either:

- **`CoolProp`** (via `Common.Stream`): enthalpy-based energy balance with real-fluid properties.
- **`User`**: constant-$c_p$ energy balance with user-supplied specific heats.

When `Property_Source == 'CoolProp'`, the function also populates `m_p` with full stream objects and thermophysical properties at inlet and outlet conditions.

### Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `m_p` | `dict` | Model-parameter dictionary. Must contain `Outlet_Temperature_Spec`, `Property_Source`, and the required inlet/outlet temperatures. |

### Required keys in `m_p`

| Key | Condition | Description |
|-----|-----------|-------------|
| `Outlet_Temperature_Spec` | Always | `'cold'` → `Tco` is known, calculate `Tho`; `'hot'` → `Tho` is known, calculate `Tco`. |
| `Property_Source` | Always | `'CoolProp'` or `'User'`. |
| `Tco` | If `Outlet_Temperature_Spec == 'cold'` | Specified cold outlet temperature [°C]. |
| `Tho` | If `Outlet_Temperature_Spec == 'hot'` | Specified hot outlet temperature [°C]. |
| `Thi`, `Tci` | Always | Inlet temperatures [°C]. |
| `mh`, `mc` | Always | Mass flow rates [kg/s]. |
| `Cph`, `Cpc` | If `Property_Source == 'User'` | Specific heats [J/(kg·K)]. |
| `hot_composition`, `cold_composition` | If `Property_Source == 'CoolProp'` | Fluid composition strings. |
| `hot_pressure`, `cold_pressure` | If `Property_Source == 'CoolProp'` | Pressures [Pa]. |

### Returns

| Type | Description |
|------|-------------|
| `dict` | Updated `m_p` with the calculated outlet temperature (`Tho` or `Tco`). When `Property_Source == 'CoolProp'`, also includes stream objects (`hot_stream_in`, `hot_stream_out`, `cold_stream_in`, `cold_stream_out`) and thermophysical properties (`rho`, `Cp`, `mu`, `k`) at inlet and outlet. |

### Usage example — User-defined properties

```python
from Common.HEX_Calculations.Calculations_HEX_Tho_Tco import HEX_Tho_Tco

m_p = {
    'Outlet_Temperature_Spec': 'cold',
    'Property_Source': 'User',
    'Thi': 150.0,
    'Tci': 30.0,
    'Tco': 80.0,
    'mh': 5.0,
    'mc': 10.0,
    'Cph': 2100.0,
    'Cpc': 4180.0,
}

m_p = HEX_Tho_Tco(m_p)
print(f"Calculated Tho = {m_p['Tho']:.2f} °C")
# → Calculated Tho = 106.19 °C
```

### Usage example — CoolProp properties

```python
m_p = {
    'Outlet_Temperature_Spec': 'hot',
    'Property_Source': 'CoolProp',
    'Thi': 150.0,
    'Tho': 100.0,
    'Tci': 30.0,
    'mh': 5.0,
    'mc': 10.0,
    'hot_composition': 'Water',
    'cold_composition': 'Water',
    'hot_pressure': 101325,
    'cold_pressure': 101325,
}

m_p = HEX_Tho_Tco(m_p)
print(f"Calculated Tco = {m_p['Tco']:.2f} °C")
print(f"Hot inlet density = {m_p['roh']:.2f} kg/m³")
```

### Notes

- Temperatures are stored in **°C** inside `m_p`, but CoolProp calculations use **K** internally (conversion is handled automatically).
- When `Property_Source == 'CoolProp'`, the function creates `Stream` objects via `Common.Stream` and `ThermoBackend.HEOS`.
- For `Property_Source == 'User'`, the simple $Q = \dot{m} c_p \Delta T$ balance is used.
- The function raises `ValueError` if `Outlet_Temperature_Spec` is neither `'cold'` nor `'hot'`.

---

## 🔗 Relationship Between the Calculation Modules

Together, these calculation modules provide the core of the **rating**, **sizing**, **data-consistency**, **fluid-allocation**, and **outlet-temperature** workflow for a heat exchanger:

```
┌─────────────────────────┐
│   HEX_Tho_Tco()         │
│ (outlet temperature)    │
└───────────┬─────────────┘
            │
            ▼
┌─────────────────────────┐     ┌─────────────────────────┐
│  HEX_Consistency        │     │   HEX_Allocation()      │
│  (verify data)          │     │  (tube / shell side)    │
└───────────┬─────────────┘     └─────────────────────────┘
            │
            ▼
┌─────────────────────────┐     ┌─────────────────────────┐
│  HEX_heat_load()        │     │    HEX_lmtd()           │
│  (energy balance)       │     │  (driving force)        │
└───────────┬─────────────┘     └───────────┬─────────────┘
            │                               │
            ▼                               ▼
          Q̇ (W)                        ΔT_lm (K)
            │                               │
            └───────────────┬───────────────┘
                            │
                            ▼
                  A = Q̇ / (U · ΔT_lm)
```

- `HEX_Tho_Tco` resolves the unknown outlet temperature before any thermal sizing.
- `HEX_Consistency` validates temperatures, heat loads, and input flags.
- `HEX_Allocation` maps hot/cold properties to tube/shell side for STHE geometry.
- `HEX_heat_load` gives the **duty**.
- `HEX_lmtd` gives the **effective temperature difference**.
- Dividing one by the other (scaled by $U$) yields the **required heat-transfer area**.

---

## 🧪 Suggested Tests

| Test | What to check |
|------|---------------|
| Heat-load sign convention | Positive when $T_{in} > T_{out}$, negative when $T_{in} < T_{out}$. |
| Heat-load magnitude | Known hand-calculated values (e.g. water $\dot{m}=1$ kg/s, $\Delta T=10$ K, $c_p=4180$ J/(kg·K) → 41.8 kW). |
| LMTD — balanced case | When $\Delta T_1 = \Delta T_2$, LMTD should equal that common value. |
| LMTD — error handling | `ValueError` raised for $\Delta T \leq 0$ (e.g. hot inlet colder than cold outlet in counter-current). |
| LMTD — known values | Classic textbook examples (e.g. Kern, *Process Heat Transfer*). |
| Consistency — positive variables | `sys.exit()` triggered when any numerical parameter is negative. |
| Consistency — temperature relationships | Valid HEX temperature hierarchies and minimum temperature approaches. |
| Consistency — heat load | `Tco` auto-correction when $\dot{Q}_h \neq \dot{Q}_c$ within tolerance. |
| Consistency — STHE multipass | Restriction to $N_{pt}=1$ when $T_{c,o} > T_{h,o} - \Delta T_{min}$. |
| Consistency — flag inputs | `ValueError` for invalid `Property_Source` or `Outlet_Temperature_Spec`. |
| Allocation — cold in tubes | Tube-side variables match cold-stream properties; shell-side match hot-stream. |
| Allocation — hot in tubes | Tube-side variables match hot-stream properties; shell-side match cold-stream. |
| Tho_Tco — User mode | Correct $T_{h,o}$ or $T_{c,o}$ from constant-$c_p$ balance. |
| Tho_Tco — CoolProp mode | Correct outlet temperature and updated stream properties from enthalpy balance. |

---

## 📄 License

*Under construction*
