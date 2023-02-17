# Reddit Saved Submissions Downloader

You can use this app to download your imgur/i.redd.it image links (gifs too!) to your hard drive, sorted by subreddit.

## Setup
1. Go to https://www.reddit.com/prefs/apps/ (while being logged in on Reddit)
2. Go to the bottom of the page and click "create another app..."

   2.1 Name: whatever you like

   2.2 Check the box named `script`

   2.3 Redirect uri: http://localhost:8080
3. Click on `create app`

4. Open `config.ini` and complete the variables as follows:

   4.1 `client_id`: copy the text under `personal use script`

   4.2 `client_secret`: copy the text to the right of `secret`

   4.3 `username`: your Reddit username

   4.4 `password`: your Reddit password

   4.5 `pages_to_crawl`: how many saved pages on Reddit you'd like the app to crawl and download the submissions from

## Notes
1. You need to have Python 3 installed in order for the app to run. 
2. Make sure you have installed (preferably using pip) the following modules: `praw`, `bs4`