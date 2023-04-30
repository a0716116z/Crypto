import bitarray
encrypt_file = input("請輸入加密檔案名稱")
file_content = bitarray.bitarray()
with open(encrypt_file, 'rb') as fh:
    file_content.fromfile(fh)
print(file_content[0:100])
print(len(file_content))
