# limitsetting
Common limit setting procedure for SUSY searches.

# Code style
Mostly python, some C++.

# Installation
Follow instructions in:

https://cms-hcomb.gitbooks.io/combine/content/part1/


# How to use
printdatacardscan.py create the data cards for each points so that the individual limits could be calculated.
qad_fast_print_cards.py is currently the testing version for one's self...

doLimits.sh runs through all the points in the grid and generate relevant plots.

makeLimitHist_TChiWH.C should draws the standard plot...

# Files
The files with all grid points stored are:
/nfs-7/userdata/mliu/tupler_babies/merged/onelepbabymaker/moriond2017.v13/output/SMS_tchiwh*.root
