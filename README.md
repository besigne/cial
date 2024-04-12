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
- [ ] Phone Number Verification
- [ ] Successful Scrapper Run
- [ ] Unsuccessful Scrapper Run

-------
## Information
I have provided a `websites.txt` file that I used for tests, any txt file with formatted urls can be used.

- urls malformed will not be processed.
- if `status_code` is not `request.codes.ok` it returns `Dead Page` on terminal.
- For each url the code starts a `thread`.
- The output is unbuffered, which means when a `thread` is done it print the result on terminal.
- It does not display the logo if the logo is a `.svg file`, only displays if the `.svg file` has a valid `url`.
- Phone regex is based on the first six sites phone numbers.
- The `LoggerHandler:` will generate a `log` for requests made, malformed url

## Limitations
Until now, it only matches phones from the `US region` and `BR region`, but it can be further expanded to include other regions.

<small>* As most sites listed in `websites.txt` are hosted in the `US region`</small>

## Possible Expansions
- [ ] .svg logos can be saved to a local file with a shared folder between the container and host if they don't have a valid url.
  - This one I have tested and can be implemented easily, but it costs processing power, so for it to be more viable needs to be optimized.
- [ ] Allow for manual setting or automatic determination of the URL host location worldwide to generate phone numbers accordingly.

### Dev notes
- First I was using a simple regex to find the phone number, before I found a library to do the more bulky regex matching, reducing runtime in 50%. Couldn't find a workaround for the actual `O(n²)` besides reducing the regions that it covers, but improved performance using a `dict = { region: regex }`, this generates more precise results preventing some previous matches like an `IP` or a `Date` getting mixed with Phone Numbers.
- For each `region` added at the `dict = { region: regex }` it adds about 6 seconds in runtime.
- To find possible logo images I appealed to a common string that could be inside `<img>` tags, if the tag has `'logo'` written in any of these: `alt`, `src`, `class`. Also, it skips the tag if there's no `src` as would not be possible to return a functional `url` to the image.
----------------
### Author
- [Matheus Boesing da Silva / besigne](https://github.com/besigne) - Sole Developer