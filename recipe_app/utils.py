from passlib.hash import pbkdf2_sha256


def hash_password(password: str) -> str:
    """Hashing User Password

    Args:
        password (str): Password entered by user

    Returns:
        str: Hashed password
    """
    return pbkdf2_sha256.hash(password)


def verify_password(password: str, hashed: str) -> bool:
    """Verify user password for login

    Args:
        password (str): password entered by user
        hashed (str): hashed password stored in db

    Returns:
        bool: True if password is correct
    """
    return pbkdf2_sha256.verify(password, hashed)
