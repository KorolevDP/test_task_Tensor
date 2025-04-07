from random import randint
import json
from typing import List


def generate_versions(template: str) -> List[str]:
    versions = []
    rnd_list_num = []
    num1 = randint(0,9)
    num2 = randint(0,9)
    rnd_list_number = [str(num1), str(num2)]
    for replacement in rnd_list_number:
        version = template.replace('*', replacement)
        versions.append(version)
    return versions


def parse_config_file(filename: str) -> dict:
    with open(filename, 'r') as file:
        content = file.read()
        config = json.loads(content.replace(":", ":").replace("'", '"'))
    return config


def compare_versions(version1: str, version2: str) -> int:
    v1_parts = list(map(int, version1.split('.')))
    v2_parts = list(map(int, version2.split('.')))
    return (v1_parts > v2_parts) - (v1_parts < v2_parts)


def main(version: str, config_file: str):
    templates = parse_config_file(config_file)

    all_versions = set()

    for template in templates.values():
        generated_versions = generate_versions(template)
        all_versions.update(generated_versions)

    sorted_versions = sorted(all_versions, key=lambda x: list(map(int, x.split('.'))))


    print("\nAll generated versions:")
    for ver in sorted_versions:
        print(ver)


    older_versions = [ver for ver in sorted_versions if compare_versions(ver, version) < 0]


    print("\nVersions less than specified:")
    for ver in older_versions:
        print(ver)


if __name__ == "__main__":
    input_version = input("\nEnter the product version number (example: 3.7.5): ")
    config_filename = input("Enter the name of the configuration file (example, config.json): ")

    main(input_version, config_filename)