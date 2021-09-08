from __future__ import annotations

from collections.abc import Collection

import click

from .tests import list_test_stories, run_test_stories


@click.command()
@click.option("--story", "-s", help="Story to run", type=int, multiple=True)
@click.option("--list-stories", "-l", help="List Registered Stories", is_flag=True)
def main(story: Collection[int] | None, list_stories: bool = False) -> None:
    if list_stories:
        list_test_stories()
    else:
        run_test_stories(story)
