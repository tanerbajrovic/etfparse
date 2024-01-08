#!/usr/bin/env python3

import json
import argparse

__version__ = '1.0.0'


# TODO: Add support for above_main and main differentiation
def main(filename: str):
    json_file = get_json_file(filename)
    homework_name = json_file['name']
    total_tests = len(json_file['tests'])
    try:
        with open(filename + '-output.txt', 'w') as output:
            for test_number in range(1, total_tests):
                code = json_file['tests'][test_number]['patch'][0]['code']
                expected_output = json_file['tests'][test_number]['execute']['expect'][0]
                output.write(f'// AT {test_number}' + '\n')
                output.write(code + '\n\n')
                output.write(f'Expected: {expected_output}' + '\n\n\n')
            print('Success: ' + f'"{homework_name}"' + '\n')
    except:
        print('Unable to create an output file')
        exit(2)


def get_json_file(filename: str):
    try:
        with open(filename, 'r') as input:
            json_file = json.load(input)
        return json_file
    except:
        print(
            f'Error opening {filename} -- check if it is in JSON format!')
        exit(1)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('filename', nargs='?', default='autotest2',
                        help='Input the name of your autotest file',
                        type=argparse.FileType('r', encoding='UTF-8'))
    args = parser.parse_args()
    main(args.filename.name)