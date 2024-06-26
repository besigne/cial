# Technical Assignment
## CIAL dun&bradstreet
## Dependencies
- [Python 3.12.2](https://www.python.org/downloads/release/python-3122/)
- [Docker](https://docs.docker.com/)
## Table Of Content
- [Instructions](#Instructions)
  - [Setup Docker Image](#Setup-Docker-Image)
    - [Creating Image from Dockerfile](#Creating-Image-From-Dockerfile)
    - [Running the Scrapper on Docker](#Running-the-Scrapper-on-Docker)
  - [Setup Locally](#Setup-Locally)
    - [Step One: Creating the virtual environment](#Create-virtual-env-or-venv)
    - [Step Two: Activating the venv](#Activate-virtual-environment)
    - [Step Three: Installing requirements](#Install-all-requirements-inside-virtual-environment-to-run-the-scrapper)
    - [Running Locally](#Running-the-Scrapper-Locally)
- [Tests](#Tests)
  - [Tests Covered](#Tests-covered)
- [Information](#Information)
- [Possible Expansions](#Possible-Expansions)
- [Dev Notes](#Dev-notes)
- [Author](#Author)
## Instructions
### Setup Docker Image
#### ⚠ **Warning:** be sure to verify you're inside the project's root folder.
### Creating Image From `Dockerfile`.
```bash
docker build -t module .
```
### Running the Scrapper on Docker
This `websites.txt` is a pre-built file for testing
```bash
cat websites.txt | docker run -i module
```
### Setup Locally
To run locally you will need to follow these steps, I assume you're inside the project's root folder.
#### Create virtual env or `venv`:
```bash
python -m venv venv
```
#### Activate virtual environment:
```bash
source venv/bin/activate
```
#### Install all requirements inside virtual environment to run the scrapper:
```bash
pip install -r requirements
```
### Running the Scrapper Locally
This will only work if the commands from [Setup Locally](#Setup-Locally) were successfully executed.
```bash
cat websites.txt | python -m module
```
## Tests
To run tests you will need to be inside the `venv`, verify if you're inside project's root folder. Also, your global python version should be [Python 3.12.2](https://www.python.org/downloads/release/python-3122/), and you have successfully followed the steps from [Setup Locally](#Setup-Locally).
```bash
python -m unittest tests/TestScrapper.py -v
```
### Tests covered
All tests are run on a local html copy of the site: `https://www.cmsenergy.com/contact-us/default.aspx`. I've done this to prevent scope changes so the test fails without something being wrong
 
- [X] UrlHandler
  - Filters the valid from the invalid URLs
- [x] LogoHandler
  - Matches if the found `logo url` is the same on the site.
- [x] PhoneHandler
  - Matches if the found `phones: [str]` are the ones on the site.
- [x] Scrapper Full Lifecycle
  - As the tests run single pieces of the Scrapper one at a time, there's also a test to run the Scrapper's full lifecycle

## Information
I have provided a **websites.txt** file that I used for tests containing **25 valid urls**, any txt file with formatted urls can be used.
These are some rules

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
- There are two different `logs`:
  - **log**: Located on root folder, this contains the application log.
  - **tests.tests_log**: Located inside `tests Package`, this contains only the test log, it has the same format from the other log, but only displays tests information.

Testing with this testing file shows an average of `5 URLs` scrapped per **second**, this average is variable depending on various factors, these being the most important:
- Where the website is hosted.
- Server response time.
- Size of page's content.

## Limitations
Due to striving to get all phone numbers in every part of the world my idea was, get the URLs `country_code` from it's `IP address`
and format the phone number based on that, this is the most successful case I found while trying different methods, but it still presents errors sometimes when a website
has automatic redirection to a closer host enabled.
## Possible Expansions
- .svg logos can be saved to a local file with a shared folder between the container and host if they don't have a valid url.
  - This one I have tested and can be implemented easily, but it costs processing power, so for it to be more viable needs to be optimized.
### Dev notes
- Phone formatting is limited for the IP address origins country due to much more processing power needed to match every single phone type in all websites around the world.
- To find possible logo images I appealed to a common string that could be inside tags that could contain an image, if the tag has `'logo'` written in any of these: `alt`, `src`, `class`. Also, it skips the tag if there's no `src` as would not be possible to return a functional `url` to the image.
----------------
### Author
- [Matheus Boesing da Silva / besigne](https://github.com/besigne) - Sole Developer
