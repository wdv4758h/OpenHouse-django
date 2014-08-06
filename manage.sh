#!/bin/sh

update(){
    source env/bin/activate
    pip freeze --local | grep -v '^\-e' | cut -d = -f 1  | xargs pip install -U

    cd wagtail
    status=$(git pull)
    if [ "$status" != "Already up-to-date." ]; then
        python2 setup.py install
    fi
    cd ..

    echo "yes" | python2 manage.py collectstatic
}

refresh(){
    source env/bin/activate
    echo "yes" | python2 manage.py collectstatic
}

if [ $1 == 'update' -o $1 == 'u' ]
then
    update
elif [ $1 == 'refresh' -o $1 == 'r' ]
then
    refresh
fi
