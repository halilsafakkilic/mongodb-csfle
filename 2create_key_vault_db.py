from pymongo import MongoClient, ASCENDING

from settings import connection_string, key_vault_database, key_vault_collection

mongo_client = MongoClient(connection_string)

# Drop the Key Vault Collection in case you created this collection in a previous run of this application.
mongo_client.drop_database(key_vault_database)

mongo_client[key_vault_database][key_vault_collection].create_index(
    [("keyAltNames", ASCENDING)],
    unique=True,
    partialFilterExpression={"keyAltNames": {"$exists": True}},
)
