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
All tests are run on same URL: `https://www.cmsenergy.com/contact-us/default.aspx`
 
- [X] UrlHandler
  - Filters the valid from the invalid URLs
- [x] LogoHandler
  - Matches if the found `logo url` is the same on the site.
- [x] PhoneHandler
  - Matches if the found `phones: [str]` are the ones on the site.
- [x] Scrapper Full Lifecycle
  - As the tests run single pieces of the Scrapper one at a time, there's also a test to run the Scrapper's full lifecycle


-------
## Information
I have provided a **websites.txt** file that I used for tests containing **25 valid urls**, any txt file with formatted urls can be used.
Also **I took the liberty to not include the parentheses back into phone numbers** because the updated worldwide rule is that the parentheses
are **not** needed anymore, that is because the area codes stopped being optional.

- urls malformed will not be processed.
- if `status_code` is not `request.codes.ok` it returns `Dead Page` on terminal.
- For each url the code starts a `thread`.
- The output is unbuffered, which means when a `thread` is done it print the result on terminal.
- It does not display the logo if the logo is a `.svg file`, only displays if the `.svg file` has a valid `url`.
- Phone formatting is from the same `country code` the as the `urls IP address origin`  
- The `LoggerHandler` will generate a `log` informing:
  - The starting time
  - The starting time for each thread
  - Status Code
  - Logo URL if found
  - A phone number count

## Limitations


## Possible Expansions
- .svg logos can be saved to a local file with a shared folder between the container and host if they don't have a valid url.
  - This one I have tested and can be implemented easily, but it costs processing power, so for it to be more viable needs to be optimized.


### Dev notes
- Phone formatting is limited for the IP address origins country due to much more processing power needed to match every single phone type in all websites around the world.
- To find possible logo images I appealed to a common string that could be inside tags that could contain an image, if the tag has `'logo'` written in any of these: `alt`, `src`, `class`. Also, it skips the tag if there's no `src` as would not be possible to return a functional `url` to the image.
----------------
### Author
- [Matheus Boesing da Silva / besigne](https://github.com/besigne) - Sole Developer