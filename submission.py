class Submission:
	def __init__(self):
		self.subreddit = ''
		self.title = ''
		self.subreddit_title = ''
		self.bodyUrl = ''
		self.postUrl = ''
		self.extension = ''

	def get_extension(self):
		return self.bodyUrl[self.bodyUrl.rfind('.') + 1:]
