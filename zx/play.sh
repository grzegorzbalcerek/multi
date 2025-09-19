LAST=$(ls -tr *.tap|tail -1)
FILE=${1:-$LAST}
set -x
~/.venv/bin/tzxplay $FILE
