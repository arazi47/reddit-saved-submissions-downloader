DEFAULT_PAGES_TO_CRAWL = 1
MAX_PAGES_TO_CRAWL = 100

class ConfigReader:
	def __init__(self):
		self.file = 'config.ini'
		self.client_id = ''
		self.client_secret = ''
		self.username = ''
		self.password = ''
		self.user_agent = ''
		self.pages_to_crawl = DEFAULT_PAGES_TO_CRAWL


	def set_pages_to_crawl(self, pages_to_crawl):
		pages_to_crawl = pages_to_crawl[:-1]
		if pages_to_crawl.isdigit():
			self.pages_to_crawl = int(pages_to_crawl)

			# we put this check here, since we can't possibly get to it if we get in the else block
			if self.pages_to_crawl > MAX_PAGES_TO_CRAWL:
				print('[WARNING] Pages to crawl greater than the maximum, setting it to the maximum, which is ' + str(MAX_PAGES_TO_CRAWL) + '.')
				self.pages_to_crawl = MAX_PAGES_TO_CRAWL
		else:
			print('[WARNING] Pages to crawl not int - setting it to ' + str(DEFAULT_PAGES_TO_CRAWL) + '.')
			self.pages_to_crawl = DEFAULT_PAGES_TO_CRAWL


	def set_config_accordingly(self, setting):
		'''
		Given the setting name from the file, we determine which one it is and set it in the program
		'''

		if 'clientId' in setting:
			self.client_id = setting[setting.find('=') + 1:].lstrip()
			self.client_id = self.client_id[:-1]
		elif 'clientSecret' in setting:
			self.client_secret = setting[setting.find('=') + 1:].lstrip()
			self.client_secret = self.client_secret[:-1]
		elif 'username' in setting:
			self.username = setting[setting.find('=') + 1:].lstrip()
			self.username = self.username[:-1]
		elif 'password' in setting:
			self.password = setting[setting.find('=') + 1:].lstrip()
			self.password = self.password[:-1]
		elif 'userAgent' in setting:
			self.user_agent = setting[setting.find('=') + 1:].lstrip()
			self.user_agent = self.user_agent[:-1]
		elif 'pagesToCrawl' in setting:
			self.set_pages_to_crawl(setting[setting.find('=') + 1:].lstrip())


	def read_configuration(self):
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

			self.set_config_accordingly(line)


	def get_client_id(self):
		return self.client_id


	def get_client_secret(self):
		return self.client_secret


	def get_username(self):
		return self.username


	def get_password(self):
		return self.password


	def get_user_agent(self):
		return self.user_agent


	def get_pages_to_crawl(self):
		return self.pages_to_crawl
