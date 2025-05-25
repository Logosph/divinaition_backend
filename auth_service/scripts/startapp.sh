#!/bin/bash

echo 'RUNNING MIGRATIONS:'
alembic upgrade head
echo 'MIGRATIONS RAN. EXITING'

python -m uvicorn app.main:app --port 8000 --host 0.0.0.0 --workers 2