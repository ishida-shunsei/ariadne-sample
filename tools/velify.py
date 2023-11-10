from pathlib import Path

from ariadne import gql

PROJECT_ROOT = Path(__file__).resolve().parent.parent

def validate_schema(file_name:str):
    schema_path = PROJECT_ROOT.joinpath(file_name)
    with open(schema_path, 'rt', encoding='utf-8') as f:
        text = f.read()
        schema = gql(text)
        print(schema)
        print("=== SCHEMA IS VALID ===")


if __name__ == '__main__':
    validate_schema("schema.graphql")
