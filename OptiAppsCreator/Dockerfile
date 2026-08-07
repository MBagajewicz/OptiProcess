FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

RUN apt-get update \
    && apt-get install --no-install-recommends --yes libgomp1 \
    && rm -rf /var/lib/apt/lists/* \
    && groupadd --system --gid 10001 optiapp \
    && useradd --system --uid 10001 --gid optiapp --home-dir /app optiapp

WORKDIR /app

COPY requirements-runtime.txt .
RUN pip install --no-cache-dir --requirement requirements-runtime.txt

COPY solver_api.py solver_runner.py project_store.py auth_db.py standard_values.py init_users_from_excel.py ./
COPY OptiCode/ ./OptiCode/
COPY Common_Equations_HEX/ ./Common_Equations_HEX/

COPY STHE/__init__.py ./STHE/
COPY STHE/Model/ ./STHE/Model/
COPY STHE/Calculations/ ./STHE/Calculations/
COPY STHE/Projects/Default_Design.py ./STHE/Projects/Default_Design.py
COPY STHE/Projects/Example_Projects/ ./STHE/Projects/Example_Projects/

COPY GPHE/__init__.py ./GPHE/
COPY GPHE/Model/ ./GPHE/Model/
COPY GPHE/Calculations/ ./GPHE/Calculations/
COPY GPHE/Projects/Default_Design.py ./GPHE/Projects/Default_Design.py
COPY GPHE/Projects/Example_Projects/ ./GPHE/Projects/Example_Projects/

COPY output/ ./output/
COPY docker-entrypoint.sh /usr/local/bin/docker-entrypoint.sh

RUN mkdir -p /data /tmp/opencode \
    && chown -R optiapp:optiapp /app /data /tmp/opencode \
    && chmod 0755 /usr/local/bin/docker-entrypoint.sh

USER optiapp

EXPOSE 8000

ENTRYPOINT ["/usr/local/bin/docker-entrypoint.sh"]
CMD ["uvicorn", "solver_api:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "1", "--proxy-headers"]
