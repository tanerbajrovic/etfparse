#!/usr/bin/env python3

import io
import json
import argparse


__version__ = '1.2.0'


def add_options(parser: argparse.ArgumentParser) -> None:
    """
    Adds following options to the argument parser
    """
    parser.add_argument('files', nargs='*', default=['autotest2'],
                        help='Input the name(s) of your autotest file(s)',
                        type=argparse.FileType('r', encoding='UTF-8'))
    parser.add_argument('--version', action='version',
                        version=f'%(prog)s v{__version__}')


def get_json_raw(filename: str) -> dict:
    """
    Returns a dictionary object representing parsed JSON
    for autotest file `filename`
    :return: Dictionary representing parsed autotest file
    """
    try:
        with open(filename, 'r', encoding='UTF-8') as input_file:
            json_raw = json.load(input_file)
            return json_raw
    except FileNotFoundError:
        print(f'Error: File "{filename}" not found!')
        exit(1)
    except PermissionError:
        print('Error: Unable to read file (Insufficient permissions)')
        exit(2)
    except json.JSONDecodeError:
        print('Error: Unable to read file (Not in JSON format)')
        exit(3)


def get_autotests(json_raw) -> list[str]:
    """
    Returns all the autotests from `json_raw`
    :return: List of strings representing autotest codes
    """
    autotests: list[str] = []
    try:
        total_tests = len(json_raw['tests'])
        for test_number in range(1, total_tests):
            autotests.append(json_raw['tests'][test_number]['patch'][0]['code'])
        return autotests
    except KeyError:
        print('Error: File not in expected autotest format')
        exit(5)


def get_expected_outputs(json_raw) -> list[str]:
    """
    Returns expected outputs for all autotests from `json_raw`
    :return: List of strings representing expected outputs
    """
    expected_outputs: list[str] = []
    try:
        total_tests = len(json_raw['tests'])
        for test_number in range(1, total_tests):
            expected_outputs.append(json_raw['tests'][test_number]['execute']['expect'][0])
        return expected_outputs
    except KeyError:
        print('Error: File not in expected autotest format')
        exit(5)


def get_homework_name(json_raw) -> str:
    """
    Returns homework (assignment) name from `json_raw`
    :return: Homework name
    """
    try:
        return json_raw['name']
    except KeyError:
        print('Error: File not in expected autotest format')
        exit(5)


def parse_file(filename: str) -> None:
    """
    Parses file `filename` and creates `filename-output.txt` with
    all the autotests and outputs.
    """
    json_raw = get_json_raw(filename)
    autotests = get_autotests(json_raw)
    expected_outputs = get_expected_outputs(json_raw)
    homework_name = get_homework_name(json_raw)
    try:
        with open(filename + '-output.txt', 'w', encoding='UTF-8') as output_file:
            output_file.write(homework_name + '\n\n')
            current_test_number = 1
            while len(autotests) != 0:
                output_file.write(f'// AT {current_test_number}' + '\n')
                output_file.write(autotests.pop() + '\n\n')
                output_file.write(f'Expected: {expected_outputs.pop()}' + '\n\n\n')
                current_test_number += 1
            print('Success: ' + f'"{homework_name}"')
    except PermissionError:
        print('Error: Unable to create file (Insufficient permissions)')
        exit(4)


def main() -> None:
    parser = argparse.ArgumentParser(prog='etfparse')
    add_options(parser)
    args = parser.parse_args()
    files = args.files
    for file in files:
        if isinstance(file, io.TextIOWrapper):
            parse_file(file.name)
        else:
            parse_file(file)


if __name__ == '__main__':
    main()
