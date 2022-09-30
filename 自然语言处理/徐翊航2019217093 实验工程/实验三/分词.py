# _*_ coding: utf-8 _*_
import re
import time
import tkinter as tk
from tkinter.tix import Tk, Control, ComboBox  #升级的组合控件包
from tkinter.messagebox import showinfo, showwarning, showerror #各种类型的提示框
CHPattern = re.compile(u'[\u4e00-\u9fa5]+') #所有汉字的unicode编码范围
#读取词典到List中
def load_dictionary(filename):
    startTime = time.time()
    f = open(filename, 'r', encoding = 'UTF-8-sig')
    dictionary = f.read().split('\n')
        #dictionary = dict(zip(dictionary,dictionary))
    dictionary = set(dictionary)
    f.close()
    maxLen = 1
    for i in dictionary:
        if len(i) > maxLen:
            maxLen = len(i)
    endTime = time.time()
    print ("load dictionary costs:", endTime-startTime, "s")
    return dictionary, maxLen

    #读取待分词的语句
def load_data(filename):
    '''
    :param filename: string 待分词的文本的路径和文件名
    :return toBeSegmentedText: string 待分词的文本
    '''
    f = open(filename, 'r', encoding = 'UTF-8-sig')
    toBeSegmentedText = f.read()
    f.close()
    return toBeSegmentedText

#正向最大匹配（Forward Maximum Matching，FMM)
def FMM(sentences, dicionary, maxLen):
    '''
    :param sentences: string    待分词的文本
    :param dictionary: list     词典
    :param maxLen: int          词典中词的最大长度
    :return RMMResult: string   分词的结果
    :return singleNumber: int   分词结果中的单字个数
    '''
    startTime = time.time()    
    FMMResult = ''
    singleNumber = 0 #初始化单个汉字的个数
    while len(sentences) > 0:
        lens = maxLen
        if len(sentences) < lens:
            lens = len(sentences)
        word = sentences[:lens]   #取出词
        while word not in dicionary:
            if len(word) > 1:
                word = word[:len(word)-1]
            if len(word) == 1:
                break
        FMMResult = FMMResult + word + '\\'
        if len(word) == 1 and CHPattern.search(word):  #判断取出的词长度是否为1，并且为汉字
            singleNumber += 1
        sentences = sentences[len(word):]
    endTime = time.time()
    print ("FMM costs:", endTime-startTime, "s")
    return FMMResult, singleNumber

    #逆向最大匹配（Reverse Maximum Matching，RMM）
def RMM(sentences,dictionary,maxLen):
    '''
    :param sentences: string    待分词的文本
    :param dictionary: list     词典
    :param maxLen: int          词典中词的最大长度
    :return RMMResult: string   分词的结果
    :return singleNumber: int   分词结果中的单字个数
    '''
    startTime = time.time()
    RMMResult = ''
    singleNumber = 0   #初始化单个汉字的个数
    while len(sentences) > 0 :
        lens = maxLen
        if len(sentences) < lens:
            lens = len(sentences)
        word = sentences[-lens:]
        while word not in dictionary:
            if len(word) > 1:
                word =  word[-len(word)+1:]
            if len(word) == 1:
                break
        RMMResult = word + '\\' + RMMResult
        if len(word) == 1 and CHPattern.search(word): #判断取出的词长度是否为1，并且为汉字
            singleNumber +=  1         
        sentences = sentences[:-len(word)]
    endTime = time.time()
    print ("RMM costs:", endTime-startTime, "s")
    return RMMResult, singleNumber

    # 双向最大匹配（Bi-directction Maximum Matching，BMM）
def BMM(sentences1, sentences2, count1, count2):
    lens1 = len(sentences1)
    lens2 = len(sentences2)
    if lens1 != lens2:
        if lens1 < lens2:
            return sentences1
        else:
            return sentences2
    elif sentences1 == sentences2:
        return sentences2
    else:
        if count1 < count2:
            return sentences1
        else:
            return sentences2

def insert_insert():
    # 获取entry输入的文字
    string = entry1.get()
    FMMresult, count1 = FMM(string, d, m)
    RMMresult, count2 = RMM(string, d, m)
    BMMresult = BMM(FMMresult, RMMresult, count1, count2)
    # 在光标处插入文字
    text2.delete('1.0', 'end')
    text3.delete('1.0', 'end')
    text4.delete('1.0', 'end')
    write("正向最大匹配算法分词结果:\n"+FMMresult+"\n\n逆向最大匹配算法分词结果:\n"+RMMresult+"\n\n双向最大匹配算法分词结果\n"+BMMresult)
    text2.insert("insert", FMMresult)
    text3.insert("insert", RMMresult)
    text4.insert("insert", BMMresult)
#主函数
def write(ss):
    with open("result.txt", "w", encoding='utf-8') as f:
        f.write(str(ss))
        f.close()

top = tk.Tk()
top.title("分词工具")
top.geometry("800x1000")
d, m = load_dictionary('dict.txt')
s = load_data('article_1.txt')
print ('=============待分词的文本=========================')
print (s)
print ('=================================================')
FMMresult,count1 = FMM(s, d, m)
print ('============正向最大匹配算法分词结果:=============')
print (FMMresult)
print ('单字个数：', count1)
print ('=================================================')
RMMresult,count2 = RMM(s, d, m)
print ('============逆向最大匹配算法分词结果:==============')
print (RMMresult)
print ('单字个数：', count2)
print ('=================================================')
BMMrusult = BMM(FMMresult, RMMresult, count1, count2)
print ('============双向最大匹配算法分词结果:==============')
print (BMMrusult)
print ('=================================================')
text1=tk.Label(top,text="输入你想要分词的文本")
text1.pack()
entry1 = tk.Entry(top,width=80)
entry1.pack()
button1 = tk.Button(top, text="分词", command=insert_insert)
button1.pack()
title1 = tk.Label(top, text="正向最大匹配算法分词结果")
title1.pack()
text2 = tk.Text(top,height=16)
text2.pack()

title1 = tk.Label(top, text="逆向最大匹配算法分词结果")
title1.pack()
text3 = tk.Text(top,height=16)
text3.pack()
yscrollbar = tk.Scrollbar(top)
yscrollbar.pack(side=tk.RIGHT, fill=tk.Y)

# 滚动条与text联动
yscrollbar.config(command=text3.yview)
# text与滚动条联动
text3.config(yscrollcommand=yscrollbar.set)
title1 = tk.Label(top, text="双向最大匹配算法分词结果")
title1.pack()
text4 = tk.Text(top,height=16)
text4.pack()

top.mainloop()

