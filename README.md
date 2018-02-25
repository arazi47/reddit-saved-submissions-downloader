# Reddit Saved Content Downloader

You can use this app to download your imgur/i.redd.it image links (gifs too!) to your hard drive, sorted by subreddit.

## Setup
1. Go to https://www.reddit.com/prefs/apps/ (while being logged in on Reddit)
2. Go to the bottom of the page and click "create another app..."
	2.1 Name: whatever you like
	2.2 Check the box named `script`
	2.3 Redirect uri: http://localhost:8080
3. Click on `create app`
4. Open `config.ini` and complete the variables as follows:
	4.1 clientId: copy the text under `personal use script`
	4.2 clientSecret: copy the text to the right of `secret`
	4.3 Fill in your Reddit username & password
	4.4 userAgent: leave it like that
	4.5 pagesToCrawl: how many saved pages on Reddit you'd like the app to crawl and download the submissions from
	4.6 savePath: full path to where the subreddit folders will be created and the submissions will be downloaded to (ex: "C:\Downloads\")

## Notes
1. You need to have Python 3 installed in order for the app to run. 
2. Make sure you have installed (preferably using pip) the following modules: `praw`, `bs4`