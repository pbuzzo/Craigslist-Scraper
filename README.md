# Chicago Craigslist Job Scraper
## By: Patrick Buzzo


### This is a Python program that routinely searches (Chicago) Craigslist's job section for the latest postings that include specified keywords in their titles. This program was created out of necessity, in order to allow myself early access to the most recent job postings without staring at the listings page for the whole day. 

### After this program is started by the user, three .txt files are created:
- craigslist.txt: A file that is updated only when new jobs that haven't been identified by the program in the past are found.
- output_file.txt: A file that will inlcude all jobs related to the specified keywords upon scraping the page each time the program executes, despite whether or not it is a new or previosuly identified job.
- dirwatcher.log: A log file that logs the execution of the program over time (errors, debubs, etc.). Used for data and analytical purposes.

## Usage: 

1. `git clone https://github.com/pbuzzo/Craigslist-Scraper.git craigslist-scraper`
2. `cd craigslist-scraper`
3. `poetry shell`
4. `poetry3 scraper.py`

*** Note: THe keywords are currently set to 'developer,' 'PHP,' 'tech' by default for debugging purposes and ease to presenting. 