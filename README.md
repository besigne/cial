# Technical Assignment
## CIAL dun&bradstreet

--------------
## Dependencies
- [Python 3.12.2](https://www.python.org/downloads/release/python-3122/)
- [Docker](https://docs.docker.com/)
-------------
## Instructions
### Building the image
```bash
docker build -t module .
```
### Running the scrapper
```bash
cat websites.txt | docker run -i module
```
## Information
I have provided a `websites.txt` file that I used for tests, any txt file with formatted urls can be used.

- For each url the code starts a `thread`.
- The output is unbuffered, which means when a `thread` is done it print the result on terminal.
- It does not display the logo if the logo is a .svg file.
- Phone regex is based on the first six sites phone numbers.

----------------
### Author
- [Matheus Boesing da Silva / besigne](https://github.com/besigne) - Sole Developer