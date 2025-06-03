#!/bin/bash
# Start script for production
exec gunicorn main:app \
  --workers 4 \
  --worker-class uvicorn.workers.UvicornWorker \
  --bind 0.0.0.0:${PORT:-8000} \
  --access-logfile - \
  --error-logfile -