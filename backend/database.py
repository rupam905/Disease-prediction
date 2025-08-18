from pymongo import MongoClient

MONGO_URL = "mongodb+srv://rupamdutta905:rupamdutta7980@cluster0.j5ghcds.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0",


client = MongoClient(MONGO_URL, tls=True,
    tlsAllowInvalidCertificates=True)

db = client["disease_prediction"]
users_collection = db["users"]
