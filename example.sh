#!/bin/bash
# WARNING: do not run this script. These are examples.

# start-block: virtualenv
pip install virtualenv
virtualenv env
source env
# end-block: virtualenv

# start-block: install-easy_install
easy_install onlinelinguisticdatabase
# end-block: install-easy_install

# start-block: install-pip
pip install onlinelinguisticdatabase
# end-block: install-pip

# start-block: install-source
git clone https://github.com/jrwdunham/old.git
cd old
python setup.py develop
# end-block: install-source

# start-block: build-old
mkdir myold
cd myold
paster make-config onlinelinguisticdatabase production.ini
paster setup-app production.ini
# end-block: build-old

# start-block: serve-old
paster serve production.ini
# end-block: serve-old

