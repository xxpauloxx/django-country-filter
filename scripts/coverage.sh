#!/bin/bash

# Clear old files.
if test -f "cobertura.xml"; then
    rm cobertura.xml
fi
if test -f "coverage.xml"; then
    rm coverage.xml
fi
if test -f ".pytest_cache"; then
    rm -rf .pytest_cache
fi

# Generate report to coverage.
coverage run -m pytest
coverage xml --omit=".env,*/test*"
mv coverage.xml cobertura.xml
coverage report
