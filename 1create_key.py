from secrets import token_bytes

from settings import master_key_filename

key_bytes = token_bytes(96)

with open(master_key_filename, 'wb') as f:
    f.write(key_bytes)
