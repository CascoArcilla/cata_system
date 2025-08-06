import string
import random

def generarCodigo():
    caracteres = string.ascii_letters + string.digits
    codigo = ''.join(random.choice(caracteres) for _ in range(3))
    codigo = codigo.upper()
    return codigo

def generarCodigos(numCodes):
    codes_products = []
    for i in range(numCodes):
        while True:
            code = generarCodigo()
            if not codes_products.__contains__(code):
                codes_products.append(code)
                break

    return codes_products