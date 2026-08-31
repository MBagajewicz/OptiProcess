# Model_Loader

> Generic dynamic loader for model definitions.  
> Dynamically imports model-definition modules and retrieves the corresponding model object based on a given model name.

---

## 📁 File

| File | Class / Method | Purpose |
|------|----------------|---------|
| `Model_Loader.py` | `Model_Loader` (static class) | Dynamically imports `<Model>.Model.Model_Def_<Model>` and returns `Model_<Model>`. |

---

## Overview

`Model_Loader` is a utility class that enables **dynamic loading** of model definitions at runtime. Given a model name (e.g. `'STHE_1'`), it constructs the expected module path and object name, imports the module dynamically, and returns the model definition object.

This pattern is useful when:
- Multiple equipment models share a common code structure.
- The specific model to use is determined at runtime (e.g. from user input or a configuration file).
- You want to avoid hard-coding imports for every possible model.

---

## Class: `Model_Loader`

### `load(model_name)` — Static Method

Dynamically imports the model-definition module and returns the model object.

#### Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `model_name` | `str` | Name of the model to load. Must be a non-empty string. |

#### Returns

| Type | Description |
|------|-------------|
| `object` | The model definition object (`Model_<model_name>`). |

#### Raises

| Exception | Condition |
|-----------|-----------|
| `ValueError` | If `model_name` is empty or `None`. |
| `TypeError` | If `model_name` is not a string. |
| `ImportError` | If the constructed module cannot be imported. |
| `AttributeError` | If the expected model object is not found in the imported module. |

#### Naming convention

Given a `model_name`, the loader expects:

| Element | Pattern | Example (`model_name='STHE_1'`) |
|---------|---------|--------------------------------|
| **Module path** | `<model_name>.Model.Model_Def_<model_name>` | `STHE_1.Model.Model_Def_STHE_1` |
| **Object name** | `Model_<model_name>` | `Model_STHE_1` |

#### Usage example

```python
from Common.Utils.Model_Loader import Model_Loader

# Load the STHE_1 model definition
model = Model_Loader.load('STHE_1')

# Access model information
m_i = model['Model_Info']
variables = m_i['List_of_Variables']
standard_values = m_i['Standard_Variables_Values']

print(f"Variables: {variables}")
print(f"Standard values: {standard_values}")
```

#### Error handling example

```python
from Common.Utils.Model_Loader import Model_Loader

# Empty model name
try:
    Model_Loader.load('')
except ValueError as e:
    print(e)
# → Model name cannot be empty.

# Non-string model name
try:
    Model_Loader.load(123)
except TypeError as e:
    print(e)
# → Model name must be a string. Received: int

# Non-existent model
try:
    Model_Loader.load('NonExistentModel')
except ImportError as e:
    print(e)
# → Could not import model definition.
#   Model  : NonExistentModel
#   Module : NonExistentModel.Model.Model_Def_NonExistentModel
#   Error  : No module named 'NonExistentModel'

# Missing model object in module
try:
    Model_Loader.load('BrokenModel')
except AttributeError as e:
    print(e)
# → Model object 'Model_BrokenModel' was not found in module 'BrokenModel.Model.Model_Def_BrokenModel'.
```

---

## Expected module structure

For `Model_Loader.load('STHE_1')` to succeed, the following module structure must exist:

```
STHE_1/
└── Model/
    ├── __init__.py
    └── Model_Def_STHE_1.py
```

And `Model_Def_STHE_1.py` must define:

```python
# STHE_1/Model/Model_Def_STHE_1.py

Model_STHE_1 = {
    'Model_Info': {
        'List_of_Variables': ['Do', 'Npt', 'L', 'B', ...],
        'Standard_Variables_Values': {
            'Do': [0.0127, 0.01905, 0.0254],
            'Npt': [1, 2, 4, 6],
            # ...
        },
        # ... other model metadata
    },
    # ... other model sections
}
```

---

## Integration with other modules

`Model_Loader` is typically used by consistency-checking and model-setup modules such as `Calculations_Model_Consistency`:

```python
from Common.Utils.Model_Loader import Model_Loader

# Inside Calculations_Model_Consistency:
Imported_Model = Model_Loader.load(m_d['Type_Equipment'])
m_i = Imported_Model['Model_Info']
```

This decouples the generic consistency-checking logic from any specific equipment model, enabling the same code to work for shell-and-tube heat exchangers, plate heat exchangers, distillation columns, etc.

---

## 🧪 Suggested Tests

| Test | What to check |
|------|---------------|
| Valid model | Loading an existing model returns the correct object. |
| Empty string | `ValueError` is raised for empty model name. |
| Non-string | `TypeError` is raised for non-string input (int, list, None, etc.). |
| Missing module | `ImportError` is raised with a descriptive message when the module does not exist. |
| Missing object | `AttributeError` is raised when the module exists but the expected object is absent. |
| Correct object type | The returned object is the expected model dictionary/class. |
| Module caching | `importlib` caches imported modules; repeated loads of the same model should be efficient. |

---

## 📄 License

*Under construction*
