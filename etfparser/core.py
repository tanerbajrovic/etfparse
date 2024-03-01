import io
import json
import argparse


def add_options(parser: argparse.ArgumentParser) -> None:
    """
    Adds following options to the argument parser
    """
    parser.add_argument('files', nargs='*', default=['autotest2'],
                        help='Input the name of your autotest file(s)',
                        type=argparse.FileType('r', encoding='UTF-8'))


def get_json_reader(filename: str):
    try:
        with open(filename, 'r', encoding='UTF-8') as input_file:
            json_reader = json.load(input_file)
            return json_reader
    except FileNotFoundError:
        print(f'Error: File {filename} not found!')
        exit(1)
    except PermissionError:
        print('Error: Unable to read file (Insufficient permissions)')
        exit(2)
    except json.JSONDecodeError:
        print('Error: Unable to read file (Not in JSON format)')
        exit(3)


def get_autotests(json_reader) -> list:
    """
    Returns all the autotests from `json_reader`
    :return: List of strings representing autotest codes
    """
    autotests = []
    total_tests = len(json_reader['tests'])
    for test_number in range(1, total_tests):
        autotests.append(json_reader['tests'][test_number]['patch'][0]['code'])
    return autotests


def get_expected_outputs(json_reader) -> list:
    """
    Returns expected outputs for all autotests from `json_reader`
    :return: List of strings representing expected outputs
    """
    expected_outputs = []
    total_tests = len(json_reader['tests'])
    for test_number in range(1, total_tests):
        expected_outputs.append(json_reader['tests'][test_number]['execute']['expect'][0])
    return expected_outputs


def get_homework_name(json_reader) -> str:
    return json_reader['name']


def parse_file(filename: str) -> None:
    json_reader = get_json_reader(filename)
    autotests = get_autotests(json_reader)
    expected_outputs = get_expected_outputs(json_reader)
    homework_name = get_homework_name(json_reader)
    with open(filename + '-output.txt', 'w', encoding='UTF-8') as output_file:
        output_file.write(homework_name + '\n\n')
        current_test_number = 1
        while len(autotests) != 0:
            autotest = autotests.pop()
            expected_output = expected_outputs.pop()
            output_file.write(f'// AT {current_test_number}' + '\n')
            output_file.write(autotest + '\n\n')
            output_file.write(f'Expected: {expected_output}' + '\n\n\n')
            current_test_number = current_test_number + 1
        print('Success: ' + f'"{homework_name}"')


def main() -> None:
    parser = argparse.ArgumentParser()
    add_options(parser)
    args = parser.parse_args()
    files = args.files
    try:
        for file in files:
            if isinstance(file, io.TextIOWrapper):
                parse_file(file.name)
            else:
                parse_file(file)
    except PermissionError:
        print('Error: Unable to create an output file (Insufficient permissions)')
        exit(3)
    except KeyError:
        print('Error: File not in autotest format (Not expected JSON)')
        exit(4)
