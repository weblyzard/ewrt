#!/bin/bash

set -e

echo ':: Building package...'
sed -i s/-dev/".$(date +%Y%m%d.%H%M)"/g setup.py
/usr/bin/python3 setup.py sdist --dist-dir /var/www/repo3/
PACKAGE=$(/usr/bin/python3 -W ignore ./setup.py --name | awk 'NR==1{print $1}')
VERSION=$(/usr/bin/python3 -W ignore ./setup.py --version | awk 'NR==1{print $1}')

# this line ensures that this released version cannot be overwritten
cd /var/www/repo3/ && ls -1 | grep $PACKAGE | grep -v "$PACKAGE.*-dev.*" | grep $VERSION | xargs chmod a-w

echo ":: Current version of ${PACKAGE} is ${VERSION}."
