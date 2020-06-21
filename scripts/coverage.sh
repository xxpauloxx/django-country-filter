#!/bin/bash

clear

# Clear old files.
rm cobertura.xml
rm -rf .pytest_cache

# Generate report to coverage.
coverage run -m pytest
coverage xml

mv coverage.xml cobertura.xml
coverage report
