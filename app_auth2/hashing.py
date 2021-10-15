from passlib.hash import bcrypt

def hash(password:str):
    return bcrypt.hash(password)

def verify(entered_password:str, password_hash:str):
    return bcrypt.verify(entered_password, password_hash)
