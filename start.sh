#!/bin/sh
python3 -m uvicorn main:app --host 0.0.0.0 --port $PORT --reload --proxy-headers
