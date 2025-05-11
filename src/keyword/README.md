# Requiremnt

This program adopt python 3.10. To install the environment, use:

```
pip install -r requirements.txt
```

# Usage

```
usage: main.py [-h] [-i INPUT_PATH] [-o OUTPUT_PATH] [-m {textrank,bert,llm}]

Extract keywords from markdown files.

options:
  -h, --help            show this help message and exit
  -i INPUT_PATH, --input_path INPUT_PATH
                        Input markdown files.
  -o OUTPUT_PATH, --output_path OUTPUT_PATH
                        Output file path for extracted keywords.
  -m {textrank,bert,llm}, --method {textrank,bert,llm}
                        Method to use for keyword extraction: textrank, bert, or llm.
```
You may set the environment variable `API_KEY` to use your own API key

```
keyword
├─ bert.py
├─ llm.py
├─ main.py
├─ README.md
├─ requirements.txt
└─ textrank.py

```
