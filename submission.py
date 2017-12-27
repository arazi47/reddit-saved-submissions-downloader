class Submission:
	def __init__(self):
		self.subreddit = ''
		self.title = ''
		self.subredditTitle = ''
		self.bodyUrl = ''
		self.postUrl = ''
		self.extension = ''

	def getExtension(self):
		return self.bodyUrl[self.bodyUrl.rfind('.') + 1:]
