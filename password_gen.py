"""Cryptographically secure password generation."""

import secrets
import string

SYMBOLS = "!@#$%^&*()-_=+[]{}"


def generate_password(
    length: int,
    use_upper: bool,
    use_lower: bool,
    use_digits: bool,
    use_symbols: bool,
) -> str:
    pools = []
    if use_upper:
        pools.append(string.ascii_uppercase)
    if use_lower:
        pools.append(string.ascii_lowercase)
    if use_digits:
        pools.append(string.digits)
    if use_symbols:
        pools.append(SYMBOLS)

    if not pools:
        raise ValueError("En az bir karakter türü seçilmelidir.")
    if length < len(pools):
        raise ValueError(f"Uzunluk en az {len(pools)} olmalıdır (seçilen kategori sayısı).")

    alphabet = "".join(pools)
    result = [secrets.choice(pool) for pool in pools]
    result += [secrets.choice(alphabet) for _ in range(length - len(pools))]

    for i in range(len(result) - 1, 0, -1):
        j = secrets.randbelow(i + 1)
        result[i], result[j] = result[j], result[i]

    return "".join(result)
