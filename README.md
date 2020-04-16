# twi4-downloader

## Installation

```
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Usage

- download all chapters:

```
./main.py download comic [--verbose]
```

- download last chapter:

```
./main.py download comic --start -1 [--verbose]
```

- download a range of  chapters:

```
./main.py download comic --start x --end y [--verbose]
```

## Web app

A simple web application made using Flask can be found in the `flask-app` directory. A live version can be found [here](https://twi4-reader.herokuapp.com/) (the updates are not automatic and thus the most recent chapters may not be present).

