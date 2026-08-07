#!/bin/sh
set -eu

script_dir=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
project_dir=$(dirname "$script_dir")
env_file=${ENV_FILE:-"$project_dir/.env"}
tag=${1:-}

if [ ! -f "$env_file" ]; then
    echo "Configuration file not found: $env_file" >&2
    echo "Create it from .env.example and set DOCKERHUB_IMAGE." >&2
    exit 1
fi

set -a
# shellcheck disable=SC1090
. "$env_file"
set +a

if [ -z "${DOCKERHUB_IMAGE:-}" ]; then
    echo "DOCKERHUB_IMAGE must be set in $env_file" >&2
    exit 1
fi

case "$tag" in
    ""|[.-]*|*[!A-Za-z0-9_.-]*)
        echo "Usage: $0 TAG" >&2
        echo "TAG may contain letters, numbers, underscores, periods and hyphens." >&2
        exit 1
        ;;
esac

if [ "${#tag}" -gt 128 ]; then
    echo "TAG cannot exceed 128 characters." >&2
    exit 1
fi

image="${DOCKERHUB_IMAGE}:${tag}"
python_bin=${PYTHON_BIN:-python3}

echo "Generating web interface"
"$python_bin" "$project_dir/generate_ui.py" --all --output "$project_dir/output"

for page in login.html main_menu.html STHE/problem_data.html GPHE/problem_data.html; do
    if [ ! -s "$project_dir/output/$page" ]; then
        echo "Generated page is missing or empty: output/$page" >&2
        exit 1
    fi
done

echo "Building $image"
docker build --pull --tag "$image" "$project_dir"

echo "Pushing $image"
docker push "$image"

echo "Published $image"
