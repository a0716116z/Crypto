import bitarray
import random
import math
from bitarray.util import ba2int
import os
import shutil


def partially_reverse_bitarray(originBitarray, beginIndex: int, endIndex: int):
    fullyReversedBitarray = originBitarray.copy()
    fullyReversedBitarray.reverse()

    beginIndex = int(beginIndex)
    endIndex = int(endIndex)

    reverseFilter = [0 for i in range(len(originBitarray))]
    reverseFilter[beginIndex:endIndex] = [
        1 for i in range(endIndex - beginIndex)]
    reverseFilter = bitarray.bitarray(reverseFilter)

    staythesameFilter = reverseFilter.copy()
    staythesameFilter.invert()

    partially_reversed_bitarray = ((originBitarray & staythesameFilter) | (
        fullyReversedBitarray & reverseFilter))
    #print('origin bitarray              : ', originBitarray)
    #print('staythesameFilter            : ', staythesameFilter)
    #print('fullyReversedBitarray        : ', fullyReversedBitarray)
    #print('reverseFilter                : ', reverseFilter)
    #print('partially_reversed_bitarray  : ', partially_reversed_bitarray)

    return partially_reversed_bitarray

# ********* Jun Wei ************
# ***** encrypt *****


def AudioFile2Key(AudioFileName: str, audiobitarray):
    a = bitarray.bitarray()
    # with open(AudioFileName, 'rb') as fh:
    #     a.fromfile(fh)
    a = audiobitarray
    # 讀檔只是假設這樣
    #print(len(a), ' len')
    start = int(len(a)/2-3*math.sqrt(len(a)))
    end = int(len(a)/2+3*math.sqrt(len(a)))
    N = random.randint(3, 10)

    iniKey = a[start:end]
    #p = len(iniKey)/N
    p = int(len(iniKey)/N)
    for i in range(1, int(N/2)):
        #iniKey[i*2*p-p:i*2*p] = bitarray.reverse(iniKey[i*2*p-p:i*2*p])
        iniKey[i*2*p-p:i*2 *
               p] = partially_reverse_bitarray(iniKey, i*2*p-p, i*2*p)
    key = 0
    for i in range(1, N):
        key = ba2int(iniKey[i*p-p:i*p]) ^ key
    AudioFileFullPath = os.path.abspath(AudioFileName)
    base_file, ext = os.path.splitext(AudioFileFullPath)
    if ext == ".mp4":
        #os.rename(AudioFileName, base_file + ".mp4" + str(N))
        newFileName = base_file + ".mp4" + str(N)
    elif ext == ".mp3":
        #os.rename(AudioFileName, base_file + ".mp3" + str(N))
        newFileName = base_file + ".mp3" + str(N)
    elif ext == ".m4a":
        #os.rename(AudioFileName, base_file + ".m4a" + str(N))
        newFileName = base_file + ".m4a" + str(N)
    elif ext == ".wav":
        #os.rename(AudioFileName, base_file + ".wav" + str(N))
        newFileName = base_file + ".wav" + str(N)
    else:
        #os.rename(AudioFileName, base_file + str(N))
        newFileName = base_file + str(N)
    with open(newFileName, "wb") as f:
        f.write(audiobitarray)
    #shutil.copyfile(AudioFileFullPath, newFileName)

    return key
# combine part 1 ciphertext and part 2 key


def Key_XOR(ciphertext, key):
    # AES(ciphertext,key)
    from itertools import cycle
    encrypt_result = bitarray('')
    text_len = len(ciphertext)
    key_len = len(key)
    key_cycle = cycle(key)
    for idx in range(0, text_len):
        encrypt_result.append(ciphertext[idx] ^ next(key_cycle))

    return encrypt_result


def Part2Encryption(Part1Result):
    AudioFileName = input('Enter an audio file name: ')
    key = AudioFile2Key(AudioFileName)
    Part2Result = Key_XOR(Part1Result, key)
    return Part2Result
# ***** decrypt *****


def recoverKeyFromFile(KeyFileName: str):
    a = bitarray.bitarray()
    with open(KeyFileName, 'rb') as fh:
        a.fromfile(fh)
    # 讀檔只是假設這樣(檔名要改，因副檔名已變)
    #print(len(a), ' len')
    base_file, ext = os.path.splitext(KeyFileName)
    file_ex = str()
    if ext.find('.m4a') >= 0:
        file_ex = ".m4a"
        N = ext.removeprefix('.m4a')
    elif ext.find('.mp3') >= 0:
        file_ex = ".mp3"
        N = ext.removeprefix('.mp3')
    elif ext.find('.mp4') >= 0:
        file_ex = ".mp4"
        N = ext.removeprefix('.mp4')
    elif ext.find('.wav') >= 0:
        file_ex = ".wav"
        N = ext.removeprefix('.wav')
    else:
        N = ext

    # print('-----------------------')
    #print('ext      : ', ext)
    #print('file_ex  : ', file_ex)
    #print('N        : ', N)
    # print('-----------------------')
    #os.rename(fh, base_file + file_ex)

    # with open('test.m4a', 'rb') as fh:
        # a.fromfile(fh)
    # 檔名只是假設
    start = int(len(a)/2-3*math.sqrt(len(a)))
    end = int(len(a)/2+3*math.sqrt(len(a)))
    iniKey = a[start:end]

    N = int(N)
    p = int(len(iniKey)/N)
    for i in range(1, int(N/2)):
        #iniKey[i*2*p-p:i*2*p] = bitarray.reverse(iniKey[i*2*p-p:i*2*p])
        iniKey[i*2*p-p:i*2 *
               p] = partially_reverse_bitarray(iniKey, i*2*p-p, i*2*p)
    key = 0
    for i in range(1, N):
        key = ba2int(iniKey[i*p-p:i*p]) ^ key

    return key
# ******************************
