from bcrypt import gensalt, hashpw

def hash_password(password):
    # Que encripte la contraseña sin 'b' y con el salt
    return hashpw(password.encode('utf-8'), gensalt()).decode('utf-8')

def verify_password(password, hashed_password):
    # Que verifique la contraseña sin 'b' y con el salt
    return hashpw(password.encode('utf-8'), hashed_password.encode('utf-8')) == hashed_password.encode('utf-8')