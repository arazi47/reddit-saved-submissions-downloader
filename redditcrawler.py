'''
@TODO:
	- add support for imgur's gifv files, gfycat, indirect file types (not i.imgur, for example)
	- webm (maybe?), imgur albums

	- read settings (user, pass and the rest) from a settings file
'''

from crawler import *

from configreader import *

# for calculating how long it took the crawler to finish its job
from datetime import datetime


def main():
	# requests only accepts if the string starts with http:// (no www required though)

	cfgReader = ConfigReader()
	cfgReader.readConfiguration()

	startTime = datetime.now()

	crawler = Crawler(cfgReader)
	savedLinks = crawler.getSavedLinks()
	submissions = crawler.getSavedSubmissions(savedLinks)
	crawler.downloadSubmissions(submissions)


	finishTime = datetime.now()

	print('Done! Operation completed in ' + str(int((finishTime - startTime).total_seconds())) + ' seconds.')

if __name__ == '__main__':
	main()