#!/bin/bash

bibtex software_impacts_minvime

bibtex software_impacts_minvime

pdflatex software_impacts_minvime.tex 

rm software_impacts_minvime.out 
rm software_impacts_minvime.log 
rm software_impacts_minvime.spl
 
