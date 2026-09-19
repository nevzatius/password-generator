"""Single-user account creation and login verification."""

import base64
import hmac
import json
import os
import secrets

from crypto_utils import PBKDF2_ITERATIONS, hash_password

AUTH_FILE = "auth.json"


def account_exists() -> bool:
    return os.path.exists(AUTH_FILE)


def get_stored_username() -> str:
    with open(AUTH_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data["username"]


def create_account(username: str, password: str) -> None:
    salt = secrets.token_bytes(16)
    password_hash = hash_password(password, salt, PBKDF2_ITERATIONS)
    data = {
        "username": username,
        "salt": base64.b64encode(salt).decode("ascii"),
        "password_hash": base64.b64encode(password_hash).decode("ascii"),
        "iterations": PBKDF2_ITERATIONS,
    }
    with open(AUTH_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f)


def verify_login(password: str) -> bool:
    if not account_exists():
        return False
    with open(AUTH_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)
    salt = base64.b64decode(data["salt"])
    stored_hash = base64.b64decode(data["password_hash"])
    iterations = data["iterations"]
    candidate_hash = hash_password(password, salt, iterations)
    return hmac.compare_digest(candidate_hash, stored_hash)
