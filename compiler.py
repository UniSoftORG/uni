import sys
import json
from pathlib import Path
from lang.lexer.rules import parser

def create_file(input_filepath, content, base_path):
    relative_path = input_filepath.relative_to(base_path)
    output_path = base_path / 'dist' / relative_path.with_suffix('.json')

    output_path.parent.mkdir(parents=True, exist_ok=True)

    with output_path.open("w") as f:
        f.write(json.dumps(content, separators=(',', ":")))

def parse_file(filepath, base_path):
    try:
        input_filepath = Path(filepath)
        with input_filepath.open('r') as file:
            result = parser.parse(file.read())
            create_file(input_filepath, result, base_path)
    except IOError as e:
        print(f"Error reading file: {e}")

def process_directory(directory):
    base_path = Path(directory).resolve()
    for uni_file in base_path.rglob('*.uni'):
        parse_file(uni_file, base_path)

if __name__ == "__main__":
    if len(sys.argv) > 1:
        process_directory(sys.argv[1])
    else:
        print("No directory specified")
