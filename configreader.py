DEFAULT_PAGES_TO_CRAWL = 1
MAX_PAGES_TO_CRAWL = 100

class ConfigReader:
	def __init__(self):
		self.file = 'config.ini'
		self.clientId = ''
		self.clientSecret = ''
		self.username = ''
		self.password = ''
		self.userAgent = ''
		self.pagesToCrawl = DEFAULT_PAGES_TO_CRAWL
		self.savePath = ''


	def setPagesToCrawl(self, pagesToCrawl):
		pagesToCrawl = pagesToCrawl[:-1]
		if pagesToCrawl.isdigit():
			self.pagesToCrawl = int(pagesToCrawl)

			# we put this check here, since we can't possibly get to it if we get in the else block
			if self.pagesToCrawl > MAX_PAGES_TO_CRAWL:
				print('[WARNING] Pages to crawl greater than the maximum, setting it to the maximum, which is ' + str(MAX_PAGES_TO_CRAWL) + '.')
				self.pagesToCrawl = MAX_PAGES_TO_CRAWL
		else:
			print('[WARNING] Pages to crawl not int - setting it to ' + str(DEFAULT_PAGES_TO_CRAWL) + '.')
			self.pagesToCrawl = DEFAULT_PAGES_TO_CRAWL


	def setConfigAccordingly(self, setting):
		'''
		Given the setting name from the file, we determine which one it is and set it in the program
		'''

		# debug
		#print("got setting: " + setting)

		if 'clientId' in setting:
			#print("SETTING CLIENT ID TO " + setting[setting.find('=') + 1:].lstrip())
			self.clientId = setting[setting.find('=') + 1:].lstrip()
			self.clientId = self.clientId[:-1]
		elif 'clientSecret' in setting:
			#print("SETTING SECRET TO " + setting)
			self.clientSecret = setting[setting.find('=') + 1:].lstrip()
			self.clientSecret = self.clientSecret[:-1]
		elif 'username' in setting:
			#print("SETTING USERNAME TO " + setting)
			self.username = setting[setting.find('=') + 1:].lstrip()
			self.username = self.username[:-1]
		elif 'password' in setting:
			#print("SETTING PASSWORD TO " + setting)
			self.password = setting[setting.find('=') + 1:].lstrip()
			self.password = self.password[:-1]
		elif 'userAgent' in setting:
			#print("SETTING USER AGENT TO " + setting)
			self.userAgent = setting[setting.find('=') + 1:].lstrip()
			self.userAgent = self.userAgent[:-1]
		elif 'pagesToCrawl' in setting:
			#print("SETTING PAGES TO CRAWL TO " + setting[setting.find('=') + 1:].lstrip())
			self.setPagesToCrawl(setting[setting.find('=') + 1:].lstrip())
		elif 'savePath' in setting:
			#print("SETTING SAVEPATH TO " + setting)
			self.savePath = setting[setting.find('=') + 1:].lstrip()
			self.savePath = self.savePath[:-1]


	def readConfiguration(self):
		'''
		Read the configuration file and set the client id, secret etc, accordingly
		'''

		# r - read mode
		with open(self.file, "r") as f:
			data = f.readlines()

		for line in data:
			line.lstrip()
			# line is empty
			if len(line) == 1:
				continue

			# this is a comment
			if line[0] == '#':
				continue

			self.setConfigAccordingly(line)


	def getClientId(self):
		return self.clientId


	def getClientSecret(self):
		return self.clientSecret


	def getUsername(self):
		return self.username


	def getPassword(self):
		return self.password


	def getUserAgent(self):
		return self.userAgent


	def getPagesToCrawl(self):
		return self.pagesToCrawl


	def getSavePath(self):
		return self.savePath