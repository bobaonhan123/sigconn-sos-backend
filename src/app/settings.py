from os import getenv

MONGO_HOST = getenv("MONGO_HOST", "localhost")
MONGO_PORT = int(getenv("MONGO_PORT", 0)) or 27017
MONGO_USER = getenv("MONGO_USER", "root")
MONGO_PASSWORD = getenv("MONGO_PASSWORD", "rootpassword")
MONGO_DB_NAME = getenv("MONGO_DB_NAME", "sigconn_sos")

SECURITY_ALGORITHM = getenv("SECURITY_ALGORITHM", "HS256")
SECRET_KEY = getenv("SECRET_KEY", "")
ACCESS_TOKEN_EXPIRE_MINUTES = int(getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 60*24*30))
