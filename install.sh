#!/bin/bash

apt-get install dialog

function e {
    echo "$*"
    }

function menu_ {
    echo ''
    }

function ret {
    e
    read -p "Press [enter] to continue"
    e
    }


rr() {
    if [[ "$2" == "" ]]; then
      read -p "$1" retvalue
    else
      read -p "$1[$2]" retvalue
      if [[ "$retvalue" == "" ]]; then
	retvalue="$2"
      fi
    fi
    echo "$retvalue"
    }

function menu_exit {
    exit
    }

function conf {
    # call with a prompt string or use a default
    read -r -p "${1:-Are you sure? [Y/n]} " response
    if [[ "$response" == "" ]]; then
	true
    else 
    case $response in
        [yY][eE][sS]|[yY]) 
            true
            ;;
        *)
            false
            ;;
    esac
    fi
}

conf_comm() {
    echo "Command we're going to execute:"
    rd=`tput setaf 1`
    rst=`tput sgr0`
    echo "${rd}"
    echo "$1" | sed 's/^/    /g'
    echo "${rst}"
    if conf; then
	e
        eval "$1"
	if [[ "$2" == "" ]]; then
	    ret
	fi
        true
    else
      false
    fi
}


function runsql {
    conf_comm "su postgres -c \"echo \\\"$1\\\" | psql\""
    }

function runsql_dump {
    profidb=`cat secret_data.py | grep 'DB_NAME' | sed -e 's/^\s*DB_NAME\s*=\s*['"'"'"]\([^'"'"'"]*\).*$/\1/g' `
    filenam=$(rr "$1" "$2")
    conf_comm "su postgres -c 'cat $filenam | psql $profidb'"
    }

function menu_deb {
    conf_comm "apt-get update
apt-get install libpq-dev libapache2-mod-wsgi"
    }

function menu_db_backup {
    profidb=`cat secret_data.py | grep 'DB_NAME' | sed -e 's/^\s*DB_NAME\s*=\s*['"'"'"]\([^'"'"'"]*\).*$/\1/g' `
    conf_comm "su postgres -c 'echo \"ALTER DATABASE $profidb RENAME TO bak_$profidb""_$date\" | psql'"
    }

function menu_db_struct {
    runsql_dump 'Enter sql structure filename' database_structure.sql
    }

function menu_db_initial {
    runsql_dump 'Enter sql initial data filename' database_initial_data.sql
    }

function menu_db_create {
    profidb=`cat secret_data.py | grep 'DB_NAME' | sed -e 's/^\s*DB_NAME\s*=\s*['"'"'"]\([^'"'"'"]*\).*$/\1/g' `
    psqldb=$(rr 'Enter postgresql database name' $profidb)
    
    profiuser=`cat secret_data.py | grep 'DB_USER' | sed -e 's/^\s*DB_USER\s*=\s*['"'"'"]\([^'"'"'"]*\).*$/\1/g' `
    runsql "CREATE DATABASE $psqldb WITH ENCODING 'UTF8' LC_COLLATE='C.UTF-8' LC_CTYPE='C.UTF-8'  OWNER = $profiuser TEMPLATE=template0"
    }

function menu_db_user_pass {
    echo "Going to create user/pass from secret data and create such user/pass using postgres user"
    echo "If user exists, only password will be changed"
    
    profiuser=`cat secret_data.py | grep 'DB_USER' | sed -e 's/^\s*DB_USER\s*=\s*['"'"'"]\([^'"'"'"]*\).*$/\1/g' `
    psqluser=$(rr 'Enter postgresql user' $profiuser)
    
    profipass=`cat secret_data.py | grep 'DB_PASSWORD' | sed -e 's/^\s*DB_PASSWORD\s*=\s*['"'"'"]\([^'"'"'"]*\).*$/\1/g' `
    psqlpass=$(rr 'Enter postgresql password' $profipass)
    runsql "CREATE USER $psqluser with password '$psqlpass'"
    
    }


function menu_environment {
    conf_comm "sed -i '/\(db\|web\|mail\).profi/d' /etc/hosts
sed -i '/\(companyportal\|aprofi\).d.ntaxa.com/d' /etc/hosts
echo '' >> /etc/hosts
echo '127.0.0.1 aprofi.d.ntaxa.com companyportal.d.ntaxa.com' >> /etc/hosts
echo '127.0.0.1 db.profi web.profi mail.profi' >> /etc/hosts
cat /etc/hosts"
    }

function menu_secret_data {
    echo "Going to run commands:"
    echo "  wget --user='ntaxauser' --password='ntaxapassword' -O secret_data.txt http://x.d.ntaxa.com/profireader/secret_data.txt"
    echo "  mv secret_data.txt secret_data.py"
    echo "If exists, secret_data.py will be copied to secret_data.bak.py"
    ntaxauser=$(rr 'Enter ntaxa user')
    ntaxapass=$(rr "Enter ntaxa password")
    conf_comm "wget --user='$ntaxauser' --password='$ntaxapass' http://x.d.ntaxa.com/profireader/secret_data.txt
if [[ \"\$?\" == \"0\" ]]; then
    if [[ -f secret_data.py  ]]; then
	echo 'cp ./secret_data.py ./secret_data.bak.py'
	cp ./secret_data.py ./secret_data.bak.py
    fi
    mv secret_data.txt secret_data.py
else
  echo 'wget failed!'
fi"
    }

function menu_python_3 {
    pversion=$(rr 'Enter python version' 3.4.2)
    destdir=$(rr 'destination dir' /usr/local/opt/python-$pversion)
    if [[ -e $destdir ]]; then
	echo "error: $destdir exists"
    else
	conf_comm "cd /tmp/
rm -rf 'Python-$pversion/*'
rm 'Python-$pversion.tgz'
wget 'https://www.python.org/ftp/python/$pversion/Python-$pversion.tgz'
tar -zxf 'Python-$pversion.tgz'
cd 'Python-$pversion'
./configure --prefix='$destdir'
make
make install
ln -s $destdir/bin/python3 /usr/bin/python3
ln -s $destdir/bin/pyvenv /usr/bin/pyvenv
cd /tmp
rm -rf 'Python-$pversion'"
    fi
    }

function menu_port {
    toport=$(rr 'redirect port 80 to port' 8080)
    conf_comm "iptables -t nat -A OUTPUT  -d 127.0.0.1  -p tcp --dport 80 -j REDIRECT --to-port $toport"
    }

function menu_modules {
    req=$(rr 'file with modules' requirements.txt)
    destdir=$(rr 'venv directory' .venv)
    conf_comm "source $destdir/bin/activate
pip3 install -r $req"
    }

$destdir

function menu_venv {
    destdir=$(rr 'destination dir for virtual directory' .venv)
    if [[ -e $destdir ]]; then
	echo "error: $destdir exists"
    else
	conf_comm "pyvenv $destdir"
    fi
    }

next='_'

while :
do
next='exit'
dialog --title "profireader" --nocancel --default-item $next --menu "Choose an option" 20 78 16 \
"deb" "install deb packages" \
"environment" "create virtual domain zone in /etc/hosts" \
"secret_data" "download secret data" \
"python_3" "install python 3" \
"venv" "create virtual environment" \
"modules" "install required python modules (via pip)" \
"port" "redirect port at localhost 80->8080" \
"db_user_pass" "create postgres user/password" \
"db_create" "create empty database" \
"db_struct" "import database structure from file" \
"db_initial" "import database initial data" \
"db_backup" "rename database (create backup)" \
"exit" "Exit" 2> /tmp/selected_menu_
reset
date=`date +"%y_%m_%d___%H_%M"`
menu_`cat /tmp/selected_menu_`

done
