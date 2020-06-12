#!/bin/bash

# clean files.
rm cobertura.xml
rm coverage.xml
rm -rf .pytest_cache

# execute
coverage xml --omit=".env,*/test*"
mv coverage.xml cobertura.xml
python-codacy-coverage -r cobertura.xml 

