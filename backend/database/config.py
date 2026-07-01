from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from dotenv import load_dotenv
import certifi
import os

load_dotenv()

PASS = os.getenv("PASS")

uri = f"mongodb+srv://VedantGupta:{PASS}@smartnotes.zst1wy8.mongodb.net/"

client = MongoClient(
    uri,
    server_api=ServerApi("1"),
    tlsCAFile=certifi.where(),
)

try:
    client.admin.command("ping")
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)
