import bcrypt

def password(password):
    return bytes(bcrypt.hashpw(
        bytes(password, 'utf-8'), bcrypt.gensalt()
    )).decode('utf-8')
