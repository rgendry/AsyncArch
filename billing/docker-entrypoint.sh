#!/bin/bash
set -e

PORT=${2:-8080}

case "$1" in
    init)
        alembic upgrade head
        ;;
    api)
        exec uvicorn app.mian:app --host 0.0.0.0 --port $PORT --forwarded-allow-ips '*'
        ;;
    start)
        alembic upgrade head
        exec uvicorn app.main:app --host 0.0.0.0 --port $PORT --reload --reload-dir app
        ;;
    *)
        exec "$@"
        ;;
esac
