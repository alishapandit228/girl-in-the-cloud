import getpass
from backend.services import password_hash
if __name__ == "__main__":
    password=getpass.getpass("New owner password (at least 14 characters): ")
    if len(password)<14:raise SystemExit("Choose at least 14 characters.")
    print(password_hash(password))
