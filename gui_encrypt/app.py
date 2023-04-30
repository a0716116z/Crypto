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
def say_something(filename, selectedFile, voicekey, voicename):  # filename是當時要加密的檔案名稱，含副檔名
    # file_content = bitarray.bitarray()
    # print(type(selectedFile))
    # print(selectedFile[0:1000])
    # filelist = selectedFile.split('base64,')
    # clean_file = filelist[1]
    key_bitarray = convertBase64ToBitArray(voicekey)  # 把網頁的聲音檔案變成是bitarray
    plainttext_bitarray = convertBase64ToBitArray(
        selectedFile)  # 把網頁plaintext變成是bitarray
    testfileIsCorrect(filename, plainttext_bitarray)
    print(filename)
    print(voicename)
    # 元挺這裡給你放加密函數的Call

    # 測試轉型別 base64的語法
    # print(selectedFile)
    # base64.b64decode(base64_to_binary_input)
    # results = base64.decodebytes(selectedFile)
    # results = bytearray(selectedFile)
    # -----------------------------終止線
    #results = binascii.a2b_base64(clean_file)
    # print(type(results))
    # print(len(file_content))
    # file_content.frombytes(results)
    # print(file_content[0:100])
    #
    # with open('qq.jpg', 'wb') as fh:
    #     file_content.tofile(fh)

    # 終止線－－－－－－－－－－－－－－－－－－－－－－－－
    # 返回 字串加上被呼叫的次數
    return f'加密成功，檔案輸出在加密資料夾底下'  # 回傳網頁端


# 以下為網頁初始化不可刪---------------------------------
eel.init('web')
eel.start('index.html', size=(800, 600))
