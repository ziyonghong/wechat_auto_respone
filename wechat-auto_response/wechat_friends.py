# -*- coding: utf-8 -*-
import itchat
import re
import io
from os import path
from wordcloud import WordCloud, ImageColorGenerator
import jieba
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
import random
import os
from matplotlib import pyplot as plt

OUTPUT = ".\\Output\\"


# 绘制柱状图
def draw_plot(datas, tag=''):
    for key in datas.keys():
        plt.bar(key, datas[key])

    plt.legend()
    plt.xlabel('sex')
    plt.ylabel('rate')
    plt.title("Gender of Alfred's friends")
    if tag == '':
        plt.savefig(OUTPUT + USER_NAME + '_' + u'柱状图.png')
    else:
        plt.savefig(OUTPUT + USER_NAME + '_' + tag + u'柱状图.png')


# 绘制词云
def draw_wordcloud(path, tag=''):
    f = open(path, 'r').read()
    cut_text = "".join(jieba.cut(f))
    coloring = np.array(Image.open('.\\Pic\\wechat.jpg'))
    wordcloud = WordCloud(font_path='./font/simhei.ttf', background_color="white", max_words=2000, mask=coloring,
                          scale=2).generate(cut_text)
    image_colors = ImageColorGenerator(coloring)

    # plt.imshow(wordcloud.recolor(color_func=image_colors))
    plt.imshow(wordcloud)
    plt.axis("off")
    if tag == '':
        wordcloud.to_file(OUTPUT + USER_NAME + '_' + u'词云.png')
    else:
        wordcloud.to_file(OUTPUT + USER_NAME + '_' + tag + u'词云.png')


def LogIn(hotReload):
    itchat.auto_login(hotReload=hotReload)
    friends = itchat.get_friends(update=True)[0:1]
    global USER_NAME
    USER_NAME = friends[0]['NickName']


def parse_friedns():
    text = dict()
    friedns = itchat.get_friends(update=True)[0:]
    # (friedns)
    male = "male"
    female = "female"
    other = "other"

    for i in friedns[1:]:
        sex = i['Sex']
        if sex == 1:
            text[male] = text.get(male, 0) + 1
        elif sex == 2:
            text[female] = text.get(female, 0) + 1
        else:
            text[other] = text.get(other, 0) + 1
    total = len(friedns[1:])
    print('好友数量：%.2f' % total)
    print("男性好友： %.2f%%" % (float(text[male]) / total * 100) + "\n" +
          "女性好友： %.2f%%" % (float(text[female]) / total * 100) + "\n" +

          "不明性别好友： %.2f%%" % (float(text[other]) / total * 100))

    draw_plot(text, u'朋友圈男女比例_')


def parse_signature():
    siglist = []
    SIGNATURE_PATH = 'signature.txt'

    friedns = itchat.get_friends(update=True)[1:]
    for i in friedns:
        signature = i["Signature"].strip().replace("span", "").replace("class", "").replace("emoji", "")
        rep = re.compile("1f\d+\w*|[<>/=]")
        signature = rep.sub("", signature)
        siglist.append(signature)
    text = "".join(siglist)
    with io.open(SIGNATURE_PATH, 'w', encoding='utf-8') as f:
        wordlist = jieba.cut(text, cut_all=True)
        word_space_split = " ".join(wordlist)
        f.write(word_space_split)
        f.close()
    draw_wordcloud(SIGNATURE_PATH, tag=u'朋友圈签名')


def get_city_data():
    city_list = []
    CITY_PATH = 'city.txt'
    friend_list = itchat.get_friends(update=True)[1:]

    for i in friend_list[1:]:
        city_list.append(i['City'])

    with io.open(CITY_PATH, 'w', encoding='utf-8') as f:
        word_space_split = " ".join(city_list)
        f.write(word_space_split)
        f.close()

    draw_wordcloud(CITY_PATH, tag=u'朋友圈城市分布_')


def get_room_data():
    city_list = []
    ROOM_PATH = 'room.txt'
    friend_list = itchat.get_friends(update=True)[1:]

    for i in friend_list[1:]:
        city_list.append(i['City'])

    with io.open(CITY_PATH, 'w', encoding='utf-8') as f:
        word_space_split = " ".join(city_list)
        f.write(word_space_split)
        f.close()

    draw_wordcloud(CITY_PATH, tag=u'朋友圈城市分布_')


if __name__ == '__main__':
    LogIn(False)

    parse_friedns()

    parse_signature()

    get_city_data()