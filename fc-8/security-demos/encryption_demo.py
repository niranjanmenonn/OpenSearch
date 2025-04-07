# Encrypts sensitive data in search results
# Protects user queries and response data
# Used throughout the main program for data protection


from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import base64

def setup_encryption():
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=b'your-salt-here',
        iterations=100000,
    )
    key = base64.urlsafe_b64encode(kdf.derive(b'your-password'))
    return Fernet(key)

if __name__ == "__main__":
    fernet = setup_encryption()
    user_input = input("Enter sensitive data: ")
    
    encrypted = fernet.encrypt(user_input.encode()).decode()
    decrypted = fernet.decrypt(encrypted.encode()).decode()
    
    print(f"\nOriginal data: {user_input}")
    print(f"Encrypted data: {encrypted}")
    print(f"Decrypted data: {decrypted}")
