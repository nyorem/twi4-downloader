#! /usr/bin/env python3

import click
from twi4 import get_javascript, parse_javascript, download_chapters

AVAILABLE_COMICS = [ "fushigineko", "kanako" ]
DOWNLOAD_DIR = "comics"

if __name__ == "__main__":
    import os
    comic = "kanako"
    assert comic in AVAILABLE_COMICS

    # Download and parse the corresponding javascript file
    contents = get_javascript(comic)
    pages = parse_javascript(comic, contents)

    # Create the directory if necessary
    output_dir = os.path.join(DOWNLOAD_DIR, comic)
    if not os.path.isdir(output_dir):
        os.mkdir(output_dir)

    # Download the chapters
    download_chapters(output_dir, pages, start=0, end=None, verbose=True)
