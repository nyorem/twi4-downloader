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
./main.py comic [--verbose]
```

- download last chapter:

```
./main.py comic --start -1 [--verbose]
```

- download a range of  chapters:

```
./main.py comic --start x --end y [--verbose]
```

