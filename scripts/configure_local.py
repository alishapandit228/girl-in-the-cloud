"""Create a private, development-only Compose environment without overwriting one."""
import getpass
import os
from pathlib import Path
import secrets

from backend.passwords import password_hash

ROOT = Path(__file__).resolve().parents[1]

def main():
    destination = ROOT / ".env"
    if destination.exists():
        raise SystemExit("Existing .env preserved. Edit it directly to change settings.")
    password = getpass.getpass("Local owner password (14+ characters; Enter to skip owner login): ")
    if password and len(password) < 14:
        raise SystemExit("Choose a password with at least 14 characters.")
    owner_hash = ""
    if password:
        if password != getpass.getpass("Confirm local owner password: "):
            raise SystemExit("Passwords did not match.")
        owner_hash = password_hash(password)
    values = {"POSTGRES_PASSWORD":secrets.token_hex(32),"APP_SECRET":secrets.token_hex(32),"ADMIN_HASH":owner_hash}
    lines = []
    for line in (ROOT/".env.example").read_text().splitlines():
        key = line.split("=",1)[0]
        lines.append(f"{key}={values[key]}" if key in values else line)
    descriptor = os.open(destination, os.O_EXCL | os.O_CREAT | os.O_WRONLY, 0o600)
    with os.fdopen(descriptor,"w") as output:
        output.write("\n".join(lines)+"\n")
    print("Local configuration created. Run docker compose up -d --build --wait.")

if __name__=="__main__":
    main()
