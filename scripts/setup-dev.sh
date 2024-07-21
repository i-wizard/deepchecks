#!/bin/bash

echo Starting uvicorn ...
uvicorn main:app --host 0.0.0.0 --port 8001 --reload # Start uvicorn server