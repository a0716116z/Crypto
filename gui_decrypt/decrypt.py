from Crypto.Cipher import AES
from base64 import b64decode
import bitarray
from Crypto.Util.Padding import unpad
from Crypto.Random import get_random_bytes
import binascii
from distutils.command.clean import clean
import eel
from bitarray.util import base2ba, ba2base, int2ba, ba2int, ba2hex, hex2ba
import sys
from P1_0601 import unpack
from P2_Key_Generation import recoverKeyFromFile


def convertBase64ToBitArray(raw_data):
    file_content = bitarray.bitarray()
    filelist = raw_data.split('base64,')
    clean_file = filelist[1]
    results = binascii.a2b_base64(clean_file)
    file_content.frombytes(results)
    return file_content


@eel.expose  # 用decorator的方式，將JS要呼叫的PY function暴露給eel, 讓eel當作一個library  去給JS使用
def say_something(encrypt_filename, encrypt_file, voicekey, voicename):  # filename是當時要加密的檔案名稱，含副檔名
    key_bitarray = convertBase64ToBitArray(voicekey)  # 把網頁的聲音檔案變成是bitarray

    plainttext_bitarray = convertBase64ToBitArray(
        encrypt_file)  # 把網頁encrypt變成是bitarray
    # testfileIsCorrect(encrypt_filename, plainttext_bitarray)
    # print(encrypt_filename)
    # print(voicename)
    decryptTotal(encrypt_filename, plainttext_bitarray,
                 voicename, key_bitarray)
    return f'解密成功，檔案輸出在加密資料夾底下'  # 回傳網頁端


def decryptTotal(inputFile, ciphered, keyPath, audiobitarray):
    # 輸入的加密檔案名稱
    #inputFile = 'encrypted.bin'
    # NEED TO BE REPLACED!!!
    inputFile = 'Encrypted'
    #keyPath = "my_key.bin"
    #keyPath = input('Enter key file name: ')
    # keyPath = 'test.mp310'
    key = recoverKeyFromFile(keyPath, audiobitarray)
    key = key.to_bytes(sys.getsizeof(key), sys.byteorder)
    key = key[:32]

    #print('----- Decryption -----')
    #print('key              : \n', key)

    #key = 0
    # with open(keyPath, "rb") as f:
    #    key = f.read()

    # 從檔案讀取初始向量與密文
    # with open(inputFile, "rb") as f:
    #     iv = f.read(16)        # 讀取 16 位元組的初始向量
    #     cipheredData = f.read()  # 讀取其餘的密文
    iv = ciphered[0:16*8].tobytes()
    cipheredData = ciphered[16*8:].tobytes()
    # print('cipheredData     : \n', cipheredData)
    #print('iv length', len(iv), 'iv data', iv)
    #print('len cipheredData', len(cipheredData))
    # 以金鑰搭配 CFB 模式與初始向量建立 cipher 物件
    cipher = AES.new(key, AES.MODE_CBC, iv=iv)

    # 解密資料
    originalData = unpad(cipher.decrypt(cipheredData), AES.block_size)

    #print('originalData     : \n', originalData)

    # 輸出解密後的資料
    a = bitarray.bitarray()
    a.frombytes(originalData)
    #print('a                : \n', a)
    (fileName, plaintext) = unpack(a)

    #print('plaintext        : \n', plaintext)
    # print('----------------------')

    with open(fileName, 'wb') as fh:
        plaintext.tofile(fh)


eel.init('web')
eel.start('index.html', size=(800, 600))
