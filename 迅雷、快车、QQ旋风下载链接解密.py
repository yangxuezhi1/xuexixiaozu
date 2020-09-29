import base64


def Thunder_Deciphering_Encryption(link,bools=True):
    """
    迅雷下载链接加解密
    :param link: str 要加密/解密的链接
    :param bools: bool 加密：False/解密:True,默认True
    :return:
    """
    if bools:
        address = link.split('//')[1]
        str_url = base64.b64decode(address).decode("utf-8")
        if str_url.startswith('AA') and str_url.endswith('ZZ'):
            str_url = str_url[2:-2]
        return str_url
    else:
        url = f'AA{link}ZZ'
        bytes_url = url.encode("utf-8")
        str_url = base64.b64encode(bytes_url).decode("utf-8")  # 被编码的参数必须是二进制数据
        str_url = f"thunder://{str_url}"
        return str_url
def Express_Deciphering_Encryption(link,bools=True):
    """
    快车下载链接加解密
    :param link: str 要加密/解密的链接
    :param bools: bool 加密：False/解密:True,默认True
    :return:
    """
    if bools:
        address = link.split('//')[1].split('&')[0]
        str_url = base64.b64decode(address).decode("utf-8")
        if str_url.startswith('[FLASHGET]') and str_url.endswith('[FLASHGET]'):
            str_url = str_url[10:-10]
        return str_url
    else:
        url = f'[FLASHGET]{link}[FLASHGET]'
        bytes_url = url.encode("utf-8")
        str_url = base64.b64encode(bytes_url).decode("utf-8")  # 被编码的参数必须是二进制数据
        str_url = f"flashget://{str_url}&yang"
        return str_url
def QQ_whirlwind_Deciphering_Encryption(link,bools=True):
    """
        QQ旋风下载链接加解密
        :param link: str 要加密/解密的链接
        :param bools: bool 加密：False/解密:True,默认True
        :return:
        """
    if bools:
        address = link.split('//')[1]
        str_url = base64.b64decode(address).decode("utf-8")
        return str_url
    else:
        url = f'{link}'.encode("utf-8")
        str_url = base64.b64encode(url).decode("utf-8")  # 被编码的参数必须是二进制数据
        str_url = f"qqdl://{str_url}"
        return str_url

if __name__ == '__main__':
    URL = Thunder_Deciphering_Encryption('thunder://QUFodHRwOi8vZGxkaXIxLnFxLmNvbS9xcWZpbGUvcXEvUVE4LjMvMTgwMzgvUVE4LjMuZXhlWlo=')
    print(URL)