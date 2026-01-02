import typer
from pathlib import Path
from collections import deque

def validate_path():
    return True

def main(given_path: Path):
    assert validate_path(given_path), "Path is not valid"

    




if __name__ == "__main__":
    typer.run(main)
