# HEX_Calculations

> Pure-math utilities for preliminary heat-exchanger (HEX) sizing and thermal analysis.  
> These modules provide the two fundamental equations required to size or rate a shell-and-tube, plate, or any other indirect heat exchanger: the energy balance (heat load) and the driving-force calculation (LMTD).

---

## 📁 Module Index

| File | Function | Purpose |
|------|----------|---------|
| `Calculations_HEX_heatload.py` | `HEX_heat_load()` | Computes the heat duty exchanged by a single fluid stream. |
| `Calculations_HEX_LMTD.py` | `HEX_lmtd()` | Computes the Log Mean Temperature Difference between two fluid streams. |
| `Calculations_HEX_Consistency.py` | Consistency verification functions | Checks the consistency of HEX model parameters, temperatures, and heat-load data. |

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

# Cold stream heating from 20 °C to 60 °C (same magnitude, opposite sign)
Q_cold = HEX_heat_load(
    mass_flow_rate=2.0,
    specific_heat=4200,
    inlet_temperature=293.15,  # K (20 °C)
    outlet_temperature=353.15  # K (80 °C)
)
print(f"Heat absorbed by cold stream: {Q_cold/1000:.2f} kW")
# → Heat absorbed by cold stream: 504.00 kW
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
| `verification_positive_variables(m_p, save_result)` | Verifies that numerical model parameters are non-negative. |
| `verification_DeltaTmin(m_p, save_result)` | Verifies the presence of `DeltaT_min` and assigns a default value when it is not provided. |
| `verification_Thi_Tho(m_p, save_result)` | Checks the hot-stream inlet/outlet temperature relationship. |
| `verification_Tco_Tci(m_p, save_result)` | Checks the cold-stream inlet/outlet temperature relationship. |
| `verification_Tco_Thi(m_p, save_result)` | Checks the minimum temperature approach between cold outlet and hot inlet. |
| `verification_Tci_Tho(m_p, save_result)` | Checks the minimum temperature approach between cold inlet and hot outlet. |
| `verification_heatload(m_p, save_result)` | Verifies consistency between the hot- and cold-side heat loads and updates the cold outlet temperature when the implemented consistency criterion requires it. |

### Notes

- The functions operate directly on the model-parameter dictionary `m_p`.
- `save_result` is used to report warnings, corrections, and consistency errors.
- Temperature consistency checks use `DeltaT_min` as the minimum allowed temperature approach.
- This module is intended to centralize common HEX consistency logic and avoid duplicating these checks in individual equipment models.

### Usage example

```python
from Common.HEX_Calculations.Calculations_HEX_Consistency import verification_heatload

m_p = verification_heatload(m_p, save_result)
```

## 🔗 Relationship Between the Calculation Modules

Together, these calculation modules provide the core of the **rating**, **sizing**, and **data-consistency** workflow for a heat exchanger. The heat-load and LMTD calculations provide the thermal quantities, while the consistency module validates the input data and temperature/energy relationships before the equipment calculations proceed:

```
┌─────────────────────┐     ┌─────────────────────┐
│  HEX_heat_load()    │     │    HEX_lmtd()       │
│  (energy balance)   │     │  (driving force)    │
└─────────┬───────────┘     └─────────┬───────────┘
          │                           │
          ▼                           ▼
        Q̇ (W)                    ΔT_lm (K)
          │                           │
          └───────────┬───────────────┘
                      │
                      ▼
            A = Q̇ / (U · ΔT_lm)
```

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
| Consistency checks | Valid HEX temperature relationships, minimum temperature approach, positive parameters, and heat-load consistency. |

---

## 📄 License

*Under construction*
