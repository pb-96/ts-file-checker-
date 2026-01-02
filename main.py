import typer
from pathlib import Path
from collections import deque
import os


# TODO: Figure out how to make this configure able
IGNORE_FOLDERS = {
    "node_modules",

}

def validate_path(given_path: Path) -> bool:
    return given_path.exists()


def convert_to_camel(file_name: Path, file_type: str) -> Path:
    if "_" in file_name.name:
        as_list = file_name.name.replace(file_type, "").lower().split("_")

        converted_file_name = as_list[0]
        for elem in as_list[1:]:
            converted_file_name = converted_file_name + elem.title()

        return file_name.parent.resolve() / f"{converted_file_name}{file_type}"

    return file_name


def handle_file(file_path: Path, file_type: str):
    adjusted_path = convert_to_camel(file_path, file_type)
    if adjusted_path == file_path:
        return

    os.rename(str(file_path.resolve()), str(adjusted_path.resolve()))


def predicate_file(file_path: Path, file_type: str):
    return (
        file_path.is_file()
        and file_path.name.endswith(file_type)
        and validate_path(file_path)
    )

def validate_folder(_path: Path):
    return _path.is_dir() and not _path.name in IGNORE_FOLDERS

def traverse_target(given_path: Path, file_type: str):
    to_search = deque([given_path])
    while to_search:
        this_layer = to_search.pop()
        if validate_folder(this_layer):
            for file_path in this_layer.iterdir():
                if predicate_file(file_path, file_type):
                    handle_file(file_path, file_type)
                else:
                    to_search.append(file_path)

        if predicate_file(file_path, file_type):
            handle_file(file_path, file_type)


def main(given_path: Path, file_type: str = ".ts"):
    assert validate_path(given_path), "Path is not valid"
    traverse_target(given_path, file_type)


if __name__ == "__main__":
    typer.run(main)
