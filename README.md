# ETFParse

## About

Python program for parsing ETF autotest scripts for courses such as UUP, TP, ASP, and NA. It produces a 
`txt` output file with unit tests and expected outputs.

## How to use it?

To use the program, simply run the following command:

```bash
python etfparse.py <filename>
```

You should replace `<filename>` with the name of the file containing unit tests. By default, this argument will be 
`autotest2`, so simply running `python etfparse.py` will look for `autotest2` in the current directory.

For parsing multiple files, use:

```bash
python etfparse.py <filename1> <filename2> ... <filenameN>
``` 

and replace `<filenameX>` with specific filenames.

