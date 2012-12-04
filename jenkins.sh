#!/bin/sh

if [ -d ".env" ]; then
 echo "**> virtualenv exists"
else
 echo "**> creating virtualenv"
 virtualenv .env
 mkdir -p $HOME/pip-cache
 .env/bin/pip install --download-cache $HOME/pip-cache nose==1.1.2 coverage pylint pep8 clonedigger
fi

. .env/bin/activate
PYTHONPATH=. python setup.py nosetests --with-xunit --with-coverage --cover-package=gepetto --cover-inclusive
coverage xml
pylint -f parseable -d I0011,R0801 gepetto | tee pylint.out
clonedigger --cpd-output gepetto
pep8 gepetto | tee pep8.out
