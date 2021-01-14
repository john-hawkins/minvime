#!/bin/bash

bibtex paper

bibtex paper

pdflatex paper.tex 

rm paper.aux 
rm paper.out 
rm paper.brf 
rm paper.log 
 
