#!/bin/bash
# pylint returns non-zero exit codes, when it thinks your code stinks.
# Unfortunately, tox then believes that the script failed, even though
# everything went as it should have. 

pylint --rcfile=pylint.cfg src/eWRT/ || pylint-exit $?
if [ $? -ne 0 ]; then
    echo "An error occured while running pylint." >&2
    exit 1
fi

