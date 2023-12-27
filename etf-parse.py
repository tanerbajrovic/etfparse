#!/usr/bin/env python3

import json # JSON Parsing
import argparse # Parsing CLI arguments

# TODO: Add support for above_main and main differentiation
def main(filename: str):
  fileJSON = get_json_file(filename)
  name = fileJSON['name']
  length = len(fileJSON['tests'])
  fileOutput = open(filename + '-output.txt', 'w')
  for i in range(1, length):
    code = fileJSON['tests'][i]['patch'][0]['code']
    fileOutput.write(f'// AT {i}' + '\n')
    fileOutput.write(code + '\n\n')
  print('Success: ' + f'"{name}"' + '\n')
  fileOutput.close()

# TODO: Add error-checking if file doesn't exist
def get_json_file(filename: str):
  try:
    with open(filename, 'r') as file:
      fileJSON = json.load(file)
  except:
    print(f'Error opening the file {filename} -- possibly not in JSON format')
    exit(1)
  return fileJSON

# TODO: Add error-checking if file doesn't exist
if __name__ == '__main__':
  parser = argparse.ArgumentParser()
  parser.add_argument('filename', default='autotest2', type=argparse.FileType('r'))
  args = parser.parse_args()
  main(args.filename.name)