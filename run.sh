#!/bin/bash
PYTHONPATH=src uvicorn src.app.main:app --host 0.0.0.0 --port 8000