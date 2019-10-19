#! /usr/bin/env python3

import click
import os
from twi4 import get_javascript, parse_javascript, download_chapters

AVAILABLE_COMICS = [ "fushigineko", "kanako" ]
DOWNLOAD_DIR = "comics"

@click.command()
@click.argument("comic")
@click.option("--start", default=0, help="First chapter to download")
@click.option("--end", default=None, help="Last chapter to download")
@click.option("--verbose/--no-verbose", default=False)
def app(comic, start, end, verbose):
    """
    Download comics from twi4.

    Available comics are: fushigineko, kanako.
    """

    assert comic in AVAILABLE_COMICS

    # Download and parse the corresponding javascript file
    contents = get_javascript(comic)
    pages = parse_javascript(comic, contents)

    # Create the directory if necessary
    output_dir = os.path.join(DOWNLOAD_DIR, comic)
    if not os.path.isdir(output_dir):
        os.mkdir(output_dir)

    if start is not None:
        start = int(start)
    if end is not None:
        end = int(end)

    # Download the chapters
    download_chapters(output_dir, pages, start=start, end=end, verbose=verbose)

if __name__ == "__main__":
    app()
