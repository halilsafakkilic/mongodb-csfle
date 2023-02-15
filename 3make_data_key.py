import base64

from bson import STANDARD, CodecOptions
from pymongo import MongoClient
from pymongo.encryption import ClientEncryption

from settings import connection_string, get_kms_providers, key_vault_namespace

mongo_client = MongoClient(connection_string)

client_encryption = ClientEncryption(
    get_kms_providers(),
    key_vault_namespace,
    mongo_client,
    CodecOptions(uuid_representation=STANDARD),
)
data_key_id = client_encryption.create_data_key("local")
base_64_data_key_id = base64.b64encode(data_key_id)

with open('.env', 'w') as f:
    f.write('MAIN_DEK_ID=' + base_64_data_key_id.decode('utf-8'))

print("DEK (DataEncId): " + base_64_data_key_id.decode('utf-8'))
