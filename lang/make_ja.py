#!/usr/bin/python
# coding: utf-8

# ./out/lang.csvと./data/Frostpunk 翻訳作業所 - 翻訳.csvから./out/japanese_*.langを生成します。
# (翻訳シートの構成が変わった場合は使用できません。)

import codecs
import csv
import struct

def read_csv(path):
    print("read file: %s" % path)
    try:
        f = codecs.open(path, "r", "utf_8_sig") # with bom
    except IOError:
        print("error: file open error: %s" % path)
        quit()
    r = csv.reader(f, delimiter=",", doublequote=True, lineterminator="\r\n", quotechar='"', skipinitialspace=True)
    head = next(r)
    data = []
    for d in r:
        data.append(d)
    f.close()
    print("read len: %d" % len(data))
    return data

def split_data(data):
    strs = []
    for i in range(1,len(data[0])):
        strs.append({})
    for d in data:
        s = d[0]
        for i in range(1,len(d)):
            if False:
                if d[i] != "":
                    strs[i-1][s] = d[i]
            else:
                strs[i-1][s] = d[i]
    return strs

def marge_data(data1, data2, skip, index1, index2):
    strs = {}
    cnt = 0
    for d in data1.keys():
        if skip > 0:
            skip -= 1
            continue
        if cnt >= len(data2):
            break
        if data2[cnt][index1] != "":
            strs[d] = data2[cnt][index1]
        elif index2>=0 and data2[cnt][index2] != "":
            _d = data2[cnt][index2]
            _d = _d.replace("</ n>", "\n")
            _d = _d.replace("</ N>", "\n")
            strs[d] = _d
        else:
            strs[d] = data1[d]
        cnt += 1
    return strs

# for test
# Frostpunk LANG Tool incompatible
def write_txt(path, data):
    print("write file: %s" % path)
    try:
        f = codecs.open(path, "w", "utf_8_sig") # with bom
    except IOError:
        print("error: file open error: %s" % path)
        quit()
    for d in data.keys():
        f.write("%s\n" % d)
        _d = data[d].replace("</n>", "\n") # for Frostpunk LANG Tool
        f.write("%s\n" % _d)
    f.close()
    print("write len: %d" % len(data))

def make_lang(data):
    bin = bytearray()
    bin.extend(struct.pack("<II", 0, len(data)))
    for d in data.keys():
        bin.extend(struct.pack("<H", len(d)))
        bin.extend(d.encode("ascii"))
        _d = data[d].replace("</n>", "\n") # for Frostpunk LANG Tool
        bin.extend(struct.pack("<H", len(_d)))
        bin.extend(_d.encode("utf_16_le"))
    bin[:4] = struct.pack("<I", len(bin)-4)
    return bin

def write_bin(path, data):
    print("write file: %s" % path)
    try:
        f = open(path, "wb")
    except IOError:
        print("error: file open error: %s" % path)
        quit()
    f.write(data)
    f.close()
    print("write size: %xh" % len(data))

def make_ja():
    data = read_csv("./out/lang.csv")
    if False:
        en,fr,de,es,pl,ru,zh = split_data(data)
    else:
        en,zh,fr,de,es,pl,ru = split_data(data)

    data2 = read_csv("./data/Frostpunk 翻訳作業所 - 翻訳.csv")

    # uninclude Machine Translation
    ja = marge_data(en, data2, 4, 1, -1)
#    write_txt("./out/japanese.txt", ja)
    write_bin("./out/japanese.lang", make_lang(ja))

    # include Machine Translation
    ja = marge_data(en, data2, 4, 1, 2)
#    write_txt("./out/japanese_wmt.txt", ja)
    write_bin("./out/japanese_wmt.lang", make_lang(ja))

make_ja()