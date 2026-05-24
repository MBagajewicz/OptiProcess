# Planificación para la creación del Creador de Aplicaciones de Optimización

## Objetivo

Definir un sistema que permita capturar los distintos modelos ya desarrollados, tomando como ejemplo el caso STHE, y que sea capaz de consumir la información en el directorio correspondiente para construir una aplicación web de optimización en forma automática.

## Estado: IMPLEMENTADO (enfoque híbrido)

La arquitectura híbrida propuesta fue implementada con éxito para el modelo STHE. Los 5 HTML se generan automáticamente y la aplicación web es funcional con resultados completos (variables óptimas, propiedades termohidráulicas, costos).

## Datos de partida

En el directorio **ejemplos-interfaz-grafica-html-estatica** se encuentran versiones base de las ventanas que sirvieron como modelo de diseño.

Las ventanas generadas automáticamente son: `login.html`, `main-menu.html`, `problem-data.html`, `geometric-options.html`, `results.html`.

La información se obtiene de:
- **STHE/Model/Model_Def_STHE.py** — estructura (variables, constraints, OF, valores estándar)
- **STHE/Examples_STHE.py** — defaults (parámetros de problema, selecciones discretas)
- **STHE/STHE_ui.yaml** — metadatos de presentación (labels, unidades, agrupaciones, layout)

## Opciones de implementación

### Opción 1: Parser de comentarios en Examples_STHE.py
**Veredicto: Descartada.** Frágil ante cambios de formato, requiere leer dos archivos Python simultáneamente.

### Opción 2: YAML estructurado completo
**Veredicto: Descartada.** Duplica el modelo de datos, riesgo de divergencia con los archivos Python.

### Opción 3: Híbrida (IMPLEMENTADA)
Model_Def + Examples como fuente de verdad estructural, YAML solo para metadatos de UI.

**Archivos del sistema:**
- `STHE/STHE_ui.yaml` — metadatos de presentación por página/panel/campo (~370 líneas)
- `templates/` — 6 plantillas Jinja2 (base, login, main_menu, problem_data, geometric_options, results)
- `generate_ui.py` — generador HTML (~480 líneas)
- `solver_runner.py` — ejecutor del solver vía JSON (~430 líneas)
- `solver_api.py` — servidor FastAPI + serving estático (~165 líneas)
- `requirements.txt` — dependencias pineadas

**Cómo usar:**
```bash
cd OptiAppsCreator
pip install -r requirements.txt
python generate_ui.py --model STHE --example Example1
uvicorn solver_api:app --host 127.0.0.1 --port 8000
# Abrir http://127.0.0.1:8000/ui/main_menu.html
```

Ver `USER_MANUAL.md` para documentación completa.
