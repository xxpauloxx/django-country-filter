#!/bin/bash

OMIT=".env,**/test*"

# Clear old files.
rm cobertura.xml
rm -rf .pytest_cache

# Generate report to coverage.
coverage run -m pytest
coverage xml --omit=".env,*/test*"

mv coverage.xml cobertura.xml
coverage report
