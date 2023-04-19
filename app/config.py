# from dotenv import load_dotenv
# import os
# load_dotenv()
from pydantic import BaseSettings, root_validator


class Settings(BaseSettings):
	POSTGRESQL_LOCALHOST: str
	POSTGRESQL_PORT: int
	POSTGRESQL_USERNAME: str
	POSTGRESQL_DATABASE_NAME: str
	POSTGRESQL_PASSWORD: str

	@property
	def DATABASE_URL(self):
		return (f'postgresql+asyncpg://{self.POSTGRESQL_USERNAME}:'
				f'{self.POSTGRESQL_PASSWORD}@{self.POSTGRESQL_LOCALHOST}:'
				f'{self.POSTGRESQL_PORT}/{self.POSTGRESQL_DATABASE_NAME}')

	class Config:
		env_file = '.env'


settings = Settings()

# print(settings.DATABASE_URL)



# DB_HOST = os.getenv('POSTGRESQL_LOCALHOST')
# DB_PORT = os.getenv('POSTGRESQL_PORT')
# DB_USERNAME = os.getenv('POSTGRESQL_USERNAME')
# DB_NAME = os.getenv('POSTGRESQL_DATABASE_NAME')
# DB_PASSWORD = os.getenv('POSTGRESQL_PASSWORD')
#
# DB_HOST_TEST = os.getenv('POSTGRESQL_LOCALHOST_TEST')
# DB_PORT_TEST = os.getenv('POSTGRESQL_PORT_TEST')
# DB_USERNAME_TEST = os.getenv('POSTGRESQL_USERNAME_TEST')
# DB_NAME_TEST = os.getenv('POSTGRESQL_DATABASE_NAME_TEST')
# DB_PASSWORD_TEST = os.getenv('POSTGRESQL_PASSWORD_TEST')