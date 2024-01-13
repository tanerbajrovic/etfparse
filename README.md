# ETF Autotest Parser

## About

Python program for parsing ETF autotest scripts. It produces a `.txt` output file with all the unit tests and expected 
outputs.

## Usage

To use the program simply run the following command:

```bash
python etfparse.py <filename>
```

You should replace `<filename>` with the name of the file containing unit tests. By default, this argument will be 
`autotest2`, so simply running `python etf-parse.py` will look for `autotest2` in the current directory.
