import base64

def Base64_Encryption(encrypted_str, code='utf-8'):
    """
    base64加密
    :param encrypted_str:  需加密的字符串
    :param code: str #字符串编码，默认'utf-8'
    :return: 加密后的字符串
    """
    byte_str = encrypted_str.encode(code)
    encrypted_s = base64.b64encode(byte_str).decode(code)
    return encrypted_s

def Base64_Decrypt(encrypted_str, code1='utf-8'):
    """
    base64解密
    :param encrypted_str:  需解密的字符串
    :param code1: str #字符串编码，默认'utf-8'
    :return: 解密后的字符串
    """
    decrypt_s = base64.b64decode(encrypted_str)
    decrypt_s = decrypt_s.decode(code1)
    decrypt_s = str(decrypt_s)
    return decrypt_s

