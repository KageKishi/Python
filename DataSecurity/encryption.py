from pathlib import Path
import os
import json
import base64

from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes


# Generate RSA keys
private_key = rsa.generate_private_key(
    public_exponent=65537,
    key_size=2048
)

public_key = private_key.public_key()

# Save keys to files
Path("private_key.pem").write_bytes(
    private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.BestAvailableEncryption(
            b"change-this-password"
        )
    )
)

Path("public_key.pem").write_bytes(
    public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )
)


def encrypt_file(filename):
    path = Path(filename)

    # Generate AES key and IV
    aes_key = os.urandom(32)
    iv = os.urandom(16)

    # Encrypt file contents using AES
    cipher = Cipher(algorithms.AES(aes_key), modes.CTR(iv))
    encryptor = cipher.encryptor()

    encrypted_data = encryptor.update(path.read_bytes())
    encrypted_data += encryptor.finalize()

    # Encrypt AES key using RSA public key
    encrypted_key = public_key.encrypt(
        aes_key,
        padding.OAEP(
            mgf=padding.MGF1(hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )

    # Store encrypted key, IV, and encrypted data
    output = {
        "key": base64.b64encode(encrypted_key).decode(),
        "iv": base64.b64encode(iv).decode(),
        "data": base64.b64encode(encrypted_data).decode()
    }

    Path(str(path) + ".encrypted").write_text(json.dumps(output))
    print("Encrypted file:", str(path) + ".encrypted")


def decrypt_file(filename):
    # Load private key
    private_key = serialization.load_pem_private_key(
        Path("private_key.pem").read_bytes(),
        password=b"change-this-password"
    )

    # Load encrypted file
    contents = json.loads(Path(filename).read_text())

    encrypted_key = base64.b64decode(contents["key"])
    iv = base64.b64decode(contents["iv"])
    encrypted_data = base64.b64decode(contents["data"])

    # Recover AES key using RSA private key
    aes_key = private_key.decrypt(
        encrypted_key,
        padding.OAEP(
            mgf=padding.MGF1(hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )

    # Decrypt file contents
    cipher = Cipher(algorithms.AES(aes_key), modes.CTR(iv))
    decryptor = cipher.decryptor()

    data = decryptor.update(encrypted_data)
    data += decryptor.finalize()

    output_name = filename.removesuffix(".encrypted") + ".decrypted"
    Path(output_name).write_bytes(data)

    print("Decrypted file:", output_name)


# Example usage:
encrypt_file("example.pdf")
decrypt_file("example.pdf.encrypted")