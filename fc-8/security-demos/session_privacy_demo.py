# Handles user session security in the main application
# Creates secure hashes for session tracking


import hashlib

def secure_session(session_data):
    return hashlib.sha256(str(session_data).encode()).hexdigest()

if __name__ == "__main__":
    user_input = input("Enter session data: ")  #Enter session data: username123
    hashed = secure_session(user_input)
    print(f"\nOriginal data: {user_input}")
    print(f"SHA-256 hash: {hashed}")
