import base64
import os

from bson import Binary, UUID_SUBTYPE
from dotenv import load_dotenv

load_dotenv()

connection_string = os.getenv('MONGODB', "mongodb://127.0.0.1:27021/")

MAIN_DEK_ID = None
if os.getenv('MAIN_DEK_ID'):
    MAIN_DEK_ID = Binary(base64.b64decode(os.getenv('MAIN_DEK_ID').encode('utf-8')), UUID_SUBTYPE)

master_key_filename = 'master-key.txt'

key_vault_database = "vault"
key_vault_collection = "__keyVault"
key_vault_namespace = f"{key_vault_database}.{key_vault_collection}"

collection_name = 'hsk_encyrpt'


def get_kms_providers():
    path = "./" + master_key_filename
    with open(path, "rb") as f:
        local_master_key = f.read()

    return {
        "local": {
            "key": local_master_key
        },
    }
