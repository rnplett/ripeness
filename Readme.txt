git clone ...

cd FlaskBareDash

virtualenv -p /usr/local/bin/python3.6 vFlaskBareDash

pip install -r requirements.txt

git init
git add .
git commit -m "First commit"

FLASK_APP=hello.py flask run
http://127.0.0.1:5000/hello
