from distutils.command.clean import clean
from email.mime import audio
import eel
from bitarray.util import base2ba, ba2base, int2ba, ba2int, ba2hex, hex2ba
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from Crypto.Random import get_random_bytes
from base64 import b64encode
import bitarray
import binascii

import sys
from P1_0601 import Encrypt_Structure
from P2_Key_Generation import AudioFile2Key


def convertBase64ToBitArray(raw_data):
    file_content = bitarray.bitarray()
    filelist = raw_data.split('base64,')
    clean_file = filelist[1]
    results = binascii.a2b_base64(clean_file)
    file_content.frombytes(results)
    return file_content


@eel.expose
def say_something(filename, selectedFile, voicekey, voicename):
    key_bitarray = convertBase64ToBitArray(voicekey)  # 把網頁的聲音檔案變成是bitarray
    # print('test1')
    plainttext_bitarray = convertBase64ToBitArray(selectedFile)
    print('test2')
    StartEncrypt(filename, plainttext_bitarray, voicename, key_bitarray)
    print('test3')
    # 把網頁plaintext變成是bitarray
    # testfileIsCorrect(filename, plainttext_bitarray)
    # print(filename)
    # print(voicename)
    return f'加密成功，檔案輸出在加密資料夾底下'


def StartEncrypt(encrypt_file_name, encrypt_file_content, audioFileName, audiobitarray):
    # def StartEncrypt(encrypt_file_name, audioFileName):
    outputFile = 'Encrypted'
    # keyPath = 'test.mp3'
    # encrypt_file_name = "plaintext.txt"
    #print('hi   1')
    # encrypt_file_content = bitarray.bitarray()
    # print('test1')
    # with open(encrypt_file_name, 'rb') as fh:
    #     encrypt_file_content.fromfile(fh)
    b = Encrypt_Structure(encrypt_file_name, encrypt_file_content)
    #print('hi   2')
    #print('----- Encryption -----')
    #print('encrypt_file_content: ', encrypt_file_content)
    print('b                : \n')
    #print('b.tobytes()      : \n', b.tobytes())

    #c = b.tobytes()
    #d = bitarray.bitarray()
    # d.frombytes(c)
    #print('d                :\n', d)

    #AudioFileName = input('Enter an audio file name: ')
    key = AudioFile2Key(audioFileName, audiobitarray)
    # key = AudioFile2Key(audioFileName)
    print('c                : \n')
    key = key.to_bytes(sys.getsizeof(key), sys.byteorder)
    key = key[:32]

    #print('key              : \n', key)

    # data = b'My secret data.'
    data = b.tobytes()
    print('d                : \n')
    # print(data.decode("utf-8"))
    # 以金鑰搭配 CBC 模式建立 cipher 物件
    cipher = AES.new(key, AES.MODE_CBC)
    # iv = b64encode(cipher.iv).decode('utf-8')
    # 將輸入資料加上 padding 後進行加密
    print('e                : \n')
    cipheredData = cipher.encrypt(pad(data, AES.block_size))
    # ct = b64encode(cipheredData).decode('utf-8')

    #print('cipherData       : \n', cipheredData)
    # print('----------------------')
    print('iv length', len(cipher.iv), 'iv data', cipher.iv)
    print('len cipheredData', len(cipheredData))
    # print(len(cipheredData))
    # 將初始向量與密文寫入檔案

    with open(outputFile, "wb") as f:
        f.write(cipher.iv)
        f.write(cipheredData)


eel.init('web')
eel.start('index.html', size=(800, 600))
