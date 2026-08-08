import os
import streamlit as st
from pymongo import MongoClient
from pymongo.errors import ServerSelectionTimeoutError, ConnectionFailure
from dotenv import load_dotenv

load_dotenv()


@st.cache_resource
def get_client() -> MongoClient:
    uri = os.getenv("MONGO_URI", "mongodb://127.0.0.1:27017/")
    client = MongoClient(uri, serverSelectionTimeoutMS=5000)
    return client


def get_db():
    db_name = os.getenv("MONGO_DB", "gamemetrics")
    return get_client()[db_name]


def check_connection() -> tuple[bool, str]:
    try:
        client = get_client()
        client.admin.command("ping")
        return True, "Connexion MongoDB établie avec succès."
    except (ServerSelectionTimeoutError, ConnectionFailure) as e:
        return False, f"Impossible de joindre MongoDB : {e}"
    except Exception as e:
        return False, f"Erreur inattendue : {e}"
