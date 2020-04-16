#! /usr/bin/env bash

if [ ! -d "heroku-app" ]; then
    echo "heroku-app directory must be present, initialize a Heroku app with COMICS_DIR variable in this directory"
    exit 1
fi

# Regenerate pkl for comics
COMICS="fushigineko kanako"

source venv/bin/activate
for comic in $COMICS; do
    python3 main.py dump $comic
done
deactivate

cp comics/*.pkl heroku-app/comics/

# Copy Python files
rm -rf heroku-app/app
cp -r flask-app/app heroku-app/
rm -rf heroku-app/app/__pycache__/

# Commit and push
cd heroku-app/
git commit -am "update heroku build"
git push heroku master
