from configparser import ConfigParser

CONFIG_FILE = "config.ini"
DEFAULT_PAGES_TO_CRAWL = 1
MAX_PAGES_TO_CRAWL = 100

class ConfigReader:
	def __init__(self):
		config = ConfigParser()
		config.read('config.ini')
		self.__client_id = config.get('application', 'client_id')
		self.__client_secret = config.get('application', 'client_secret')
		self.__user_agent = config.get('application', 'user_agent')
		self.__username = config.get('reddit', 'username')
		self.__password = config.get('reddit', 'password')
		self.__pages_to_crawl = config.getint('settings', 'pages_to_crawl')

		if self.__pages_to_crawl > MAX_PAGES_TO_CRAWL:
			print('[WARNING] Pages to crawl greater than the maximum, setting it to the maximum, which is ' + str(MAX_PAGES_TO_CRAWL) + '.')
			self.__pages_to_crawl = MAX_PAGES_TO_CRAWL

		assert self.__client_id
		assert self.__client_secret
		assert self.__user_agent
		assert self.__username
		assert self.__password
		assert self.__pages_to_crawl


	def get_client_id(self):
		return self.__client_id


	def get_client_secret(self):
		return self.__client_secret


	def get_username(self):
		return self.__username


	def get_password(self):
		return self.__password


	def get_user_agent(self):
		return self.__user_agent


	def get_pages_to_crawl(self):
		return self.__pages_to_crawl
