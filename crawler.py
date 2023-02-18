from configreader import *
from submission import *

import praw

import urllib.request
import os

from bs4 import BeautifulSoup

MAX_SUBMISSIONS_PER_PAGE = 25
DEFAULT_DOWNLOAD_FOLDER = "Downloads"

class Crawler:
	def __init__(self):
		self.__config_reader = ConfigReader()


	def remove_invalid_file_name_symbols(self, file_name):
		invalid_filename_characters = "/\:*?\"<>|"
		for char in invalid_filename_characters:
			file_name = file_name.replace(char, "")
		
		return file_name


	def get_saved_links(self):
		result = praw.Reddit(client_id = self.__config_reader.get_client_id(), client_secret = self.__config_reader.get_client_secret(), username = self.__config_reader.get_username(), password = self.__config_reader.get_password(), user_agent = self.__config_reader.get_user_agent())

		saved_links = result.user.me().saved(limit = self.__config_reader.get_pages_to_crawl() * MAX_SUBMISSIONS_PER_PAGE)
		saved_links = list(saved_links)

		return saved_links


	def get_saved_submissions(self, saved_links):
		submissions = []

		total_submissions = len(saved_links)

		for submission_index, curr_submission in enumerate(saved_links):
			# Apparently the videos will also go in here
			if type(curr_submission) is praw.models.Submission:
				new_submission = Submission()
				# /r/abc/
				new_submission.subreddit = curr_submission.subreddit.url.split("/")[2]
				new_submission.title = self.remove_invalid_file_name_symbols(curr_submission.title)

				# i.imgur.com/something.jpg
				new_submission.url = curr_submission.url
				new_submission.extension = curr_submission.url[curr_submission.url.rfind('.') + 1:]
				submissions.append(new_submission)

				print(self.get_percentage_complete(submission_index, total_submissions))
			else:
				print('[ERROR] Submission doesn\'t seem to be an image, skipping.')

		return submissions

	# This is needed for checking if an image exists or not
	def get_file_extension_from_url(self, url):
		return url[url.find('.') + 1:]


	def file_exists(self, path):
		return os.path.isfile(path)


	def get_percentage_complete(self, current_item, total_items):
		if total_items:
			return str(int(((float(current_item + 1) / float(total_items)) * 100))) + '%'


	# i.redd.it image links
	def is_reddit_image_url(self, url):
		if len(url) == 0:
			return False

		if 'i.redd.it' in url:
			return True

		return False


	# when it's imgur.com/something
	# and not i.imgur/something.extension
	# basically, when the link does not point directly to the image
	def is_indirect_imgur_url(self, url):
		if len(url) == 0:
			return False

		if 'i.imgur' in url:
			return False

		# if there's an /a/, it's an album
		if 'imgur' in url and '/a/' not in url:
			return True

		return False


	def is_direct_imgur_url(self, url):
		if len(url) == 0:
			return False

		if 'i.imgur' in url and '/a/' not in url:
			return True

		return False


	def is_imgur_album(self, url):
		if len(url) == 0:
			return False

		if 'i.imgur' in url:
			return False

		if 'imgur' in url and ('/a/' in url or '/gallery/' in url):
			return True

		return False


	def download_direct_url(self, url, save_path):
		if (self.file_exists(save_path)):
			print('[WARNING] File ' + save_path + ' has already been downloaded, skipping.')
			return

		try:
			print("================================================")
			print('Trying direct download: ', url, save_path)
			urllib.request.urlretrieve(url, save_path)
		except IOError as error:
			print('[ERROR] AT DOWNLOADING...')
			print(error)
		print("================================================")


	def download_indirect_imgur_url(self, sourceCode, url, save_path):
		print('Trying indirect download ' + save_path)
		# get the direct imgur url from the page that contains a single image
		#print(url)
		#soup = BeautifulSoup(sourceCode, 'lxml')
		#imageUrl = soup.select('.post-image')[0].a['href']

		# 2: because the link starts with //
		# we could just write 'http:' + imageUrl, but I did it this way
		# just for a better understanding :)
		#self.downloadDirectImgurUrl('http://' + imageUrl[2:], savePath)

		# I don't know if this is a hackfix or not, but it seems to do it's job
		# Add the i. to get the direct download link from imgur
		url = url[:8] + 'i.' + url[8:]
		self.download_direct_url(url, save_path)


	def download_imgur_album(self, source_code, save_path):
		print('Downloading album')
		soup = BeautifulSoup(source_code, 'html.parser')
		source_code = str(soup)
		what_to_search_for = '\\"basename\\":\\"\\",\\"url\\":\\"'

		found_at = source_code.find(what_to_search_for)
		while found_at != -1:
			beginning_of_image_url = found_at + len(what_to_search_for)
			image_url = source_code[beginning_of_image_url:].split('\\"')[0]

			file_name = image_url[image_url.rfind('/') + 1:]
			self.download_direct_url(image_url, save_path + file_name)

			source_code = source_code[beginning_of_image_url + len(image_url):]
			found_at = source_code.find(what_to_search_for)


	def download_submissions(self, submissions):
		for curr_submission_index, submission in enumerate(submissions):
			save_path = os.getcwd() + "\\" + DEFAULT_DOWNLOAD_FOLDER + "\\" + submission.subreddit + "\\"
			url = submission.url
		
			if not os.path.exists(save_path):
				os.makedirs(save_path)

			if self.is_direct_imgur_url(url) or self.is_reddit_image_url(url):
				save_path = save_path + submission.title + '.' + submission.extension
				self.download_direct_url(url, save_path)
			elif self.is_indirect_imgur_url(url) or self.is_imgur_album(url):
				request = urllib.request.Request(url)
				page = urllib.request.urlopen(request)
				source_code = page.read()
				if self.is_imgur_album(url):
					self.download_imgur_album(source_code, save_path)
				else:
					save_path = save_path + submission.title + '.' + submission.extension
					self.download_indirect_imgur_url(source_code, url, save_path)

			else:
				print('[ERROR] Not direct && not indirect && not album:', url, save_path)

			print(self.get_percentage_complete(curr_submission_index, len(submissions)))

	def delete_empty_folders(self):
		files = os.listdir(DEFAULT_DOWNLOAD_FOLDER)
		for file in files:
			if not os.listdir(DEFAULT_DOWNLOAD_FOLDER + "\\" + file):
				os.rmdir(DEFAULT_DOWNLOAD_FOLDER + "\\" + file)
