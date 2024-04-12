# Technical Assignment
## CIAL dun&bradstreet

--------------
## Dependencies
- [Python 3.12.2](https://www.python.org/downloads/release/python-3122/)
- [Docker](https://docs.docker.com/)
-------------
## Instructions
### Building the image
#### ⚠ **Warning:** be sure to verify you're inside the project's root folder.
```bash
docker build -t module .
```
### Running the scrapper
This `websites.txt` is a pre-built file for testing
```bash
cat websites.txt | docker run -i module
```
----------

## Tests
To run tests you will need to be inside the `venv`, verify if you're inside project's root folder. Also, your global python version should be the [Python 3.12.2](https://www.python.org/downloads/release/python-3122/).
```bash
python -m venv venv
```
```bash
python -m unittest tests/TestScrapper.py -v
```

### Tests covered
- [x] URL Verification
- [ ] Acceptable Phone Numbers

-------
## Information
I have provided a `websites.txt` file that I used for tests, any txt file with formatted urls can be used.

- urls malformed will not be processed.
- if `status_code` is not `request.codes.ok` it returns `Dead Page` on terminal.
- For each url the code starts a `thread`.
- The output is unbuffered, which means when a `thread` is done it print the result on terminal.
- It does not display the logo if the logo is a `.svg file`, only displays if the `.svg file` has a valid `url`.
- Phone regex is based on the first six sites phone numbers.

## Limitations
Until now, it only matches phones from the `US region` and `BR region`, but it can be further expanded to include other regions.

<small>* As most sites listed in `websites.txt` are hosted in the `US region`</small>

## Possible Expansions
- [ ] .svg logos can be saved to a local file with a shared folder between the container and host if they don't have a valid url.
- [ ] Allow for manual setting or automatic determination of the URL host location worldwide to generate phone numbers accordingly.

----------------
### Author
- [Matheus Boesing da Silva / besigne](https://github.com/besigne) - Sole Developer