from bcrypt import  gensalt , hashpw

def hash_password(password):
    #que encripte la contraseña sin en 'b' y con el salt
    return hashpw(password.encode('utf-8'), gensalt()).decode('utf-8')

def verify_password(password, hashed_password):
    #que verifique la contraseña sin en 'b' y con el salt
    return hashpw(password.encode('utf-8'), hashed_password.encode('utf-8')) == hashed_password.encode('utf-8')