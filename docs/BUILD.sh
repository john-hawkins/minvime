#!/bin/bash

rm ./source/minvime.rst
rm ./source/modules.rst

make clean
sphinx-apidoc -o ./source ../minvime
make html


