import uuid

# Lookup table (the "vault"): token -> original data
lookup_table = {}


def tokenize(data):
    """Replace real data with a random token and remember the mapping."""
    token = str(uuid.uuid4())
    lookup_table[token] = data
    return token


def reverse_tokenize(token):
    """Look the token up and return the original data."""
    return lookup_table.get(token, "Token not found")


original_email = "john.doe@example.com"

tokenized_email = tokenize(original_email)
print(f"Original Email: {original_email}")
print(f"Tokenized Email: {tokenized_email}")

retrieved_email = reverse_tokenize(tokenized_email)
print(f"Retrieved Email: {retrieved_email}")

# Extra check: an unknown token returns the fallback message
print(f"Bad token: {reverse_tokenize('not-a-real-token')}")