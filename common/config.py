import os

try:
    MONGO_USER = os.environ.get("MONGO_USER", "chetanjarande")
    PASSWORD = os.environ.get("PASSWORD", "Chetan31")
    MONGO_CLUSTER = os.environ.get("MONGO_CLUSTER", "chetanmongodbcluster1")
    DB_NAME = os.environ.get("DB_NAME", "TelegramBots")
    COLLECTION_NAME = os.environ.get("COLLECTION_NAME", "UrlShortner")
    MONGO_DB_URL = os.environ.get("MONGO_DB_URL", "mongodb+srv://chetanjarande:Chetan31@chetanmongodbcluster1.muj08bi.mongodb.net/?retryWrites=true&w=majority")

except Exception as err:
    raise KeyError("could not find the key", str(err))

