source env/bin/activate
pip freeze --local | grep -v '^\-e' | cut -d = -f 1  | xargs pip install -U

cd wagtail
status=$(git pull)
if [ "$status" != "Already up-to-date." ]; then
    python2 setup.py install
fi
cd ..

echo "yes" | python2 manage.py collectstatic
