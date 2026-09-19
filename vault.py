"""Encrypted vault of saved password entries."""

import base64
import json
import os
import secrets
import uuid

from crypto_utils import decrypt_bytes, derive_key, encrypt_bytes

VAULT_FILE = "vault.dat"


class VaultEntry:
    def __init__(self, name: str, password: str, entry_id: str | None = None):
        self.id = entry_id or str(uuid.uuid4())
        self.name = name
        self.password = password

    def to_dict(self) -> dict:
        return {"id": self.id, "name": self.name, "password": self.password}

    @staticmethod
    def from_dict(data: dict) -> "VaultEntry":
        return VaultEntry(data["name"], data["password"], data["id"])


class Vault:
    def __init__(self, key: bytes, salt: bytes, entries: list[VaultEntry] | None = None):
        self.key = key
        self.salt = salt
        self.entries: list[VaultEntry] = entries or []

    def add_entry(self, name: str, password: str) -> None:
        self.entries.append(VaultEntry(name, password))

    def delete_entry(self, entry_id: str) -> None:
        self.entries = [e for e in self.entries if e.id != entry_id]

    def to_json_bytes(self) -> bytes:
        return json.dumps({"entries": [e.to_dict() for e in self.entries]}).encode("utf-8")


def load_vault(password: str) -> Vault:
    if not os.path.exists(VAULT_FILE):
        salt = secrets.token_bytes(16)
        key = derive_key(password, salt)
        return Vault(key, salt, [])

    with open(VAULT_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)

    salt = base64.b64decode(data["salt"])
    token = base64.b64decode(data["token"])
    key = derive_key(password, salt)

    plaintext = decrypt_bytes(key, token)
    parsed = json.loads(plaintext.decode("utf-8"))
    entries = [VaultEntry.from_dict(e) for e in parsed.get("entries", [])]
    return Vault(key, salt, entries)


def save_vault(vault: Vault) -> None:
    token = encrypt_bytes(vault.key, vault.to_json_bytes())
    data = {
        "salt": base64.b64encode(vault.salt).decode("ascii"),
        "token": base64.b64encode(token).decode("ascii"),
    }
    with open(VAULT_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f)
