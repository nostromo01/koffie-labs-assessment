#!/usr/bin/bash
schemathesis run \
  --base-url=http://localhost:8000 \
  --checks all \
  --show-errors-tracebacks \
  --workers 8 \
  --hypothesis-deadline=None \
  --hypothesis-suppress-health-check=too_slow \
  openapi.json
