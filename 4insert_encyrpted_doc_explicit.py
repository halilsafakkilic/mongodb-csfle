from pymongo import MongoClient
from pymongo.encryption import ClientEncryption, Algorithm

from settings import connection_string, get_kms_providers, key_vault_namespace, collection_name, MAIN_DEK_ID

mongo_client = MongoClient(connection_string)

collection = mongo_client[collection_name].citizens

mongo_client_encryption = ClientEncryption(
    get_kms_providers(),
    key_vault_namespace,
    mongo_client,
    collection.codec_options,
)

encrypted_name = mongo_client_encryption.encrypt(
    "HSK",
    Algorithm.AEAD_AES_256_CBC_HMAC_SHA_512_Deterministic,
    key_id=MAIN_DEK_ID,
)
encrypted_foods = mongo_client_encryption.encrypt(
    ["Turkish Kebab"],
    Algorithm.AEAD_AES_256_CBC_HMAC_SHA_512_Random,
    key_id=MAIN_DEK_ID,
)
collection.insert_one({"name": encrypted_name, "age": 30, "foods": encrypted_foods})
