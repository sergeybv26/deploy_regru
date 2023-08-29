#!/bin/bash

cd $HOME/www/test.derzn.ru/dz/
git pull
source $HOME/www/derzn.ru/venv/bin/activate
pip install -r $HOME/www/derzn.ru/dz/requirements.txt
$HOME/www/derzn.ru/dz/manage.py migrate
$HOME/www/derzn.ru/dz/manage.py collectstatic --noinput
rm -Rf $HOME/www/derzn.ru/static
mkdir $HOME/www/derzn.ru/static
cp -r $HOME/www/derzn.ru/dz/static/* $HOME/www/derzn.ru/static
touch $HOME/www/derzn.ru/.restart-app
