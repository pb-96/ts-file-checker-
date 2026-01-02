import typer
from pathlib import Path
from collections import deque
import os
import re



def validate_path(given_path: Path) -> bool:
    return True


def convert_to_camel(file_name: Path, file_type: str = ".ts") -> str:
    if not "_" in file_name:
        return file_name
    
    as_list = file_name.name.replace(file_type, "").lower().split("_")
    it = iter(as_list)

    converted_file_name = next(it)
    for elem in as_list:
        converted_file_name = converted_file_name + elem.title()
    
    return f"{converted_file_name}{file_type}"

def traverse_target(given_path: Path):
    to_search = deque([given_path])
    while to_search:
        this_layer = to_search.pop()
        for file_path in this_layer.iterdir():
            if file_path.is_file() and file_path.name.endswith(".ts"):
                adjusted_path = (this_layer / convert_to_camel(file_path))
                os.rename(str(file_path.resolve()) , str(adjusted_path.resolve()))
            else:
                to_search.append(file_path)
    
def main(given_path: Path):
    assert validate_path(given_path), "Path is not valid"
    





if __name__ == "__main__":
    typer.run(main)
