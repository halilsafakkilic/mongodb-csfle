from pymongo import MongoClient
from pymongo.encryption import Algorithm, ClientEncryption

from settings import get_kms_providers, connection_string, key_vault_namespace, collection_name, MAIN_DEK_ID

mongo_client = MongoClient(connection_string)

collection = mongo_client[collection_name].citizens

mongo_client_encryption = ClientEncryption(
    get_kms_providers(),
    key_vault_namespace,
    mongo_client,
    collection.codec_options,
)

name_to_query = "HSK"
encrypted_name_to_query = mongo_client_encryption.encrypt(
    name_to_query,
    Algorithm.AEAD_AES_256_CBC_HMAC_SHA_512_Deterministic,
    key_id=MAIN_DEK_ID,
)
doc = collection.find_one({"name": encrypted_name_to_query})
print("Encrypted document: %s" % (doc,))

doc["name"] = mongo_client_encryption.decrypt(doc["name"])
doc["foods"] = mongo_client_encryption.decrypt(doc["foods"])
print("Decrypted document: %s" % (doc,))
