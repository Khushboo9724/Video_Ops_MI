from passlib.hash import argon2


def hash_password(password):
    return argon2.hash(password)


def verify_password(hashed_password, input_password):
    return argon2.verify(input_password, hashed_password)
