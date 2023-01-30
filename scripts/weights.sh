#!/bin/bash
###############################################################################
#
#  weights.sh - print out the weights (and names) of the .md files in the 
#               directory $1 as wellas the weights (and names) of any _index.md
#               files in the subdirectories of $1, sorted by increasing weight.
#
#  Frank Halasz 2023-01-30
#
#  Copyright 2023 Interlisp.org
#
###############################################################################


if [ -z "$1" ]; then dir="."; else dir="$1"; fi
find "${dir}" -mindepth 2 -maxdepth 2 -name _index.md  -exec grep -i -H weight {} \; >/tmp/weights-$$
find "${dir}" -mindepth 1 -maxdepth 1 -type f  \
       ! -name _index.md -name "*.md" \
       -exec grep -i -H weight {} \; \
       >>/tmp/weights-$$
sed -i \
    -e "s/:\s*weight:/ /" \
    -e "s/\s+/ /" \
    -e "s/\s+\$//" \
    -e "s#${dir%/}/##" \
    -e "s/_index.md//" \
    /tmp/weights-$$
awk "{print \$2 \"\t\" \$1}" < /tmp/weights-$$ | sort -n

