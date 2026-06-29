# MANUAL DE USUARIO — OptiAppsCreator / OptiHexx

**OptiHexx** es una aplicación web para optimización de intercambiadores de calor usando **Set Trimming** y **Smart Enumeration** con garantía de optimalidad global. La UI se genera automáticamente a partir de modelos Python y archivos YAML de metadatos de presentación.

> **Nota de nomenclatura actual:** los diseños de referencia read-only se muestran como **Design Tutorial Library**. Los antiguos `ExampleX.py` se tratan como tutoriales. Los **User Projects** son ahora contenedores de usuario que pueden incluir distintos **Designs** de uno o más modelos; cada Design es el caso resoluble individual y se almacena únicamente en el servidor.

> **Backup/Restore:** la aplicación ya no importa ni exporta Designs como archivos `.py`. Los Projects y Designs del usuario autenticado se respaldan mediante **Backup My Projects** y se restauran con **Restore Backup** desde un archivo JSON local. La restauración sobrescribe por defecto Projects/Designs con nombres coincidentes, incluyendo la descripción del Project.

---

## 1. Arquitectura

```
OptiAppsCreator/
├── common_ui.yaml               ← Metadatos globales (header, login, menú principal)
├── STHE/                        ← Directorio del modelo Shell & Tube
│   ├── STHE_ui.yaml             ← Metadatos UI específicos del modelo
│   ├── Examples_STHE.py         ← Instancias de problema (Example1..Example13)
│   ├── Model/
│   │   ├── Model_Def_STHE.py    ← Metadatos estructurales (variables, restricciones, OF)
│   │   ├── Output_Info.py       ← Cálculos post-optimización (21 campos)
│   │   ├── Parameters_Update_STHE.py
│   │   └── Constraints_and_OF_STHE.py
│   └── Calculations/            ← Modelo termohidráulico
├── GPHE/                        ← Directorio del modelo Gasketed Plate
│   ├── GPHE_ui.yaml
│   ├── Examples_GPHE.py
│   ├── Model/
│   │   ├── Model_Def_GPHE.py
│   │   ├── Output_Info.py       ← Cálculos post-optimización (36 campos)
│   │   ├── Parameters_Update_GPHE.py
│   │   └── Constraints_and_OF_GPHE.py
│   └── Calculations/
├── OptiCode/                    ← Motor de optimización compartido
├── Common_Equations_HEX/        ← Ecuaciones comunes (LMTD, carga térmica)
├── templates/                   ← Plantillas Jinja2
│   ├── login.html
│   ├── main_menu.html
│   ├── problem_data.html
│   ├── geometric_options.html
│   └── results.html
├── generate_ui.py               ← Generador HTML (YAML + .py → HTML)
├── solver_runner.py             ← Ejecutor del solver (JSON in → JSON out)
├── solver_api.py                ← Servidor FastAPI (/ui/ + /api/optimize)
├── requirements.txt             ← Dependencias
└── output/                      ← HTML generado
    ├── login.html
    ├── main_menu.html
    ├── STHE/
    │   ├── problem_data.html
    │   ├── geometric_options.html
    │   └── results.html
    └── GPHE/
        ├── problem_data.html
        ├── geometric_options.html
        └── results.html
```

**Flujo de generación de UI:**

```
common_ui.yaml ──────────┐
Model_Def_{M}.py ────────┼──► generate_ui.py ──► output/*.html
Examples_{M}.py ─────────┤                       output/{M}/*.html
{M}_ui.yaml ─────────────┘
```

**Flujo en tiempo de ejecución:**

```
Navegador (problem_data.html)
    │ sessionStorage
    ▼
Navegador (geometric_options.html)
    │ sessionStorage
    ▼
Navegador (results.html) ──► POST /api/optimize ──► solver_runner.py ──► pipeline OptiProcess ──► JSON
```

---

## 2. Prerrequisitos

| Dependencia | Propósito |
|-------------|-----------|
| Python ≥ 3.10 | Runtime |
| numpy, scipy | Motor del solver |
| pyyaml | Parseo de YAML |
| jinja2 | Renderizado de plantillas HTML |
| fastapi, uvicorn | Servidor API |
| Tailwind CSS | Cargado desde CDN (sin instalación) |

```bash
pip install -r requirements.txt
```

---

## 3. Inicio Rápido

### 3.1 Generar las páginas

```bash
cd OptiAppsCreator
python generate_ui.py --all                    # todos los modelos activos
# o:
python generate_ui.py --model STHE GPHE        # modelos específicos
# o:
python generate_ui.py                          # solo STHE (default)
```

Esto produce:

```
output/login.html               ← compartido, generado una vez
output/main_menu.html           ← compartido, generado una vez
output/STHE/problem_data.html   ← pre-llenado con defaults de Example1
output/STHE/geometric_options.html
output/STHE/results.html
output/GPHE/problem_data.html
output/GPHE/geometric_options.html
output/GPHE/results.html
```

### 3.2 Iniciar el servidor

```bash
cd OptiAppsCreator
uvicorn solver_api:app --host 127.0.0.1 --port 8000
```

Un solo proceso sirve:
- **UI web** en `/ui/` (HTML estático)
- **API REST** en `/api/` (POST /api/optimize)

### 3.3 Abrir la aplicación

Abrir **http://127.0.0.1:8000/ui/main_menu.html** en el navegador.

> **No** abrir los `.html` directamente desde disco (`file://`). El navegador bloquea llamadas `fetch` cross-origin a `http://127.0.0.1:8000`.

### 3.4 Flujo del usuario

1. **Main Menu** → seleccionar tipo de intercambiador
2. **Problem Data** → revisar/editar parámetros → **Next: Geometric Options →**
3. **Geometric Options** → marcar/desmarcar rangos de variables discretas → **Run Optimization →**
4. **Results** → la página llama al API y llena todas las tablas automáticamente

### 3.5 Configuración SMTP para correos de usuarios

El sistema de usuarios envía correos para:

- Primer login con contraseña inicial importada desde Excel.
- Recuperación de contraseña mediante **I forgot my password**.
- Enlaces de actualización de password de un solo uso.

La configuración SMTP se realiza mediante un archivo local `.env` dentro de `OptiAppsCreator/`.

1. Copiar el archivo de ejemplo:

```bash
cd OptiAppsCreator
cp .env.example .env
```

2. Editar `.env` con los datos reales del servidor SMTP:

```env
AUTH_DB_PATH=data/users.db

SMTP_HOST=smtp.example.com
SMTP_PORT=587
SMTP_USER=user@example.com
SMTP_PASSWORD=change_me
SMTP_FROM=user@example.com
SMTP_USE_TLS=true
SMTP_TIMEOUT=10

APP_BASE_URL=http://127.0.0.1:8000
SESSION_COOKIE_NAME=optihex_session
SESSION_HOURS=8
```

| Variable | Descripción |
|----------|-------------|
| `AUTH_DB_PATH` | Ruta de la base SQLite de usuarios. Default recomendado: `data/users.db` |
| `SMTP_HOST` | Host SMTP. Ejemplo: `smtp.gmail.com`, `smtp.office365.com` |
| `SMTP_PORT` | Puerto SMTP. Usualmente `587` para STARTTLS |
| `SMTP_USER` | Usuario de autenticación SMTP |
| `SMTP_PASSWORD` | Password o app-password del servidor SMTP |
| `SMTP_FROM` | Remitente que verá el usuario |
| `SMTP_USE_TLS` | `true` para STARTTLS |
| `SMTP_TIMEOUT` | Timeout de conexión SMTP en segundos |
| `APP_BASE_URL` | URL pública/base de la app. Se usa para generar links de reset |
| `SESSION_COOKIE_NAME` | Nombre de la cookie de sesión |
| `SESSION_HOURS` | Duración de sesión activa en horas |

> Para Gmail, normalmente se debe usar una **App Password**, no la contraseña normal de la cuenta.

3. Inicializar usuarios desde Excel:

El archivo Excel debe contener exactamente estas columnas:

```text
username | email | password
```

Ejecutar:

```bash
python init_users_from_excel.py --file data/users_import.xlsx
```

Esto crea/actualiza la base de datos `data/users.db`, hashea los passwords y marca a los usuarios para cambio obligatorio de contraseña en el primer login.

4. Probar envío de correos:

- Iniciar el servidor con `uvicorn solver_api:app --host 127.0.0.1 --port 8000`.
- Abrir `http://127.0.0.1:8000/ui/login.html`.
- Ingresar con usuario y password inicial.
- El sistema registra el IP, genera un token válido por 24 horas y envía un correo con el enlace:

```text
{APP_BASE_URL}/ui/reset_password.html?token=...
```

5. Recuperación de contraseña:

- En `login.html`, usar **I forgot my password**.
- Ingresar el email del usuario.
- Si el email existe en la base, se envía un enlace válido por 1 hora.
- Por seguridad, si el email no existe, la respuesta visible es la misma.

6. Modo desarrollo sin SMTP:

Si `SMTP_HOST` no está configurado, el sistema no falla: imprime el contenido del email en la consola del servidor. Esto permite probar el flujo completo sin servidor SMTP real.

Si `SMTP_HOST` está configurado pero el servidor no responde, rechaza la conexión o expira el timeout, el sistema registra el error en consola y también imprime el email como fallback. En ese caso revisar:

- `SMTP_HOST`
- `SMTP_PORT`
- `SMTP_USE_TLS`
- firewall/red
- credenciales SMTP
- si el proveedor requiere app-password

7. Seguridad de archivos:

Los siguientes archivos no deben versionarse:

```text
OptiAppsCreator/.env
OptiAppsCreator/data/users.db
OptiAppsCreator/data/users.db-journal
OptiAppsCreator/data/users.db-wal
OptiAppsCreator/data/users.db-shm
```

Ya están incluidos en `.gitignore`.

---

## 4. Referencia CLI

### `generate_ui.py`

```bash
python generate_ui.py [--model MODEL [MODEL ...]] [--all] [--example EXAMPLE] [--output OUTPUT] [--no-sort-numeric-options]
```

| Opción | Default | Descripción |
|--------|---------|-------------|
| `--model STHE GPHE` | `["STHE"]` | Nombres de modelos (ignorado si se usa `--all`) |
| `--all` | — | Genera todos los modelos marcados activos en `common_ui.yaml` |
| `--example` | `Example1` | Nombre del ejemplo para valores por defecto |
| `--output` | `output` | Directorio de salida |
| `--no-sort-numeric-options` | — | Desactiva el ordenamiento de listas numéricas en checkbox_grids |

Ejemplos:

```bash
python generate_ui.py                                    # solo STHE
python generate_ui.py --model STHE GPHE
python generate_ui.py --all                              # todos los activos
python generate_ui.py --all --no-sort-numeric-options    # sin ordenar
```

### `solver_api.py`

```bash
uvicorn solver_api:app --host 127.0.0.1 --port 8000
```

| Opción | Default | Descripción |
|--------|---------|-------------|
| `--host` | `127.0.0.1` | Dirección de bind (`0.0.0.0` para acceso en red) |
| `--port` | `8000` | Puerto |
| `--reload` | off | Reinicio automático (solo desarrollo) |

---

## 5. Referencia de la API REST

### `GET /api/health`

```json
{"status": "ok", "service": "OptiProcess Solver API"}
```

### `POST /api/optimize`

**Request:**

| Campo | Tipo | Requerido | Descripción |
|-------|------|-----------|-------------|
| `model` | string | sí | Nombre del modelo (`"STHE"`, `"GPHE"`) |
| `parameters` | object | sí | Pares clave-valor de `Model_Parameters` |
| `discrete_variables` | object | sí | `{"Ds": [...], "dte": [...], ...}` |
| `selected_of` | string | no | `"TAC_OF"`, `"CAPEX_OF"`, `"AREA_OF"` (default: `"TAC_OF"`) |
| `number_of_equipment` | int | no | Número de equipos (default: 1) |

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
        "Nt": 302, "A_total": 146.9, "A_shell": 146.9, "A_ratio": 1.16, "F": 0.971
    },
    "number_of_solutions": 1,
    "elapsed_seconds": 0.19
}
```

| Campo | Tipo | Descripción |
|-------|------|-------------|
| `status` | string | `"ok"` o `"error"` |
| `model` | string | Nombre del modelo |
| `objective` | object | Función, variable, valor y unidad de la OF |
| `optimal_variables` | object | Valores óptimos de variables discretas |
| `calculations` | object | Resultados intermedios (21 campos STHE, 36 GPHE) |
| `number_of_solutions` | int | Cantidad de candidatos igualmente óptimos |
| `elapsed_seconds` | number | Tiempo de ejecución del solver |

### `POST /api/models/{model}/calculated-inputs`

Endpoint liviano para recalcular campos de entrada marcados como `(calculated)` sin ejecutar la optimización completa.

Se usa desde `Problem Data` cuando el usuario modifica un campo o presiona `ENTER`. El navegador envía los `parameters` actuales, el servidor completa faltantes desde `Default_Design.py`, ejecuta la lógica Python mínima de cálculo/consistencia y devuelve solo los campos calculados actualizados.

**Request:**

```json
{
    "parameters": {
        "mh": 20,
        "Cph": 2840,
        "Thi": 120,
        "Tho": 80,
        "mc": 60,
        "Cpc": 4187,
        "Tci": 47,
        "Tco": 56
    }
}
```

**Response:**

```json
{
    "status": "ok",
    "model": "STHE",
    "parameters": {
        "Tco": 56.0
    },
    "consistency": {
        "passed": true,
        "warnings": [],
        "mandatory_failures": []
    }
}
```

Este endpoint no ejecuta Set Trimming, Enumeration ni el solver completo. Solo actualiza campos calculados de entrada.

---

## 6. Formato de los Archivos YAML

OptiAppsCreator usa dos tipos de archivos YAML:

1. **`common_ui.yaml`** — metadatos globales compartidos entre todos los modelos.
2. **`{Modelo}/{Modelo}_ui.yaml`** — metadatos específicos de un modelo.

### 6.1 `common_ui.yaml` — Metadatos Globales

Define la cabecera, la página de login y el menú principal. Se carga una sola vez, independientemente del modelo.

```yaml
# ============================================================
# HEADER — usado en todas las páginas
# ============================================================
header:
  title: "OptiHexx"                              # Título principal
  subtitle: "Heat Exchanger Optimal Design Suite" # Subtítulo
  prototype: "Prototype P07"                      # Versión

# ============================================================
# LOGIN PAGE
# ============================================================
login:
  default_user: "|"                               # Usuario por defecto (decorativo)

# ============================================================
# MAIN MENU — lista de todos los tipos de intercambiador conocidos
# ============================================================
available_models:
  - {id: "STHE", label: "Shell & Tube", active: true, link: "STHE/problem_data.html"}
  - {id: "GPHE", label: "Plate Exchangers", active: true, link: "GPHE/problem_data.html"}
  - {id: "DoublePipe", label: "Double Pipe Structures", active: false, link: "#"}
```

**Etiquetas:**

| Etiqueta | Padre | Significado |
|----------|-------|-------------|
| `header` | raíz | Datos de cabecera para todas las páginas |
| `header.title` | header | Título de la aplicación |
| `header.subtitle` | header | Subtítulo descriptivo |
| `header.prototype` | header | Identificador de versión/prototipo |
| `login` | raíz | Configuración de la página de login |
| `login.default_user` | login | Usuario pre-llenado (decorativo) |
| `available_models` | raíz | Lista de modelos para el menú principal |
| `available_models[].id` | item | Identificador del modelo (debe coincidir con el nombre del directorio) |
| `available_models[].label` | item | Etiqueta visible en el botón del menú |
| `available_models[].active` | item | `true` si el modelo está activo, `false` si está en gris |
| `available_models[].link` | item | URL relativa desde `output/` hacia la página `problem_data` del modelo |

---

### 6.2 `{Modelo}_ui.yaml` — Metadatos Específicos del Modelo

Define la presentación de las tres ventanas del modelo: Problem Data, Geometric Options y Results.

#### 6.2.1 Estructura General

```yaml
model:                          # Identificación del modelo
  display_name: "Shell & Tube"  # Nombre para mostrar
  icon: "fa-industry"           # Clase FontAwesome (no usado actualmente)

pages:                          # Páginas del modelo
  problem_data:    {...}        # Ventana 1: datos del problema
  geometric_options: {...}      # Ventana 2: opciones geométricas
  results:         {...}        # Ventana 3: resultados
```

---

#### 6.2.2 Página: `problem_data`

Define los paneles de entrada de datos del problema (temperaturas, caudales, propiedades, economía).

**Etiquetas de `problem_data`:**

| Etiqueta | Nivel | Significado |
|----------|-------|-------------|
| `title` | página | Título de la ventana |
| `columns` | página | Distribución de secciones en columnas. Cada elemento es una lista de IDs de sección. |
| `sections` | página | Diccionario de secciones, cada una con un ID único |

**Tipos de `element` (elementos de sección) para `problem_data`:**

| `element` | Renderiza | Usado para |
|-----------|-----------|------------|
| `radio_group` | Grupo de radio buttons | Selección de OF, asignación de fluido |
| `form_group` | Inputs de texto etiquetados | Propiedades de corrientes, economía |
| `limit_table` | Tabla de 3 columnas (mín / ítem / máx) | Límites de velocidad, Reynolds, L/D |
| `computed_display` | Campo de solo lectura | Valores calculados como LMTD o carga térmica |

##### `radio_group`

Grupo de botones de opción excluyente.

```yaml
optimization_target:
  title: "OPTIMIZATION TARGET"       # Título visible del panel
  element: radio_group               # Tipo de elemento
  source: "Model_Declarations"       # Fuente en Examples_{M}.py → EquipmentN.{source}
  source_key: "Selected_OF"          # Clave dentro de la fuente para el valor por defecto
  options:                           # Lista de opciones
    - {value: "TAC_OF", label: "TAC"}
    - {value: "CAPEX_OF", label: "CAPEX"}
    - {value: "AREA_OF", label: "AREA"}
```

| Etiqueta | Significado |
|----------|-------------|
| `title` | Título visible del panel |
| `element` | Debe ser `radio_group` |
| `source` | `"Model_Declarations"` o `"Model_Parameters"`. Indica de dónde leer el valor por defecto desde `Examples_{M}.py` |
| `source_key` | Clave dentro de `source` que contiene el valor preseleccionado |
| `options` | Lista de opciones. Cada opción tiene `value` (valor enviado al solver) y `label` (texto visible) |

> **Valor por defecto:** El generador lee `Equipment1.{source}.{source_key}` de `Examples_{M}.py` y marca la opción cuyo `value` coincida.

##### `form_group`

Grupo de campos de entrada de texto o select.

```yaml
hot_stream:
  title: "HOT STREAM"
  element: form_group
  color: red                         # red, blue, yellow, gray, green, pink
  source: "Model_Parameters"         # Fuente en Examples_{M}.py
  fields:
    Thi:                             # Clave del parámetro
      label: "Inlet Temperature"     # Etiqueta visible
      unit: "°C"                     # Unidad (se agrega a la etiqueta)
    Tho:
      label: "Outlet Temperature"
      unit: "°C"
    mh:
      label: "Flow Rate"
      unit: "kg/s"
    int_rate:                        # Ejemplo con factor de display
      label: "Interest"
      unit: "%"
      display_factor: 100           # Valor × 100 para mostrar (0.1 → 10%)
    Shell_Method:
      label: "Shell Method"
      element: select                # Renderiza <select> en vez de <input>
      options: ["Kern", "Bell"]      # Opciones del dropdown
    Tco:
      label: "Outlet Temperature"
      unit: "°C"
      computed_hint: true            # Campo deshabilitado (calculado)
```

| Etiqueta | Significado |
|----------|-------------|
| `title` | Título visible del panel |
| `element` | Debe ser `form_group` |
| `color` | Esquema de color: `red`, `blue`, `yellow`, `gray`, `green`, `pink` |
| `source` | `"Model_Parameters"`. Fuente de valores por defecto |
| `fields` | Diccionario clave → metadatos del campo |

**Metadatos por campo (`fields.{key}`):**

| Etiqueta | Significado |
|----------|-------------|
| `label` | Etiqueta visible (requerido) |
| `unit` | Unidad de medida (opcional, se agrega a la etiqueta) |
| `element` | `select` para dropdown, omitir para input de texto |
| `options` | Lista de strings para el dropdown (solo si `element: select`) |
| `display_factor` | Multiplicador para conversión de display (ej. `int_rate: 0.1` → mostrado como `10` si `display_factor: 100`). No afecta el valor enviado al solver. |
| `computed_hint` | `true` para deshabilitar el campo (valor calculado, no editable) |
| `default` | Valor por defecto si no existe en `Examples_{M}.py` |

##### Límites recomendados para `form_group`

Los campos de un `form_group` pueden tener límites recomendados definidos en el modelo Python, sin duplicar esos rangos en el YAML.

El generador busca opcionalmente este diccionario dentro de `Model_Info` en `{MODEL}/Model/Model_Def_{MODEL}.py`:

```python
"Model_Info": {
    ...
    "Recomended_Limit_Parameters": {
        "mh": (10, 150),
        "Cph": (1800, 4300),
        "int_rate": (0.05, 0.20),
    },
}
```

Si una key del YAML dentro de `fields` coincide con una key de `Recomended_Limit_Parameters`, el input generado recibe los atributos:

```html
data-recommended-min="10"
data-recommended-max="150"
```

Cuando el usuario carga un valor numérico fuera de ese rango, la celda se colorea en amarillo. Esto es una advertencia visual, no bloquea el guardado ni la optimización.

Ejemplo:

```yaml
hot_stream:
  title: "HOT STREAM"
  element: form_group
  color: red
  source: "Model_Parameters"
  fields:
    mh:
      label: "Flow Rate"
      unit: "kg/s"
```

Si `Model_Def_STHE.py` contiene:

```python
"Recomended_Limit_Parameters": {
    "mh": (10, 150),
}
```

entonces `mh` se marcará en amarillo si el usuario carga un valor menor que `10` o mayor que `150`.

Si el campo usa `display_factor`, los límites recomendados se convierten a la misma escala visible para el usuario. Por ejemplo, si el modelo guarda `int_rate` como fracción y el YAML muestra porcentaje:

```yaml
int_rate:
  label: "Interest"
  unit: "%"
  display_factor: 100
```

con:

```python
"int_rate": (0.05, 0.20)
```

la UI usa límites visibles `5.0` a `20.0`.

Por compatibilidad, si `Recomended_Limit_Parameters` no existe en `Model_Info`, el generador asume que ningún parámetro tiene límites recomendados. El modelo sigue funcionando sin cambios.

Para verificar esta regla:

```bash
cd OptiAppsCreator
python generate_ui.py --all
python scripts/verify_recommended_limits.py
```

##### Campos `computed_hint: true`

Un campo con:

```yaml
computed_hint: true
```

se renderiza como:

- campo deshabilitado;
- campo marcado visualmente con `(calculated)`;
- valor no editable por el usuario;
- valor actualizado desde servidor mediante `POST /api/models/{model}/calculated-inputs`.

Ejemplo:

```yaml
cold_stream:
  title: "COLD STREAM"
  element: form_group
  color: blue
  source: "Model_Parameters"
  fields:
    Tci:
      label: "Inlet Temperature"
      unit: "°C"
    Tco:
      label: "Outlet Temperature"
      unit: "°C"
      computed_hint: true
```

En este caso `Tco` se actualiza desde Python usando el balance de energía:

```text
Tco = Tci + mh * Cph * (Thi - Tho) / (mc * Cpc)
```

El navegador no debe duplicar fórmulas del modelo. La UI solo solicita el cálculo al servidor y actualiza el valor recibido.

##### Cómo agregar una nueva variable `(calculated)`

Para incorporar una nueva variable calculada de entrada:

1. Declarar el campo en `{MODEL}_ui.yaml` dentro de un `form_group`:

```yaml
NewVar:
  label: "New Calculated Variable"
  unit: "..."
  computed_hint: true
```

2. Asegurar que `NewVar` exista en `{MODEL}/Projects/Default_Design.py` dentro de `Equipment1["Model_Parameters"]`. Ese valor funciona como default inicial antes de cualquier recálculo interactivo.

3. Implementar el cálculo server-side en `solver_api.py`, dentro del flujo usado por `POST /api/models/{model}/calculated-inputs`. Actualmente ese flujo está centralizado en `build_calculated_inputs_response(...)` y helpers asociados.

4. Devolver el valor calculado en el objeto `parameters` de la respuesta:

```json
{
    "parameters": {
        "NewVar": 123.45
    }
}
```

5. Regenerar la UI:

```bash
python generate_ui.py --all
```

6. Probar en `Problem Data`:

- modificar un parámetro dependiente;
- presionar `ENTER` o cambiar de campo;
- confirmar que el campo `(calculated)` se actualiza;
- confirmar que `RUN` pasa a verde porque cambió el input del modelo.

**Regla de arquitectura:** las variables `(calculated)` de entrada deben calcularse del lado servidor. El frontend no debe implementar fórmulas del modelo; solo debe enviar los parámetros actuales y aplicar la respuesta.

##### `limit_table`

Tabla de límites con columnas: mínimo, ítem, máximo.

```yaml
flow_limits:
  title: "FLOW LIMITS"
  element: limit_table
  color: red
  source: "Model_Parameters"
  rows:
    - {item: "Tube velocity", unit: "m/s", lower: vtmin, upper: vtmax}
    - {item: "Shell velocity", unit: "m/s", lower: vsmin, upper: vsmax}
    - {item: "Tube Reynolds", lower: Retmin, upper: Retmax}
    - {item: "Shell Reynolds", lower: Resmin, upper: Resmax}
    - {item: "L/D ratio", lower: LBLD, upper: UBLD}
```

| Etiqueta | Significado |
|----------|-------------|
| `title` | Título visible del panel |
| `element` | Debe ser `limit_table` |
| `color` | `red` (único usado) |
| `source` | `"Model_Parameters"`. Fuente de valores por defecto |
| `rows` | Lista de filas de la tabla |

**Metadatos por fila (`rows[]`):**

| Etiqueta | Significado |
|----------|-------------|
| `item` | Etiqueta de la fila (columna central) |
| `unit` | Unidad (opcional, columna central) |
| `lower` | Clave del parámetro para el límite inferior |
| `upper` | Clave del parámetro para el límite superior |

##### `computed_display`

Panel de solo lectura para valores calculados por el servidor (sin enviar al solver).

```yaml
lmtd_display:
  title: ""
  element: computed_display
  color: pink
  rows:
    - {label: "LMTD (Calculated)", key: "LMTD", unit: "°C", computed: true}
```

| Etiqueta | Significado |
|----------|-------------|
| `element` | Debe ser `computed_display` |
| `color` | `pink` (único usado) |
| `rows` | Lista de filas |

Si una fila define `key`, el frontend la usa solo como identificador visual (`data-display-key`) para actualizar el valor devuelto por `POST /api/models/{model}/calculated-inputs`. No se guarda como `Model_Parameters` ni se envía al solver.

Para verificar esta regla después de modificar YAML, templates o cálculos server-side:

```bash
cd OptiAppsCreator
python generate_ui.py --all
python scripts/verify_computed_displays.py
```

---

#### 6.2.3 Página: `geometric_options`

Define los paneles de selección de variables discretas que el optimizador puede considerar.

**Etiquetas de `geometric_options`:**

| Etiqueta | Nivel | Significado |
|----------|-------|-------------|
| `title` | página | Título de la ventana |
| `columns` | página | Distribución de secciones en columnas |
| `sections` | página | Diccionario de secciones |

**Tipos de `element` para `geometric_options`:**

| `element` | Renderiza | Usado para |
|-----------|-----------|------------|
| `checkbox_grid` | Grilla de checkboxes | Variables discretas del modelo (Ds, dte, Npt, etc.) |
| `form_group` | Inputs de texto | Parámetros adicionales (opciones de tubo, Bell) |
| `computed_display` | Campo de solo lectura | Información complementaria |

##### `checkbox_grid`

Grilla de checkboxes con opciones seleccionables. Es el elemento principal de esta ventana.

**Caso A — Vinculado a una variable del modelo:**

```yaml
shell_diameter:
  title: "Shell Diameter"
  unit: "m"                         # Unidad mostrada en el título
  element: checkbox_grid
  color: yellow                     # brown, blue, yellow, brown_dark, red_dark, green
  variable: "Ds"                    # Nombre en List_of_Variables de Model_Def
```

| Etiqueta | Significado |
|----------|-------------|
| `title` | Título del panel |
| `unit` | Unidad (opcional, se agrega al título) |
| `element` | Debe ser `checkbox_grid` |
| `color` | `brown`, `blue`, `yellow`, `brown_dark`, `red_dark`, `green` |
| `variable` | Nombre de la variable (debe coincidir con `List_of_Variables` en `Model_Def_{M}.py`) |

> Las opciones disponibles (valores) se leen de `Model_Def_{M}.py → Standard_Variables_Values[variable]`.
> Las opciones preseleccionadas se leen de `Examples_{M}.py → Discrete_Values_of_Variables[índice]`.

**`value_labels` — etiquetas personalizadas para valores:**

```yaml
layouts:
  title: "Layouts Available"
  element: checkbox_grid
  color: blue
  variable: "lay"
  value_labels:                     # Mapa valor → etiqueta
    1: "Square (90°)"
    2: "Triangle (30°)"
    3: "Rotated Square (45°)"
```

Sin `value_labels`, el valor numérico se muestra como string directamente.

**Caso B — Estático (no vinculado a variable):**

```yaml
configurations:
  title: "Configurations Available"
  element: checkbox_grid
  color: brown
  static: true                      # No vinculado a variable del modelo
  items:
    - {value: "Series"}
    - {value: "Parallel"}
```

| Etiqueta | Significado |
|----------|-------------|
| `static` | `true` para previsualizar alternativas futuras sin vinculación al modelo |
| `items` | Lista explícita de opciones visibles |

Una sección `static: true` se usa para mostrar alternativas que todavía no existen como variables reales del modelo. Estas opciones:

- se leen solamente desde el YAML;
- no se leen desde `Standard_Variables_Values`;
- no se leen desde `Discrete_Values_of_Variables`;
- se muestran siempre marcadas (`checked`);
- no pueden ser modificadas por el usuario;
- se muestran con el indicador azul `(future)` junto al título;
- no se guardan en `sessionStorage` como variables geométricas;
- no se envían al solver.

Formato recomendado para una previsualización simple:

```yaml
items:
  - {value: "Series"}
  - {value: "Parallel"}
  - {value: "Hot series cold parallel"}
  - {value: "Cold series hot parallel"}
```

También se admite separar valor interno y texto visible:

```yaml
items:
  - {value: "series", label: "Series"}
```

Esto no genera problemas de renderizado, porque el generador usa `label` para mostrar texto y `value` como valor interno. Sin embargo, en secciones `static: true` el generador emite un warning si detecta `label`, ya que para previsualizaciones puramente visuales se recomienda `{value: "Texto visible"}`. El formato `value + label` solo debería usarse si se quiere reservar desde ahora el identificador interno que luego usará el modelo.

**Cómo convertir una sección `static: true` en variable real del modelo**

Cuando las alternativas estén implementadas en el solver, la sección debe dejar de ser estática y conectarse al modelo:

1. Elegir un nombre interno de variable, por ejemplo `Config` o `Nshell`.
2. Agregar ese nombre a `Model_Def_{M}.py → Model_Info["List_of_Variables"]`.
3. Agregar sus alternativas a `Model_Def_{M}.py → Model_Info["Standard_Variables_Values"]`.
4. Agregar la lista de alternativas seleccionadas en cada proyecto, dentro de `Discrete_Values_of_Variables`, respetando el orden de `List_of_Variables`.
5. Cambiar el YAML de:

```yaml
static: true
items:
  - {value: "Series"}
```

a:

```yaml
variable: "Config"
value_labels:
  series: "Series"
  parallel: "Parallel"
```

6. Adaptar `Parameters_Update`, `Constraints_and_OF`, módulos de `Calculations` y `Output_Info` si la nueva variable cambia cálculos, restricciones, costos, hidráulica o resultados.
7. Probar que la nueva variable aparece en `optimal_variables`, que afecta la solución esperada y que no rompe proyectos existentes.

##### `form_group` (en geometric_options)

Similar al de `problem_data`, pero con colores distintos.

```yaml
tube_options:
  title: "Tube Options"
  element: form_group
  color: brown_dark                 # brown_dark, red_dark, brown, etc.
  source: "Model_Parameters"
  fields:
    ktube: {label: "Thermal Conductivity", unit: "W/(m K)"}
    thk:   {label: "Tube Thickness", unit: "m"}
    LBLD:  {label: "Minimum Tube Length", unit: "m"}
    UBLD:  {label: "Maximum Tube Length", unit: "m"}
```

---

#### 6.2.4 Página: `results`

Define los paneles de la ventana de resultados. Los valores se llenan dinámicamente desde la respuesta del API.

**Etiquetas de `results`:**

| Etiqueta | Nivel | Significado |
|----------|-------|-------------|
| `title` | página | Título de la ventana |
| `columns` | página | Distribución de secciones en columnas |
| `sections` | página | Diccionario de secciones |

**Tipo de `element` para `results`:**

| `element` | Usado para |
|-----------|------------|
| `data_table` | Tablas de datos (único elemento disponible) |

##### `data_table`

Tabla de resultados con filas de datos. Puede contener subsecciones y filas de pie.

```yaml
hot_stream_results:
  title: "HOT STREAM"
  element: data_table
  color: green_display              # green_display, blue_display, yellow_display, red_display
  rows:                             # Filas de la tabla
    - {label: "Mass flow rate", key: "mh", unit: "kg/s"}
    - {label: "Inlet temperature", key: "Thi", unit: "°C"}
    - {label: "Viscosity", key: "mih", unit: "mPa s", display_factor: 1000}
```

| Etiqueta | Significado |
|----------|-------------|
| `title` | Título del panel |
| `element` | Debe ser `data_table` |
| `color` | `green_display`, `blue_display`, `yellow_display`, `red_display` |
| `rows` | Lista de filas |

**Metadatos por fila (`rows[]`):**

| Etiqueta | Significado |
|----------|-------------|
| `label` | Etiqueta visible (columna izquierda) |
| `key` | Clave que identifica el valor. Para parámetros de entrada: nombre del parámetro (`"mh"`, `"Thi"`). Para resultados calculados: nombre en `calculations` del JSON (`"vt"`, `"U"`, `"TAC"`). Para variables óptimas: nombre de la variable (`"Ds"`, `"Ntp"`) |
| `unit` | Unidad de medida (opcional) |
| `computed` | `true` si el valor viene del solver (cálculos intermedios) |
| `result_var` | `true` si el valor es una variable discreta óptima |
| `highlight` | `true` para texto en negrita |
| `display_factor` | Multiplicador para conversión de display (ej. `1000` para Pa·s → mPa·s) |

**Subsecciones (`subsections`):**

Tablas anidadas con sus propios títulos.

```yaml
thermo_properties:
  title: "THERMO PROPERTIES"
  element: data_table
  color: yellow_display
  subsections:                      # Sub-tablas con encabezados propios
    - title: "TUBE SIDE"
      rows:
        - {label: "Velocity flow", key: "vt", unit: "m/s", computed: true}
        - {label: "Reynolds number", key: "Ret", computed: true}
    - title: "SHELL SIDE"
      rows:
        - {label: "Velocity flow", key: "vs", unit: "m/s", computed: true}
        - {label: "Reynolds number", key: "Res", computed: true}
  footer_rows:                      # Filas debajo de todas las subsecciones
    - {label: "Overall HTC (dirty)", key: "U", unit: "W/(m² K)", computed: true}
    - {label: "Overall HTC (clean)", key: "Uc", unit: "W/(m² K)", computed: true}
```

| Etiqueta | Significado |
|----------|-------------|
| `subsections` | Lista de subsecciones, cada una con `title` y `rows` |
| `footer_rows` | Filas que aparecen después de todas las subsecciones |

**Subsección sin título dentro de `optimization_results`:**

```yaml
optimization_results:
  title: "OPTIMIZATION"
  element: data_table
  color: blue_display
  subsections:
    - title: ""                     # Sin título
      rows:
        - {label: "Objective function", key: "OF_value", unit_from: "OF", computed: true, highlight: true}
    - title: "ECONOMICS"
      rows:
        - {label: "Capital cost", key: "CAPEX", unit: "$", computed: true}
        - {label: "Total annualized cost", key: "TAC", unit: "$/y", computed: true}
```

La clave especial `OF_value` se llena desde `objective.value` de la respuesta del API, no desde `calculations`.

---

## 7. Cómo Agregar un Modelo Nuevo

### Paso 1: Crear estructura de directorio

```
MiModelo/
├── MiModelo_ui.yaml              ← Metadatos de presentación
├── Examples_MiModelo.py          ← Instancias de problema
├── Model/
│   ├── __init__.py
│   ├── Model_Def_MiModelo.py     ← Metadatos estructurales
│   ├── Parameters_Update_MiModelo.py
│   ├── Constraints_and_OF_MiModelo.py
│   └── Output_Info.py            ← Cálculos post-optimización (opcional)
├── Calculations/
│   └── (módulos termohidráulicos)
└── __init__.py
```

### Paso 2: Escribir `Model_Def_MiModelo.py`

Debe exportar `Model_MiModelo` con:

```python
Model_MiModelo = {
    "Model_Info": {
        "List_of_Variables": ["var1", "var2", ...],          # Orden de variables discretas
        "Standard_Variables_Values": {                        # Universo de opciones
            "var1": [val1, val2, ...],
            "var2": [val3, val4, ...],
        },
        "Objective_Function": {
            "Equation_Name": ["TAC_OF", "CAPEX_OF", "AREA_OF"],
            "Optimization_Variables_Names": ["TAC", "CAPEX", "Area"],
            "Unit_OF": ["$/year", "$", "m²"]
        },
        "Recomended_Limit_Parameters": {                     # Opcional
            "param1": (min_recomendado, max_recomendado),
        },
    },
    ...
}
```

`Recomended_Limit_Parameters` es opcional. Si no se define, la UI interpreta que el modelo no tiene límites recomendados para sus parámetros de entrada.

### Paso 3: Escribir `Examples_MiModelo.py`

Debe exportar al menos `Example1` con:

```python
Example1 = {
    "Number_of_Equipment": 1,
    "Equipment1": {
        "Model_Declarations": {
            "Type_Equipment": "MiModelo",
            "Discrete_Values_of_Variables": [
                [v1, v2, ...],    # var1
                [v3, v4, ...],    # var2  (mismo orden que List_of_Variables)
            ],
            "Selected_OF": ["TAC_OF"],
        },
        "Model_Parameters": {
            "param1": valor1,
            "param2": valor2,
            ...
        },
    },
}
```

### Paso 4: Escribir `Output_Info.py` (opcional)

```python
def build_output_info(optimal_vars, params, objective=None):
    """Calcula variables derivadas post-optimización."""
    return {
        "objective": objective or {},
        "calculations": {},  # dict con resultados intermedios
    }

def write_output_json(output_info, output_path):
    """Escribe el diccionario como JSON."""
    import json
    with open(output_path, "w") as f:
        json.dump(output_info, f, indent=2)
```

Si este archivo no existe, la API devuelve `calculations: {}` sin error.

### Paso 5: Escribir `MiModelo_ui.yaml`

Crear el YAML siguiendo el formato explicado en la Sección 6.2. Definir `model`, `pages.problem_data`, `pages.geometric_options` y `pages.results`.

### Paso 6: Registrar en `common_ui.yaml`

Agregar el modelo a la lista `available_models`:

```yaml
available_models:
  - {id: "MiModelo", label: "Mi Intercambiador", active: true, link: "MiModelo/problem_data.html"}
```

### Paso 7: Generar y probar

```bash
python generate_ui.py --all
uvicorn solver_api:app --host 127.0.0.1 --port 8000
```

---

## 8. Solución de Problemas

| Problema | Causa probable | Solución |
|----------|---------------|----------|
| **Todas las celdas muestran "—"** | El API no responde | Verificar que el servidor esté corriendo: `curl http://127.0.0.1:8000/api/health`. No usar `file://` |
| **"No input data found"** | Navegó directo a results.html | Ir al menú principal → modelo → Problem Data → Next → Geometric Options → Run |
| **"No feasible design found"** | Los rangos discretos son muy restrictivos | Ampliar rangos de Ds, L, Nb (STHE) o Ntp, Pl, Sa (GPHE) |
| **"Missing required parameters"** | Parámetros internos no enviados por la UI | Regenerar HTML: `python generate_ui.py --all`. El merge con Example1 inyecta los faltantes |
| **500 Internal Server Error** | Crash del solver | Revisar consola del servidor. Causas: parámetros faltantes, arrays vacíos, tipos inválidos |
| **Port 8000 ocupado** | Instancia previa corriendo | `pkill -f uvicorn` y reiniciar |
| **Error de importación** | Script ejecutado desde otro directorio | Ejecutar siempre desde `OptiAppsCreator/` |
| **Modelo no aparece en el menú** | No registrado en `common_ui.yaml` | Agregar entrada en `available_models` con `active: true` |
| **checkbox_grid vacío** | `variable` no coincide con `List_of_Variables` | Verificar que el nombre en el YAML coincida exactamente con el de `Model_Def` |
