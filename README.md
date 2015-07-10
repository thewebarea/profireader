# profireader
Installation instruction:

In order to install psycopg2 in virtual environment you should install
libpq-dev python-dev packages first:
$ sudo apt-get install libpq-dev python-dev

also you have to install 'python3-venv' package in order to work with Python 3
$ sudo apt-get install python3-venv

create new postgresql user 'pfuser':
$ sudo -u postgres createuser -D -A -P pfuser
(here system asks a password for just created user. Password: min~Kovski)

pfuser have to create new db named 'profireader'
$ sudo -u postgres createdb -O pfuser profireader

now virtual environment with all necessary packages have to be created:
$ apt-get install python3-pip
$ pyvenv env && source env/bin/activate && pip3 install -r requirements.txt

------------------------------------------------------

Tips:
If psycopg2 cann't be installed correctly then...
