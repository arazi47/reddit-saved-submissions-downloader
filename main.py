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
	start_time = datetime.now()

	crawler = Crawler()
	saved_links = crawler.get_saved_links()
	submissions = crawler.get_saved_submissions(saved_links)
	crawler.download_submissions(submissions)
	crawler.delete_empty_folders()

	finish_time = datetime.now()
	print('Done! Operation completed in ' + str(int((finish_time - start_time).total_seconds())) + ' seconds.')

if __name__ == '__main__':
	main()
