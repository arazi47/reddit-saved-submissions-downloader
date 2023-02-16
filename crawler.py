from submission import *

import praw

import urllib.request
import os

from bs4 import BeautifulSoup

MAX_SUBMISSIONS_PER_PAGE = 25

class Crawler:
	def __init__(self, cfg):
		self.cfg = cfg


	def get_saved_links(self):
		result = praw.Reddit(client_id = self.cfg.get_client_id(), client_secret = self.cfg.get_client_secret(), username = self.cfg.get_username(), password = self.cfg.get_password(), user_agent = self.cfg.get_user_agent())

		saved_links = result.user.me().saved(limit = self.cfg.get_pages_to_crawl() * MAX_SUBMISSIONS_PER_PAGE)
		saved_links = list(saved_links)

		return saved_links


	def get_saved_submissions(self, savedLinks):
		submissions = []

		total_submissions = len(savedLinks)

		for submission_index, curr_submission in enumerate(savedLinks):
			# Apparently the videos will also go in here
			if type(curr_submission) is praw.models.Submission:
				new_submission = Submission()

				# /r/abc
				new_submission.subreddit = curr_submission.subreddit.url

				new_submission.title = curr_submission.title
				new_submission.subreddit_title = curr_submission.subreddit.title


				# i.imgur.com/something.jpg
				new_submission.bodyUrl = curr_submission.url

				# this is reddit's post url
				new_submission.postUrl = curr_submission.permalink

				new_submission.extension = new_submission.get_extension()

				submissions.append(new_submission)

				print(self.get_percentage_complete(submission_index, total_submissions))
			else:
				print('[ERROR] Submission doesn\'t seem to be an image, skipping.')

		return submissions


	def directory_non_existant(self, path):
		if not os.path.exists(path):
			return True

		return False


	def make_dir(self, path):
		os.makedirs(path)


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

		if 'imgur' in url and '/a/' in url:
			return True

		return False


	def download_direct_url(self, url, savePath):
		# TODO solve this
		# if we download an album, all files will have the same name
		if (self.file_exists(savePath)):
			print('[WARNING] File ' + savePath[savePath.rfind('/') + 1:] + ' has already been downloaded, skipping.')
			return

		try:
			print('Trying direct download')
			urllib.request.urlretrieve(url, savePath)
		except IOError as error:
			print('[ERROR] AT DOWNLOADING...')
			print(error)


	def download_indirect_imgur_url(self, sourceCode, url, savePath):
		print('Trying indirect download ' + savePath)
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
		self.download_direct_url(url, savePath)


	def download_imgur_album(self, sourceCode, url, savePath):
		print('Downloading album')
		soup = BeautifulSoup(sourceCode, 'lxml')

		for image in soup.select('.post-image'):
			imageUrl = image.a['href']
			self.download_direct_url('http://' + imageUrl[2:], savePath)


	def download_submissions(self, submissions):
		for curr_submission_index, submission in enumerate(submissions):
			# 3 => skip /r/
			save_path = os.getcwd() + "\\Downloads\\" + submission.subreddit[3:]

			url = submission.bodyUrl

			if self.directory_non_existant(save_path):
				self.make_dir(save_path)

			if self.is_direct_imgur_url(url) or self.is_reddit_image_url(url):
				self.download_direct_url(url, save_path + submission.title + '.' + submission.extension)
			# join these 2 elifs together, why would we need two if they almost do the same thing?
			elif self.is_indirect_imgur_url(url):
				request = urllib.request.Request(url)
				page = urllib.request.urlopen(request)
				sourceCode = page.read()
				self.download_indirect_imgur_url(sourceCode, url, save_path + submission.title + '.' + submission.extension)
			elif self.is_imgur_album(url):
				request = urllib.request.Request(url)
				page = urllib.request.urlopen(request)
				sourceCode = page.read()
				self.download_imgur_album(sourceCode, url, save_path + submission.title + '.' + submission.extension)
			else:
				# @TODO
				# gifv, gfycat
				print('[ERROR] Not direct && not indirect && not album!')

			# @TODO
			# does this even print something?
			self.get_percentage_complete(curr_submission_index, len(submissions))

	def delete_empty_folders(self):
		files = os.listdir('downloads')
		for file in files:
			if not os.listdir('downloads\\' + file):
				os.rmdir('downloads\\' + file)
