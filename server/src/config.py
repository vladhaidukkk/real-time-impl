from decouple import Config, RepositoryEnv

config = Config(RepositoryEnv(".env"))

SECRET_KEY = config("SECRET_KEY")
