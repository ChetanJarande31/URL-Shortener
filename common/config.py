import os

try:
    MONGO_USER=os.environ("MONGO_USER")
    PASSWORD =os.environ("PASSWORD")
    MONGO_CLUSTER =os.environ("MONGO_CLUSTER")
    DB_NAME =os.environ("DB_NAME")
    COLLECTION_NAME =os.environ("COLLECTION_NAME")
    MONGO_DB_URL =os.environ("MONGO_DB_URL")

except Exception:
    raise ValueError("could not find the key")
