source env/bin/activate
pip freeze --local | grep -v '^\-e' | cut -d = -f 1  | xargs pip install -U
cd wagtail && git pull && python2 setup.py install
cd ..
echo "yes" | python2 manage.py collectstatic
