#!/bin/bash

cd $HOME/www/test.derzn.ru/dz/
git pull
source $HOME/www/test.derzn.ru/venv/bin/activate
pip install -r $HOME/www/test.derzn.ru/dz/requirements.txt
$HOME/www/test.derzn.ru/dz/manage.py migrate
touch $HOME/www/test.derzn.ru/.restart-app
