'''
@TODO:
	- add support for imgur's gifv files, gfycat, indirect file types (not i.imgur, for example)
	- webm (maybe?), imgur albums

	- read settings (user, pass and the rest) from a settings file
'''

from crawler import *

# for calculating how long it took the crawler to finish its job
from datetime import datetime


def main():
	# requests only accepts if the string starts with http:// (no www required though)
	startTime = datetime.now()

	crawler = Crawler()
	savedLinks = crawler.get_saved_links()
	submissions = crawler.get_saved_submissions(savedLinks)
	crawler.download_submissions(submissions)
	crawler.delete_empty_folders()

	finishTime = datetime.now()

	print('Done! Operation completed in ' + str(int((finishTime - startTime).total_seconds())) + ' seconds.')

if __name__ == '__main__':
	main()
