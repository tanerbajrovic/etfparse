import json
import argparse


def add_options(parser: argparse.ArgumentParser) -> None:
    """
    Adds following options to the argument parser
    """
    parser.add_argument('filename', nargs='?', default='autotest2',
                        help='Input the name of your autotest file',
                        type=argparse.FileType('r', encoding='UTF-8'))


def get_json_file(filename: str):
    try:
        with open(filename, 'r') as input_file:
            json_file = json.load(input_file)
        return json_file
    except PermissionError:
        print('Error: Unable to read file (Insufficient permissions)')
        exit(1)
    except json.JSONDecodeError:
        print('Error: Unable to read file (Not in JSON format)')
        exit(2)


def main() -> None:
    parser = argparse.ArgumentParser()
    add_options(parser)
    args = parser.parse_args()
    filename = args.filename.name
    try:
        json_file = get_json_file(filename)
        homework_name = json_file['name']
        total_tests = len(json_file['tests'])
        with open(filename + '-output.txt', 'w') as output_file:
            output_file.write(homework_name + '\n\n')
            for test_number in range(1, total_tests):
                code = json_file['tests'][test_number]['patch'][0]['code']
                expected_output = json_file['tests'][test_number]['execute']['expect'][0]
                output_file.write(f'// AT {test_number}' + '\n')
                output_file.write(code + '\n\n')
                output_file.write(f'Expected: {expected_output}' + '\n\n\n')
            print('Success: ' + f'"{homework_name}"' + '\n')
    except PermissionError:
        print('Error: Unable to create an output file (Insufficient permissions)')
        exit(3)
    except KeyError:
        print('Error: File not in autotest format (Not expected JSON)')
        exit(4)
