import binascii
from distutils.command.clean import clean
import eel
import bitarray
from bitarray.util import base2ba, ba2base, int2ba, ba2int, ba2hex, hex2ba


def convertBase64ToBitArray(raw_data):
    file_content = bitarray.bitarray()
    filelist = raw_data.split('base64,')
    clean_file = filelist[1]
    results = binascii.a2b_base64(clean_file)
    file_content.frombytes(results)
    return file_content


def testfileIsCorrect(filename, filebitarray):
    with open(filename, 'wb') as fh:
        filebitarray.tofile(fh)


@eel.expose  # 用decorator的方式，將JS要呼叫的PY function暴露給eel, 讓eel當作一個library  去給JS使用
def say_something(encrypt_filename, encrypt_file, voicekey, voicename):  # filename是當時要加密的檔案名稱，含副檔名
    key_bitarray = convertBase64ToBitArray(voicekey)  # 把網頁的聲音檔案變成是bitarray
    plainttext_bitarray = convertBase64ToBitArray(
        encrypt_file)  # 把網頁encrypt變成是bitarray
    testfileIsCorrect(encrypt_filename, plainttext_bitarray)
    print(encrypt_filename)
    print(voicename)

    return f'解密成功，檔案輸出在加密資料夾底下'  # 回傳網頁端


# 以下為網頁初始化不可刪---------------------------------
eel.init('web')
eel.start('index.html', size=(800, 600))
