#!/bin/sh
convert png:./output/filled.png pnm:plan.pnm
potrace -s plan.pnm --alphamax 0 --flat --invert -o ./downloads/plan.svg
