from submission import *

import praw

import urllib.request
import os

from bs4 import BeautifulSoup

MAX_SUBMISSIONS_PER_PAGE = 25

class Crawler:
	def __init__(self, cfg):
		self.cfg = cfg


	def getSavedLinks(self):
		result = praw.Reddit(client_id = self.cfg.getClientId(), client_secret = self.cfg.getClientSecret(), username = self.cfg.getUsername(), password = self.cfg.getPassword(), user_agent = self.cfg.getUserAgent())

		savedLinks = result.user.me().saved(limit = self.cfg.getPagesToCrawl() * MAX_SUBMISSIONS_PER_PAGE)
		savedLinks = list(savedLinks)

		return savedLinks


	def getSavedSubmissions(self, savedLinks):
		submissions = []

		totalSubmissions = len(savedLinks)

		for submissionIndex, currSubmission in enumerate(savedLinks):
			# Apparently the videos will also go in here
			if type(currSubmission) is praw.models.Submission:
				newSubmission = Submission()

				# /r/abc
				newSubmission.subreddit = currSubmission.subreddit.url

				newSubmission.title = currSubmission.title
				newSubmission.subredditTitle = currSubmission.subreddit.title


				# i.imgur.com/something.jpg
				newSubmission.bodyUrl = currSubmission.url

				# this is reddit's post url
				newSubmission.postUrl = currSubmission.permalink

				newSubmission.extension = newSubmission.getExtension()

				submissions.append(newSubmission)

				print(self.printPercentageComplete(submissionIndex, totalSubmissions))
			else:
				print('[ERROR] Submission doesn\'t seem to be an image, skipping.')

		return submissions


	def directoryNonExistant(self, path):
		if not os.path.exists(path):
			return True

		return False


	def makeDir(self, path):
		os.makedirs(path)


	# This is needed for checking if an image exists or not
	def getFileTypeFromUrl(self, url):
		return url[url.find('.') + 1:]


	def fileAlreadyExists(self, path):
		return os.path.isfile(path)


	def printPercentageComplete(self, currentItem, numItems):
		if numItems:
			return str(int(((float(currentItem + 1) / float(numItems)) * 100))) + '%'


	# i.redd.it image links
	def isRedditImageUrl(self, url):
		if len(url) == 0:
			return False

		if 'i.redd.it' in url:
			return True

		return False


	# when it's imgur.com/something
	# and not i.imgur/something.extension
	# basically, when the link does not point directly to the image
	def isIndirectImgurUrl(self, url):
		if len(url) == 0:
			return False

		if 'i.imgur' in url:
			return False

		# if there's an /a/, it's an album
		if 'imgur' in url and '/a/' not in url:
			return True

		return False


	def isDirectImgurUrl(self, url):
		if len(url) == 0:
			return False

		if 'i.imgur' in url and '/a/' not in url:
			return True

		return False


	def isImgurAlbum(self, url):
		if len(url) == 0:
			return False

		if 'i.imgur' in url:
			return False

		if 'imgur' in url and '/a/' in url:
			return True

		return False


	def downloadDirectUrl(self, url, savePath):
		# TODO solve this
		# if we download an album, all files will have the same name
		if (self.fileAlreadyExists(savePath)):
			print('[WARNING] File ' + savePath[savePath.rfind('/') + 1:] + ' has already been downloaded, skipping.')
			return

		try:
			print('Trying direct download')
			urllib.request.urlretrieve(url, savePath)
		except IOError as error:
			print('[ERROR] AT DOWNLOADING...')
			print(error)


	def downloadIndirectImgurUrl(self, sourceCode, url, savePath):
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
		self.downloadDirectUrl(url, savePath)


	def downloadImgurAlbum(self, sourceCode, url, savePath):
		print('Downloading album')
		soup = BeautifulSoup(sourceCode, 'lxml')

		for image in soup.select('.post-image'):
			imageUrl = image.a['href']
			self.downloadDirectUrl('http://' + imageUrl[2:], savePath)


	def downloadSubmissions(self, submissions):
		for currSubmissionIndex, submission in enumerate(submissions):
			# 3 => skip /r/
			savePath = os.getcwd() + "\\Downloads\\" + submission.subreddit[3:]

			url = submission.bodyUrl

			if self.directoryNonExistant(savePath):
				self.makeDir(savePath)

			if self.isDirectImgurUrl(url) or self.isRedditImageUrl(url):
				self.downloadDirectUrl(url, savePath + submission.title + '.' + submission.extension)
			# join these 2 elifs together, why would we need two if they almost do the same thing?
			elif self.isIndirectImgurUrl(url):
				request = urllib.request.Request(url)
				page = urllib.request.urlopen(request)
				sourceCode = page.read()
				self.downloadIndirectImgurUrl(sourceCode, url, savePath + submission.title + '.' + submission.extension)
			elif self.isImgurAlbum(url):
				request = urllib.request.Request(url)
				page = urllib.request.urlopen(request)
				sourceCode = page.read()
				self.downloadImgurAlbum(sourceCode, url, savePath + submission.title + '.' + submission.extension)
			else:
				# @TODO
				# gifv, gfycat
				print('[ERROR] Not direct && not indirect && not album!')

			# @TODO
			# does this even print something?
			self.printPercentageComplete(currSubmissionIndex, len(submissions))

	def deleteEmptyFolders(self):
		files = os.listdir('downloads')
		for file in files:
			if not os.listdir('downloads\\' + file):
				os.rmdir('downloads\\' + file)
